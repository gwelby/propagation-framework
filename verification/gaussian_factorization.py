"""
Exact Gaussian factorization test for Family C quadratic forms.

Role
----
This module implements Algorithm 2 (GaussianFactorizationTest) of
derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md
and Section "Algorithm 2" of .kiro/specs/god-eq-path-b-family-c/design.md.

Given a real symmetric 3x3 kernel triple {K_0, K_1, K_2} defining quadratic
observables

    X^(r) = chi(0)^T K_r chi(0),

and an explicit probe ensemble

    chi(0) ~ N(0, Sigma),     Sigma a C_3-circulant positive definite 3x3 matrix,

the test decides whether the probe-level factorization hypothesis

    P_theta(X^(0), X^(1), X^(2)) = prod_r p_r(X^(r))

survives two exact checks:

    1. Necessary condition (covariance / Isserlis).
       For centered real Gaussians and real symmetric A, B,

           Cov( chi^T A chi, chi^T B chi ) = 2 * Tr( Sigma A Sigma B )

       (Isserlis/Wick theorem; see Requirement 4.3 and the factor-of-2
       correction from the Family A audit). Independence implies zero
       covariance for every pair r != s, so

           C_rs := 2 * Tr( Sigma K_r Sigma K_s ) = 0    for all r != s

       is a necessary condition. If any C_rs != 0 the triple already
       FAILS the Gaussian probe and no further test is needed.

    2. Exact sufficient criterion on whitened kernels.
       Zero covariance is necessary but NOT sufficient for independence
       of Gaussian quadratic forms. The exact criterion (design.md
       Algorithm 2, Requirement 4.4) acts on the whitened kernels

           B_r := Sigma^{1/2} K_r Sigma^{1/2}

       and demands B_r @ B_s = 0 as a matrix identity for every pair
       r != s. This is the STANDARD independence criterion for Gaussian
       quadratic forms (it implies the whitened kernels project onto
       orthogonal invariant subspaces); simultaneous diagonalizability
       of K_0, K_1, K_2 alone is NOT sufficient and MUST NOT be used,
       per Requirement 4.4.

       Here Sigma^{1/2} is the unique real symmetric positive-definite
       square root of Sigma, computed from the eigendecomposition
       Sigma = V diag(lambda) V^T by Sigma^{1/2} = V diag(sqrt(lambda)) V^T.

Return contract
---------------
`gaussian_factorization_test(kernels, sigma)` returns a
`GaussianFactorizationResult` (dataclass) with fields:

    * status:             "FAILS_GAUSSIAN_PROBE"
                          or "PASSES_EXACT_GAUSSIAN_TEST".
    * failing_stage:      "covariance", "whitened_product", or None
                          (None iff the triple passed both stages).
    * failing_pair:       a tuple (r, s) with r < s naming the first pair
                          that violated the current stage, or None on pass.
    * failing_magnitude:  the diagnostic scalar that triggered the failure:
                          |C_rs| for the covariance stage, or the Frobenius
                          norm ||B_r B_s||_F for the whitened-product stage.
                          0.0 on pass.
    * cross_covariance:   the full 3x3 matrix of C_rs = 2 Tr(Sigma K_r Sigma K_s)
                          values, always populated (useful for diagnostics).
    * whitened_products:  dict {(r, s): ||B_r B_s||_F} for r < s, populated
                          iff the covariance stage passed and the whitened
                          stage ran; otherwise an empty dict.

Requirements validated
----------------------
This module validates the Family C requirements (see
.kiro/specs/god-eq-path-b-family-c/requirements.md):

    * R4.1: explicit Gaussian probe ensemble chi(0) ~ N(0, Sigma), distinct
      from any claimed physical one-medium law.
    * R4.2: uses Isserlis/Wick for joint law of quadratic forms.
    * R4.3: computes C_rs = 2 Tr(Sigma K_r Sigma K_s) for all pairs r != s.
    * R4.4: when C_rs = 0 for all r != s, applies the exact whitened-kernel
      independence criterion B_r B_s = 0 BEFORE claiming probe-level
      independence; does NOT rely on simultaneous diagonalizability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from verification.operator_algebra import (
    I3,
    TOL,
    is_c3_circulant_symmetric,
)


# ----------------------------------------------------------------------
# Status constants
# ----------------------------------------------------------------------

FAILS_GAUSSIAN_PROBE: Literal["FAILS_GAUSSIAN_PROBE"] = "FAILS_GAUSSIAN_PROBE"
PASSES_EXACT_GAUSSIAN_TEST: Literal["PASSES_EXACT_GAUSSIAN_TEST"] = (
    "PASSES_EXACT_GAUSSIAN_TEST"
)

GaussianFactorizationStatus = Literal[
    "FAILS_GAUSSIAN_PROBE", "PASSES_EXACT_GAUSSIAN_TEST"
]

FailingStage = Literal["covariance", "whitened_product"]


# ----------------------------------------------------------------------
# Result dataclass
# ----------------------------------------------------------------------


@dataclass
class GaussianFactorizationResult:
    """Outcome of `gaussian_factorization_test`.

    Attributes
    ----------
    status : {"FAILS_GAUSSIAN_PROBE", "PASSES_EXACT_GAUSSIAN_TEST"}
        Final verdict.
    failing_stage : {"covariance", "whitened_product"} | None
        Stage at which the test failed. None iff status is
        PASSES_EXACT_GAUSSIAN_TEST.
    failing_pair : tuple[int, int] | None
        First (r, s) with r < s that violated the failing stage.
        None iff status is PASSES_EXACT_GAUSSIAN_TEST.
    failing_magnitude : float
        Diagnostic scalar associated with `failing_pair`: |C_rs| for the
        covariance stage, ||B_r B_s||_F for the whitened stage. 0.0 on pass.
    cross_covariance : np.ndarray
        Full 3x3 symmetric matrix with entries C_rs = 2 Tr(Sigma K_r Sigma K_s).
        Diagonal entries C_rr = 2 Tr(Sigma K_r Sigma K_r) = 2 ||Sigma^{1/2}
        K_r Sigma^{1/2}||_F^2 are populated for diagnostics but not used by
        the decision logic.
    whitened_products : dict[tuple[int, int], float]
        Dictionary keyed by (r, s) with r < s, mapping each pair to
        ||B_r B_s||_F. Populated iff the whitened stage actually ran
        (i.e. the covariance stage passed). Empty otherwise.
    """

    status: GaussianFactorizationStatus
    failing_stage: FailingStage | None
    failing_pair: tuple[int, int] | None
    failing_magnitude: float
    cross_covariance: np.ndarray
    whitened_products: dict[tuple[int, int], float] = field(
        default_factory=dict
    )


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _validate_sigma(Sigma: np.ndarray, tol: float = TOL) -> np.ndarray:
    """Return a symmetrized float copy of Sigma, checking PD-ness.

    Enforces:
      * shape (3, 3);
      * real (imaginary part below tol);
      * symmetric (after explicit 0.5 * (S + S^T) symmetrization);
      * positive definite (all eigenvalues > tol).

    Raises ValueError on failure. Does NOT enforce C_3-circulance here
    (the algorithm itself does not require circulance; R4.1 only says
    the canonical probe is C_3-circulant, which is a separate modeling
    choice). Callers that want to enforce circulance can check via
    `operator_algebra.is_c3_circulant_symmetric` on the returned array.
    """
    arr = np.asarray(Sigma)
    if arr.shape != (3, 3):
        raise ValueError(
            f"Sigma must be a 3x3 matrix, got shape {arr.shape}"
        )
    if np.iscomplexobj(arr) and np.max(np.abs(np.imag(arr))) > tol:
        raise ValueError(
            f"Sigma has non-negligible imaginary part "
            f"(max |Im| = {np.max(np.abs(np.imag(arr)))})"
        )
    arr = np.real(arr).astype(float)
    if not np.allclose(arr, arr.T, atol=tol):
        raise ValueError(
            "Sigma is not symmetric "
            f"(max asymmetry = {np.max(np.abs(arr - arr.T))})"
        )
    arr = 0.5 * (arr + arr.T)
    eigs = np.linalg.eigvalsh(arr)
    if np.min(eigs) <= tol:
        raise ValueError(
            f"Sigma is not positive definite (min eigenvalue = {eigs.min()})"
        )
    return arr


def _validate_kernels(
    kernels: list[np.ndarray], tol: float = TOL
) -> list[np.ndarray]:
    """Return symmetrized float copies of the three kernels.

    Enforces exactly three entries, each a real 3x3 matrix symmetric
    to tolerance `tol`. Explicitly symmetrizes the returned copies to
    remove machine-precision asymmetry.
    """
    if len(kernels) != 3:
        raise ValueError(
            f"Expected exactly 3 kernels, got {len(kernels)}"
        )
    out: list[np.ndarray] = []
    for r, K in enumerate(kernels):
        arr = np.asarray(K)
        if arr.shape != (3, 3):
            raise ValueError(
                f"K_{r} must be 3x3, got shape {arr.shape}"
            )
        if np.iscomplexobj(arr) and np.max(np.abs(np.imag(arr))) > tol:
            raise ValueError(
                f"K_{r} has non-negligible imaginary part "
                f"(max |Im| = {np.max(np.abs(np.imag(arr)))})"
            )
        arr = np.real(arr).astype(float)
        if not np.allclose(arr, arr.T, atol=tol):
            raise ValueError(
                f"K_{r} is not symmetric "
                f"(max asymmetry = {np.max(np.abs(arr - arr.T))})"
            )
        out.append(0.5 * (arr + arr.T))
    return out


def symmetric_sqrt(Sigma: np.ndarray, tol: float = TOL) -> np.ndarray:
    """Return the unique real symmetric positive-definite square root of Sigma.

    Computed from the eigendecomposition Sigma = V diag(lambda) V^T as
    Sigma^{1/2} = V diag(sqrt(lambda)) V^T. Requires Sigma to be real
    symmetric positive definite; callers should pass the output of
    `_validate_sigma` or an equivalently validated matrix.

    Parameters
    ----------
    Sigma : np.ndarray
        Real symmetric positive-definite 3x3 matrix.
    tol : float, optional
        Tolerance used both to lower-bound eigenvalues (guards against
        near-singular inputs) and for the post-hoc identity check
        S^{1/2} @ S^{1/2} == Sigma. Defaults to the module TOL.

    Returns
    -------
    np.ndarray
        A real symmetric positive-definite 3x3 matrix S with S @ S = Sigma.
    """
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    if np.min(eigvals) <= tol:
        raise ValueError(
            f"symmetric_sqrt: Sigma is not strictly positive definite "
            f"(min eigenvalue = {eigvals.min()})"
        )
    root = (eigvecs * np.sqrt(eigvals)) @ eigvecs.T
    # Force exact symmetry against machine-precision noise.
    root = 0.5 * (root + root.T)
    # Sanity: root @ root should reproduce Sigma.
    if not np.allclose(root @ root, Sigma, atol=1e-10):
        raise RuntimeError(
            "symmetric_sqrt: internal consistency failure "
            f"(max |root^2 - Sigma| = {np.max(np.abs(root @ root - Sigma))})"
        )
    return root


def cross_covariance(
    K_r: np.ndarray, K_s: np.ndarray, Sigma: np.ndarray
) -> float:
    """Return C_rs = 2 * Tr(Sigma @ K_r @ Sigma @ K_s) (Isserlis/Wick).

    For chi ~ N(0, Sigma) with Sigma real symmetric PD and K_r, K_s real
    symmetric, this is exactly Cov(chi^T K_r chi, chi^T K_s chi) by the
    Isserlis theorem for centered real Gaussians. The factor of 2 is
    the one that was corrected in the Family A audit; preserving it
    here is the content of Requirement 4.3.

    The trace of a product is computed as the Frobenius inner product
    Tr(A B) = sum_{i,j} A_{ij} B_{ji} = np.einsum('ij,ji->', A, B), which
    avoids materializing the full A @ B product where unneeded.
    """
    A = Sigma @ K_r
    B = Sigma @ K_s
    # Tr(A B) = sum_{i,j} A_{ij} B_{ji}
    return 2.0 * float(np.einsum("ij,ji->", A, B))


def whiten_kernel(K: np.ndarray, sqrt_sigma: np.ndarray) -> np.ndarray:
    """Return B = Sigma^{1/2} @ K @ Sigma^{1/2}, symmetrized.

    Assumes `sqrt_sigma` is the real symmetric positive-definite square
    root returned by `symmetric_sqrt(Sigma)`. The output B is the
    whitened kernel used by the exact independence criterion.
    """
    B = sqrt_sigma @ K @ sqrt_sigma
    return 0.5 * (B + B.T)


# ----------------------------------------------------------------------
# Main algorithm
# ----------------------------------------------------------------------


def gaussian_factorization_test(
    kernels: list[np.ndarray],
    sigma: np.ndarray,
    tol: float = TOL,
) -> GaussianFactorizationResult:
    """Run the two-stage Gaussian factorization test on {K_0, K_1, K_2}.

    See the module docstring for the full mathematical statement.
    Briefly:

      1. Validate inputs (three real symmetric 3x3 kernels; sigma a
         real symmetric positive-definite 3x3 matrix).
      2. Compute C_rs = 2 Tr(Sigma K_r Sigma K_s) for every pair r != s.
         If |C_rs| > tol for any pair, return FAILS_GAUSSIAN_PROBE with
         failing_stage = "covariance".
      3. Otherwise compute Sigma^{1/2} and the whitened kernels
         B_r = Sigma^{1/2} K_r Sigma^{1/2}. Check B_r B_s = 0 (Frobenius
         norm) for every pair r != s. If ||B_r B_s||_F > tol for any
         pair, return FAILS_GAUSSIAN_PROBE with failing_stage =
         "whitened_product".
      4. Otherwise return PASSES_EXACT_GAUSSIAN_TEST.

    The tolerance is absolute; for inputs on drastically different
    scales, callers should rescale the kernels to unit Frobenius norm
    beforehand if they want scale-invariant behavior. The covariance
    matrix and whitened-product diagnostics are returned in full so
    callers can inspect the numerical margins.

    Parameters
    ----------
    kernels : list[np.ndarray]
        Exactly three 3x3 real symmetric matrices [K_0, K_1, K_2].
    sigma : np.ndarray
        A 3x3 real symmetric positive-definite matrix. C_3-circulance
        is the canonical modeling choice (Requirement 4.1) but is not
        enforced here; the algorithm is correct for any PD Sigma.
    tol : float, optional
        Absolute tolerance for both |C_rs| and ||B_r B_s||_F.
        Defaults to the module TOL = 1e-12.

    Returns
    -------
    GaussianFactorizationResult
        See dataclass docstring for field semantics.

    Requirements validated
    ----------------------
    Requirements 4.1, 4.2, 4.3, 4.4.
    """
    Ks = _validate_kernels(kernels, tol=tol)
    S = _validate_sigma(sigma, tol=tol)

    # Stage 1: full 3x3 cross-covariance matrix (Isserlis).
    C = np.zeros((3, 3), dtype=float)
    for r in range(3):
        for s in range(3):
            C[r, s] = cross_covariance(Ks[r], Ks[s], S)

    # Check off-diagonal entries in canonical (r, s) with r < s order.
    for r in range(3):
        for s in range(r + 1, 3):
            if abs(C[r, s]) > tol:
                return GaussianFactorizationResult(
                    status=FAILS_GAUSSIAN_PROBE,
                    failing_stage="covariance",
                    failing_pair=(r, s),
                    failing_magnitude=float(abs(C[r, s])),
                    cross_covariance=C,
                    whitened_products={},
                )

    # Stage 2: whitened-kernel product criterion.
    sqrt_S = symmetric_sqrt(S, tol=tol)
    Bs = [whiten_kernel(K, sqrt_S) for K in Ks]

    products: dict[tuple[int, int], float] = {}
    first_failure: tuple[int, int] | None = None
    first_magnitude: float = 0.0

    for r in range(3):
        for s in range(r + 1, 3):
            prod = Bs[r] @ Bs[s]
            mag = float(np.linalg.norm(prod, ord="fro"))
            products[(r, s)] = mag
            if mag > tol and first_failure is None:
                first_failure = (r, s)
                first_magnitude = mag

    if first_failure is not None:
        return GaussianFactorizationResult(
            status=FAILS_GAUSSIAN_PROBE,
            failing_stage="whitened_product",
            failing_pair=first_failure,
            failing_magnitude=first_magnitude,
            cross_covariance=C,
            whitened_products=products,
        )

    return GaussianFactorizationResult(
        status=PASSES_EXACT_GAUSSIAN_TEST,
        failing_stage=None,
        failing_pair=None,
        failing_magnitude=0.0,
        cross_covariance=C,
        whitened_products=products,
    )


__all__ = [
    "FAILS_GAUSSIAN_PROBE",
    "PASSES_EXACT_GAUSSIAN_TEST",
    "GaussianFactorizationResult",
    "cross_covariance",
    "whiten_kernel",
    "symmetric_sqrt",
    "gaussian_factorization_test",
]


# ----------------------------------------------------------------------
# Self-check / CLI
# ----------------------------------------------------------------------


if __name__ == "__main__":
    # The three cases below exercise every branch of the decision logic
    # of gaussian_factorization_test:
    #
    #   Case A  PASSES both stages (standard channel projectors, Sigma = I).
    #   Case B  FAILS the covariance stage (three identical nonzero kernels,
    #           which is the canonical Family C collapse signature of
    #           Theorem 1 in
    #           derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md).
    #   Case C  PASSES the covariance stage but FAILS the whitened-product
    #           stage -- this is the scenario Requirement 4.4 warns about,
    #           where zero Isserlis covariance is NOT sufficient for
    #           independence of Gaussian quadratic forms.

    print("verification.gaussian_factorization")
    print("-" * 60)

    Sigma_I = I3.copy()

    # --- Case A: standard channel projectors -----------------------------
    # K_r = e_r e_r^T, Sigma = I. Then B_r = K_r and B_r B_s = 0 for r != s
    # (different standard basis directions are orthogonal), and
    # Tr(K_r K_s) = (e_r^T e_s)^2 = 0 for r != s. Must PASS both stages.
    channel_projectors: list[np.ndarray] = []
    for r in range(3):
        e_r = np.zeros(3)
        e_r[r] = 1.0
        channel_projectors.append(np.outer(e_r, e_r))
    result_A = gaussian_factorization_test(channel_projectors, Sigma_I)
    print()
    print("Case A: standard channel projectors {e_r e_r^T} with Sigma = I")
    print(f"  status            = {result_A.status}")
    print(f"  failing_stage     = {result_A.failing_stage}")
    print(f"  cross_covariance diagonal = {np.diag(result_A.cross_covariance)}")
    print(
        "  cross_covariance off-diagonals = "
        f"{result_A.cross_covariance[~np.eye(3, dtype=bool)]}"
    )
    print(f"  whitened_products = {result_A.whitened_products}")
    assert result_A.status == PASSES_EXACT_GAUSSIAN_TEST, (
        "Case A (channel projectors, Sigma = I) should PASS both stages "
        f"but got status={result_A.status}, "
        f"stage={result_A.failing_stage}, pair={result_A.failing_pair}"
    )

    # --- Case B: three identical nonzero kernels ------------------------
    # Canonical Family C collapse signature (Theorem 1). With
    # K_0 = K_1 = K_2 = K and Sigma = I, every off-diagonal entry of the
    # covariance matrix is C_rs = 2 Tr(K^2) = 2 ||K||_F^2 > 0, so the
    # covariance stage must fail.
    K_common = np.array(
        [[1.0, 0.2, 0.3],
         [0.2, 0.5, 0.1],
         [0.3, 0.1, 0.8]],
        dtype=float,
    )
    result_B = gaussian_factorization_test(
        [K_common.copy(), K_common.copy(), K_common.copy()],
        Sigma_I,
    )
    print()
    print("Case B: three identical nonzero kernels with Sigma = I")
    print(f"  status            = {result_B.status}")
    print(f"  failing_stage     = {result_B.failing_stage}")
    print(f"  failing_pair      = {result_B.failing_pair}")
    print(f"  failing_magnitude = {result_B.failing_magnitude:.6g}")
    expected_C_off = 2.0 * float(np.einsum("ij,ij->", K_common, K_common))
    print(
        "  expected |C_rs| = 2 * ||K||_F^2 = "
        f"{expected_C_off:.6g}"
    )
    assert result_B.status == FAILS_GAUSSIAN_PROBE, (
        "Case B (identical kernels) should FAIL the test but got "
        f"status={result_B.status}"
    )
    assert result_B.failing_stage == "covariance", (
        "Case B should fail at the covariance stage but got "
        f"stage={result_B.failing_stage}"
    )
    assert np.isclose(result_B.failing_magnitude, expected_C_off, atol=1e-12), (
        "Case B failing_magnitude should equal 2 * ||K||_F^2 = "
        f"{expected_C_off}, got {result_B.failing_magnitude}"
    )

    # --- Case C: covariance passes, whitened-product fails ---------------
    # Construction: with Sigma = I, B_r = K_r so we need Tr(K_r K_s) = 0
    # for every r != s (stage 1 passes) AND K_r K_s != 0 for some r != s
    # (stage 2 must fail). Take
    #
    #   K_0 = diag(1, -1,  0)
    #   K_1 = diag(1,  1, -2)
    #   K_2 = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    #
    # Tr(K_0 K_1) = 1 - 1 - 0 = 0, Tr(K_0 K_2) = 0 (K_0 is diagonal and
    # K_2 is off-diagonal), Tr(K_1 K_2) = 0 (same reason). But
    # K_0 @ K_1 = diag(1, -1, 0) is nonzero, so Case C must fail at the
    # whitened-product stage.
    K0 = np.diag([1.0, -1.0, 0.0])
    K1 = np.diag([1.0, 1.0, -2.0])
    K2 = np.array(
        [[0.0, 1.0, 0.0],
         [1.0, 0.0, 0.0],
         [0.0, 0.0, 0.0]],
        dtype=float,
    )
    result_C = gaussian_factorization_test([K0, K1, K2], Sigma_I)
    print()
    print(
        "Case C: zero Isserlis covariance but nonzero whitened product "
        "(Sigma = I)"
    )
    print(f"  status                = {result_C.status}")
    print(f"  failing_stage         = {result_C.failing_stage}")
    print(f"  failing_pair          = {result_C.failing_pair}")
    print(f"  failing_magnitude     = {result_C.failing_magnitude:.6g}")
    print(
        "  cross_covariance off-diagonals = "
        f"{result_C.cross_covariance[~np.eye(3, dtype=bool)]}"
    )
    print(f"  whitened_products     = {result_C.whitened_products}")
    assert result_C.status == FAILS_GAUSSIAN_PROBE, (
        "Case C should FAIL the test but got "
        f"status={result_C.status}"
    )
    assert result_C.failing_stage == "whitened_product", (
        "Case C should fail at the whitened-product stage but got "
        f"stage={result_C.failing_stage}"
    )
    # Stage 1 diagnostics: all off-diagonal Isserlis covariances vanish.
    off_mask = ~np.eye(3, dtype=bool)
    assert np.max(np.abs(result_C.cross_covariance[off_mask])) <= TOL, (
        "Case C should have zero off-diagonal Isserlis covariance, got "
        f"{result_C.cross_covariance[off_mask]}"
    )

    # --- Sanity: Sigma C_3-circulant branch also works (smoke test) -----
    # Confirm the test runs cleanly on a nontrivial C_3-circulant Sigma
    # (the canonical Family C probe, Requirement 4.1).
    Sigma_circ = I3 + 0.1 * (
        np.ones((3, 3)) - I3
    )  # diag 1.0, off-diag 0.1, PD
    assert is_c3_circulant_symmetric(Sigma_circ), (
        "Sigma_circ should be C_3-circulant symmetric"
    )
    result_circ = gaussian_factorization_test(
        channel_projectors, Sigma_circ
    )
    print()
    print("Sanity: channel projectors under a C_3-circulant Sigma")
    print(f"  Sigma diagonal    = {np.diag(Sigma_circ)}")
    print(
        f"  Sigma off-diag    = {Sigma_circ[off_mask][0]:.3f} "
        "(uniform)"
    )
    print(f"  status            = {result_circ.status}")
    print(f"  failing_stage     = {result_circ.failing_stage}")
    # Channel projectors e_r e_r^T under a non-identity C_3-circulant
    # Sigma generally do NOT satisfy Tr(Sigma K_r Sigma K_s) = 0, because
    # Sigma mixes the channel directions. We expect this sanity run to
    # fail at the covariance stage for any Sigma with nonzero off-diagonal;
    # that is the correct behavior (the "probe ensemble matters" lesson).
    assert result_circ.status == FAILS_GAUSSIAN_PROBE, (
        "Channel projectors should fail under a non-identity C_3-circulant "
        f"Sigma, got {result_circ.status}"
    )

    print()
    print("all gaussian_factorization self-checks passed")
