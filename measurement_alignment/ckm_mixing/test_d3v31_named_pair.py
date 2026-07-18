#!/usr/bin/env python3
"""Executable test for the D3 v3.1 named root pairs and their endpoints.

Per Codex 2026-07-15 repair contract: test both exact named pairs by actually
passing them to the production continuation function.

This test verifies that:
1. The low-angle pair (-0.5537461078, -3.5420230460) passed to
   track_branch_interpolation produces endpoint ~4.308496 deg.
2. The high-angle pair (89.4462538922, 86.4579769540) passed to
   track_branch_interpolation produces endpoint ~0.182728 deg.
3. The two endpoints differ (negative assertion).

Run:
    python3 test_d3v31_named_pair.py
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ENDPOINT_TOL = 0.01  # 0.01 degrees


def _get_pdg_angles():
    """Get PDG 2024 FX angles for the endpoint configuration."""
    import d3_ckm_scan_v3_1 as v31
    fx = v31.extract_FX_angles(
        v31.V_CKM_standard(
            v31.S12, v31.S23, v31.S13, v31.DELTA_CP
        )
    )
    return fx["theta_d"], fx["theta_u"]


def test_low_pair_endpoint():
    """The low-angle initial pair must produce ~4.308496 deg."""
    import d3_ckm_scan_v3_1 as v31

    theta_d_pdg, theta_u_pdg = _get_pdg_angles()

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        initial_pair=v31.INITIAL_PAIR_LOW,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"Low-pair branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    expected = 4.308496
    diff = abs(endpoint - expected)
    assert diff < ENDPOINT_TOL, (
        f"Low-pair branch produced {endpoint:.7f} deg, "
        f"expected ~{expected} deg (diff={diff:.7f})"
    )
    print(f"[PASS] Low-pair -> {endpoint:.7f} deg (expected ~{expected})")


def test_high_pair_endpoint():
    """The high-angle initial pair must produce ~0.182728 deg."""
    import d3_ckm_scan_v3_1 as v31

    theta_d_pdg, theta_u_pdg = _get_pdg_angles()

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        initial_pair=v31.INITIAL_PAIR_HIGH,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"High-pair branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    expected = 0.182728
    diff = abs(endpoint - expected)
    assert diff < ENDPOINT_TOL, (
        f"High-pair branch produced {endpoint:.7f} deg, "
        f"expected ~{expected} deg (diff={diff:.7f})"
    )
    print(f"[PASS] High-pair -> {endpoint:.7f} deg (expected ~{expected})")


def test_endpoints_differ():
    """The low and high pair endpoints must differ (negative assertion)."""
    import d3_ckm_scan_v3_1 as v31

    theta_d_pdg, theta_u_pdg = _get_pdg_angles()

    result_low = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        initial_pair=v31.INITIAL_PAIR_LOW,
        k=1.0, n_steps=100,
    )
    result_high = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        initial_pair=v31.INITIAL_PAIR_HIGH,
        k=1.0, n_steps=100,
    )

    assert "error" not in result_low, f"Low-pair failed: {result_low.get('error')}"
    assert "error" not in result_high, f"High-pair failed: {result_high.get('error')}"

    ep_low = result_low["final_theta_23_deg"]
    ep_high = result_high["final_theta_23_deg"]
    diff = abs(ep_low - ep_high)
    assert diff > 0.5, (
        f"Endpoints too close: low={ep_low:.7f}, high={ep_high:.7f}, "
        f"diff={diff:.7f} deg. Branch selection may not be working."
    )
    print(f"[PASS] Endpoints differ: low={ep_low:.7f}, high={ep_high:.7f} "
          f"(diff={diff:.4f} deg)")


def test_not_smallest_positive_root():
    """The low-pair endpoint must be ~4.31, not smallest-positive-root ~0.21."""
    import d3_ckm_scan_v3_1 as v31

    theta_d_pdg, theta_u_pdg = _get_pdg_angles()

    result = v31.track_branch_interpolation(
        v31.ZEN_THETA_D, v31.ZEN_THETA_U,
        v31.PAPER_DOWN, v31.PAPER_UP,
        v31.PDG_DOWN, v31.PDG_UP,
        theta_d_pdg, theta_u_pdg,
        initial_pair=v31.INITIAL_PAIR_LOW,
        k=1.0, n_steps=100,
    )

    assert "error" not in result, f"Branch continuation failed: {result.get('error')}"

    endpoint = result["final_theta_23_deg"]
    smallest_root = 0.2077  # v2's result
    diff_from_smallest = abs(endpoint - smallest_root)
    assert diff_from_smallest > 0.5, (
        f"Endpoint {endpoint:.7f} deg is too close to the smallest-positive-root "
        f"{smallest_root} deg (diff={diff_from_smallest:.7f})."
    )
    print(f"[PASS] Endpoint {endpoint:.7f} deg is the paper branch, not smallest-root {smallest_root} deg")


def test_no_rounded_selector():
    """Verify that track_branch_interpolation requires initial_pair (no rounded selector)."""
    import d3_ckm_scan_v3_1 as v31
    import inspect

    sig = inspect.signature(v31.track_branch_interpolation)
    assert "initial_pair" in sig.parameters, (
        "track_branch_interpolation must have an initial_pair parameter"
    )
    assert "target_diff" not in str(sig), (
        "track_branch_interpolation must not use target_diff"
    )
    # Verify initial_pair has no default (required argument)
    param = sig.parameters["initial_pair"]
    assert param.default is inspect.Parameter.empty, (
        "initial_pair must be a required argument, not optional"
    )
    print(f"[PASS] track_branch_interpolation requires initial_pair (no rounded selector)")


def main():
    print("=== D3 v3.1 Named Pair and Endpoint Test ===")
    print()

    tests = [
        test_no_rounded_selector,
        test_low_pair_endpoint,
        test_high_pair_endpoint,
        test_endpoints_differ,
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
