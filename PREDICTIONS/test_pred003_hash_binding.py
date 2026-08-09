#!/usr/bin/env python3
"""
test_pred003_hash_binding.py — Hostile mutation tests for PRED-003 v2 hash binding.

These tests prove that the v2 schema change (adding sigma_denominator and
committed_at to CANONICAL_FIELDS) actually binds both fields to the content
hash lock. The tests:

  1. Load each record, verify the stored hash passes.
  2. Mutate sigma_denominator → verify hash FAILS.
  3. Mutate committed_at → verify hash FAILS.
  4. Restore original → verify hash passes again.

Per Codex re-verification (2026-08-08, cfae2df): the v1 records had
sigma_denominator and committed_at outside the hash surface, so mutating
either left verify_hash() True. This file proves the v2 fix closes that gap.

Run:
    python3 PREDICTIONS/test_pred003_hash_binding.py
"""

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pre_register import verify_hash  # noqa: E402

RECORDS = [
    os.path.join(HERE, "pre_registrations",
                 "20260806T190015Z_neutrino_koide_Q_NO.json"),
    os.path.join(HERE, "pre_registrations",
                 "20260806T190020Z_neutrino_koide_Q_IO.json"),
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

    # 1. Original hash passes
    _check(verify_hash(record), "original record verify_hash == True")

    # 2. Mutate sigma_denominator → hash must FAIL
    mutated_sigma = copy.deepcopy(record)
    mutated_sigma["payload"]["sigma_denominator"] = "HOSTILE_MUTATION_test"
    _check(not verify_hash(mutated_sigma),
           "mutated sigma_denominator → verify_hash == False")

    # 3. Mutate committed_at (in payload) → hash must FAIL
    mutated_committed = copy.deepcopy(record)
    mutated_committed["payload"]["committed_at"] = "2099-01-01T00:00:00+00:00"
    _check(not verify_hash(mutated_committed),
           "mutated committed_at → verify_hash == False")

    # 4. Restore original → hash passes again
    restored = copy.deepcopy(record)
    _check(verify_hash(restored), "restored record verify_hash == True")

    # 5. Confirm schema version is v2
    _check(record.get("schema_version") == 2,
           f"schema_version == 2 (got {record.get('schema_version')})")

    # 6. Confirm amendments trail exists and documents the v1→v2 migration
    amendments = record.get("amendments", [])
    _check(len(amendments) >= 1, "amendments array non-empty")
    if amendments:
        am = amendments[0]
        _check("prior_hash" in am and "new_hash" in am,
               "amendment records prior_hash and new_hash")
        _check(am.get("prior_schema_version") == 1,
               "amendment records prior_schema_version == 1")
        _check(am.get("new_schema_version") == 2,
               "amendment records new_schema_version == 2")

    # 7. Confirm both new fields are in the payload (hash surface)
    _check("sigma_denominator" in record["payload"],
           "sigma_denominator present in payload")
    _check("committed_at" in record["payload"],
           "committed_at present in payload")

    # 8. Confirm the unit is dimensionless, not eV
    sigma_den = record["payload"]["sigma_denominator"]
    _check("eV" not in sigma_den,
           "sigma_denominator does not contain 'eV' (dimensionless Q units)")
    _check("dimensionless" in sigma_den,
           "sigma_denominator contains 'dimensionless'")

    print(f"  → {name}: ALL CHECKS PASSED")


def main():
    failures = 0
    for path in RECORDS:
        try:
            test_record(path)
        except AssertionError as exc:
            print(f"  → FAILED: {exc}")
            failures += 1
        except Exception as exc:
            print(f"  → ERROR: {exc}")
            failures += 1

    print()
    if failures:
        print(f"RESULT: {failures} record(s) FAILED hostile mutation tests.")
        return 1
    print("RESULT: all records PASSED hostile mutation tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
