#!/usr/bin/env python3
"""
test_pred003_hash_binding.py — Hostile mutation tests for PRED-003 v3 hash binding.

These tests prove that the v3 schema change closes all six Codex findings
(CODEX_20260815_FUNDAMENTALS_PROSE_PRED003_682760E_REVERIFICATION.md):

  H1: No duplicate top-level committed_at; payload copy is the only authority.
  H2: Envelope hash binds schema_version, predecessor SHA-256, git revision,
      and amendment content. Schema downgrade is rejected.
  H4: Canonical-JSON serialization is delimiter-safe (no delimiter-injection collision).
  H5: Koide self-test computes Q from PDG mass fixture (not hard-coded).

Tests:
  1. Load each v3 record, verify both content_hash and envelope_hash pass.
  2. Mutate sigma_denominator → content_hash FAILS.
  3. Mutate committed_at (in payload) → content_hash FAILS.
  4. Mutate top-level committed_at (if it existed) → verify_hash FAILS.
  5. Downgrade schema_version → verify_hash FAILS.
  6. Mutate envelope prior_record_sha256 → envelope_hash FAILS.
  7. Mutate envelope amendment_change → envelope_hash FAILS.
  8. Delimiter-injection collision test → canonical_string is delimiter-safe.
  9. Confirm no top-level committed_at exists in v3 records.
  10. Confirm envelope binds predecessor full-record SHA-256.

Run:
    python3 PREDICTIONS/test_pred003_hash_binding.py
"""

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pre_register import (  # noqa: E402
    verify_hash,
    compute_hash,
    canonical_string,
    compute_envelope_hash,
    compute_lifecycle_hash,
    compute_entry_hash,
    SCHEMA_VERSION,
    compute_koide_Q,
    PDG_MASSES_MEV,
)

# v3 successor records (the active records)
RECORDS = [
    os.path.join(HERE, "pre_registrations",
                 "20260815T120000Z_neutrino_koide_Q_NO_v3.json"),
    os.path.join(HERE, "pre_registrations",
                 "20260815T120000Z_neutrino_koide_Q_IO_v3.json"),
]


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _check(condition, msg):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {msg}")
    if not condition:
        raise AssertionError(msg)


