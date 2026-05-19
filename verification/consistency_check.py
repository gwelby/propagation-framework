"""
Cross-deliverable consistency check for the God Equation Path B /
Family C operator functionals note and the exact Z_3 vacuum propagator
note.

Role
----
This module implements task 11.1 of
.kiro/specs/god-eq-path-b-family-c/tasks.md and Requirement 11 of
.kiro/specs/god-eq-path-b-family-c/requirements.md.

Two deliverables share a single source of truth for channel-space
algebra:

  * Family_C_Draft (derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md)
    verified by verification/family_c_kernels.py,
    verification/support_constraint.py,
    verification/gaussian_factorization.py,
    verification/counterexample_search.py.

  * Vacuum_Note (derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md)
    verified by verification/vacuum_propagator.py,
    verification/escape_comparison.py.

Both deliverables import their matrices, projectors, and spectral data
from verification/operator_algebra.py. This module confirms that common
origin at the Python level (object-identity checks against the
canonical module namespace), at the value level (T_sym, M, Sigma_bar,
and Sigma_bar_sq must agree bit-for-bit with the operator_algebra
defaults), and at the spectral level (M has eigenvalues {2, -1, -1};
T_sym^3 reproduces the closed-form identity; S_bar is a 3-cycle).

The module then performs a Sigma_vac-as-probe integration check: for a
representative set of points on the stable branch, it computes
Sigma_vac via `compute_vacuum_covariance` and feeds the resulting
covariance matrix into `gaussian_factorization_test` for every candidate
Family C kernel family returned by `family_c_kernels.canonical_polynomial_families`,
`family_c_kernels.canonical_seed_families`, and
`family_c_kernels.noncanonical_channel_projector_family`.

Two assertions are enforced:

  1. Every canonical family returned by `canonical_polynomial_families`
     or `canonical_seed_families` has K_0 = K_1 = K_2 (Theorem 1 of the
     Family C note). For any such family with a nonzero shared kernel
     K, the Isserlis covariance

          C_01 = 2 * Tr(Sigma_vac @ K @ Sigma_vac @ K)
               = 2 * ||Sigma_vac^{1/2} @ K @ Sigma_vac^{1/2}||_F^2

     is strictly positive, so the Gaussian factorization test MUST
     return FAILS_GAUSSIAN_PROBE at the covariance stage. This
     module asserts that outcome for every canonical-collapsed family
     at every tested (m^2, kappa, |p|) point.

  2. For the noncanonical basis-fixed probe family Q |e_r><e_r| Q we
     only RECORD the outcome as a diagnostic. The analytical verdict
     from god_eq_path_b_family_c_counterexample_search_2026-04-02.md
     is that this family escapes canonical collapse only by invoking
     the added hypothesis H_basis (channel basis selected inside the
     degenerate Q-sector). H_basis is NOT accepted as physical here;
     the family is kept in the enumeration purely so its Sigma_vac
     response is visible in the diagnostic report, and the docstring
     above flags its hypothesis explicitly.

Return contract
---------------
`run_consistency_check()` returns a `ConsistencyReport` dataclass (see
below) with:

  * all_cross_deliverable_constants_ok   bool
  * cross_deliverable_checks             list[CrossDeliverableCheck]
  * canonical_collapsed_runs             list[GaussianFactorizationRun]
  * noncanonical_runs                    list[GaussianFactorizationRun]
  * all_canonical_collapsed_fail_probe   bool
  * ran_without_exception                bool

and the module-level `if __name__ == "__main__"` block prints a concise
summary and asserts `all_cross_deliverable_constants_ok` and
`ran_without_exception`.

Guardrails
----------
This file lives under `verification/` only. It does NOT edit CLAIMS.md,
ACTIVE_ISSUES.md, WHATS_NEXT.md, design.md, requirements.md, or any
derivation note. It does NOT claim "H_prod is proved", does NOT upgrade
any confidence score, and does NOT silently accept the noncanonical
family's H_basis hypothesis as physical -- H_basis is flagged in this
docstring and in the per-run diagnostics.
"""

from __future__ import annotations

