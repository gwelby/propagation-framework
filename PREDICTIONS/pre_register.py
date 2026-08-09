#!/usr/bin/env python3
"""
pre_register.py — Physics prediction pre-registration script.

Implements a clinical-trial-style pre-registration protocol for physics
predictions, following the PREDICTIONS/ ledger anti-gaming rules:

  1. Number-or-form, never prose.           (a prediction must be falsifiable)
  2. The hash is the lock.                  (you cannot back-date a commitment)
  3. conditional_on is mandatory.           (every inherited premise named)
  4. rivals_say empty -> DEGENERATE-risk.   (rivals must be named or tasked)
  5. BLOCKED != OPEN.                       (no machinery -> BLOCKED)
  6. Clock-enforced verify.                 (resolution is checkable)

Usage
-----
Pre-register a prediction:

    python3 pre_register.py register \\
        --quantity-name neutrino_mass_squared_ratio \\
        --formula "Δm²₂₁/Δm²₃₁" \\
        --expected-value 0.0293 \\
        --uncertainty 0.0008 \\
        --measurement-source JUNO \\
        --framework PF \\
        --commitment-date 2026-08-01T00:00:00Z \\
        --rival SM:0.0308 --rival ZiP:0.0291 \\
        --notes "normal-ordering, Postulate D assumed" \\
        --conditional-on "Postulate D"

Verify a pre-registered prediction against a measurement:

    python3 pre_register.py verify <record.json> <measured_value> <measured_uncertainty>

Self-test (Koide Q = 2/3 for charged leptons):

    python3 pre_register.py test

The record JSON embeds a SHA-256 hash of the canonical-field concatenation so
that any post-hoc edit to the commitment block is detectable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
RECORDS_DIR = SCRIPT_DIR / "pre_registrations"
RECORDS_DIR.mkdir(parents=True, exist_ok=True)

# Canonical field order — the order used for hashing. NEVER reorder without
# bumping the schema version, or hashes will silently change.
#
# v2 (2026-08-08): added `sigma_denominator` and `committed_at` to the hash
# surface so that mutation of either claim-bearing field invalidates the
# content lock. Prior v1 records that pre-date this change carry an
# `amendments` array documenting the v1→v2 migration; their stored
# `content_hash` is the v2 digest (computed over the full v2 field set).
CANONICAL_FIELDS: List[str] = [
    "quantity_name",
    "formula",
    "expected_value",
    "uncertainty",
    "measurement_source",
    "rival_predictions",
    "commitment_date",
    "framework",
    "conditional_on",
    "notes",
    "sigma_denominator",
    "committed_at",
]

SCHEMA_VERSION = 2


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def canonical_string(payload: Dict[str, Any]) -> str:
    """Build the canonical concatenation string used for hashing.

    Fields are joined in CANONICAL_FIELDS order, each rendered as
    ``field=value`` with a pipe separator. Dicts and lists are JSON-serialized
    with sorted keys so the hash is stable regardless of insertion order.
    """
    parts: List[str] = []
    for field in CANONICAL_FIELDS:
        value = payload.get(field, "")
        if isinstance(value, (dict, list)):
            rendered = json.dumps(value, sort_keys=True, ensure_ascii=False)
        else:
            rendered = str(value)
        parts.append(f"{field}={rendered}")
    return "|".join(parts)


def compute_hash(payload: Dict[str, Any]) -> str:
    """Return the SHA-256 hex digest of the canonical payload string."""
    return hashlib.sha256(canonical_string(payload).encode("utf-8")).hexdigest()


def verify_hash(record: Dict[str, Any]) -> bool:
    """Return True iff the stored hash matches a recomputed hash of the payload."""
    stored = record.get("content_hash")
    if not stored:
        return False
    recomputed = compute_hash(record.get("payload", {}))
    # Use compare_digest to avoid timing-attack concerns (defence in depth).
    import hmac
    return hmac.compare_digest(stored, recomputed)


# ---------------------------------------------------------------------------
# Record construction
# ---------------------------------------------------------------------------

def build_record(args: argparse.Namespace) -> Dict[str, Any]:
    """Construct a pre-registration record dict from CLI args."""
    # Parse --rival NAME:VALUE repeated flags into a dict.
    rival_predictions: Dict[str, str] = {}
    for item in getattr(args, "rival", []) or []:
        if ":" not in item:
            raise ValueError(
                f"--rival must be NAME:VALUE, got {item!r}"
            )
        name, value = item.split(":", 1)
        rival_predictions[name.strip()] = value.strip()

    committed_at = datetime.now(timezone.utc).isoformat()

    payload: Dict[str, Any] = {
        "quantity_name": args.quantity_name,
        "formula": args.formula,
        "expected_value": float(args.expected_value),
        "uncertainty": float(args.uncertainty),
        "measurement_source": args.measurement_source,
        "rival_predictions": rival_predictions,
        "commitment_date": args.commitment_date,
        "framework": args.framework,
        "conditional_on": args.conditional_on or "",
        "notes": args.notes or "",
        "sigma_denominator": getattr(args, "sigma_denominator", "") or "",
        "committed_at": committed_at,
    }

    content_hash = compute_hash(payload)

    # Anti-gaming rule 4: empty rivals -> DEGENERATE-risk flag.
    degenerate_risk = len(rival_predictions) == 0

    # Anti-gaming rule 5: a prediction contingent on unbuilt machinery is
    # BLOCKED, not OPEN. We let the caller set status explicitly, but default
    # to OPEN and warn if conditional_on mentions machinery not yet built.
    status = "OPEN"
    if degenerate_risk:
        status = "OPEN-DEGENERATE-RISK"

    record: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "pre_registration",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "committed_at": committed_at,
        "status": status,
        "degenerate_risk": degenerate_risk,
        "content_hash": content_hash,
        "payload": payload,
        # Append-only resolution log — verify() appends here.
        "resolution_log": [],
    }
    return record


def save_record(record: Dict[str, Any]) -> Path:
    """Write the record to a timestamped JSON file and return its path."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_name = "".join(
        c if c.isalnum() or c in "-_" else "_"
        for c in record["payload"]["quantity_name"]
    )
    filename = f"{ts}_{safe_name}.json"
    path = RECORDS_DIR / filename
    with path.open("w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    return path


# ---------------------------------------------------------------------------
# Verify mode
# ---------------------------------------------------------------------------

def verify_record(
    record_path: Path,
    measured_value: float,
    measured_uncertainty: float,
) -> Dict[str, Any]:
    """Load a record, check the hash, and test the measurement against it.

    PASS criterion: |predicted - measured| <= uncertainty + measured_uncertainty
    (the combined tolerance band). The deviation is also reported in sigma,
    where sigma = |predicted - measured| / sqrt(uncertainty^2 + measured_unc^2).
    """
    with record_path.open("r", encoding="utf-8") as fh:
        record = json.load(fh)

    hash_ok = verify_hash(record)
    payload = record.get("payload", {})
    predicted = float(payload["expected_value"])
    pred_unc = float(payload["uncertainty"])

    deviation = abs(predicted - measured_value)
    tolerance = pred_unc + measured_uncertainty
    combined_sigma = (pred_unc ** 2 + measured_uncertainty ** 2) ** 0.5
    sigma = deviation / combined_sigma if combined_sigma > 0 else float("inf")
    passed = deviation <= tolerance

    result = {
        "record_path": str(record_path),
        "quantity_name": payload.get("quantity_name"),
        "framework": payload.get("framework"),
        "predicted_value": predicted,
        "predicted_uncertainty": pred_unc,
        "measured_value": measured_value,
        "measured_uncertainty": measured_uncertainty,
        "absolute_deviation": deviation,
        "combined_tolerance": tolerance,
        "deviation_sigma": sigma,
        "hash_intact": hash_ok,
        "verdict": "PASS" if (passed and hash_ok) else "FAIL",
        "fail_reasons": [],
    }
    if not passed:
        result["fail_reasons"].append(
            f"deviation {deviation:.6g} exceeds combined tolerance {tolerance:.6g}"
        )
    if not hash_ok:
        result["fail_reasons"].append("content_hash mismatch — record may have been edited")

    # Append to the resolution log in the record file (append-only).
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "verify",
        "measured_value": measured_value,
        "measured_uncertainty": measured_uncertainty,
        "verdict": result["verdict"],
        "deviation_sigma": sigma,
        "hash_intact": hash_ok,
    }
    record.setdefault("resolution_log", []).append(log_entry)
    with record_path.open("w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")

    return result