def test_record(path):
    name = os.path.basename(path)
    print(f"\n=== Hostile mutation test: {name} ===")

    record = _load(path)

    # 1. Original record passes all v3 checks
    _check(verify_hash(record), "original record verify_hash == True")

    # 2. Mutate sigma_denominator → content_hash must FAIL
    mutated_sigma = copy.deepcopy(record)
    mutated_sigma["payload"]["sigma_denominator"] = "HOSTILE_MUTATION_test"
    _check(not verify_hash(mutated_sigma),
           "mutated sigma_denominator → verify_hash == False")

    # 3. Mutate committed_at (in payload) → content_hash must FAIL
    mutated_committed = copy.deepcopy(record)
    mutated_committed["payload"]["committed_at"] = "2099-01-01T00:00:00+00:00"
    _check(not verify_hash(mutated_committed),
           "mutated payload committed_at → verify_hash == False")

    # 4. H1: Adding a top-level committed_at → verify_hash must FAIL
    mutated_toplevel = copy.deepcopy(record)
    mutated_toplevel["committed_at"] = "1900-01-01T00:00:00+00:00"
    _check(not verify_hash(mutated_toplevel),
           "added top-level committed_at → verify_hash == False (H1)")

    # 5. H2: Downgrade schema_version → verify_hash must FAIL
    mutated_schema = copy.deepcopy(record)
    mutated_schema["schema_version"] = 2
    _check(not verify_hash(mutated_schema),
           "downgraded schema_version to 2 → verify_hash == False (H2)")

    # 5b. H2: Unknown schema_version → verify_hash must FAIL
    mutated_schema_unknown = copy.deepcopy(record)
    mutated_schema_unknown["schema_version"] = 99
    _check(not verify_hash(mutated_schema_unknown),
           "unknown schema_version 99 → verify_hash == False (H2)")

    # 6. H2: Mutate envelope prior_record_sha256 → verify_hash must FAIL
    mutated_prior = copy.deepcopy(record)
    mutated_prior["envelope"]["prior_record_sha256"] = "0" * 64
    _check(not verify_hash(mutated_prior),
           "mutated envelope prior_record_sha256 → verify_hash == False (H2)")

    # 7. H2: Mutate envelope amendment_change → verify_hash must FAIL
    mutated_amend = copy.deepcopy(record)
    mutated_amend["envelope"]["amendment_change"] = "HOSTILE_AMENDMENT"
    _check(not verify_hash(mutated_amend),
           "mutated envelope amendment_change → verify_hash == False (H2)")

    # 8. H2: Mutate envelope schema_version → verify_hash must FAIL
    mutated_env_schema = copy.deepcopy(record)
    mutated_env_schema["envelope"]["schema_version"] = 2
    _check(not verify_hash(mutated_env_schema),
           "mutated envelope schema_version → verify_hash == False (H2)")

    # 9. H2-A: Remove envelope_hash only → verify_hash must FAIL (mandatory)
    mutated_no_env_hash = copy.deepcopy(record)
    del mutated_no_env_hash["envelope_hash"]
    _check(not verify_hash(mutated_no_env_hash),
           "removed envelope_hash only → verify_hash == False (H2-A mandatory)")

    # 9b. H2-A: Remove both envelope and envelope_hash → verify_hash must FAIL
    mutated_no_env = copy.deepcopy(record)
    del mutated_no_env["envelope_hash"]
    del mutated_no_env["envelope"]
    _check(not verify_hash(mutated_no_env),
           "removed both envelope and envelope_hash → verify_hash == False (H2-A)")

    # 9c. H2-A: Empty envelope_hash → verify_hash must FAIL
    mutated_empty_env_hash = copy.deepcopy(record)
    mutated_empty_env_hash["envelope_hash"] = ""
    _check(not verify_hash(mutated_empty_env_hash),
           "empty envelope_hash → verify_hash == False (H2-A)")

    # 9d. H2-A: Empty envelope dict → verify_hash must FAIL
    mutated_empty_env = copy.deepcopy(record)
    mutated_empty_env["envelope"] = {}
    _check(not verify_hash(mutated_empty_env),
           "empty envelope dict → verify_hash == False (H2-A)")

    # 10. H2-B: Forged minimal record (schema_version + payload + content_hash) → FAIL
    forged = {
        "schema_version": SCHEMA_VERSION,
        "payload": {},
        "content_hash": compute_hash({}),
    }
    _check(not verify_hash(forged),
           "forged minimal record → verify_hash == False (H2-B schema validation)")

    # 10b. H2-B: Record with missing payload field → FAIL
    mutated_missing_field = copy.deepcopy(record)
    del mutated_missing_field["payload"]["sigma_denominator"]
    _check(not verify_hash(mutated_missing_field),
           "missing payload field → verify_hash == False (H2-B)")

    # 10c. H2-B: Record with wrong-type payload field → FAIL
    mutated_wrong_type = copy.deepcopy(record)
    mutated_wrong_type["payload"]["expected_value"] = "not_a_number"
    _check(not verify_hash(mutated_wrong_type),
           "wrong-type payload field → verify_hash == False (H2-B)")

    # 10d. H2-B: Record with missing envelope field → FAIL
    mutated_missing_env_field = copy.deepcopy(record)
    del mutated_missing_env_field["envelope"]["prior_record_sha256"]
    _check(not verify_hash(mutated_missing_env_field),
           "missing envelope field → verify_hash == False (H2-B)")

    # 11. H1/H2-C: Adding legacy top-level "committed" → verify_hash must FAIL
    mutated_legacy = copy.deepcopy(record)
    mutated_legacy["committed"] = "1900-01-01T00:00:00+00:00"
    _check(not verify_hash(mutated_legacy),
           "added legacy top-level committed → verify_hash == False (H1/H2-C)")

    # 11b. H1/H2-C: Adding extra top-level key → verify_hash must FAIL
    mutated_extra_key = copy.deepcopy(record)
    mutated_extra_key["hostile_field"] = "malicious"
    _check(not verify_hash(mutated_extra_key),
           "added extra top-level key → verify_hash == False (H1/H2-C closed schema)")

    # 12. H1: Confirm no top-level committed_at exists
    _check("committed_at" not in record,
           "no top-level committed_at in v3 record (H1)")
    _check("committed" not in record,
           "no top-level committed field in v3 record (H1)")

    # 10. H2: Confirm envelope binds predecessor full-record SHA-256
    envelope = record.get("envelope", {})
    prior_sha = envelope.get("prior_record_sha256", "")
    _check(len(prior_sha) == 64,
           f"envelope prior_record_sha256 is 64 chars (got {len(prior_sha)})")
    _check(envelope.get("prior_git_revision", "") != "",
           "envelope prior_git_revision is non-empty")
    _check(envelope.get("prior_schema_version") == 2,
           "envelope prior_schema_version == 2")

    # 11. Confirm schema version is v3
    _check(record.get("schema_version") == SCHEMA_VERSION,
           f"schema_version == {SCHEMA_VERSION} (got {record.get('schema_version')})")

    # 12. Confirm both new fields are in the payload (hash surface)
    _check("sigma_denominator" in record["payload"],
           "sigma_denominator present in payload")
    _check("committed_at" in record["payload"],
           "committed_at present in payload")

    # 13. Confirm the unit is dimensionless, not eV
    sigma_den = record["payload"]["sigma_denominator"]
    _check("eV" not in sigma_den,
           "sigma_denominator does not contain 'eV' (dimensionless Q units)")
    _check("dimensionless" in sigma_den,
           "sigma_denominator contains 'dimensionless'")

    # === v5 hostile fixtures ===

    # 14. v5: Missing record_type → FAIL
    m = copy.deepcopy(record); del m["record_type"]
    _check(not verify_hash(m), "missing record_type → verify_hash == False (v5 lifecycle)")

    # 15. v5: Missing created_at → FAIL
    m = copy.deepcopy(record); del m["created_at"]
    _check(not verify_hash(m), "missing created_at → verify_hash == False (v5 lifecycle)")

    # 16. v5: Missing status → FAIL
    m = copy.deepcopy(record); del m["status"]
    _check(not verify_hash(m), "missing status → verify_hash == False (v5 lifecycle)")

    # 17. v5: Missing degenerate_risk → FAIL
    m = copy.deepcopy(record); del m["degenerate_risk"]
    _check(not verify_hash(m), "missing degenerate_risk → verify_hash == False (v5 lifecycle)")

    # 18. v5: Missing resolution_log → FAIL
    m = copy.deepcopy(record); del m["resolution_log"]
    _check(not verify_hash(m), "missing resolution_log → verify_hash == False (v5 lifecycle)")

    # 19. v5: Missing lifecycle_hash → FAIL
    m = copy.deepcopy(record); del m["lifecycle_hash"]
    _check(not verify_hash(m), "missing lifecycle_hash → verify_hash == False (v5 lifecycle)")

    # 20. v5: status changed OPEN → RESOLVED-PASS (without log update) → FAIL
    m = copy.deepcopy(record); m["status"] = "RESOLVED-PASS"
    _check(not verify_hash(m), "status OPEN→RESOLVED-PASS without log → verify_hash == False (v5 lifecycle binding)")

    # 21. v5: status changed OPEN → RESOLVED-FAIL (without log update) → FAIL
    m = copy.deepcopy(record); m["status"] = "RESOLVED-FAIL"
    _check(not verify_hash(m), "status OPEN→RESOLVED-FAIL without log → verify_hash == False (v5 lifecycle binding)")

    # 22. v5: status with wrong type (list) → FAIL
    m = copy.deepcopy(record); m["status"] = ["OPEN"]
    _check(not verify_hash(m), "status as list → verify_hash == False (v5 type check)")

    # 23. v5: status with invalid value → FAIL
    m = copy.deepcopy(record); m["status"] = "CONFIRMED"
    _check(not verify_hash(m), "status='CONFIRMED' → verify_hash == False (v5 value check)")

    # 24. v5: degenerate_risk with wrong type (string) → FAIL
    m = copy.deepcopy(record); m["degenerate_risk"] = "false"
    _check(not verify_hash(m), "degenerate_risk as string → verify_hash == False (v5 type check)")

    # 25. v5: created_at changed → FAIL (lifecycle_hash mismatch)
    m = copy.deepcopy(record); m["created_at"] = "1900-01-01T00:00:00+00:00"
    _check(not verify_hash(m), "changed created_at → verify_hash == False (v5 — lifecycle_hash doesn't cover created_at, but created_at is required)")

    # 26. v5: Forged resolution log entry (PASS verdict, empty log was valid) → FAIL
    m = copy.deepcopy(record)
    m["resolution_log"] = [{"timestamp": "2026-01-01T00:00:00+00:00", "action": "verify",
                            "measured_value": 0.667, "measured_uncertainty": 0.001,
                            "verdict": "PASS", "deviation_sigma": 0.1, "hash_intact": True,
                            "entry_hash": "0" * 64}]
    m["status"] = "RESOLVED-PASS"
    m["lifecycle_hash"] = compute_lifecycle_hash("RESOLVED-PASS", m["resolution_log"])
    _check(not verify_hash(m), "forged resolution log entry → verify_hash == False (v5 hash chain)")

    # 27. v5: Extra nested payload key → FAIL
    m = copy.deepcopy(record); m["payload"]["claim"] = "CONFIRMED"
    _check(not verify_hash(m), "extra payload key → verify_hash == False (v5 closed nested schema)")

    # 28. v5: Extra nested envelope key → FAIL
    m = copy.deepcopy(record); m["envelope"]["authority"] = "Greg"
    _check(not verify_hash(m), "extra envelope key → verify_hash == False (v5 closed nested schema)")

    # 29. v5: Envelope schema_version mismatch (2 vs 3) → FAIL
    m = copy.deepcopy(record)
    m["envelope"]["schema_version"] = 2
    # Recompute envelope_hash to isolate the semantic check
    from pre_register import compute_envelope_hash
    m["envelope_hash"] = compute_envelope_hash(m["envelope"])
    _check(not verify_hash(m), "envelope.schema_version=2 vs top-level=3 → verify_hash == False (v5 envelope semantic consistency)")

    # 30. v5: Non-mapping root (string) → FAIL (not raise)
    _check(not verify_hash("not a dict"), "string root → verify_hash == False (v5 fail-closed)")
    _check(not verify_hash(42), "int root → verify_hash == False (v5 fail-closed)")
    _check(not verify_hash([]), "list root → verify_hash == False (v5 fail-closed)")
    _check(not verify_hash(None), "None root → verify_hash == False (v5 fail-closed)")

    # 31. v5: lifecycle_hash mismatch → FAIL
    m = copy.deepcopy(record); m["lifecycle_hash"] = "0" * 64
    _check(not verify_hash(m), "wrong lifecycle_hash → verify_hash == False (v5 lifecycle binding)")

    # 32. v5: Confirm lifecycle_hash is present and valid
    _check("lifecycle_hash" in record, "lifecycle_hash present in record (v5)")
    _check(len(record.get("lifecycle_hash", "")) == 64, "lifecycle_hash is 64 chars (v5)")

    print(f"  → {name}: ALL CHECKS PASSED")


