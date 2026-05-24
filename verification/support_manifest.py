"""Support manifest loader for the verification harness.

The support manifest is a small read-only YAML file
(``verification/support_manifest.yaml``) that annotates which derivation
references already cited in ``CLAIMS.md`` qualify as Codex-audited local
support for a claim. The manifest is *metadata only*: it must never
introduce claims absent from the board, never redefine statuses, and
never change confidence scores.

This loader

    * validates shape (top-level mapping, optional ``support:`` wrapper,
      per-claim lists of entries),
    * resolves each human-friendly claim id against the real slugified
      ids produced by :mod:`verification.claim_parser` using the same
      resolver used by :mod:`verification.dependency_overlay`,
    * verifies every ``path`` entry actually exists on disk,
    * rejects any ``status:`` / ``confidence:`` key anywhere in the
      file, and
    * returns a dict keyed by resolved claim id that is drop-in
      compatible with ``parse_claims_md(..., support_manifest=...)``.

Run ``python -m verification.support_manifest`` as a self-check; the
``__main__`` block loads the real manifest and CLAIMS.md and reports
what resolved and what did not.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 2.8, 4.1, 4.7, 11.4
"""

from __future__ import annotations

import datetime as _dt
import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from verification.claim_parser import parse_claims_md
from verification.dependency_overlay import resolve_claim_id
from verification.models import Claim


logger = logging.getLogger(__name__)


# Keys that are forbidden anywhere in the manifest; see Req. 2.8.
_FORBIDDEN_KEYS: frozenset[str] = frozenset({"status", "confidence"})

# Keys permitted inside a single support entry. Unknown keys are tolerated
# (future-compatible) but logged at INFO.
_KNOWN_ENTRY_KEYS: frozenset[str] = frozenset(
    {"path", "audit_status", "date", "note"}
)