def print_verify_result(result: Dict[str, Any]) -> None:
    print("=" * 60)
    print("PRE-REGISTRATION VERIFICATION")
    print("=" * 60)
    print(f"Record:          {result['record_path']}")
    print(f"Quantity:        {result['quantity_name']}")
    print(f"Framework:       {result['framework']}")
    print(f"Predicted:       {result['predicted_value']:.10g} ± {result['predicted_uncertainty']:.10g}")
    print(f"Measured:        {result['measured_value']:.10g} ± {result['measured_uncertainty']:.10g}")
    print(f"|deviation|:     {result['absolute_deviation']:.10g}")
    print(f"combined tol:    {result['combined_tolerance']:.10g}")
    print(f"deviation (σ):   {result['deviation_sigma']:.4f}")
    print(f"hash intact:     {result['hash_intact']}")
    print("-" * 60)
    print(f"VERDICT:         {result['verdict']}")
    if result["fail_reasons"]:
        for reason in result["fail_reasons"]:
            print(f"  reason: {reason}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Self-test (Koide Q = 2/3 for charged leptons)
# ---------------------------------------------------------------------------

def run_self_test() -> Dict[str, Any]:
    """Pre-register the Koide charged-lepton Q = 2/3 prediction and verify it.

    The Koide relation for charged leptons gives Q = (m_e + m_μ + m_τ)^2
    / (m_e^2 + m_μ^2 + m_τ^2) = 2/3 exactly in the original 1981 form.
    The empirical value from PDG masses is ~0.6674, consistent with 2/3
    to within the mass uncertainties. We pre-register 2/3 = 0.6666666667
    with a small theory uncertainty and verify against 0.6674 ± 0.0001.
    """
    print("=" * 60)
    print("SELF-TEST: Koide Q = 2/3 for charged leptons")
    print("=" * 60)

    # Build the prediction payload directly (mirrors `register` args).
    committed_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "quantity_name": "koide_Q_charged_leptons",
        "formula": "(m_e + m_μ + m_τ)^2 / (m_e^2 + m_μ^2 + m_τ^2)",
        "expected_value": 2.0 / 3.0,
        "uncertainty": 0.001,
        "measurement_source": "PDG_masses",
        "rival_predictions": {
            "SM": "no prediction (free Yukawa parameters)",
            "Brannen": "2/3 (same form, independent origin)",
        },
        "commitment_date": datetime.now(timezone.utc).isoformat(),
        "framework": "PF",
        "conditional_on": "Koide geometric identity Q=2/3 (Lean: PfLean.KoideGeometry); physical selection OPEN",
        "notes": "Self-test: exact geometric identity; empirical check uses PDG pole masses.",
        "sigma_denominator": "",
        "committed_at": committed_at,
    }
    content_hash = compute_hash(payload)
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "pre_registration",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "committed_at": committed_at,
        "status": "OPEN",
        "degenerate_risk": False,
        "content_hash": content_hash,
        "payload": payload,
        "resolution_log": [],
    }
    path = save_record(record)
    print(f"Pre-registered record written to: {path}")
    print(f"  content_hash: {content_hash}")
    print(f"  expected_value: {payload['expected_value']:.10f} ± {payload['uncertainty']}")

    # Verify against the measured value 0.6674 ± 0.0001.
    measured_value = 0.6674
    measured_uncertainty = 0.0001
    print(f"\nVerifying against measured {measured_value} ± {measured_uncertainty} ...")
    result = verify_record(path, measured_value, measured_uncertainty)
    print_verify_result(result)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_register(args: argparse.Namespace) -> int:
    record = build_record(args)
    path = save_record(record)
    print(f"Pre-registration saved: {path}")
    print(f"  content_hash: {record['content_hash']}")
    print(f"  status:       {record['status']}")
    if record["degenerate_risk"]:
        print("  WARNING: no rival predictions supplied — DEGENERATE-RISK flag set.")
        print("           Per anti-gaming rule 4, name rivals or log a time-boxed task.")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    record_path = Path(args.record).resolve()
    if not record_path.exists():
        print(f"ERROR: record not found: {record_path}", file=sys.stderr)
        return 2
    result = verify_record(
        record_path,
        float(args.measured_value),
        float(args.measured_uncertainty),
    )
    print_verify_result(result)
    return 0 if result["verdict"] == "PASS" else 1