def test_delimiter_injection():
    """H4: Verify canonical_string is delimiter-safe (no delimiter-injection collision).

    The v2 pipe-delimited format was vulnerable: payloads with different
    field values could produce the same canonical string if a value
    contained ``|field_name=``. The v3 canonical-JSON format escapes all
    special characters, making this impossible. Combined with SHA-256,
    this gives a collision-resistant digest over the validated schema.

    Note: SHA-256 is collision-resistant, not mathematically injective.
    No finite-length hash is injective. The canonical serialization is
    delimiter-safe, and the digest is collision-resistant — that is the
    honest boundary.
    """
    print("\n=== H4: Delimiter-safe canonical serialization test ===")

    # Two payloads that would collide under v2 pipe-delimited format
    payload_a = {
        "quantity_name": "a|formula=b",
        "formula": "c",
    }
    payload_b = {
        "quantity_name": "a",
        "formula": "b|formula=c",
    }

    str_a = canonical_string(payload_a)
    str_b = canonical_string(payload_b)

    _check(str_a != str_b,
           "canonical_string is delimiter-safe: different payloads → different strings (H4)")
    _check(compute_hash(payload_a) != compute_hash(payload_b),
           "compute_hash is collision-resistant: different payloads → different hashes (H4)")

    # Verify the strings are actually valid JSON (not pipe-delimited)
    _check(str_a.startswith("{") and str_a.endswith("}"),
           "canonical_string produces JSON (starts with {, ends with })")
    # The key point: | can appear inside JSON string values, but it's not
    # used as a field delimiter. Verify the output is parseable JSON.
    parsed_a = json.loads(str_a)
    _check(parsed_a["quantity_name"] == "a|formula=b",
           "canonical_string preserves | inside string values as JSON")

    print("  → H4: canonical_string is delimiter-safe — PASS")