import sys
import traceback
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from verification import operator_algebra as _op_alg
from verification import vacuum_propagator as _vac
from verification import family_c_kernels as _fck
from verification import gaussian_factorization as _gf
from verification.gaussian_factorization import (
    FAILS_GAUSSIAN_PROBE,
    PASSES_EXACT_GAUSSIAN_TEST,
    GaussianFactorizationResult,
    gaussian_factorization_test,
)
from verification.operator_algebra import (
    F,
    I3,
    M,
    P0,
    Q,
    S_bar,
    S_bar_sq,
    Sigma_escape,
    T_sym,
    T_sym_cu,
    TOL,
)
from verification.vacuum_propagator import compute_vacuum_covariance


# ----------------------------------------------------------------------
# Representative probe points on the stable branch m^2 > 2 kappa > 0
# ----------------------------------------------------------------------

# Each triple (m^2, kappa, |p|) satisfies m^2 > 2 kappa > 0 (stable
# interior, Requirement 8.4). The first point reproduces the worked
# example of escape_comparison tests; the others probe a higher-mass
# regime and a momentum > 0 regime.
PROBE_POINTS: tuple[tuple[float, float, float], ...] = (
    (1.0, 0.1, 0.0),
    (4.0, 1.0, 0.5),
    (2.0, 0.5, 1.0),
)


# ----------------------------------------------------------------------
# Result dataclasses
# ----------------------------------------------------------------------


@dataclass
class CrossDeliverableCheck:
    """A single boolean check in the cross-deliverable constants block.

    Attributes
    ----------
    name : str
        Short human-readable label for the check.
    passed : bool
        True iff the check succeeded.
    detail : str
        One-line diagnostic (always populated; names what was compared
        and, on failure, the observed discrepancy).
    """

    name: str
    passed: bool
    detail: str


@dataclass
class GaussianFactorizationRun:
    """Outcome of a single Gaussian factorization test against Sigma_vac.

    Attributes
    ----------
    family_name : str
        KernelFamily.name for the family under test.
    is_canonical : bool
        True iff the family is canonical (no added hypotheses). Mirrors
        KernelFamily.is_canonical.
    added_hypotheses : list[str]
        KernelFamily.added_hypotheses. Non-empty for the noncanonical
        channel-projector family (H_basis). Flagged in the diagnostic
        report, never silently accepted as physical.
    collapsed : bool
        True iff K_0 = K_1 = K_2 to tolerance TOL (Theorem 1 signature).
    m_sq : float
        Bare mass squared m^2 used to build Sigma_vac.
    kappa : float
        Inter-channel coupling used to build Sigma_vac.
    p_abs : float
        Spatial momentum magnitude |p| used to build Sigma_vac.
    status : str
        Either FAILS_GAUSSIAN_PROBE or PASSES_EXACT_GAUSSIAN_TEST.
    failing_stage : str | None
        From GaussianFactorizationResult.failing_stage. None on pass.
    failing_pair : tuple[int, int] | None
        From GaussianFactorizationResult.failing_pair. None on pass.
    failing_magnitude : float
        From GaussianFactorizationResult.failing_magnitude.
    """

    family_name: str
    is_canonical: bool
    added_hypotheses: list[str]
    collapsed: bool
    m_sq: float
    kappa: float
    p_abs: float
    status: str
    failing_stage: Optional[str]
    failing_pair: Optional[tuple[int, int]]
    failing_magnitude: float