def load_support_manifest(
    path: str | Path | None,
    parsed_claims: dict[str, Claim],
) -> dict[str, list[dict[str, str]]]:
    """Load ``path`` as a support manifest YAML.

    Args:
        path: Filesystem path to the manifest, or ``None``. When ``None``
            or the file does not exist, an empty dict is returned (a
            manifest is optional by design).
        parsed_claims: Dict of parsed :class:`Claim` records, used to
            resolve human-friendly ids into the real slugified ids.

    Returns:
        A dict of the shape ``{resolved_claim_id: [entry, entry, ...]}``
        where each ``entry`` is a dict with at least ``path`` and
        optionally ``audit_status``, ``date``, ``note``. The output is
        drop-in compatible with
        ``parse_claims_md(path, support_manifest=...)``.

    Raises:
        ValueError: BLOCK-level, on unresolvable claim ids, missing file
            paths, or any attempt to set ``status`` / ``confidence``
            anywhere in the file.
    """

    if path is None:
        return {}
    manifest_path = Path(path)
    if not manifest_path.is_file():
        logger.info(
            "load_support_manifest: %s not found; continuing with no manifest",
            manifest_path,
        )
        return {}

    with manifest_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(
            f"support manifest {manifest_path}: top-level document must be a "
            f"mapping (got {type(raw).__name__})"
        )

    _reject_forbidden_keys(raw, context=f"{manifest_path} top-level")

    # Allow either {"support": {id: [...]}, ...} or a flat {id: [...], ...}
    if "support" in raw:
        support_raw = raw["support"]
        if not isinstance(support_raw, dict):
            raise ValueError(
                f"support manifest {manifest_path}: 'support' must be a mapping"
                f" (got {type(support_raw).__name__})"
            )
    else:
        support_raw = raw

    resolved: dict[str, list[dict[str, str]]] = {}

    for ref_id, entries in support_raw.items():
        if ref_id in _FORBIDDEN_KEYS:
            # Already rejected above; defensive skip.
            continue
        if not isinstance(entries, list):
            raise ValueError(
                f"support manifest {manifest_path}: entries for {ref_id!r} "
                f"must be a list (got {type(entries).__name__})"
            )

        resolved_id = resolve_claim_id(
            ref_id,
            parsed_claims,
            source_hint=f"{manifest_path} claim {ref_id!r}",
        )

        clean_entries: list[dict[str, str]] = []
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValueError(
                    f"support manifest {manifest_path}: {ref_id!r} entry "
                    f"#{index} must be a mapping (got {type(entry).__name__})"
                )
            _reject_forbidden_keys(
                entry, context=f"{manifest_path} {ref_id!r} entry #{index}"
            )

            path_value = entry.get("path")
            if not isinstance(path_value, str) or not path_value.strip():
                raise ValueError(
                    f"support manifest {manifest_path}: {ref_id!r} entry "
                    f"#{index} missing required non-empty 'path' string"
                )

            # Validate the path exists on disk. Paths in the manifest are
            # workspace-relative; fall back to checking an absolute path
            # literally, which keeps the loader portable for test fixtures.
            repo_root = Path.cwd()
            file_path = Path(path_value)
            candidates = [file_path]
            if not file_path.is_absolute():
                candidates.append(repo_root / file_path)
                # Also try relative to this module's parent of parent so the
                # loader works when invoked via ``python -m`` from any cwd.
                here = Path(__file__).resolve().parent.parent
                candidates.append(here / file_path)
            if not any(p.is_file() for p in candidates):
                raise ValueError(
                    f"support manifest {manifest_path}: {ref_id!r} entry "
                    f"#{index} path {path_value!r} does not exist on disk "
                    f"(tried: {[str(p) for p in candidates]})"
                )

            clean_entry: dict[str, str] = {"path": path_value}
            for opt_key in ("audit_status", "date", "note"):
                if opt_key in entry and entry[opt_key] is not None:
                    value = entry[opt_key]
                    if not isinstance(
                        value,
                        (str, int, float, _dt.date, _dt.datetime),
                    ):
                        raise ValueError(
                            f"support manifest {manifest_path}: {ref_id!r} "
                            f"entry #{index} key {opt_key!r} must be string-"
                            f"like (got {type(value).__name__})"
                        )
                    clean_entry[opt_key] = (
                        value if isinstance(value, str) else str(value)
                    )

            # Warn about unknown keys so the operator knows they are ignored.
            unknown = set(entry) - _KNOWN_ENTRY_KEYS - _FORBIDDEN_KEYS
            if unknown:
                logger.info(
                    "support manifest %s: %r entry #%d has unknown keys %s "
                    "(ignored)",
                    manifest_path,
                    ref_id,
                    index,
                    sorted(unknown),
                )

            clean_entries.append(clean_entry)

        if resolved_id in resolved:
            resolved[resolved_id].extend(clean_entries)
        else:
            resolved[resolved_id] = clean_entries

    return resolved


def _reject_forbidden_keys(mapping: dict[str, Any], *, context: str) -> None:
    """Raise if ``mapping`` carries a ``status`` or ``confidence`` key."""

    for key in mapping:
        if key in _FORBIDDEN_KEYS:
            raise ValueError(
                f"{context}: key {key!r} is forbidden. The support manifest "
                f"must not redefine claim statuses or confidence scores "
                f"(Req. 2.8)."
            )


# ---------------------------------------------------------------------------
# Self-check entry point
# ---------------------------------------------------------------------------


def _main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "CLAIMS.md"
    manifest_path = repo_root / "verification" / "support_manifest.yaml"

    if not claims_path.exists():
        print(f"[skip] CLAIMS.md not found at {claims_path}", file=sys.stderr)
        return 1
    if not manifest_path.exists():
        print(f"[skip] manifest not found at {manifest_path}", file=sys.stderr)
        return 1

    parsed = parse_claims_md(claims_path)
    print(f"=== support manifest self-check ===")
    print(f"  claims parsed: {len(parsed)}")

    try:
        resolved = load_support_manifest(manifest_path, parsed)
    except ValueError as exc:
        print(f"  manifest BLOCK: {exc}")
        return 2

    print(f"  manifest entries: {sum(len(v) for v in resolved.values())}")
    for resolved_id, entries in resolved.items():
        print(f"  {resolved_id} ({len(entries)} entries):")
        for entry in entries:
            label = entry.get("audit_status", "?")
            print(f"    [{label}] {entry['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
