"""
Exact sign-structure comparison: Sigma_vac vs Sigma_escape.

Role
----
This module implements task 8.1 of
.kiro/specs/god-eq-path-b-family-c/tasks.md and Requirements 7.1-7.4 of
.kiro/specs/god-eq-path-b-family-c/requirements.md.

Given:

  * Sigma_vac  -- the exact free linearized Z_3 vacuum covariance in the
                  channel basis from verification.vacuum_propagator, which
                  is C_3-circulant symmetric with POSITIVE off-diagonals on
                  the stable branch m^2 > 2 kappa > 0.

  * Sigma_escape -- the Family A whitening covariance (A A^T)^{-1} with
                    A = T_sym^3 from verification.operator_algebra, which is
                    C_3-circulant symmetric with exact integer entries
                    (diag 43, off-diag -21) and NEGATIVE off-diagonals.

The note derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md fixes
the sign structure at every point of the stable branch:

  off_diag(Sigma_vac)    =  (nu_0 - nu_1) / 3 > 0   (Requirement 7.1, 7.2)
  off_diag(Sigma_escape) =  -21               < 0   (Requirement 7.3)

Because the two off-diagonal signs are opposite everywhere on the stable
branch, and multiplication by a positive scalar cannot flip a sign, no
positive rescaling of Sigma_vac can coincide with Sigma_escape as
matrices. Sign structure alone therefore rules out an approach of
Sigma_vac to Sigma_escape on the stable branch (Requirement 7.4). This
module records that verdict programmatically and also offers a
parameter-space scan that finds the closest regime under several
distance metrics, with an explicit note that proximity under a metric
is a strictly weaker notion than literal coincidence.

Public API
----------
- `EscapeComparison`                dataclass summarising compare_with_escape
- `compare_with_escape(Sigma_vac, Sigma_escape)`      -> EscapeComparison
- `signed_distance(A, B, metric=...)`                 -> float
- `ScanResult`                      dataclass summarising scan_stable_branch
- `scan_stable_branch(...)`                           -> ScanResult
- `SUPPORTED_METRICS`               tuple of valid metric names
- CLI self-check via `if __name__ == "__main__"`

Scope
-----
This module only compares the exact Sigma_vac of the free linearized
vacuum with the exact Family A escape covariance. It does not make any
claim about nonlinear PF or about a physically justified one-medium
probability law. It explicitly does not upgrade any confidence score and
does not claim "H_prod is proved" or equivalent.

Guardrails
----------
This file lives under `verification/` only. It does not edit CLAIMS.md,
ACTIVE_ISSUES.md, WHATS_NEXT.md, requirements.md, design.md, or any
derivation note.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np

from verification.operator_algebra import (
    Sigma_escape,
    TOL,
    is_c3_circulant_symmetric,
)
from verification.vacuum_propagator import compute_vacuum_covariance


# ----------------------------------------------------------------------
# Metric registry
# ----------------------------------------------------------------------

SUPPORTED_METRICS: Tuple[str, ...] = (
    # Absolute Frobenius norm ||A - B||_F. Scale-dependent.
    "frobenius",
    # Euclidean distance in the (diagonal, off-diagonal) reduced coordinate.
    # Both inputs are assumed C_3-circulant; for such matrices the full
    # Frobenius distance is 3 * sqrt((d_A - d_B)^2 + 2 (o_A - o_B)^2), so
    # this metric is a clean two-dimensional projection of that data.
    "circulant_euclidean",
    # Scale-invariant comparison of the ratio o/d. Positive for Sigma_vac,
    # negative for Sigma_escape, so the gap is bounded below by the
    # absolute value of (o_escape / d_escape) whenever o_vac >= 0.
    "normalized_off_diagonal_ratio",
    # Best achievable Frobenius distance after positive rescaling of A.
    # d_rescaled(A, B) = min_{c > 0} ||c A - B||_F. Zero only if c A = B.
    # For C_3-circulant inputs with opposite off-diagonal signs the
    # optimal rescaling is constrained by that sign flip; in particular
    # when o_A > 0 and o_B < 0 the best c is pinned on the c >= 0 boundary
    # at the unconstrained optimum and cannot drive the distance to zero.
    "rescaled_frobenius",
)


def _circulant_reduced_coords(A: np.ndarray) -> Tuple[float, float]:
    """Return (diagonal, off_diagonal) of a C_3-circulant symmetric 3x3.

    Raises
    ------
    ValueError
        If A is not C_3-circulant symmetric to the module tolerance.
    """
    if not is_c3_circulant_symmetric(A, tol=TOL):
        raise ValueError(
            "Input matrix is not C_3-circulant symmetric within tolerance; "
            "escape comparison assumes canonical C_3-circulant structure."
        )
    arr = np.real(np.asarray(A))
    d = float(arr[0, 0])
    o = float(arr[0, 1])
    return d, o


def signed_distance(
    A: np.ndarray,
    B: np.ndarray,
    metric: str = "frobenius",
) -> float:
    """Return a distance between two C_3-circulant symmetric 3x3 matrices.

    Parameters
    ----------
    A, B : np.ndarray
        3x3 C_3-circulant symmetric matrices.
    metric : str
        One of `SUPPORTED_METRICS`.

    Returns
    -------
    float
        Non-negative scalar distance. Zero iff the two matrices are equal
        (for 'frobenius', 'circulant_euclidean') or iff B is a positive
        multiple of A (for 'rescaled_frobenius'); `normalized_off_diagonal_ratio`
        returns |o_A / d_A - o_B / d_B|, which is the absolute gap in the
        scale-invariant off-diagonal ratio (unsigned).

    Notes
    -----
    The metric is "signed" only in the colloquial sense that it records a
    structural comparison; the returned value itself is always >= 0.
    """
    if metric not in SUPPORTED_METRICS:
        raise ValueError(
            f"Unknown metric {metric!r}; supported metrics are "
            f"{SUPPORTED_METRICS}"
        )

    d_A, o_A = _circulant_reduced_coords(A)
    d_B, o_B = _circulant_reduced_coords(B)

    if metric == "frobenius":
        return float(np.linalg.norm(np.asarray(A) - np.asarray(B)))

    if metric == "circulant_euclidean":
        return float(np.hypot(d_A - d_B, np.sqrt(2.0) * (o_A - o_B)))

    if metric == "normalized_off_diagonal_ratio":
        if abs(d_A) < TOL or abs(d_B) < TOL:
            raise ValueError(
                "normalized_off_diagonal_ratio requires nonzero diagonal "
                f"entries; got d_A={d_A}, d_B={d_B}"
            )
        return float(abs(o_A / d_A - o_B / d_B))

    if metric == "rescaled_frobenius":
        # Best c >= 0 minimising ||c A - B||_F^2. Unconstrained optimum is
        # c* = <A, B>_F / ||A||_F^2. If c* < 0, the constrained optimum is
        # c = 0 with distance ||B||_F. Zero distance requires c A = B,
        # which for C_3-circulant inputs means d_B = c d_A and
        # o_B = c o_A with the same sign (so sign(o_A) == sign(o_B) is
        # necessary).
        A_arr = np.asarray(A, dtype=float)
        B_arr = np.asarray(B, dtype=float)
        A_norm_sq = float(np.sum(A_arr * A_arr))
        if A_norm_sq < TOL:
            return float(np.linalg.norm(B_arr))
        c_star = float(np.sum(A_arr * B_arr) / A_norm_sq)
        c_opt = c_star if c_star > 0.0 else 0.0
        return float(np.linalg.norm(c_opt * A_arr - B_arr))

    # Unreachable given the membership check above.
    raise AssertionError(f"metric {metric!r} dispatch fell through")


# ----------------------------------------------------------------------
# Structured comparison result
# ----------------------------------------------------------------------


@dataclass
class EscapeComparison:
    """Result of `compare_with_escape`.

    Attributes
    ----------
    vac_diagonal, vac_off_diagonal : float
        Reduced coordinates of Sigma_vac.
    escape_diagonal, escape_off_diagonal : float
        Reduced coordinates of Sigma_escape.
    vac_sign : int
        sign(vac_off_diagonal): +1, 0, or -1.
    escape_sign : int
        sign(escape_off_diagonal): +1, 0, or -1.
    signs_opposite : bool
        True iff vac_sign and escape_sign are strictly opposite non-zero
        signs (one +1, the other -1).
    can_coincide_in_sign : bool
        False iff signs are opposite; True otherwise. Positive rescaling
        preserves signs, so False here means no positive rescaling of
        Sigma_vac can coincide with Sigma_escape.
    normalized_off_diagonal_ratio_gap : float
        |o_vac / d_vac - o_escape / d_escape|. The scale-invariant gap
        between the off-diagonal-to-diagonal ratios.
    frobenius_distance : float
        ||Sigma_vac - Sigma_escape||_F. Absolute, scale-dependent.
    rescaled_frobenius_distance : float
        min_{c >= 0} ||c Sigma_vac - Sigma_escape||_F. Zero iff a positive
        rescaling of Sigma_vac equals Sigma_escape; strictly positive when
        the off-diagonal signs disagree.
    verdict : str
        Human-readable summary of the structural comparison.
    """

    vac_diagonal: float
    vac_off_diagonal: float
    escape_diagonal: float
    escape_off_diagonal: float
    vac_sign: int
    escape_sign: int
    signs_opposite: bool
    can_coincide_in_sign: bool
    normalized_off_diagonal_ratio_gap: float
    frobenius_distance: float
    rescaled_frobenius_distance: float
    verdict: str


def _sign(x: float, tol: float = TOL) -> int:
    """Return +1, 0, -1 for x with a tolerance around zero."""
    if x > tol:
        return 1
    if x < -tol:
        return -1
    return 0


def compare_with_escape(
    Sigma_vac: np.ndarray,
    Sigma_escape_: np.ndarray = Sigma_escape,
) -> EscapeComparison:
    """Compare the sign structure of Sigma_vac against Sigma_escape.

    Implements Requirements 7.1-7.4:

      7.1 Record whether off-diagonals of Sigma_vac are zero, positive, or
          negative.
      7.2 On the stable branch (nu_0 > nu_1), the off-diagonals are strictly
          positive; this is a precondition of callers using
          compute_vacuum_covariance, which enforces m^2 > 2 kappa > 0.
      7.3 Compare explicitly against Sigma_escape, whose off-diagonals are
          strictly negative (-21 with the canonical scale from
          operator_algebra.py).
      7.4 State whether Sigma_vac can approach Sigma_escape on the stable
          branch. This function records that sign structure alone rules
          out literal approach (matrices can never coincide, even up to
          positive rescaling) and reports the rescaled Frobenius distance
          to show the gap is strictly positive. It explicitly does not
          claim any stronger result than sign structure; for that a
          parameter scan under an explicit metric is provided by
          `scan_stable_branch`.

    Parameters
    ----------
    Sigma_vac : np.ndarray
        3x3 C_3-circulant symmetric matrix, typically the output of
        `compute_vacuum_covariance`.
    Sigma_escape_ : np.ndarray, optional
        Escape covariance. Defaults to the module-level Sigma_escape.

    Returns
    -------
    EscapeComparison
        Structured comparison result.

    Raises
    ------
    ValueError
        If either input is not C_3-circulant symmetric.
    """
    d_vac, o_vac = _circulant_reduced_coords(Sigma_vac)
    d_esc, o_esc = _circulant_reduced_coords(Sigma_escape_)

    s_vac = _sign(o_vac)
    s_esc = _sign(o_esc)
    signs_opposite = (s_vac == 1 and s_esc == -1) or (s_vac == -1 and s_esc == 1)
    can_coincide_in_sign = not signs_opposite

    ratio_gap = signed_distance(
        Sigma_vac, Sigma_escape_, metric="normalized_off_diagonal_ratio"
    )
    frob_distance = signed_distance(Sigma_vac, Sigma_escape_, metric="frobenius")
    rescaled_distance = signed_distance(
        Sigma_vac, Sigma_escape_, metric="rescaled_frobenius"
    )

    if signs_opposite and s_vac == 1 and s_esc == -1:
        verdict = (
            "Sigma_vac off-diagonals are positive (stable branch: nu_0 > nu_1), "
            "Sigma_escape off-diagonals are negative. The two off-diagonal "
            "signs are opposite everywhere on the stable branch, so no "
            "positive rescaling of Sigma_vac can coincide with Sigma_escape. "
            "Sign structure alone rules out approach of Sigma_vac to "
            "Sigma_escape as matrices (Requirement 7.4 closed by sign). "
            "Closeness under a quantitative metric is a strictly weaker "
            "notion than literal approach; see scan_stable_branch for a "
            "parameter-space scan under an explicit distance metric."
        )
    elif s_vac == 0 or s_esc == 0:
        verdict = (
            "Sigma_vac off-diagonal has sign {svac} and Sigma_escape off-"
            "diagonal has sign {sesc}. At least one is zero within "
            "tolerance; sign structure alone does not rule out approach. "
            "Inspect the quantitative distances below."
        ).format(svac=s_vac, sesc=s_esc)
    elif not signs_opposite:
        verdict = (
            "Sigma_vac and Sigma_escape off-diagonals share the same sign "
            "({svac}). Sign structure alone does not rule out approach; "
            "inspect the quantitative distances below."
        ).format(svac=s_vac)
    else:
        # signs_opposite with s_vac = -1 and s_esc = +1 (not physical for
        # the canonical escape matrix, but handle symmetrically).
        verdict = (
            "Sigma_vac off-diagonals are negative and Sigma_escape off-"
            "diagonals are positive. Opposite signs rule out matrix "
            "coincidence under positive rescaling."
        )

    return EscapeComparison(
        vac_diagonal=d_vac,
        vac_off_diagonal=o_vac,
        escape_diagonal=d_esc,
        escape_off_diagonal=o_esc,
        vac_sign=s_vac,
        escape_sign=s_esc,
        signs_opposite=signs_opposite,
        can_coincide_in_sign=can_coincide_in_sign,
        normalized_off_diagonal_ratio_gap=ratio_gap,
        frobenius_distance=frob_distance,
        rescaled_frobenius_distance=rescaled_distance,
        verdict=verdict,
    )


# ----------------------------------------------------------------------
# Parameter-space scan
# ----------------------------------------------------------------------


@dataclass
class ScanResult:
    """Result of `scan_stable_branch`.

    Attributes
    ----------
    metric : str
        The distance metric used for the scan.
    n_points : int
        Number of (m_sq, kappa, p_abs) grid points evaluated on the
        stable branch m^2 > 2 kappa > 0.
    best_params : tuple[float, float, float]
        (m_sq, kappa, p_abs) at which the metric attained its minimum.
    best_distance : float
        Minimum value of the metric over the grid.
    best_sigma_vac : np.ndarray
        Sigma_vac evaluated at best_params.
    best_comparison : EscapeComparison
        Full structural comparison at best_params.
    distance_range : tuple[float, float]
        (min, max) of the metric across the whole grid, for context.
    note : str
        Plain-language caveat that proximity under a metric is weaker
        than literal coincidence, and that the scan is a reproducer on a
        bounded grid, not a Monte Carlo search.
    """

    metric: str
    n_points: int
    best_params: Tuple[float, float, float]
    best_distance: float
    best_sigma_vac: np.ndarray
    best_comparison: EscapeComparison
    distance_range: Tuple[float, float]
    note: str = field(default="")


def scan_stable_branch(
    metric: str = "rescaled_frobenius",
    m_sq_values: Optional[np.ndarray] = None,
    kappa_fractions: Optional[np.ndarray] = None,
    p_abs_values: Optional[np.ndarray] = None,
    kappa_eps: float = 1e-3,
    sigma_escape_: np.ndarray = Sigma_escape,
) -> ScanResult:
    """Scan a bounded grid on the stable branch and report the closest regime.

    The grid is constructed as

        m^2       in m_sq_values   (default: 12 log-spaced points in [0.5, 10])
        kappa/m^2 in kappa_fractions (default: 10 linearly spaced points in
                                     [kappa_eps, 0.5 - kappa_eps])
        |p|       in p_abs_values  (default: 8 linearly spaced points in [0, 5])

    with every point satisfying the stability constraint m^2 > 2 kappa
    by construction. For each (m^2, kappa, |p|) the function computes
    Sigma_vac via `compute_vacuum_covariance` and records the distance to
    Sigma_escape under the requested metric. The minimum and its
    argminimum are returned together with the full structural
    comparison at that point.

    The scan is a short reproducer, not a Monte Carlo search. Its purpose
    is to exhibit the regime of closest approach under an explicit metric
    so that Requirement 7.4 can be closed either "by sign structure" (if
    best_comparison.signs_opposite is True) or by reporting the best
    approach under a quantitative metric. Proximity under a metric is a
    strictly weaker notion than literal coincidence.

    Parameters
    ----------
    metric : str
        One of `SUPPORTED_METRICS`. Default 'rescaled_frobenius'.
    m_sq_values, kappa_fractions, p_abs_values : np.ndarray, optional
        Explicit grids; override the defaults above.
    kappa_eps : float
        Safety margin away from kappa = 0 and kappa = m^2 / 2 (stability
        edge where nu_0 diverges). Defaults to 1e-3.
    sigma_escape_ : np.ndarray, optional
        Reference escape covariance. Defaults to the module-level
        Sigma_escape.

    Returns
    -------
    ScanResult
    """
    if metric not in SUPPORTED_METRICS:
        raise ValueError(
            f"Unknown metric {metric!r}; supported metrics are {SUPPORTED_METRICS}"
        )

    if m_sq_values is None:
        m_sq_values = np.geomspace(0.5, 10.0, 12)
    if kappa_fractions is None:
        kappa_fractions = np.linspace(kappa_eps, 0.5 - kappa_eps, 10)
    if p_abs_values is None:
        p_abs_values = np.linspace(0.0, 5.0, 8)

    best_distance = np.inf
    best_params: Tuple[float, float, float] = (float("nan"),) * 3
    best_sigma: Optional[np.ndarray] = None
    max_distance = -np.inf
    n_points = 0

    for m_sq in m_sq_values:
        m_sq_f = float(m_sq)
        for frac in kappa_fractions:
            kappa = float(frac) * m_sq_f
            # Respect strict stability: m^2 > 2 kappa > 0.
            if kappa <= 0.0 or kappa >= 0.5 * m_sq_f:
                continue
            for p_abs in p_abs_values:
                p_abs_f = float(p_abs)
                if p_abs_f < 0.0:
                    continue
                sigma = compute_vacuum_covariance(m_sq_f, kappa, p_abs_f)
                dist = signed_distance(sigma, sigma_escape_, metric=metric)
                n_points += 1
                if dist > max_distance:
                    max_distance = dist
                if dist < best_distance:
                    best_distance = dist
                    best_params = (m_sq_f, kappa, p_abs_f)
                    best_sigma = sigma

    if best_sigma is None or n_points == 0:
        raise ValueError(
            "Parameter grid produced no stable-branch points; adjust "
            "m_sq_values, kappa_fractions, or kappa_eps."
        )

    best_comparison = compare_with_escape(best_sigma, sigma_escape_)
    distance_range = (float(best_distance), float(max_distance))

    note = (
        "Scan is a bounded-grid reproducer on the stable branch "
        "(m^2 > 2 kappa > 0). Proximity under the chosen metric is "
        "STRICTLY WEAKER than literal coincidence of Sigma_vac with "
        "Sigma_escape: the two matrices have opposite off-diagonal signs "
        "everywhere on the stable branch, so no positive rescaling of "
        "Sigma_vac reaches Sigma_escape. The regime below is reported "
        "only to exhibit the closest grid point under the metric."
    )

    return ScanResult(
        metric=metric,
        n_points=n_points,
        best_params=best_params,
        best_distance=float(best_distance),
        best_sigma_vac=best_sigma,
        best_comparison=best_comparison,
        distance_range=distance_range,
        note=note,
    )


__all__ = [
    "SUPPORTED_METRICS",
    "EscapeComparison",
    "ScanResult",
    "compare_with_escape",
    "signed_distance",
    "scan_stable_branch",
]


# ----------------------------------------------------------------------
# CLI / self-check
# ----------------------------------------------------------------------


if __name__ == "__main__":
    print("verification.escape_comparison")
    print("-" * 60)

    # --- Worked example (design.md Example 2): m^2 = 1, kappa = 0.1, |p| = 0
    sigma_vac_example = compute_vacuum_covariance(m_sq=1.0, kappa=0.1, p_abs=0.0)
    cmp_example = compare_with_escape(sigma_vac_example)

    np.set_printoptions(precision=4, suppress=True)
    print()
    print("Worked example (m^2 = 1, kappa = 0.1, |p| = 0):")
    print("  Sigma_vac =")
    print(sigma_vac_example)
    print("  Sigma_escape =")
    print(Sigma_escape)
    print()
    print(f"  Sigma_vac    diagonal = {cmp_example.vac_diagonal:.6f}, "
          f"off-diagonal = {cmp_example.vac_off_diagonal:.6f}")
    print(f"  Sigma_escape diagonal = {cmp_example.escape_diagonal:.6f}, "
          f"off-diagonal = {cmp_example.escape_off_diagonal:.6f}")
    print(f"  signs: vac = {cmp_example.vac_sign:+d}, "
          f"escape = {cmp_example.escape_sign:+d}")
    print(f"  signs_opposite       = {cmp_example.signs_opposite}")
    print(f"  can_coincide_in_sign = {cmp_example.can_coincide_in_sign}")
    print(f"  normalized off-diag ratio gap = "
          f"{cmp_example.normalized_off_diagonal_ratio_gap:.6f}")
    print(f"  frobenius distance            = "
          f"{cmp_example.frobenius_distance:.6f}")
    print(f"  rescaled frobenius distance   = "
          f"{cmp_example.rescaled_frobenius_distance:.6f}")
    print()
    print("  verdict:")
    print(f"    {cmp_example.verdict}")
    np.set_printoptions()

    # --- Assertions on the worked example ---
    # Sigma_vac off-diagonals must be positive on the stable branch.
    assert cmp_example.vac_sign == 1, (
        f"expected positive Sigma_vac off-diagonal sign, got {cmp_example.vac_sign}"
    )
    # Sigma_escape off-diagonals must be negative.
    assert cmp_example.escape_sign == -1, (
        f"expected negative Sigma_escape off-diagonal sign, got "
        f"{cmp_example.escape_sign}"
    )
    # Core R7.3 / R7.4 verdict: signs are opposite, no positive rescaling
    # brings them together.
    assert cmp_example.signs_opposite is True, (
        "Sigma_vac and Sigma_escape must have opposite off-diagonal signs "
        "on the stable branch"
    )
    assert cmp_example.can_coincide_in_sign is False, (
        "Opposite signs must imply can_coincide_in_sign = False"
    )
    # Quantitative distances must be strictly positive.
    assert cmp_example.frobenius_distance > 0.0
    assert cmp_example.rescaled_frobenius_distance > 0.0
    # Scale-invariant ratio gap: Sigma_escape ratio is -21/43 ~ -0.488;
    # Sigma_vac ratio on this point is about 0.027 / 0.504 ~ 0.054.
    # The gap must therefore be at least ~0.54.
    assert cmp_example.normalized_off_diagonal_ratio_gap > 0.5, (
        "normalized off-diagonal ratio gap should reflect the opposite "
        "signs and be well above 0.5; got "
        f"{cmp_example.normalized_off_diagonal_ratio_gap}"
    )
    # Verdict string must mention the sign-structure closure.
    assert "sign structure" in cmp_example.verdict.lower()
    assert "positive" in cmp_example.verdict.lower()
    assert "negative" in cmp_example.verdict.lower()

    # --- signed_distance sanity ---
    # Frobenius distance of Sigma_vac to itself is zero.
    assert signed_distance(
        sigma_vac_example, sigma_vac_example, metric="frobenius"
    ) < TOL
    # Rescaled Frobenius distance of Sigma_vac to a positive multiple is zero.
    two_sigma = 2.0 * sigma_vac_example
    assert signed_distance(
        sigma_vac_example, two_sigma, metric="rescaled_frobenius"
    ) < 1e-10, (
        "rescaled_frobenius of Sigma_vac vs 2*Sigma_vac should vanish"
    )
    # Unknown metric raises.
    raised = False
    try:
        signed_distance(sigma_vac_example, Sigma_escape, metric="nonsense")
    except ValueError:
        raised = True
    assert raised, "signed_distance should reject unknown metrics"

    # --- Parameter-space scan ---
    print()
    print("Parameter-space scan on the stable branch (m^2 > 2 kappa > 0)")
    for metric in (
        "frobenius",
        "circulant_euclidean",
        "normalized_off_diagonal_ratio",
        "rescaled_frobenius",
    ):
        scan = scan_stable_branch(metric=metric)
        m_sq_b, kappa_b, p_abs_b = scan.best_params
        print()
        print(f"  metric = {metric}")
        print(f"    grid size      = {scan.n_points} points")
        print(
            f"    best point     = m^2 = {m_sq_b:.4f}, "
            f"kappa = {kappa_b:.4f}, |p| = {p_abs_b:.4f}"
        )
        print(
            f"    distance range = [{scan.distance_range[0]:.4e}, "
            f"{scan.distance_range[1]:.4e}]"
        )
        print(
            f"    best distance  = {scan.best_distance:.4e} "
            "(strictly positive; opposite off-diagonal signs persist)"
        )
        # The minimum must be strictly positive under every metric because
        # the off-diagonal signs disagree on the whole stable branch.
        assert scan.best_distance > 0.0, (
            f"scan under metric {metric} reached distance 0 unexpectedly"
        )
        # At the best grid point the comparison must still report opposite
        # off-diagonal signs.
        assert scan.best_comparison.signs_opposite is True, (
            f"best grid point under metric {metric} lost opposite-sign "
            "property; this would contradict the stable-branch proof"
        )

    # Final line states R7.4 resolution explicitly.
    print()
    print(
        "Conclusion (Requirement 7.4): Sigma_vac off-diagonals are "
        "POSITIVE on the stable branch (from nu_0 > nu_1); Sigma_escape "
        "off-diagonals are NEGATIVE. The opposite signs persist at every "
        "grid point of the scan, so no positive rescaling of Sigma_vac "
        "can coincide with Sigma_escape. Sign structure alone settles "
        "the matrix-level comparison; proximity under a specific metric "
        "is a strictly weaker notion and is reported above only for "
        "reference."
    )
    print()
    print("all escape_comparison self-checks passed")