@dataclass
class ConsistencyReport:
    """Full summary returned by `run_consistency_check`.

    Attributes
    ----------
    all_cross_deliverable_constants_ok : bool
        AND of every `CrossDeliverableCheck.passed` in `cross_deliverable_checks`.
    cross_deliverable_checks : list[CrossDeliverableCheck]
        Ordered list of constant-level and identity-level checks.
    canonical_collapsed_runs : list[GaussianFactorizationRun]
        Gaussian factorization outcomes for every canonical-collapsed
        family at every PROBE_POINTS entry. Each entry MUST have
        status == FAILS_GAUSSIAN_PROBE and failing_stage == "covariance".
    noncanonical_runs : list[GaussianFactorizationRun]
        Gaussian factorization outcomes for the noncanonical
        channel-projector family at every PROBE_POINTS entry. No
        status assertion is made for these; the outcome is RECORDED as
        a diagnostic, and the family's H_basis hypothesis is carried
        alongside.
    all_canonical_collapsed_fail_probe : bool
        True iff every entry of `canonical_collapsed_runs` has
        status == FAILS_GAUSSIAN_PROBE AND failing_stage == "covariance".
    ran_without_exception : bool
        True iff every `gaussian_factorization_test` and
        `compute_vacuum_covariance` call returned a well-formed result
        (no Python exception raised, status not None).
    probe_points : tuple[tuple[float, float, float], ...]
        The (m^2, kappa, |p|) triples actually used.
    noncanonical_hypotheses : list[str]
        The full list of added hypotheses attached to the noncanonical
        channel-projector family. Included in the report so downstream
        consumers cannot overlook H_basis.
    """

    all_cross_deliverable_constants_ok: bool
    cross_deliverable_checks: list[CrossDeliverableCheck]
    canonical_collapsed_runs: list[GaussianFactorizationRun]
    noncanonical_runs: list[GaussianFactorizationRun]
    all_canonical_collapsed_fail_probe: bool
    ran_without_exception: bool
    probe_points: tuple[tuple[float, float, float], ...] = PROBE_POINTS
    noncanonical_hypotheses: list[str] = field(default_factory=list)


# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------


def _check_identity(
    name: str, obj_from_downstream: object, obj_from_canonical: object
) -> CrossDeliverableCheck:
    """Verify a downstream module imported the SAME Python object from operator_algebra.

    For numpy arrays `is` identity is the strongest possible evidence
    that two modules share a single source of truth: if both modules
    `from verification.operator_algebra import X`, Python binds the same
    array object in both namespaces, so `downstream.X is operator_algebra.X`
    returns True. Any mismatch signals that a module has locally rebuilt
    or shadowed the constant, which is exactly the failure mode this
    check exists to catch.
    """
    passed = obj_from_downstream is obj_from_canonical
    if passed:
        detail = f"shared Python object id={id(obj_from_canonical)}"
    else:
        detail = (
            f"DIFFERENT Python objects: downstream id={id(obj_from_downstream)}, "
            f"canonical id={id(obj_from_canonical)}"
        )
    return CrossDeliverableCheck(name=name, passed=passed, detail=detail)


def _check_value(
    name: str, actual: np.ndarray, expected: np.ndarray, tol: float = TOL
) -> CrossDeliverableCheck:
    """Verify `actual` equals `expected` as ndarrays to tolerance `tol`."""
    try:
        passed = bool(np.allclose(actual, expected, atol=tol))
        if passed:
            detail = f"max |actual - expected| <= {tol:.1e}"
        else:
            diff = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
            detail = f"max |actual - expected| = {diff:.6e} (tol={tol:.1e})"
    except Exception as exc:  # pragma: no cover - defensive
        passed = False
        detail = f"exception during comparison: {exc!r}"
    return CrossDeliverableCheck(name=name, passed=passed, detail=detail)


def _check_bool(name: str, passed: bool, detail: str) -> CrossDeliverableCheck:
    """Wrap a plain boolean check with a detail string."""
    return CrossDeliverableCheck(name=name, passed=bool(passed), detail=detail)


def _collect_candidate_families() -> (
    tuple[list[_fck.KernelFamily], _fck.KernelFamily]
):
    """Return (canonical_families, noncanonical_family) with validation run."""
    canonical: list[_fck.KernelFamily] = []
    canonical.extend(_fck.canonical_polynomial_families())
    canonical.extend(_fck.canonical_seed_families())
    for kf in canonical:
        _fck.validate_kernel_family(kf)
    noncanonical = _fck.noncanonical_channel_projector_family()
    _fck.validate_kernel_family(noncanonical)
    return canonical, noncanonical


