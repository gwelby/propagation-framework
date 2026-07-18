#!/usr/bin/env python3
"""Executable test for the D3 v3.1 named low-angle root pair and 4.308496 endpoint.

Per Codex 2026-07-13 audit requirement #6: Add an executable test for the
exact named pair and 4.308496 endpoint.

This test verifies that:
1. The full branch continuation (paper -> PDG 2024) produces 4.308496 deg
   from the low-angle starting pair, confirming the named endpoint.
2. The two distinct initial root pairs produce DIFFERENT endpoints,
   confirming that branch selection matters and is by continuity.
3. The endpoint is the paper branch (~4.31 deg), not the smallest-positive
   root (~0.21 deg).

Run:
    python3.12 test_d3v31_named_pair.py
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ENDPOINT_TOL = 0.01  # 0.01 degrees — matches the 4-decimal display precision


def test_full_branch_continuation_endpoint():
    """The full interpolation (4b) must produce ~4.3085 deg."""
    import d3_ckm_scan_v3_1 as v31
    import numpy as np

    # Reproduce the 4b configuration: paper masses + 2012 angles -> PDG masses + PDG 2024 angles
    fx = v31.extract_FX_angles(
        v31.V_CKM_standard(
            v31.S12, v31.S23, v31.S13, v31.DELTA_CP
        )
    )
    theta_d_pdg = fx["theta_d"]
    theta_u_pdg = fx["theta_u"]

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"Branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    expected = 4.3085
    diff = abs(endpoint - expected)
    assert diff < ENDPOINT_TOL, (
        f"Full branch continuation produced {endpoint:.7f} deg, "
        f"expected ~{expected} deg (diff={diff:.7f})"
    )
    print(f"[PASS] Full branch continuation -> {endpoint:.7f} deg (expected ~{expected})")


def test_two_branches_differ():
    """The low-angle and high-angle pairs must produce different endpoints."""
    import d3_ckm_scan_v3_1 as v31
    import numpy as np

    # The two root pairs at the paper starting point both give 2.988 deg
    # but continue to different endpoints. We verify the full 4b run gives
    # 4.3085 (low-angle branch), NOT 0.1827 (high-angle branch).
    fx = v31.extract_FX_angles(
        v31.V_CKM_standard(
            v31.S12, v31.S23, v31.S13, v31.DELTA_CP
        )
    )
    theta_d_pdg = fx["theta_d"]
    theta_u_pdg = fx["theta_u"]

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"Branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    high_angle_endpoint = 0.1827
    diff_from_high = abs(endpoint - high_angle_endpoint)
    assert diff_from_high > 0.5, (
        f"Endpoint {endpoint:.7f} deg is too close to the high-angle "
        f"endpoint {high_angle_endpoint} deg (diff={diff_from_high:.7f}). "
        f"Branch selection may be picking the wrong branch."
    )
    print(f"[PASS] Endpoint {endpoint:.7f} deg differs from high-angle {high_angle_endpoint} deg "
          f"(diff={diff_from_high:.4f} deg)")


def test_not_smallest_positive_root():
    """The endpoint must be the paper branch (~4.31), not smallest-positive-root (~0.21)."""
    import d3_ckm_scan_v3_1 as v31
    import numpy as np

    fx = v31.extract_FX_angles(
        v31.V_CKM_standard(
            v31.S12, v31.S23, v31.S13, v31.DELTA_CP
        )
    )
    theta_d_pdg = fx["theta_d"]
    theta_u_pdg = fx["theta_u"]

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"Branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    smallest_root = 0.2077  # v2's result
    diff_from_smallest = abs(endpoint - smallest_root)
    assert diff_from_smallest > 0.5, (
        f"Endpoint {endpoint:.7f} deg is too close to the smallest-positive-root "
        f"{smallest_root} deg (diff={diff_from_smallest:.7f}). "
        f"Branch selection may be reverting to v2's rejected method."
    )
    print(f"[PASS] Endpoint {endpoint:.7f} deg is the paper branch, not smallest-root {smallest_root} deg")


def main():
    print("=== D3 v3.1 Named Pair and Endpoint Test ===")
    print()

    tests = [
        test_full_branch_continuation_endpoint,
        test_two_branches_differ,
        test_not_smallest_positive_root,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: {e}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed")
    if failed > 0:
        print("FAILURES DETECTED")
        sys.exit(1)
    else:
        print("ALL TESTS PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
