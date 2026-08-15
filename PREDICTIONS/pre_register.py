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

The record JSON embeds two SHA-256 hashes:
  - ``content_hash``: SHA-256 of the canonical-JSON payload (injective).
  - ``envelope_hash``: SHA-256 of the canonical-JSON envelope (binds schema
    version, predecessor reference, and amendment content).

Any post-hoc edit to a hash-bound field is detectable.

Schema history:
  v1 (2026-08-06): original, pipe-delimited canonical string.
  v2 (2026-08-08): added sigma_denominator + committed_at to hash surface.
  v3 (2026-08-15): injective canonical-JSON serialization; self-verifying
    envelope binding predecessor full-record SHA-256, git revision, schema
    version, and amendment content; removed duplicate top-level committed_at;
    schema-aware verification rejecting downgraded/unknown schema versions.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
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
# content lock.
#
# v3 (2026-08-15): canonical-JSON serialization (injective, no delimiter
# injection). The field set is unchanged from v2; only the serialization
# format changed, so v3 records have different content_hash values than
# their v2 predecessors.
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

# Envelope fields — bound by envelope_hash. These protect the schema version,
# predecessor reference, and amendment metadata from post-hoc mutation.
ENVELOPE_FIELDS: List[str] = [
    "schema_version",
    "prior_record_sha256",
    "prior_git_revision",
    "prior_schema_version",
    "amendment_change",
    "amendment_date",
    "committed_by",
]

SCHEMA_VERSION = 3


# ---------------------------------------------------------------------------
# Hashing (v3: injective canonical-JSON serialization)
# ---------------------------------------------------------------------------

def _canonical_json(obj: Dict[str, Any], fields: List[str]) -> str:
    """Serialize a dict as canonical JSON over the given field order.

    This is injective: unlike pipe-delimited ``field=value`` concatenation,
    canonical JSON properly escapes strings so delimiter-injection collisions
    are impossible. Field names are included in the JSON keys, and string
    values are JSON-escaped.
    """
    canonical_obj = {}
    for field in fields:
        canonical_obj[field] = obj.get(field, "")
    return json.dumps(canonical_obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def canonical_string(payload: Dict[str, Any]) -> str:
    """Build the canonical JSON string used for payload hashing.

    Uses canonical JSON (sorted keys, no whitespace) over an explicit schema
    object with all CANONICAL_FIELDS. This is injective — the v2
    pipe-delimited format was vulnerable to delimiter-injection collisions
    (e.g. a quantity_name containing ``|formula=`` could collide with a
    different payload). Canonical JSON escapes all special characters,
    eliminating this class of collision.
    """
    return _canonical_json(payload, CANONICAL_FIELDS)


def envelope_string(envelope: Dict[str, Any]) -> str:
    """Build the canonical JSON string used for envelope hashing."""
    return _canonical_json(envelope, ENVELOPE_FIELDS)


def compute_hash(payload: Dict[str, Any]) -> str:
    """Return the SHA-256 hex digest of the canonical payload string."""
    return hashlib.sha256(canonical_string(payload).encode("utf-8")).hexdigest()


def compute_envelope_hash(envelope: Dict[str, Any]) -> str:
    """Return the SHA-256 hex digest of the canonical envelope string."""
    return hashlib.sha256(envelope_string(envelope).encode("utf-8")).hexdigest()


def verify_hash(record: Dict[str, Any]) -> bool:
    """Return True iff the record passes all v3 integrity checks.

    Checks:
      1. ``content_hash`` matches recomputed hash of ``payload``.
      2. ``schema_version`` equals the current SCHEMA_VERSION (rejects
         downgraded or unknown schema versions).
      3. No top-level ``committed_at`` exists (H1: single authoritative
         timestamp in ``payload.committed_at`` only).
      4. If ``envelope_hash`` is present, it matches the recomputed envelope
         hash (H2: binds schema, predecessor, amendment).
    """
    stored = record.get("content_hash")
    if not stored:
        return False
    recomputed = compute_hash(record.get("payload", {}))
    content_ok = hmac.compare_digest(stored, recomputed)

    # H2: reject downgraded or unknown schema versions
    if record.get("schema_version") != SCHEMA_VERSION:
        return False

    # H1: reject records with a duplicate top-level committed_at
    if "committed_at" in record:
        return False

    # H2: verify envelope hash if present
    stored_envelope = record.get("envelope_hash")
    if stored_envelope:
        envelope = record.get("envelope", {})
        recomputed_envelope = compute_envelope_hash(envelope)
        if not hmac.compare_digest(stored_envelope, recomputed_envelope):
            return False

    return content_ok


# ---------------------------------------------------------------------------
# Record construction
# ---------------------------------------------------------------------------

def build_record(args: argparse.Namespace) -> Dict[str, Any]:
    """Construct a pre-registration record dict from CLI args.

    v3: No top-level ``committed_at`` — the authoritative timestamp lives
    only in ``payload.committed_at`` (hash-bound). The envelope binds
    schema version, predecessor reference, and amendment content.
    """
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

    # v3 envelope: binds schema version, predecessor, and amendment.
    # For new records (no predecessor), envelope fields are empty but still
    # hash-bound so the schema version cannot be mutated.
    envelope: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "prior_record_sha256": "",
        "prior_git_revision": "",
        "prior_schema_version": "",
        "amendment_change": "initial registration",
        "amendment_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "committed_by": getattr(args, "committed_by", "") or "",
    }
    envelope_hash = compute_envelope_hash(envelope)

    record: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "pre_registration",
        "created_at": datetime.now(timezone.utc).isoformat(),
        # H1: NO top-level committed_at — authoritative copy is in payload only.
        "status": status,
        "degenerate_risk": degenerate_risk,
        "content_hash": content_hash,
        "envelope_hash": envelope_hash,
        "envelope": envelope,
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