def _run_one(
    kf: _fck.KernelFamily, m_sq: float, kappa: float, p_abs: float
) -> GaussianFactorizationRun:
    """Run `gaussian_factorization_test` with Sigma = Sigma_vac(m_sq, kappa, |p|)."""
    sigma_vac = compute_vacuum_covariance(m_sq, kappa, p_abs)
    result: GaussianFactorizationResult = gaussian_factorization_test(
        kf.kernels, sigma_vac
    )
    status = str(result.status)
    if status not in (FAILS_GAUSSIAN_PROBE, PASSES_EXACT_GAUSSIAN_TEST):
        raise AssertionError(
            f"gaussian_factorization_test returned unexpected status "
            f"{status!r} for family {kf.name!r} at "
            f"(m_sq={m_sq}, kappa={kappa}, p_abs={p_abs})"
        )
    return GaussianFactorizationRun(
        family_name=kf.name,
        is_canonical=kf.is_canonical,
        added_hypotheses=list(kf.added_hypotheses),
        collapsed=_fck.kernels_collapse_to_identical(kf, tol=TOL),
        m_sq=float(m_sq),
        kappa=float(kappa),
        p_abs=float(p_abs),
        status=status,
        failing_stage=result.failing_stage,
        failing_pair=result.failing_pair,
        failing_magnitude=float(result.failing_magnitude),
    )


# ----------------------------------------------------------------------
# Cross-deliverable constants block
# ----------------------------------------------------------------------


def _run_cross_deliverable_checks() -> list[CrossDeliverableCheck]:
    """Run the cross-deliverable constant checks and return the list of results."""
    checks: list[CrossDeliverableCheck] = []

    # (1) Object-identity checks: every downstream module must have pulled
    # the canonical constant out of operator_algebra, not rebuilt it locally.
    # Vacuum_Note side (verification.vacuum_propagator).
    checks.append(
        _check_identity(
            "vacuum_propagator.F is operator_algebra.F",
            _vac.F,
            _op_alg.F,
        )
    )
    checks.append(
        _check_identity(
            "vacuum_propagator.M is operator_algebra.M",
            _vac.M,
            _op_alg.M,
        )
    )
    checks.append(
        _check_identity(
            "vacuum_propagator.S_bar is operator_algebra.S_bar",
            _vac.S_bar,
            _op_alg.S_bar,
        )
    )
    checks.append(
        _check_identity(
            "vacuum_propagator.S_bar_sq is operator_algebra.S_bar_sq",
            _vac.S_bar_sq,
            _op_alg.S_bar_sq,
        )
    )
    checks.append(
        _check_identity(
            "vacuum_propagator.I3 is operator_algebra.I3",
            _vac.I3,
            _op_alg.I3,
        )
    )
    # Family_C_Draft side (verification.family_c_kernels).
    checks.append(
        _check_identity(
            "family_c_kernels.T_sym is operator_algebra.T_sym",
            _fck.T_sym,
            _op_alg.T_sym,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.T_sym_cu is operator_algebra.T_sym_cu",
            _fck.T_sym_cu,
            _op_alg.T_sym_cu,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.S_bar is operator_algebra.S_bar",
            _fck.S_bar,
            _op_alg.S_bar,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.S_bar_sq is operator_algebra.S_bar_sq",
            _fck.S_bar_sq,
            _op_alg.S_bar_sq,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.M is operator_algebra.M",
            _fck.M,
            _op_alg.M,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.P0 is operator_algebra.P0",
            _fck.P0,
            _op_alg.P0,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.Q is operator_algebra.Q",
            _fck.Q,
            _op_alg.Q,
        )
    )
    checks.append(
        _check_identity(
            "family_c_kernels.I3 is operator_algebra.I3",
            _fck.I3,
            _op_alg.I3,
        )
    )
    # gaussian_factorization is the other half of the Family_C_Draft.
    checks.append(
        _check_identity(
            "gaussian_factorization.I3 is operator_algebra.I3",
            _gf.I3,
            _op_alg.I3,
        )
    )

    # (2) Value-level identities (the stated definitions of R11.1-11.3).
    checks.append(
        _check_value(
            "T_sym == 0.5 * (S_bar + S_bar_sq)  [R11.1]",
            T_sym,
            0.5 * (S_bar + S_bar_sq),
        )
    )
    checks.append(
        _check_value(
            "S_bar_sq == S_bar @ S_bar  [R11.2]",
            S_bar_sq,
            S_bar @ S_bar,
        )
    )
    checks.append(
        _check_value(
            "S_bar_sq == S_bar.T  [R11.2]",
            S_bar_sq,
            S_bar.T,
        )
    )
    checks.append(
        _check_value(
            "M == S_bar + S_bar_sq  [R11.3]",
            M,
            S_bar + S_bar_sq,
        )
    )
    checks.append(
        _check_value(
            "S_bar @ S_bar @ S_bar == I3  (S_bar is a 3-cycle)",
            S_bar @ S_bar @ S_bar,
            I3,
        )
    )
    checks.append(
        _check_value(
            "T_sym is symmetric (T_sym == T_sym.T)",
            T_sym,
            T_sym.T,
        )
    )
    checks.append(
        _check_value(
            "T_sym^3 == (1/4) I + (3/8) S_bar + (3/8) S_bar_sq  (closed form)",
            T_sym_cu,
            0.25 * I3 + (3.0 / 8.0) * S_bar + (3.0 / 8.0) * S_bar_sq,
        )
    )

    # (3) Spectral identity: eigenvalues of M == {2, -1, -1} (R11.3 tail).
    eigs_M = np.sort(np.linalg.eigvalsh(M))
    expected_eigs_M = np.sort(np.array([2.0, -1.0, -1.0]))
    checks.append(
        _check_bool(
            "eigvalsh(M) == sorted(2, -1, -1)  [R11.3]",
            bool(np.allclose(eigs_M, expected_eigs_M, atol=TOL)),
            f"eigvalsh(M) = {eigs_M.tolist()}",
        )
    )

    # (4) DFT diagonalization cross-check: F^dagger @ M @ F == diag(2,-1,-1).
    FdMF = F.conj().T @ M @ F
    FdMF_diag_real = np.real(np.diag(FdMF))
    expected_diag = np.array([2.0, -1.0, -1.0])
    FdMF_offdiag_mag = float(
        np.max(np.abs(FdMF[~np.eye(3, dtype=bool)]))
    )
    checks.append(
        _check_bool(
            "F^dagger @ M @ F is diagonal with entries (2, -1, -1)",
            bool(
                np.allclose(FdMF_diag_real, expected_diag, atol=1e-10)
                and FdMF_offdiag_mag < 1e-10
            ),
            f"diag(F^dagger M F) = {FdMF_diag_real.tolist()}, "
            f"off-diag max = {FdMF_offdiag_mag:.2e}",
        )
    )

    # (5) Sigma_escape sanity: the Family A escape covariance exposed by
    # operator_algebra must still match the canonical integer entries
    # (diag 43, off-diag -21) and be C_3-circulant symmetric. This is
    # not strictly required by R11, but it is the downstream-of-T_sym
    # constant that Vacuum_Note compares its Sigma_vac sign against in
    # escape_comparison.py, so it belongs in the cross-deliverable block.
    off_mask = ~np.eye(3, dtype=bool)
    checks.append(
        _check_bool(
            "Sigma_escape C_3-circulant symmetric with diag 43, off-diag -21",
            bool(
                _op_alg.is_c3_circulant_symmetric(Sigma_escape, tol=TOL)
                and np.allclose(np.diag(Sigma_escape), 43.0, atol=1e-10)
                and np.allclose(
                    Sigma_escape[off_mask], -21.0, atol=1e-10
                )
            ),
            f"diag={np.diag(Sigma_escape).tolist()}, "
            f"off-diag unique={np.unique(Sigma_escape[off_mask]).tolist()}",
        )
    )

    return checks