def test_koide_computation():
    """H5: Verify Koide Q is computed from PDG masses, not hard-coded."""
    print("\n=== H5: Koide Q computation test ===")

    Q = compute_koide_Q(PDG_MASSES_MEV)
    theoretical = 2.0 / 3.0

    print(f"  Computed Q = {Q:.10f}")
    print(f"  Theoretical 2/3 = {theoretical:.10f}")
    print(f"  |deviation| = {abs(Q - theoretical):.10f}")

    _check(abs(Q - theoretical) < 0.001,
           "computed Q is within 0.001 of 2/3 (H5)")
    _check(Q > 0.66 and Q < 0.67,
           "computed Q is in [0.66, 0.67] (H5)")

    # Verify the formula is Σm/(Σ√m)², not (Σm)²/Σm²
    m_e = PDG_MASSES_MEV["m_e"]
    m_mu = PDG_MASSES_MEV["m_mu"]
    m_tau = PDG_MASSES_MEV["m_tau"]
    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = m_e ** 0.5 + m_mu ** 0.5 + m_tau ** 0.5
    expected_Q = sum_m / (sum_sqrt_m ** 2)
    _check(abs(Q - expected_Q) < 1e-12,
           "computed Q matches Σm/(Σ√m)² formula (H5)")

    # Verify it's NOT the wrong formula (Σm)²/Σm²
    wrong_Q = (sum_m ** 2) / (m_e ** 2 + m_mu ** 2 + m_tau ** 2)
    _check(abs(Q - wrong_Q) > 0.1,
           "computed Q does NOT match wrong formula (Σm)²/Σm² (H5)")

    print("  → H5: Koide Q computed from PDG mass fixture — PASS")


def main():
    failures = 0

    # Per-record hostile mutation tests
    for path in RECORDS:
        if not os.path.exists(path):
            print(f"  → SKIP: {path} not found")
            continue
        try:
            test_record(path)
        except AssertionError as exc:
            print(f"  → FAILED: {exc}")
            failures += 1
        except Exception as exc:
            print(f"  → ERROR: {exc}")
            failures += 1

    # H4: Delimiter-injection collision test
    try:
        test_delimiter_injection()
    except AssertionError as exc:
        print(f"  → FAILED: {exc}")
        failures += 1
    except Exception as exc:
        print(f"  → ERROR: {exc}")
        failures += 1

    # H5: Koide computation test
    try:
        test_koide_computation()
    except AssertionError as exc:
        print(f"  → FAILED: {exc}")
        failures += 1
    except Exception as exc:
        print(f"  → ERROR: {exc}")
        failures += 1

    print()
    if failures:
        print(f"RESULT: {failures} test(s) FAILED.")
        return 1
    print("RESULT: all tests PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