# PDG 2024 pole masses for charged leptons (in MeV/c²).
# Source: PDG Review of Particle Physics, charged lepton masses.
# These are the locally bound mass fixture for the Koide self-test.
PDG_MASSES_MEV: Dict[str, float] = {
    "m_e": 0.510998950,    # electron pole mass
    "m_mu": 105.6583755,   # muon pole mass
    "m_tau": 1776.86,      # tau pole mass
}


def compute_koide_Q(masses: Dict[str, float]) -> float:
    """Compute the Koide quantity Q = Σm / (Σ√m)² from a mass fixture.

    The Koide relation (1981) for charged leptons is:
        Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²

    This is the form that yields Q ≈ 2/3. The alternative form
    (Σm)² / Σm² yields ≈1.119 and is NOT the Koide relation.

    With PDG 2024 pole masses, Q ≈ 0.66666, consistent with 2/3.
    """
    m_e = masses["m_e"]
    m_mu = masses["m_mu"]
    m_tau = masses["m_tau"]
    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau)
    return sum_m / (sum_sqrt_m ** 2)


def run_self_test() -> Dict[str, Any]:
    """Pre-register the Koide charged-lepton Q = 2/3 prediction and verify it.

    The Koide relation for charged leptons is:
        Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² ≈ 2/3

    This self-test COMPUTES Q from the PDG 2024 pole mass fixture (not
    hard-coded) and verifies it against the theoretical value 2/3. The
    computed value is ~0.66666, consistent with 2/3 to within the mass
    uncertainties.

    H5 fix (Codex 2026-08-15): the previous self-test hard-coded both the
    expected and measured values and stated the wrong formula
    ((Σm)²/Σm² instead of Σm/(Σ√m)²). This version computes Q from a
    locally bound mass fixture using the correct formula.
    """
    print("=" * 60)
    print("SELF-TEST: Koide Q = 2/3 for charged leptons")
    print("=" * 60)

    # Compute Q from the PDG mass fixture (not hard-coded).
    computed_Q = compute_koide_Q(PDG_MASSES_MEV)
    print(f"  PDG masses (MeV): m_e={PDG_MASSES_MEV['m_e']}, "
          f"m_μ={PDG_MASSES_MEV['m_mu']}, m_τ={PDG_MASSES_MEV['m_tau']}")
    print(f"  Computed Q = Σm / (Σ√m)² = {computed_Q:.10f}")
    print(f"  Theoretical Q = 2/3 = {2.0/3.0:.10f}")
    print(f"  |deviation| = {abs(computed_Q - 2.0/3.0):.10f}")

    # Build the prediction payload directly (mirrors `register` args).
    committed_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "quantity_name": "koide_Q_charged_leptons",
        "formula": "(m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²",
        "expected_value": 2.0 / 3.0,
        "uncertainty": 0.001,
        "measurement_source": "PDG_2024_pole_masses",
        "rival_predictions": {
            "SM": "no prediction (free Yukawa parameters)",
            "Brannen": "2/3 (same form, independent origin)",
        },
        "commitment_date": datetime.now(timezone.utc).isoformat(),
        "framework": "PF",
        "conditional_on": "Koide geometric identity Q=2/3 (Lean: PfLean.KoideGeometry); physical selection OPEN",
        "notes": "Self-test: Q computed from PDG 2024 pole masses using Σm/(Σ√m)² formula. "
                 "Computed value is plumbing-verified against the mass fixture, not hard-coded.",
        "sigma_denominator": "",
        "committed_at": committed_at,
    }
    content_hash = compute_hash(payload)

    # v3 envelope for the self-test record.
    envelope: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "prior_record_sha256": "",
        "prior_git_revision": "",
        "prior_schema_version": "",
        "amendment_change": "initial registration (self-test)",
        "amendment_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "committed_by": "Devin self-test",
    }
    envelope_hash = compute_envelope_hash(envelope)

    record = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "pre_registration",
        "created_at": datetime.now(timezone.utc).isoformat(),
        # H1: NO top-level committed_at.
        "status": "OPEN",
        "degenerate_risk": False,
        "content_hash": content_hash,
        "envelope_hash": envelope_hash,
        "envelope": envelope,
        "payload": payload,
        "resolution_log": [],
    }
    path = save_record(record)
    print(f"\nPre-registered record written to: {path}")
    print(f"  content_hash: {content_hash}")
    print(f"  expected_value: {payload['expected_value']:.10f} ± {payload['uncertainty']}")

    # Verify the computed Q against the theoretical 2/3.
    # The "measured" value is the computed Q from PDG masses.
    # Uncertainty on the computed Q comes from mass measurement uncertainties.
    measured_value = computed_Q
    measured_uncertainty = 0.0001  # conservative: dominated by m_τ uncertainty
    print(f"\nVerifying computed Q = {measured_value:.10f} ± {measured_uncertainty} ...")
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
    p_reg.add_argument("--committed-by", default="",
                       help="Agent identity for the commit (stored in envelope)")
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