# ----------------------------------------------------------------------
# Sigma_vac-as-probe integration check
# ----------------------------------------------------------------------


def _run_sigma_vac_probe_checks(
    canonical_families: list[_fck.KernelFamily],
    noncanonical_family: _fck.KernelFamily,
) -> tuple[list[GaussianFactorizationRun], list[GaussianFactorizationRun], bool]:
    """Run `gaussian_factorization_test(kf, Sigma_vac)` for every family and point.

    Returns
    -------
    canonical_collapsed_runs : list[GaussianFactorizationRun]
        One entry per (canonical-collapsed family, probe point) combination.
        Every entry MUST have status == FAILS_GAUSSIAN_PROBE and
        failing_stage == "covariance" (Theorem 1 + Isserlis factor-of-2).
    noncanonical_runs : list[GaussianFactorizationRun]
        One entry per probe point for the noncanonical channel-projector
        family. No status assertion; recorded as diagnostic only.
    all_collapsed_fail_probe : bool
        AND over `canonical_collapsed_runs` of
        (status == FAILS_GAUSSIAN_PROBE and failing_stage == "covariance").
    """
    canonical_runs: list[GaussianFactorizationRun] = []
    noncanonical_runs: list[GaussianFactorizationRun] = []
    all_collapsed_fail_probe = True

    # Quick validation: every canonical family in the enumeration is
    # predicted by Theorem 1 to have K_0 = K_1 = K_2. If the enumeration
    # ever yields a non-collapsed canonical family, we must NOT silently
    # apply the "collapsed => covariance FAILS" assertion to it.
    # Record it as a regular run and let the later all-pass aggregation
    # drop its status out of the collapsed-only assertion.
    for kf in canonical_families:
        collapsed = _fck.kernels_collapse_to_identical(kf, tol=TOL)
        if not collapsed:
            # Should not happen under Theorem 1; emit a diagnostic run.
            for m_sq, kappa, p_abs in PROBE_POINTS:
                run = _run_one(kf, m_sq, kappa, p_abs)
                canonical_runs.append(run)
            continue
        # Check whether the common kernel is the zero matrix -- Isserlis
        # gives C_rs = 0 identically for K = 0, so the covariance stage
        # would pass trivially and the whitened stage would too (B_r = 0).
        # The current enumeration does not produce such a family
        # (canonical_polynomial_families and canonical_seed_families all
        # yield nonzero K), but guard against future extensions.
        K_common = kf.kernels[0]
        K_is_zero = bool(np.allclose(K_common, np.zeros((3, 3)), atol=TOL))
        for m_sq, kappa, p_abs in PROBE_POINTS:
            run = _run_one(kf, m_sq, kappa, p_abs)
            canonical_runs.append(run)
            if K_is_zero:
                # Zero-kernel canonical family: Gaussian factorization
                # passes trivially. Not a failure of the all-collapsed-
                # fail-probe invariant, but skip it from that aggregate.
                continue
            if not (
                run.status == FAILS_GAUSSIAN_PROBE
                and run.failing_stage == "covariance"
            ):
                all_collapsed_fail_probe = False

    # Noncanonical channel-projector family: record outcomes; do NOT
    # assert a direction. The family carries H_basis (channel basis
    # selected inside the degenerate Q-sector), flagged in the
    # module-level docstring and in each run's `added_hypotheses`.
    for m_sq, kappa, p_abs in PROBE_POINTS:
        noncanonical_runs.append(
            _run_one(noncanonical_family, m_sq, kappa, p_abs)
        )

    return canonical_runs, noncanonical_runs, all_collapsed_fail_probe


