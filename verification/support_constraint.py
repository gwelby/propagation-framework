"""
Corrected support-constraint test for Family C kernel triples.

Role
----
This module implements Algorithm 1 (SupportConstraintTest) of
derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md
and Section 3 of the Family C design document.

Given a real symmetric 3x3 kernel triple {K_0, K_1, K_2} defining quadratic
observables X^(r) = chi(0)^T K_r chi(0), the test classifies the triple
into one of three buckets:

    BLOCKED
        There exist nontrivial real coefficients (a_0, a_1, a_2) != 0
        with sum_r a_r K_r = 0 (as a symmetric 3x3 matrix). Equivalently,
        the three symmetric matrices are linearly dependent. On any
        full-support probe (e.g. chi(0) ~ N(0, Sigma) with Sigma > 0),
        this forces sum_r a_r X^(r) = 0 almost surely, which is an
        exact deterministic relation among the observables. Such a
        triple cannot support a nontrivial one-medium H_prod
        factorization on that support.

        This is the actual no-go mechanism the edge-flux Family B audit
        relied on when it found K_0 + K_1 + K_2 = 0 deterministically
        (god_eq_path_b_edge_flux_current_no_go_2026-04-01.md Section 2):
        the kernels are linearly dependent, so J^(0) + J^(1) + J^(2) = 0
        for every chi(0), not just on average.

    OPEN_with_shared_norm_coupling
        The kernels are linearly independent, but their sum is a
        scalar multiple of the identity:

            K_0 + K_1 + K_2 = c * I     for some c in R.

        Under a Gaussian probe chi(0) ~ N(0, Sigma) this gives only

            X^(0) + X^(1) + X^(2) = c * ||chi(0)||^2,

        which is NOT deterministic -- it depends on the random norm
        ||chi(0)||. So this bucket is NOT an automatic no-go. The
        triple merely exhibits a shared-norm coupling and must still
        be tested at the probe-level Gaussian factorization stage
        (verification/gaussian_factorization.py).

        This is the specific correction the Family C design document
        emphasizes (Requirement 3.3 and Correctness Property P3 of
        .kiro/specs/god-eq-path-b-family-c/design.md): earlier
        Family B audits occasionally over-called K_0 + K_1 + K_2 = cI
        as a support-level no-go. It is not, under a full-support
        Gaussian probe. The deterministic case is strictly stronger.

    OPEN
        The kernels are linearly independent and their sum is not
        proportional to the identity. There is no support-level
        obstruction of either type, so the triple must continue to
        the covariance / joint-law analysis.

Canonical algorithm
-------------------
For each candidate kernel triple {K_0, K_1, K_2}:

    1. Vectorize each symmetric 3x3 matrix into a 6-vector via
       sym_to_vec6(K) = [K[0,0], K[0,1], K[0,2], K[1,1], K[1,2], K[2,2]].
       This is a faithful linear injection of Sym(3) into R^6, so
       linear dependence among the K_r as symmetric matrices is
       exactly linear dependence among the 6-vectors.

    2. Stack the three vectorized kernels as the columns of a 6x3
       real matrix V.

    3. Compute the SVD V = U S V^T. V has rank 3 iff its smallest
       singular value sigma_min is "large enough". We use the
       relative criterion sigma_min > tol * sigma_max to decide
       this, where sigma_max = s[0] is the largest singular value.

    4. If sigma_min <= tol * sigma_max (rank < 3), the right
       singular vector associated with sigma_min is a nonzero
       3-vector (a_0, a_1, a_2) satisfying V @ (a_0, a_1, a_2)^T
       approximately zero, i.e. sum_r a_r K_r is approximately the
       zero matrix. Classify as BLOCKED and return the coefficients.

    5. Otherwise, check whether K_0 + K_1 + K_2 = c * I to tolerance
       tol. If yes, return OPEN_with_shared_norm_coupling.
       Otherwise return OPEN.

The relative-tolerance check in step 3 is robust against uniform
rescaling of the kernels (multiplying all K_r by a common factor
scales both sigma_min and sigma_max by the same amount, leaving
the ratio unchanged).

Module-level self-check
-----------------------
At import time, the module verifies classifications on four
reference cases:

    * trivially collapsed canonical family K_0 = K_1 = K_2 = P_0
      (rank-1 in the vectorized sense, so BLOCKED);
    * the symmetric edge-flux kernels from
      god_eq_path_b_edge_flux_current_no_go_2026-04-01.md Section 1,
      which sum to 0 deterministically (BLOCKED);
    * the standard channel-basis projector family {|e_r><e_r|}, which
      is rank-3 in vec-space and sums to the identity
      (OPEN_with_shared_norm_coupling);
    * the noncanonical channel-projector family {Q |e_r><e_r| Q}
      from verification/family_c_kernels.py, whose sum equals Q
      (i.e. NOT proportional to I), giving OPEN.

The fourth case is important: Q e_j e_j^T Q summed over j is Q (not
cI), because sum_j e_j e_j^T = I forces sum_j Q e_j e_j^T Q = Q I Q
= Q. Since Q is rank 2 rather than scalar multiple of I, this family
does NOT trigger the shared-norm branch and is classified as OPEN.
The module-level check records this numerically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from verification.family_c_kernels import (
    KernelFamily,
    noncanonical_channel_projector_family,
)
from verification.operator_algebra import I3, P0, Q, TOL


# ----------------------------------------------------------------------
# Classification constants (typing.Literal for static checking)
# ----------------------------------------------------------------------


BLOCKED: Literal["BLOCKED"] = "BLOCKED"
OPEN_SHARED_NORM: Literal["OPEN_with_shared_norm_coupling"] = (
    "OPEN_with_shared_norm_coupling"
)
OPEN: Literal["OPEN"] = "OPEN"

Classification = Literal[
    "BLOCKED", "OPEN_with_shared_norm_coupling", "OPEN"
]


# ----------------------------------------------------------------------
# Vectorization helper
# ----------------------------------------------------------------------


def sym_to_vec6(K: np.ndarray) -> np.ndarray:
    """Return the 6-vector form of a 3x3 symmetric matrix.

    The ordering is the upper-triangular entries row by row:

        [K[0,0], K[0,1], K[0,2], K[1,1], K[1,2], K[2,2]]

    This is a faithful linear injection of Sym(3) into R^6, so
    linear (in)dependence among symmetric kernels is exactly linear
    (in)dependence among the 6-vectors.

    Parameters
    ----------
    K : np.ndarray
        A 3x3 real matrix. Symmetry is not enforced here; callers
        should pass symmetric matrices (Family C scope). The function
        reads only the upper triangle, so asymmetric inputs are
        silently projected to their upper-triangular part.

    Returns
    -------
    np.ndarray
        A real 1D array of length 6.
    """
    arr = np.asarray(K, dtype=float)
    if arr.shape != (3, 3):
        raise ValueError(
            f"sym_to_vec6 expects a 3x3 matrix, got shape {arr.shape}"
        )
    return np.array(
        [arr[0, 0], arr[0, 1], arr[0, 2], arr[1, 1], arr[1, 2], arr[2, 2]],
        dtype=float,
    )


# ----------------------------------------------------------------------
# Linear dependence finder (SVD-based)
# ----------------------------------------------------------------------


def find_affine_relation(
    kernels: list[np.ndarray], tol: float = TOL
) -> tuple[np.ndarray | None, float]:
    """Search for a nontrivial linear relation among three symmetric kernels.

    Stacks the three kernels as the columns of a 6x3 matrix V (one
    column per kernel, via sym_to_vec6), takes the SVD, and tests
    whether the smallest singular value is small relative to the
    largest. If it is, extracts the corresponding right singular
    vector as a nontrivial coefficient triple (a_0, a_1, a_2)
    satisfying sum_r a_r K_r ~= 0.

    The decision uses the relative criterion

        sigma_min <= tol * sigma_max

    so that uniform rescaling of the kernels does not flip the
    classification. When sigma_max is itself below tol (all three
    kernels are ~zero), we fall back to the absolute test
    sigma_min <= tol and return an arbitrary nonzero coefficient
    vector (the "relation" 1 * 0 + 0 * 0 + 0 * 0 = 0 is trivially
    satisfied, but we still report linear dependence so the BLOCKED
    branch fires).

    Parameters
    ----------
    kernels : list[np.ndarray]
        Exactly three 3x3 real symmetric matrices.
    tol : float, optional
        Relative tolerance for the smallest singular value.
        Defaults to the module TOL = 1e-12 from operator_algebra.

    Returns
    -------
    coeffs : np.ndarray | None
        A real 1D array of length 3 giving nontrivial coefficients
        (a_0, a_1, a_2) with sum_r a_r K_r ~= 0 when a linear
        dependence is detected, or None when the three kernels are
        linearly independent (rank of V equals 3 at the given
        tolerance). The returned coefficient vector is unit norm.
    min_singular_value : float
        The smallest singular value of the 6x3 stacked matrix V.
        Returned regardless of the branch so callers can inspect
        the numerical margin.
    """
    if len(kernels) != 3:
        raise ValueError(
            f"find_affine_relation expects exactly 3 kernels, got {len(kernels)}"
        )

    V = np.column_stack([sym_to_vec6(K) for K in kernels])  # shape (6, 3)

    # SVD: V = U @ diag(s) @ Vt, with s in descending order.
    _U, s, Vt = np.linalg.svd(V, full_matrices=False)
    sigma_max = float(s[0])
    sigma_min = float(s[-1])

    # Relative rank-deficiency test, with an absolute fallback when
    # the kernels are essentially zero.
    if sigma_max > tol:
        is_rank_deficient = sigma_min <= tol * sigma_max
    else:
        is_rank_deficient = sigma_min <= tol

    if not is_rank_deficient:
        return None, sigma_min

    # Rank < 3: extract coefficients from the right singular vector
    # associated with the smallest singular value. Vt has shape (3, 3)
    # and its last row is the right singular vector for s[-1].
    coeffs = np.asarray(Vt[-1], dtype=float)
    norm = float(np.linalg.norm(coeffs))
    if norm > 0.0:
        coeffs = coeffs / norm
    return coeffs, sigma_min


# ----------------------------------------------------------------------
# Main classifier
# ----------------------------------------------------------------------


def classify_support_constraint(
    family: KernelFamily, tol: float = TOL
) -> Classification:
    """Classify a KernelFamily by its support-level constraint structure.

    Implements Algorithm 1 of the Family C note:

        * if {K_0, K_1, K_2} are linearly dependent as symmetric
          matrices (equivalently, the 6x3 vectorized matrix has
          rank < 3 at tolerance `tol`): return BLOCKED;
        * else if K_0 + K_1 + K_2 = c * I to tolerance `tol`:
          return OPEN_with_shared_norm_coupling;
        * else: return OPEN.

    The three branches correspond precisely to the three cases of
    Requirement 3 of .kiro/specs/god-eq-path-b-family-c/requirements.md.

    Parameters
    ----------
    family : KernelFamily
        A Family C kernel triple. `family.kernels` must be a list
        of exactly three 3x3 real symmetric matrices.
    tol : float, optional
        Absolute / relative tolerance for the rank and identity
        checks. Defaults to the module TOL = 1e-12.

    Returns
    -------
    Classification
        One of BLOCKED, OPEN_with_shared_norm_coupling, OPEN.
    """
    coeffs, _sigma_min = find_affine_relation(family.kernels, tol=tol)
    if coeffs is not None:
        return BLOCKED

    # Linearly independent kernels: check for shared-norm coupling.
    S = sum(family.kernels)  # type: ignore[arg-type]
    c = float(np.trace(S)) / 3.0
    if np.allclose(S, c * I3, atol=tol):
        return OPEN_SHARED_NORM

    return OPEN


# ----------------------------------------------------------------------
# Reference kernel constructions for the module-level self-check
# ----------------------------------------------------------------------


def _trivially_collapsed_family() -> KernelFamily:
    """Return the trivially collapsed reference family K_0 = K_1 = K_2 = P_0.

    P_0 is the canonical symmetric-mode projector from operator_algebra.
    With all three kernels identical, the 6x3 vectorized matrix has
    rank 1 and any nontrivial (a_0, a_1, a_2) with sum = 0 gives a
    linear dependence, so classify_support_constraint must return
    BLOCKED. This is the trivial no-go signature predicted by
    Theorem 1 of the Family C note on canonical C_3-covariant triples.
    """
    return KernelFamily(
        name="trivially collapsed K_0 = K_1 = K_2 = P_0",
        kernels=[P0.copy(), P0.copy(), P0.copy()],
        is_canonical=True,
        added_hypotheses=[],
    )


def _edge_flux_family() -> KernelFamily:
    """Return the symmetric edge-flux kernels from the edge-flux no-go note.

    Taken verbatim from Section 1 of
    derivations/god_eq_path_b_edge_flux_current_no_go_2026-04-01.md:

        K_0 = [[ 3/8,    0,   3/16], [   0, -3/8, -3/16], [ 3/16, -3/16,    0]]
        K_1 = [[   0,  3/16, -3/16], [3/16,  3/8,     0], [-3/16,    0, -3/8]]
        K_2 = [[-3/8, -3/16,    0], [-3/16,   0,  3/16], [    0,  3/16,  3/8]]

    These are the SYMMETRIC kernels representing the antisymmetric
    edge-flux currents J^(r) = chi^T K_r chi (symmetrized to extract
    the quadratic form; the underlying observable is antisymmetric
    in time, not in channel indices). They satisfy K_0 + K_1 + K_2 = 0
    exactly, which is a rank-deficient linear dependence in the 6x3
    vectorized sense. classify_support_constraint must return BLOCKED.

    This family requires an added hypothesis in the Family C sense
    because it derives from a time-indexed current rather than from
    canonical channel-only operator data; it is marked noncanonical.
    """
    K0 = np.array(
        [[ 3.0 / 8.0,  0.0,        3.0 / 16.0],
         [ 0.0,       -3.0 / 8.0, -3.0 / 16.0],
         [ 3.0 / 16.0, -3.0 / 16.0, 0.0       ]],
        dtype=float,
    )
    K1 = np.array(
        [[ 0.0,        3.0 / 16.0, -3.0 / 16.0],
         [ 3.0 / 16.0, 3.0 / 8.0,   0.0       ],
         [-3.0 / 16.0, 0.0,        -3.0 / 8.0 ]],
        dtype=float,
    )
    K2 = np.array(
        [[-3.0 / 8.0, -3.0 / 16.0,  0.0       ],
         [-3.0 / 16.0, 0.0,         3.0 / 16.0],
         [ 0.0,        3.0 / 16.0,  3.0 / 8.0 ]],
        dtype=float,
    )
    return KernelFamily(
        name="symmetric edge-flux kernels (Family B3)",
        kernels=[K0, K1, K2],
        is_canonical=False,
        added_hypotheses=[
            "H_time: observable uses time-indexed channel amplitudes, "
            "not canonical channel-only operator data",
        ],
    )


def _standard_basis_projector_family() -> KernelFamily:
    """Return the scaled channel projector family K_r = |e_r><e_r|.

    The three standard-basis rank-1 projectors e_r e_r^T are
    linearly independent (rank 3 in vec-space), real symmetric, and
    satisfy sum_r e_r e_r^T = I exactly. Under a Gaussian probe
    chi(0) ~ N(0, Sigma) this gives

        sum_r X^(r) = chi(0)^T I chi(0) = ||chi(0)||^2,

    which is not deterministic. classify_support_constraint must
    therefore return OPEN_with_shared_norm_coupling, NOT BLOCKED.
    This is the genuine shared-norm coupling case and is the exact
    counterexample to the old "K_0 + K_1 + K_2 = cI => no-go"
    misclassification that the Family C design flags as incorrect.

    This is a noncanonical family (a basis choice is required) even
    though the basis in question is the standard channel basis.
    """
    kernels: list[np.ndarray] = []
    for r in range(3):
        e_r = np.zeros(3)
        e_r[r] = 1.0
        kernels.append(np.outer(e_r, e_r))
    return KernelFamily(
        name="standard channel projectors |e_r><e_r|",
        kernels=kernels,
        is_canonical=False,
        added_hypotheses=[
            "H_basis: standard channel basis selected",
        ],
    )


# ----------------------------------------------------------------------
# Module-level self-check (executes at import time)
# ----------------------------------------------------------------------


# Case 1: trivially collapsed canonical family --> BLOCKED.
_collapsed = _trivially_collapsed_family()
_coeffs_collapsed, _sigma_collapsed = find_affine_relation(
    _collapsed.kernels, tol=TOL
)
assert _coeffs_collapsed is not None, (
    "Trivially collapsed family K_0 = K_1 = K_2 = P_0 was reported as "
    "rank-3; expected a linear dependence among identical columns."
)
assert classify_support_constraint(_collapsed, tol=TOL) == BLOCKED, (
    "Trivially collapsed family was not classified as BLOCKED."
)
# Sanity: plugging the returned coefficients back should give ~0.
_residual_collapsed = sum(
    _coeffs_collapsed[i] * _collapsed.kernels[i] for i in range(3)
)
assert np.max(np.abs(_residual_collapsed)) <= 1e-10, (
    f"Residual sum_r a_r K_r for collapsed family has norm "
    f"{np.max(np.abs(_residual_collapsed))}, expected ~0"
)


# Case 2: symmetric edge-flux kernels --> BLOCKED (they sum to 0).
_edge_flux = _edge_flux_family()
# K_0 + K_1 + K_2 = 0 should be detected as a linear dependence with
# coefficients proportional to (1, 1, 1).
_edge_flux_sum = sum(_edge_flux.kernels)  # type: ignore[arg-type]
assert np.allclose(_edge_flux_sum, np.zeros((3, 3)), atol=1e-12), (
    f"Edge-flux kernels do not sum to zero; got max |sum| = "
    f"{np.max(np.abs(_edge_flux_sum))}. This contradicts Section 2 of "
    "god_eq_path_b_edge_flux_current_no_go_2026-04-01.md"
)
_coeffs_edge, _sigma_edge = find_affine_relation(_edge_flux.kernels, tol=TOL)
assert _coeffs_edge is not None, (
    "Edge-flux kernels were reported as linearly independent; "
    "they must be detected as rank-deficient since K_0 + K_1 + K_2 = 0."
)
assert classify_support_constraint(_edge_flux, tol=TOL) == BLOCKED, (
    "Edge-flux kernels were not classified as BLOCKED; this contradicts "
    "the exact no-go of god_eq_path_b_edge_flux_current_no_go_2026-04-01.md"
)
_residual_edge = sum(
    _coeffs_edge[i] * _edge_flux.kernels[i] for i in range(3)
)
assert np.max(np.abs(_residual_edge)) <= 1e-10, (
    f"Residual sum_r a_r K_r for edge-flux family has norm "
    f"{np.max(np.abs(_residual_edge))}, expected ~0"
)


# Case 3: standard basis projectors --> OPEN_with_shared_norm_coupling.
_basis_proj = _standard_basis_projector_family()
# Linearly independent and sum to I exactly.
_basis_sum = sum(_basis_proj.kernels)  # type: ignore[arg-type]
assert np.allclose(_basis_sum, I3, atol=TOL), (
    f"Standard channel projectors do not sum to I; got max|sum - I| = "
    f"{np.max(np.abs(_basis_sum - I3))}"
)
_coeffs_basis, _sigma_basis = find_affine_relation(
    _basis_proj.kernels, tol=TOL
)
assert _coeffs_basis is None, (
    "Standard channel projectors were reported as linearly dependent; "
    "e_r e_r^T for r=0,1,2 are a basis of the diagonal part of Sym(3)."
)
assert classify_support_constraint(_basis_proj, tol=TOL) == OPEN_SHARED_NORM, (
    "Standard channel projectors were not classified as "
    "OPEN_with_shared_norm_coupling; they sum to I and are linearly "
    "independent, so they must hit the shared-norm branch."
)


# Case 4: noncanonical Q e_r e_r^T Q family --> OPEN.
#
# Derivation of the expected classification:
#   sum_r Q e_r e_r^T Q = Q (sum_r e_r e_r^T) Q = Q I Q = Q^2 = Q.
# Q is rank 2, not a scalar multiple of I, so this family does NOT
# satisfy the shared-norm condition K_0 + K_1 + K_2 = c I. The three
# kernels are still linearly independent in the vec6 sense (verified
# at import time in verification/family_c_kernels.py), so the family
# must be classified as OPEN (not BLOCKED and not OPEN_SHARED_NORM).
_noncanonical = noncanonical_channel_projector_family()
_coeffs_nc, _sigma_nc = find_affine_relation(_noncanonical.kernels, tol=TOL)
assert _coeffs_nc is None, (
    "Noncanonical Q e_r e_r^T Q family was reported as linearly "
    "dependent; the family_c_kernels import-time checks assert they "
    "are genuinely distinct, so the vec6 rank must be 3."
)
# Numerically confirm sum equals Q (not cI), as predicted above.
_nc_sum = sum(_noncanonical.kernels)  # type: ignore[arg-type]
from verification.operator_algebra import Q as _Q_ref
assert np.allclose(_nc_sum, _Q_ref, atol=1e-12), (
    f"Q e_r e_r^T Q family sum is {_nc_sum}, expected Q = {_Q_ref}"
)
_nc_classification = classify_support_constraint(_noncanonical, tol=TOL)
assert _nc_classification == OPEN, (
    f"Noncanonical Q e_r e_r^T Q family classified as "
    f"{_nc_classification}; expected OPEN because sum_r K_r = Q, which "
    "is rank 2 and not proportional to I, so the shared-norm branch "
    "does not apply."
)


# ----------------------------------------------------------------------
# Support-restriction analysis (Task 4.2, Requirement 3.4)
# ----------------------------------------------------------------------
#
# The unrestricted classifier above answers the "is there a matrix
# identity sum_r a_r K_r = 0?" question: if yes, BLOCKED holds on every
# full-support probe; if no but sum_r K_r = c * I, we only have the
# shared-norm coupling (OPEN_SHARED_NORM); otherwise OPEN. This is a
# support-INDEPENDENT statement.
#
# The concrete example from the Family C design that forces us to
# distinguish a second regime: the noncanonical channel-projector family
# K_r = Q e_r e_r^T Q. Sum over r gives Q (rank 2), so there is no
# matrix identity sum_r a_r K_r + b I = 0 with b scalar, and the base
# classifier correctly returns OPEN. But if the probe is ADDITIONALLY
# restricted to the fixed-norm sphere ||Q chi||^2 = 1 -- equivalently,
# chi^T Q chi = 1 -- then
#
#     X^(0) + X^(1) + X^(2) = chi^T (sum_r Q e_r e_r^T Q) chi
#                            = chi^T Q chi = 1      (deterministic).
#
# That deterministic affine relation is NOT a consequence of the kernel
# matrices alone; it appears only because an added support hypothesis
# (chi^T P chi = c for some real symmetric P, real scalar c) is imposed.
# We call this regime "restriction-dependent BLOCKED" and must label it
# as such, per Requirement 3.4: "Do not present a restriction-dependent
# blockage as support-independent."
#
# The algorithm generalizes: given a restriction chi^T P chi = c with P
# real symmetric 3x3, look for coefficients (a_0, a_1, a_2, b) with
# (a_0, a_1, a_2) != 0 such that
#
#     sum_r a_r K_r + b * P = 0      (matrix identity).
#
# Plugging in chi^T (...) chi gives
#
#     sum_r a_r X^(r) + b * (chi^T P chi) = 0
#     => sum_r a_r X^(r) = -b * c      on the restricted support.
#
# Which is exactly a deterministic affine relation among the observables.
# The test stacks [K_0, K_1, K_2, P] as the columns of a 6x4 matrix in
# vec6 and checks its rank:
#
#   * rank 4: no linear relation, no deterministic blockage under the
#     restriction -> OPEN_under_restriction;
#   * rank 3 with the null vector's first three components NOT all zero:
#     the relation genuinely involves the K_r, giving
#     restriction_dependent_BLOCKED;
#   * base classification already BLOCKED: the kernels alone already
#     satisfy sum_r a_r K_r = 0 as a matrix identity, so the restriction
#     is not needed; report "support_independent" (the base no-go is the
#     authoritative statement).


@dataclass(frozen=True)
class SupportRestriction:
    """An added support hypothesis of the form chi^T P chi = c.

    Used by `classify_with_support_restriction` to express a restriction
    such as "the probe is confined to the fixed-norm sphere
    ||Q chi||^2 = 1". A restriction is an EXTRA hypothesis on top of the
    full-support probe used by `classify_support_constraint`; any
    blockage that appears only because of the restriction must be
    labeled restriction-dependent rather than support-independent.

    Attributes
    ----------
    name : str
        Short human-readable label, e.g.
        "fixed-norm sphere ||Q chi||^2 = 1".
    P : np.ndarray
        A real symmetric 3x3 matrix defining the restriction
        chi^T P chi = c. Symmetry is enforced at construction time by
        `__post_init__`.
    c : float
        The fixed value of the quadratic form on the restricted
        support. Zero is allowed.
    description : str
        Longer human-readable explanation of why this restriction is
        an added hypothesis (e.g. "fixes the Q-sector norm; not a
        consequence of the Gaussian probe alone").
    """

    name: str
    P: np.ndarray
    c: float
    description: str

    def __post_init__(self) -> None:
        P_arr = np.asarray(self.P, dtype=float)
        if P_arr.shape != (3, 3):
            raise ValueError(
                f"SupportRestriction.P must be 3x3, got shape {P_arr.shape}"
            )
        if not np.allclose(P_arr, P_arr.T, atol=TOL):
            raise ValueError(
                "SupportRestriction.P must be symmetric "
                f"(max asymmetry = {np.max(np.abs(P_arr - P_arr.T))})"
            )
        # Freeze a symmetric float copy so callers can't mutate afterward.
        object.__setattr__(self, "P", 0.5 * (P_arr + P_arr.T))


RestrictedClassification = Literal[
    "support_independent",
    "restriction_dependent_BLOCKED",
    "OPEN_under_restriction",
]


def classify_with_support_restriction(
    family: KernelFamily,
    restriction: SupportRestriction | None = None,
    tol: float = TOL,
) -> dict:
    """Classify a KernelFamily, optionally under an added support restriction.

    See the module-level comment above for the algorithm. Briefly:

      * if no restriction is passed: report the base classification from
        `classify_support_constraint` and tag
        restricted_classification = "support_independent";
      * otherwise stack [K_0, K_1, K_2, P] as columns of a 6x4 vec6
        matrix V and test its rank:
          - rank 4 and base classification is NOT BLOCKED:
              OPEN_under_restriction (no new affine relation appears);
          - rank 3 with null vector whose first three entries are not
              all zero: restriction_dependent_BLOCKED (a deterministic
              affine relation among the observables appears on the
              restricted support that was not present on the full
              support);
          - base classification is already BLOCKED: support_independent
              (matrix identity sum_r a_r K_r = 0 already holds, so the
              restriction adds nothing; the base no-go is authoritative).

    Parameters
    ----------
    family : KernelFamily
        A Family C kernel triple.
    restriction : SupportRestriction | None, optional
        The added support hypothesis chi^T P chi = c. Pass None to get
        the support-independent classification only.
    tol : float, optional
        Relative/absolute tolerance for the rank test. Defaults to TOL.

    Returns
    -------
    dict
        Keys:

        * "base_classification": the Classification returned by
          `classify_support_constraint(family)` with no restriction.
        * "restriction_name": restriction.name, or None if no
          restriction was provided.
        * "restricted_classification": one of
          "support_independent",
          "restriction_dependent_BLOCKED",
          "OPEN_under_restriction".
        * "justification": a human-readable string explaining the
          determination. When the restricted classification is
          "restriction_dependent_BLOCKED", the justification explicitly
          names the restriction (Requirement 3.4).
    """
    base = classify_support_constraint(family, tol=tol)

    if restriction is None:
        return {
            "base_classification": base,
            "restriction_name": None,
            "restricted_classification": "support_independent",
            "justification": (
                "No support restriction was supplied; the classification "
                f"'{base}' is support-independent (it follows from the "
                "kernel algebra alone under a full-support probe)."
            ),
        }

    # A restriction was supplied. If the kernels already satisfy a
    # matrix identity sum_r a_r K_r = 0, the restriction adds nothing;
    # the base BLOCKED result is authoritative and support-independent.
    if base == BLOCKED:
        return {
            "base_classification": base,
            "restriction_name": restriction.name,
            "restricted_classification": "support_independent",
            "justification": (
                "Base classification is BLOCKED: the kernels satisfy a "
                "matrix identity sum_r a_r K_r = 0, so a deterministic "
                "affine relation among the observables holds on every "
                "full-support probe. The added restriction "
                f"'{restriction.name}' is not needed to produce the "
                "no-go; the base result is support-independent."
            ),
        }

    # Stack [K_0, K_1, K_2, P] as columns of a 6x4 vec6 matrix and test
    # its rank. A relation sum_r a_r K_r + b * P = 0 exists iff the
    # stacked matrix is rank-deficient (rank < 4).
    V = np.column_stack(
        [sym_to_vec6(family.kernels[r]) for r in range(3)]
        + [sym_to_vec6(restriction.P)]
    )  # shape (6, 4)

    _U, s, Vt = np.linalg.svd(V, full_matrices=False)
    sigma_max = float(s[0])
    sigma_min = float(s[-1])

    if sigma_max > tol:
        is_rank_deficient = sigma_min <= tol * sigma_max
    else:
        is_rank_deficient = sigma_min <= tol

    if not is_rank_deficient:
        # Full rank 4: no affine relation involving P either.
        return {
            "base_classification": base,
            "restriction_name": restriction.name,
            "restricted_classification": "OPEN_under_restriction",
            "justification": (
                "No matrix identity sum_r a_r K_r + b * P = 0 exists "
                f"(rank[K_0, K_1, K_2, P] = 4 at tolerance {tol:g}); "
                "imposing the restriction "
                f"'{restriction.name}' does not produce a deterministic "
                "affine relation among the observables."
            ),
        }

    # Rank 3 or lower: a relation exists. Extract the null vector.
    null_vec = np.asarray(Vt[-1], dtype=float)
    a = null_vec[:3]
    b = float(null_vec[3])

    if np.max(np.abs(a)) <= tol:
        # Null vector has zero K-components: the relation is b * P = 0,
        # which only tells us P = 0 (degenerate restriction). Treat as
        # no genuine K-relation under the restriction.
        return {
            "base_classification": base,
            "restriction_name": restriction.name,
            "restricted_classification": "OPEN_under_restriction",
            "justification": (
                "The only linear relation found involves P alone "
                "(a_0 = a_1 = a_2 = 0), meaning P is itself "
                "vec6-degenerate; no deterministic affine relation "
                "among the observables is produced by the restriction "
                f"'{restriction.name}'."
            ),
        }

    # Genuine restriction-dependent affine relation: sum_r a_r K_r = -b P,
    # so on the restricted support sum_r a_r X^(r) = -b * c.
    rhs = -b * float(restriction.c)
    coeffs_str = ", ".join(f"{ai:+.6g}" for ai in a)
    return {
        "base_classification": base,
        "restriction_name": restriction.name,
        "restricted_classification": "restriction_dependent_BLOCKED",
        "justification": (
            "A deterministic affine relation among the observables "
            "appears ONLY under the added hypothesis "
            f"'{restriction.name}': coefficients "
            f"(a_0, a_1, a_2) = ({coeffs_str}) and b = {b:+.6g} satisfy "
            "sum_r a_r K_r + b * P = 0, so on the restricted support "
            f"chi^T P chi = {restriction.c:g} the observables obey "
            f"sum_r a_r X^(r) = {rhs:+.6g}. This blockage is "
            "RESTRICTION-DEPENDENT; it is not a matrix identity of the "
            "kernels alone and must not be presented as "
            "support-independent."
        ),
    }


# ----------------------------------------------------------------------
# Module-level self-checks for support-restriction analysis
# ----------------------------------------------------------------------


# Self-check A: noncanonical Q e_r e_r^T Q family with no restriction.
# Expected: base_classification = OPEN, restricted_classification =
# support_independent, justification mentions support-independent.
_nc_no_restriction = classify_with_support_restriction(
    _noncanonical, restriction=None, tol=TOL
)
assert _nc_no_restriction["base_classification"] == OPEN, (
    "Self-check A failed: base_classification for the Q e_r e_r^T Q "
    f"family with no restriction is {_nc_no_restriction['base_classification']}, "
    "expected OPEN."
)
assert _nc_no_restriction["restriction_name"] is None, (
    "Self-check A failed: restriction_name should be None."
)
assert (
    _nc_no_restriction["restricted_classification"] == "support_independent"
), (
    "Self-check A failed: with no restriction, restricted_classification "
    "must be 'support_independent'."
)


# Self-check B: noncanonical Q e_r e_r^T Q family with the fixed-norm
# sphere restriction P = Q, c = 1. Because sum_r K_r = Q = 1 * P, we
# have sum_r K_r - 1 * P = 0, giving the relation (a_0, a_1, a_2, b)
# = (1, 1, 1, -1) (up to sign/scale). Expected:
#   base_classification = OPEN,
#   restricted_classification = restriction_dependent_BLOCKED,
#   justification mentions the fixed-norm restriction by name.
_fixed_norm_Q_sphere = SupportRestriction(
    name="fixed-norm sphere ||Q chi||^2 = 1",
    P=Q.copy(),
    c=1.0,
    description=(
        "Added hypothesis: the probe is confined to the unit sphere of "
        "the Q-sector norm, chi^T Q chi = 1. This is NOT a consequence "
        "of the full-support Gaussian probe; it must be imposed "
        "separately. Under this restriction the observables of the "
        "Q e_r e_r^T Q family satisfy X^(0) + X^(1) + X^(2) = 1 "
        "deterministically."
    ),
)
_nc_Q_restricted = classify_with_support_restriction(
    _noncanonical, restriction=_fixed_norm_Q_sphere, tol=TOL
)
assert _nc_Q_restricted["base_classification"] == OPEN, (
    "Self-check B failed: base_classification under restriction should "
    f"still be OPEN, got {_nc_Q_restricted['base_classification']}."
)
assert _nc_Q_restricted["restriction_name"] == _fixed_norm_Q_sphere.name, (
    "Self-check B failed: restriction_name mismatch."
)
assert (
    _nc_Q_restricted["restricted_classification"]
    == "restriction_dependent_BLOCKED"
), (
    "Self-check B failed: Q e_r e_r^T Q under ||Q chi||^2 = 1 must be "
    "classified as 'restriction_dependent_BLOCKED'; got "
    f"{_nc_Q_restricted['restricted_classification']}."
)
# The justification MUST name the fixed-norm restriction so a reader
# cannot mistake this for a support-independent no-go (Requirement 3.4).
assert (
    "fixed-norm" in _nc_Q_restricted["justification"]
    or _fixed_norm_Q_sphere.name in _nc_Q_restricted["justification"]
), (
    "Self-check B failed: justification must name the fixed-norm "
    f"restriction; got: {_nc_Q_restricted['justification']}"
)
assert (
    "RESTRICTION-DEPENDENT" in _nc_Q_restricted["justification"]
    or "restriction-dependent" in _nc_Q_restricted["justification"].lower()
), (
    "Self-check B failed: justification must explicitly label the "
    "blockage as restriction-dependent."
)


# Self-check C: standard channel projector family |e_r><e_r| with no
# restriction. Expected base_classification = OPEN_SHARED_NORM (sum to I,
# linearly independent); restricted_classification = support_independent.
_basis_no_restriction = classify_with_support_restriction(
    _basis_proj, restriction=None, tol=TOL
)
assert _basis_no_restriction["base_classification"] == OPEN_SHARED_NORM, (
    "Self-check C failed: standard channel projector base classification "
    f"is {_basis_no_restriction['base_classification']}, expected "
    "OPEN_with_shared_norm_coupling."
)
assert (
    _basis_no_restriction["restricted_classification"]
    == "support_independent"
), (
    "Self-check C failed: with no restriction, restricted_classification "
    "must be 'support_independent'."
)


# Self-check D: a BLOCKED family (edge-flux) with some restriction.
# Because the kernels already satisfy sum_r K_r = 0 as a matrix identity,
# the restriction is not needed; expected restricted_classification =
# support_independent with a justification that explains this.
_edge_with_restriction = classify_with_support_restriction(
    _edge_flux, restriction=_fixed_norm_Q_sphere, tol=TOL
)
assert _edge_with_restriction["base_classification"] == BLOCKED, (
    "Self-check D failed: edge-flux base classification is not BLOCKED."
)
assert (
    _edge_with_restriction["restricted_classification"]
    == "support_independent"
), (
    "Self-check D failed: an already-BLOCKED family should be reported "
    "as support_independent regardless of any restriction, got "
    f"{_edge_with_restriction['restricted_classification']}."
)


__all__ = [
    "BLOCKED",
    "OPEN_SHARED_NORM",
    "OPEN",
    "Classification",
    "sym_to_vec6",
    "find_affine_relation",
    "classify_support_constraint",
    "SupportRestriction",
    "classify_with_support_restriction",
]


# ----------------------------------------------------------------------
# CLI summary
# ----------------------------------------------------------------------


if __name__ == "__main__":
    print("verification.support_constraint")
    print("-" * 60)

    cases: list[tuple[str, KernelFamily, str]] = [
        (
            "trivially collapsed K_0 = K_1 = K_2 = P_0",
            _trivially_collapsed_family(),
            BLOCKED,
        ),
        (
            "symmetric edge-flux kernels (Family B3)",
            _edge_flux_family(),
            BLOCKED,
        ),
        (
            "standard channel projectors |e_r><e_r|",
            _standard_basis_projector_family(),
            OPEN_SHARED_NORM,
        ),
        (
            "noncanonical Q e_r e_r^T Q family",
            noncanonical_channel_projector_family(),
            OPEN,
        ),
    ]

    for label, kf, expected in cases:
        coeffs, sigma_min = find_affine_relation(kf.kernels, tol=TOL)
        classification = classify_support_constraint(kf, tol=TOL)
        status = "ok" if classification == expected else "MISMATCH"
        print(
            f"  {label:48s}  classification={classification:40s}  "
            f"sigma_min={sigma_min:.3e}  [{status}]"
        )
        if coeffs is not None:
            print(f"    dependence coefficients (a_0, a_1, a_2) = {coeffs}")

    # Explicit numerical summary for the Q e_r e_r^T Q sum.
    nc = noncanonical_channel_projector_family()
    nc_sum = sum(nc.kernels)
    print()
    print("Sum of Q e_r e_r^T Q over r = 0,1,2:")
    print(nc_sum)
    print(
        "Note: this equals Q (rank 2), NOT a scalar multiple of I, so the "
        "shared-norm branch does not fire."
    )

    # ------------------------------------------------------------------
    # Support-restriction analysis CLI summary (Task 4.2)
    # ------------------------------------------------------------------
    print()
    print("Support-restriction analysis")
    print("-" * 60)

    # Restriction of interest: fixed-norm sphere ||Q chi||^2 = 1.
    fixed_norm_sphere = SupportRestriction(
        name="fixed-norm sphere ||Q chi||^2 = 1",
        P=Q.copy(),
        c=1.0,
        description=(
            "Added hypothesis: chi^T Q chi = 1. Not a consequence of "
            "the full-support Gaussian probe."
        ),
    )

    restricted_cases: list[tuple[str, KernelFamily, SupportRestriction | None]] = [
        (
            "Q e_r e_r^T Q, no restriction",
            noncanonical_channel_projector_family(),
            None,
        ),
        (
            "Q e_r e_r^T Q, ||Q chi||^2 = 1",
            noncanonical_channel_projector_family(),
            fixed_norm_sphere,
        ),
        (
            "standard |e_r><e_r|, no restriction",
            _standard_basis_projector_family(),
            None,
        ),
        (
            "edge-flux kernels, ||Q chi||^2 = 1",
            _edge_flux_family(),
            fixed_norm_sphere,
        ),
    ]

    for label, kf, restr in restricted_cases:
        result = classify_with_support_restriction(kf, restriction=restr, tol=TOL)
        print(f"  {label}")
        print(f"    base_classification      = {result['base_classification']}")
        print(f"    restriction_name         = {result['restriction_name']}")
        print(
            f"    restricted_classification = "
            f"{result['restricted_classification']}"
        )
        print(f"    justification            : {result['justification']}")
        print()

    print()
    print("all support_constraint checks passed")