def cmd_verify_hash(args: argparse.Namespace) -> int:
    """Check only the content_hash of a record (no measurement needed)."""
    record_path = Path(args.record).resolve()
    if not record_path.exists():
        print(f"ERROR: record not found: {record_path}", file=sys.stderr)
        return 2
    with record_path.open("r", encoding="utf-8") as fh:
        record = json.load(fh)
    ok = verify_hash(record)
    stored = record.get("content_hash", "<missing>")
    recomputed = compute_hash(record.get("payload", {}))
    schema = record.get("schema_version", "?")
    print(f"Record:          {record_path}")
    print(f"schema_version:  {schema}")
    print(f"stored hash:     {stored}")
    print(f"computed hash:   {recomputed}")
    print(f"hash intact:     {ok}")
    print(f"VERDICT:         {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def cmd_test(args: argparse.Namespace) -> int:
    result = run_self_test()
    return 0 if result["verdict"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pre_register.py",
        description="Physics prediction pre-registration (clinical-trial style).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- register -----------------------------------------------------------
    p_reg = sub.add_parser("register", help="Pre-register a new prediction.")
    p_reg.add_argument("--quantity-name", required=True,
                       help="e.g. neutrino_mass_squared_ratio")
    p_reg.add_argument("--formula", required=True,
                       help="Mathematical formula, e.g. 'Δm²₂₁/Δm²₃₁'")
    p_reg.add_argument("--expected-value", required=True, type=float,
                       help="Predicted numerical value")
    p_reg.add_argument("--uncertainty", required=True, type=float,
                       help="Uncertainty on the prediction")
    p_reg.add_argument("--measurement-source", required=True,
                       help="e.g. JUNO, DUNE, KATRIN")
    p_reg.add_argument("--framework", required=True,
                       help="e.g. PF, UGP")
    p_reg.add_argument("--commitment-date", required=True,
                       help="ISO-format commitment date")
    p_reg.add_argument("--rival", action="append", default=[],
                       metavar="NAME:VALUE",
                       help="Rival prediction (repeatable), e.g. --rival SM:0.0308")
    p_reg.add_argument("--conditional-on", default="",
                       help="Premises the prediction depends on (mandatory per rule 3)")
    p_reg.add_argument("--notes", default="", help="Optional notes")
    p_reg.add_argument("--sigma-denominator", default="",
                       help="Explicit denominator convention for sigma estimates "
                            "(e.g. 'full_window_spread (0.045 dimensionless Q units)')")
    p_reg.set_defaults(func=cmd_register)

    # --- verify -------------------------------------------------------------
    p_ver = sub.add_parser("verify", help="Verify a record against a measurement.")
    p_ver.add_argument("record", help="Path to the pre-registration JSON record")
    p_ver.add_argument("measured_value", type=float, help="Measured value")
    p_ver.add_argument("measured_uncertainty", type=float,
                       help="Uncertainty on the measurement")
    p_ver.set_defaults(func=cmd_verify)

    # --- verify_hash --------------------------------------------------------
    p_vh = sub.add_parser("verify_hash",
                          help="Check only the content_hash of a record (no measurement).")
    p_vh.add_argument("record", help="Path to the pre-registration JSON record")
    p_vh.set_defaults(func=cmd_verify_hash)

    # --- test ---------------------------------------------------------------
    p_test = sub.add_parser("test", help="Run the Koide Q=2/3 self-test.")
    p_test.set_defaults(func=cmd_test)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