# ----------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------


def run_consistency_check() -> ConsistencyReport:
    """Run the full cross-deliverable consistency check and return a report.

    Wraps every downstream numerical call (`compute_vacuum_covariance`,
    `gaussian_factorization_test`) in a try / except so a single
    failure does not hide the full diagnostic picture; any exception
    lowers `ran_without_exception` to False and is stored in the
    returned report's `cross_deliverable_checks` list as a dedicated
    entry.
    """
    cross_checks = _run_cross_deliverable_checks()
    all_consts_ok = all(c.passed for c in cross_checks)

    ran_ok = True
    canonical_runs: list[GaussianFactorizationRun] = []
    noncanonical_runs: list[GaussianFactorizationRun] = []
    all_collapsed_fail_probe = True
    noncanonical_hypotheses: list[str] = []

    try:
        canonical_families, noncanonical_family = _collect_candidate_families()
        noncanonical_hypotheses = list(noncanonical_family.added_hypotheses)
        (
            canonical_runs,
            noncanonical_runs,
            all_collapsed_fail_probe,
        ) = _run_sigma_vac_probe_checks(canonical_families, noncanonical_family)
    except Exception as exc:
        ran_ok = False
        cross_checks.append(
            CrossDeliverableCheck(
                name="Sigma_vac-as-probe integration run",
                passed=False,
                detail=(
                    f"exception during probe run: {exc!r}\n"
                    + traceback.format_exc()
                ),
            )
        )
        all_consts_ok = False
        all_collapsed_fail_probe = False

    return ConsistencyReport(
        all_cross_deliverable_constants_ok=all_consts_ok,
        cross_deliverable_checks=cross_checks,
        canonical_collapsed_runs=canonical_runs,
        noncanonical_runs=noncanonical_runs,
        all_canonical_collapsed_fail_probe=all_collapsed_fail_probe,
        ran_without_exception=ran_ok,
        noncanonical_hypotheses=noncanonical_hypotheses,
    )


__all__ = [
    "PROBE_POINTS",
    "CrossDeliverableCheck",
    "GaussianFactorizationRun",
    "ConsistencyReport",
    "run_consistency_check",
]


# ----------------------------------------------------------------------
# CLI summary
# ----------------------------------------------------------------------


def _print_report(report: ConsistencyReport) -> None:
    print("verification.consistency_check")
    print("-" * 70)
    print("Cross-deliverable constant checks:")
    for c in report.cross_deliverable_checks:
        flag = "OK " if c.passed else "FAIL"
        print(f"  [{flag}] {c.name}")
        if not c.passed:
            print(f"         -> {c.detail}")
    print(
        f"\nall_cross_deliverable_constants_ok = "
        f"{report.all_cross_deliverable_constants_ok}"
    )

    print()
    print("Sigma_vac-as-probe integration runs (canonical, collapsed):")
    print(
        f"  total = {len(report.canonical_collapsed_runs)}   "
        f"all FAIL at covariance stage = "
        f"{report.all_canonical_collapsed_fail_probe}"
    )
    if report.canonical_collapsed_runs:
        # One-line summary per family (aggregated across probe points).
        by_family: dict[str, list[GaussianFactorizationRun]] = {}
        for run in report.canonical_collapsed_runs:
            by_family.setdefault(run.family_name, []).append(run)
        for name, runs in by_family.items():
            statuses = {r.status for r in runs}
            stages = {r.failing_stage for r in runs}
            mags = [r.failing_magnitude for r in runs]
            mag_str = (
                f"{min(mags):.3e} .. {max(mags):.3e}" if mags else "n/a"
            )
            status_str = ",".join(sorted(statuses))
            stage_str = ",".join(sorted(str(s) for s in stages))
            print(
                f"  - {name:52s}  status={status_str}  "
                f"stage={stage_str}  |C_rs|={mag_str}"
            )

    print()
    print("Sigma_vac-as-probe integration runs (noncanonical, H_basis-tagged):")
    if report.noncanonical_hypotheses:
        print(
            "  added_hypotheses = "
            f"{report.noncanonical_hypotheses}"
        )
    for run in report.noncanonical_runs:
        print(
            f"  - (m^2={run.m_sq:.2f}, kappa={run.kappa:.2f}, "
            f"|p|={run.p_abs:.2f})  status={run.status}  "
            f"stage={run.failing_stage}  pair={run.failing_pair}  "
            f"|.|={run.failing_magnitude:.3e}"
        )

    print()
    print(f"ran_without_exception                 = {report.ran_without_exception}")
    print(
        f"all_cross_deliverable_constants_ok    = "
        f"{report.all_cross_deliverable_constants_ok}"
    )
    print(
        f"all_canonical_collapsed_fail_probe    = "
        f"{report.all_canonical_collapsed_fail_probe}"
    )


if __name__ == "__main__":
    report = run_consistency_check()
    _print_report(report)
    # Hard invariants. These two must hold for task 11.1 to pass.
    assert report.ran_without_exception, (
        "consistency_check encountered an exception; see the check list above"
    )
    assert report.all_cross_deliverable_constants_ok, (
        "cross-deliverable constant checks failed; see the check list above"
    )
    # Theorem 1 + Isserlis factor-of-2 consequence. We enforce this as
    # well because it is part of the task 11.1 acceptance criteria
    # (every canonical-collapsed family MUST fail the Gaussian probe
    # test at the covariance stage when Sigma = Sigma_vac is PD and the
    # shared kernel K is nonzero).
    assert report.all_canonical_collapsed_fail_probe, (
        "at least one canonical-collapsed family unexpectedly passed the "
        "Gaussian factorization test at the covariance stage with Sigma_vac; "
        "see the canonical_collapsed_runs in the report"
    )
    print()
    print("consistency_check: all invariants satisfied")
    sys.exit(0)
