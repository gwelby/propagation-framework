"""
Exact free linearized Z_3 vacuum covariance.

Role
----
This module implements Algorithm 3 (VacuumCovarianceDerivation) of
.kiro/specs/god-eq-path-b-family-c/design.md and Section 4 of
derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md.

Given the free linearized channel-space equation of motion

    (Box + m^2) delta_chi_j = kappa ( delta_chi_{j-1} + delta_chi_{j+1} )

with coupling matrix M = S_bar + S_bar^2 (eigenvalues { 2, -1, -1 }), the
discrete Fourier transform

    F[j,k] = (1/sqrt(3)) * omega^(j*k),   omega = exp(2*pi*i/3)

diagonalizes M as F^dagger M F = diag(2, -1, -1). The Fourier-mode
amplitudes then satisfy (Box + mu_k^2) tilde_chi_k = 0 with exact effective
mode masses

    mu_0^2 = m^2 - 2 kappa       (k = 0, symmetric mode)
    mu_1^2 = mu_2^2 = m^2 + kappa (k = 1, 2, degenerate anti-symmetric modes)

On the stable branch m^2 > 2 kappa > 0 all three mode masses are positive.
The equal-time free vacuum variance of a single massive scalar mode at
spatial momentum magnitude |p| is the standard

    omega_k(|p|) = sqrt( |p|^2 + mu_k^2 )
    nu_k(|p|)   = 1 / ( 2 omega_k(|p|) )

so the normal-mode covariance is diag(nu_0, nu_1, nu_1) and the channel-
basis covariance is

    Sigma_vac(|p|) = F diag(nu_0, nu_1, nu_1) F^dagger.

Expanding the DFT sum gives the exact closed form

    Sigma_vac = d * I + o * ( S_bar + S_bar^2 )

with

    d = (nu_0 + 2 nu_1) / 3
    o = (nu_0 - nu_1) / 3.

This is C_3-circulant symmetric and real. On the stable branch omega_0 <
omega_1 (since m^2 - 2 kappa < m^2 + kappa), so nu_0 > nu_1 and the off-
diagonal entry o is strictly positive. That positive sign is the opposite
of Sigma_escape (negative off-diagonals, see operator_algebra.py), which
is the central observation of the vacuum note.

Public API
----------
- `compute_vacuum_covariance(m_sq, kappa, p_abs)` -> real 3x3 ndarray
- `mode_masses_sq(m_sq, kappa)` -> (mu_0_sq, mu_1_sq)
- `mode_frequencies(m_sq, kappa, p_abs)` -> (omega_0, omega_1)
- `mode_variances(m_sq, kappa, p_abs)` -> (nu_0, nu_1)
- `VacuumCovarianceDiagnostics` dataclass for structured diagnostics
- `vacuum_covariance_diagnostics(m_sq, kappa, p_abs)` -> full diagnostic bundle

Requirements validated
----------------------
This module validates the Requirement 6 acceptance criteria for the
Vacuum_Note (see .kiro/specs/god-eq-path-b-family-c/requirements.md):

    * R6.1: the linearized EOM uses the coupling matrix M = S_bar + S_bar^2.
    * R6.2: the coupling matrix is diagonalized via the 3x3 DFT (the
      underlying identity F^dagger M F = diag(2, -1, -1) is asserted at
      import time in operator_algebra.py).
    * R6.3: mode masses mu_0^2 = m^2 - 2 kappa and mu_1^2 = m^2 + kappa.
    * R6.4: the equal-time vacuum covariance is computed in the normal-
      mode basis and transformed to the channel basis.
    * R6.5: the exact entries of Sigma_vac are stated (and asserted) as a
      C_3-circulant matrix with diagonal (nu_0 + 2 nu_1) / 3 and off-
      diagonal (nu_0 - nu_1) / 3.

Regime analysis (task 9.1, Requirement 8)
-----------------------------------------
In addition to the exact computation this module exposes analytic and
numeric regime-analysis helpers for Requirement 8:

    * `decoupling_limit(m_sq, p_abs)` — the kappa -> 0^+ limit
      Sigma_vac -> sigma^2 * I with sigma^2 = 1 / (2 sqrt(|p|^2 + m^2))
      (Requirement 8.1).
    * `small_kappa_expansion(m_sq, kappa, p_abs, order=2)` — analytic
      Taylor expansion of (nu_0, nu_1, d, o) in epsilon = kappa / E^2,
      E^2 = |p|^2 + m^2, with the documented algebra (Requirement 8.2).
    * `stability_edge_behavior(m_sq, p_abs)` — structured description
      of the kappa -> m^2 / 2^- boundary, documenting that nu_0 diverges
      at |p| = 0 and stating this as a regime boundary, not a physical
      prediction (Requirements 8.3, 8.4). This function deliberately does
      NOT return a Sigma_vac value at the edge; the input validator in
      `_validate_inputs` already enforces the stable interior.
    * `verify_regime_consistency(m_sq, p_abs, n_kappa=20)` — numerical
      cross-check of the three regimes above against
      `compute_vacuum_covariance`.

Scope
-----
This module only implements the exact vacuum covariance on the stable
branch and its regime-analysis helpers. Sign comparison with Sigma_escape
lives in `escape_comparison.py`; this module deliberately does not import
it so it can be used as a primitive by downstream code.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from verification.operator_algebra import (
    F,
    I3,
    M,
    S_bar,
    S_bar_sq,
    TOL,
    is_c3_circulant_symmetric,
)


# ----------------------------------------------------------------------
# Input validation
# ----------------------------------------------------------------------


def _validate_inputs(m_sq: float, kappa: float, p_abs: float) -> tuple[
    float, float, float
]:
    """Validate (m_sq, kappa, p_abs) lie on the stable branch with |p| >= 0.

    Enforces:
      * kappa > 0   (physical inter-channel coupling, Requirement 6.3)
      * m_sq > 2 * kappa  (stable branch, so mu_0^2 = m^2 - 2 kappa > 0,
        Requirement 8.4)
      * p_abs >= 0  (spatial momentum magnitude is a non-negative real)
      * all three inputs are finite real scalars

    Raises ValueError on any violation. Returns the inputs as plain floats.
    """
    try:
        m_sq_f = float(m_sq)
        kappa_f = float(kappa)
        p_abs_f = float(p_abs)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"m_sq, kappa, p_abs must all be real scalars; got "
            f"m_sq={m_sq!r}, kappa={kappa!r}, p_abs={p_abs!r}"
        ) from exc

    for name, val in (("m_sq", m_sq_f), ("kappa", kappa_f), ("p_abs", p_abs_f)):
        if not np.isfinite(val):
            raise ValueError(f"{name} must be finite, got {val!r}")

    if kappa_f <= 0.0:
        raise ValueError(
            f"kappa must be strictly positive (physical inter-channel "
            f"coupling), got kappa={kappa_f}"
        )

    if m_sq_f <= 2.0 * kappa_f:
        raise ValueError(
            "stable branch requires m_sq > 2 * kappa (so mu_0^2 = m^2 - "
            f"2 kappa > 0); got m_sq={m_sq_f}, kappa={kappa_f}, "
            f"m_sq - 2*kappa = {m_sq_f - 2.0 * kappa_f}"
        )

    if p_abs_f < 0.0:
        raise ValueError(
            f"p_abs (spatial momentum magnitude) must be >= 0, got {p_abs_f}"
        )

    return m_sq_f, kappa_f, p_abs_f


# ----------------------------------------------------------------------
# Mode-level helpers
# ----------------------------------------------------------------------


def mode_masses_sq(m_sq: float, kappa: float) -> tuple[float, float]:
    """Return (mu_0^2, mu_1^2) with mu_0^2 = m^2 - 2 kappa, mu_1^2 = m^2 + kappa.

    The degenerate k = 2 mass squared equals mu_1^2 and is not returned
    separately; callers that need it can reuse the second element.

    Requires m_sq > 2 * kappa > 0 (stable branch).
    """
    m_sq_f, kappa_f, _ = _validate_inputs(m_sq, kappa, 0.0)
    mu0_sq = m_sq_f - 2.0 * kappa_f
    mu1_sq = m_sq_f + kappa_f
    # Redundant sanity: both must be strictly positive on the stable branch.
    if mu0_sq <= 0.0 or mu1_sq <= 0.0:
        raise ValueError(
            "mode mass squared must be strictly positive on the stable "
            f"branch; got mu_0^2 = {mu0_sq}, mu_1^2 = {mu1_sq}"
        )
    return mu0_sq, mu1_sq


def mode_frequencies(
    m_sq: float, kappa: float, p_abs: float
) -> tuple[float, float]:
    """Return (omega_0, omega_1) = (sqrt(|p|^2 + mu_k^2)) for k = 0, 1.

    The degenerate k = 2 frequency equals omega_1 and is not returned
    separately.

    Requires m_sq > 2 * kappa > 0 and p_abs >= 0.
    """
    m_sq_f, kappa_f, p_abs_f = _validate_inputs(m_sq, kappa, p_abs)
    mu0_sq, mu1_sq = mode_masses_sq(m_sq_f, kappa_f)
    p_sq = p_abs_f * p_abs_f
    omega_0 = float(np.sqrt(p_sq + mu0_sq))
    omega_1 = float(np.sqrt(p_sq + mu1_sq))
    return omega_0, omega_1


def mode_variances(
    m_sq: float, kappa: float, p_abs: float
) -> tuple[float, float]:
    """Return (nu_0, nu_1) = (1 / (2 * omega_k)) for k = 0, 1.

    The degenerate k = 2 variance equals nu_1 and is not returned
    separately.

    Requires m_sq > 2 * kappa > 0 and p_abs >= 0.
    """
    omega_0, omega_1 = mode_frequencies(m_sq, kappa, p_abs)
    nu_0 = 1.0 / (2.0 * omega_0)
    nu_1 = 1.0 / (2.0 * omega_1)
    return nu_0, nu_1


# ----------------------------------------------------------------------
# Diagnostics dataclass
# ----------------------------------------------------------------------


@dataclass
class VacuumCovarianceDiagnostics:
    """Full diagnostic bundle for `compute_vacuum_covariance`.

    Attributes
    ----------
    m_sq : float
        Bare mass squared m^2 supplied by the caller.
    kappa : float
        Inter-channel coupling kappa supplied by the caller.
    p_abs : float
        Spatial momentum magnitude |p| supplied by the caller.
    mu_sq : tuple[float, float]
        Mode mass squared (mu_0^2, mu_1^2).
    omega : tuple[float, float]
        Mode frequencies (omega_0, omega_1) at the given |p|.
    nu : tuple[float, float]
        Mode variances (nu_0, nu_1) at the given |p|.
    diagonal : float
        d = (nu_0 + 2 nu_1) / 3, the channel-basis diagonal entry.
    off_diagonal : float
        o = (nu_0 - nu_1) / 3, the channel-basis off-diagonal entry. On
        the stable branch this is strictly positive.
    sigma_vac : np.ndarray
        The exact 3x3 real symmetric C_3-circulant channel-basis vacuum
        covariance Sigma_vac = d I + o (S_bar + S_bar^2).
    max_imag : float
        Maximum absolute imaginary part of the raw F diag(nu) F^dagger
        product (must be below TOL for a real circulant input).
    """

    m_sq: float
    kappa: float
    p_abs: float
    mu_sq: tuple[float, float]
    omega: tuple[float, float]
    nu: tuple[float, float]
    diagonal: float
    off_diagonal: float
    sigma_vac: np.ndarray
    max_imag: float


# ----------------------------------------------------------------------
# Main algorithm
# ----------------------------------------------------------------------


def compute_vacuum_covariance(
    m_sq: float, kappa: float, p_abs: float, tol: float = TOL
) -> np.ndarray:
    """Return the exact free linearized Z_3 vacuum covariance in the channel basis.

    Implements Algorithm 3 of .kiro/specs/god-eq-path-b-family-c/design.md.
    Given m^2, kappa, and |p| on the stable branch, computes mode masses
    mu_0^2 = m^2 - 2 kappa and mu_1^2 = mu_2^2 = m^2 + kappa, the mode
    frequencies omega_k = sqrt(|p|^2 + mu_k^2), and the mode variances
    nu_k = 1 / (2 omega_k). Transforms to the channel basis via

        Sigma_vac = F diag(nu_0, nu_1, nu_1) F^dagger

    with F the 3x3 DFT matrix from operator_algebra.py. Asserts that the
    result is real, symmetric, C_3-circulant, and matches the closed-form
    identity

        Sigma_vac = d I + o ( S_bar + S_bar^2 ),
        d = (nu_0 + 2 nu_1) / 3,
        o = (nu_0 - nu_1) / 3,

    which is the exact content of Requirement 6.5.

    Parameters
    ----------
    m_sq : float
        Bare mass squared m^2. Must satisfy m_sq > 2 * kappa (stable branch).
    kappa : float
        Inter-channel coupling. Must be strictly positive.
    p_abs : float
        Spatial momentum magnitude |p|. Must be >= 0.
    tol : float, optional
        Absolute tolerance for the imaginary-part, symmetry, and
        closed-form-identity checks. Defaults to the module TOL = 1e-12.

    Returns
    -------
    np.ndarray
        Real symmetric 3x3 ndarray with dtype float64: the channel-basis
        vacuum covariance Sigma_vac(|p|).

    Raises
    ------
    ValueError
        If (m_sq, kappa, p_abs) violate stability or sign constraints
        (see `_validate_inputs`).
    AssertionError
        If Sigma_vac is not real within `tol` (should never happen for
        the circulant input constructed here), not symmetric, or does
        not match the closed-form C_3-circulant identity.

    Requirements validated
    ----------------------
    Requirements 6.1, 6.2, 6.3, 6.4, 6.5.
    """
    m_sq_f, kappa_f, p_abs_f = _validate_inputs(m_sq, kappa, p_abs)

    # Step 1: mode data on the stable branch.
    nu_0, nu_1 = mode_variances(m_sq_f, kappa_f, p_abs_f)

    # Step 2: transform to channel basis via Sigma_vac = F diag(nu) F^dagger.
    # Fourier ordering: k = 0 (symmetric mode), then the two degenerate
    # modes k = 1, 2. This matches F^dagger M F = diag(2, -1, -1) asserted
    # at import time in operator_algebra.py.
    nu_diag = np.diag([nu_0 + 0.0j, nu_1 + 0.0j, nu_1 + 0.0j])
    sigma_complex = F @ nu_diag @ F.conj().T

    # Imaginary part of a circulant-input conjugation by the DFT must
    # vanish to machine precision. Keep the maximum for diagnostics and
    # then drop to float64.
    max_imag = float(np.max(np.abs(np.imag(sigma_complex))))
    if max_imag > tol:
        raise AssertionError(
            "Sigma_vac has non-negligible imaginary part "
            f"(max |Im| = {max_imag:.3e}); expected zero for circulant input"
        )

    sigma_vac = np.real(sigma_complex)
    # Force exact symmetry against machine-precision noise (F unitary plus
    # real diag(nu) already implies symmetry up to eps; this just cleans
    # up the last bit of noise for downstream consumers).
    sigma_vac = 0.5 * (sigma_vac + sigma_vac.T)

    # Step 3: verify the closed-form C_3-circulant identity
    #     Sigma_vac = d I + o ( S_bar + S_bar^2 ),
    #     d = (nu_0 + 2 nu_1) / 3,  o = (nu_0 - nu_1) / 3.
    d = (nu_0 + 2.0 * nu_1) / 3.0
    o = (nu_0 - nu_1) / 3.0
    sigma_expected = d * I3 + o * M
    if not np.allclose(sigma_vac, sigma_expected, atol=tol):
        raise AssertionError(
            "Sigma_vac does not match the closed-form C_3-circulant "
            "identity d*I + o*(S_bar + S_bar^2); "
            f"max deviation = {np.max(np.abs(sigma_vac - sigma_expected)):.3e}"
        )

    # Step 4: verify C_3-circulant symmetric structure (diagonal all equal,
    # off-diagonal all equal, symmetric, real).
    if not is_c3_circulant_symmetric(sigma_vac, tol=tol):
        raise AssertionError(
            "Sigma_vac is not C_3-circulant symmetric within tolerance"
        )

    return sigma_vac


def vacuum_covariance_diagnostics(
    m_sq: float, kappa: float, p_abs: float, tol: float = TOL
) -> VacuumCovarianceDiagnostics:
    """Return a full `VacuumCovarianceDiagnostics` bundle for the given inputs.

    Wraps `compute_vacuum_covariance` with the per-mode intermediates and
    a structural-check summary. Useful for test code, CLI diagnostics,
    and downstream modules (e.g. escape_comparison.py) that want to
    inspect the mode-level data alongside the channel-basis matrix.
    """
    m_sq_f, kappa_f, p_abs_f = _validate_inputs(m_sq, kappa, p_abs)
    mu_sq = mode_masses_sq(m_sq_f, kappa_f)
    omega = mode_frequencies(m_sq_f, kappa_f, p_abs_f)
    nu_0, nu_1 = mode_variances(m_sq_f, kappa_f, p_abs_f)

    # Recompute the complex product once to report max_imag honestly;
    # compute_vacuum_covariance then re-does the algebra and re-validates.
    nu_diag = np.diag([nu_0 + 0.0j, nu_1 + 0.0j, nu_1 + 0.0j])
    sigma_complex = F @ nu_diag @ F.conj().T
    max_imag = float(np.max(np.abs(np.imag(sigma_complex))))

    sigma_vac = compute_vacuum_covariance(m_sq_f, kappa_f, p_abs_f, tol=tol)

    return VacuumCovarianceDiagnostics(
        m_sq=m_sq_f,
        kappa=kappa_f,
        p_abs=p_abs_f,
        mu_sq=mu_sq,
        omega=omega,
        nu=(nu_0, nu_1),
        diagonal=(nu_0 + 2.0 * nu_1) / 3.0,
        off_diagonal=(nu_0 - nu_1) / 3.0,
        sigma_vac=sigma_vac,
        max_imag=max_imag,
    )


# ----------------------------------------------------------------------
# Regime analysis (task 9.1 / Requirement 8)
# ----------------------------------------------------------------------
#
# These helpers supply the analytic and numerical content for Requirement 8
# of .kiro/specs/god-eq-path-b-family-c/requirements.md:
#
#   8.1  As kappa -> 0^+, Sigma_vac -> sigma^2 * I with
#        sigma^2 = 1 / (2 sqrt(|p|^2 + m^2)).
#   8.2  For small kappa / m^2 (more precisely small kappa / E^2 where
#        E^2 = |p|^2 + m^2), state the leading-order correction.
#   8.3  As kappa -> (m^2 / 2)^-, nu_0 = 1 / (2 sqrt(|p|^2 + m^2 - 2 kappa))
#        diverges at |p| = 0 (the k=0 mode goes soft).
#   8.4  All conclusions are restricted to the stable interior m^2 > 2 kappa.
#
# Algebraic setup. Define E^2 = |p|^2 + m^2 and epsilon = kappa / E^2. Then
#
#     mu_0^2 = m^2 - 2 kappa      =>  |p|^2 + mu_0^2 = E^2 * (1 - 2 epsilon)
#     mu_1^2 = m^2 +   kappa      =>  |p|^2 + mu_1^2 = E^2 * (1 +   epsilon)
#
# so
#
#     nu_0 = sigma^2 / sqrt(1 - 2 epsilon),
#     nu_1 = sigma^2 / sqrt(1 + epsilon),
#     d    = (nu_0 + 2 nu_1) / 3,
#     o    = (nu_0 - nu_1) / 3.
#
# Taylor-expanding in epsilon (verified symbolically, see the self-check):
#
#     nu_0 / sigma^2 = 1 + epsilon + (3/2) epsilon^2 + (5/2) epsilon^3 + O(eps^4)
#     nu_1 / sigma^2 = 1 - (1/2) epsilon + (3/8) epsilon^2 - (5/16) epsilon^3 + ...
#     d    / sigma^2 = 1           + (3/4) epsilon^2 + (5/8) epsilon^3 + O(eps^4)
#     o    / sigma^2 =     (1/2) epsilon + (3/8) epsilon^2 + (15/16) epsilon^3 + ...
#
# The linear term in d cancels between nu_0 and 2 nu_1: the first
# correction to the diagonal is O(epsilon^2), while the off-diagonal has a
# nonzero O(epsilon) leading term. This matches Requirement 8.2: the
# leading-order correction to the decoupled limit is
#
#     d = sigma^2 + O(epsilon^2),
#     o = sigma^2 * epsilon / 2 + O(epsilon^2),
#
# so Sigma_vac = sigma^2 I + (sigma^2 epsilon / 2) * (S_bar + S_bar^2)
# + O(epsilon^2) with epsilon = kappa / (|p|^2 + m^2).


@dataclass(frozen=True)
class DecouplingLimit:
    """Analytic kappa -> 0^+ limit of Sigma_vac (Requirement 8.1).

    Attributes
    ----------
    m_sq : float
        Bare mass squared m^2 supplied by the caller.
    p_abs : float
        Spatial momentum magnitude |p| supplied by the caller.
    sigma_sq : float
        sigma^2 = 1 / (2 sqrt(|p|^2 + m^2)), the common mode variance
        reached by every channel in the decoupled limit.
    sigma_vac_limit : np.ndarray
        sigma^2 * I, the limiting channel-basis covariance.
    """

    m_sq: float
    p_abs: float
    sigma_sq: float
    sigma_vac_limit: np.ndarray


def decoupling_limit(m_sq: float, p_abs: float) -> DecouplingLimit:
    """Return the kappa -> 0^+ limit Sigma_vac -> sigma^2 * I (Requirement 8.1).

    Analytic content. When kappa -> 0 on the stable branch, both mode
    mass squared mu_0^2 = m^2 - 2 kappa and mu_1^2 = m^2 + kappa approach
    m^2, so both mode variances nu_0, nu_1 approach

        sigma^2 = 1 / (2 sqrt(|p|^2 + m^2))

    and the channel-basis covariance

        Sigma_vac = d I + o (S_bar + S_bar^2),
        d = (nu_0 + 2 nu_1) / 3,  o = (nu_0 - nu_1) / 3

    collapses to d -> sigma^2, o -> 0, i.e. Sigma_vac -> sigma^2 * I.

    Requires m^2 > 0 and |p| >= 0. Does not take kappa: this is the
    analytic limit, not a perturbative evaluation at finite kappa. For a
    finite-kappa numerical check see `verify_regime_consistency`.
    """
    try:
        m_sq_f = float(m_sq)
        p_abs_f = float(p_abs)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"m_sq and p_abs must be real scalars; got "
            f"m_sq={m_sq!r}, p_abs={p_abs!r}"
        ) from exc
    if not (np.isfinite(m_sq_f) and np.isfinite(p_abs_f)):
        raise ValueError(
            f"m_sq and p_abs must be finite; got m_sq={m_sq_f}, p_abs={p_abs_f}"
        )
    if m_sq_f <= 0.0:
        raise ValueError(
            f"decoupling limit requires m_sq > 0, got m_sq={m_sq_f}"
        )
    if p_abs_f < 0.0:
        raise ValueError(f"p_abs must be >= 0, got {p_abs_f}")

    sigma_sq = 1.0 / (2.0 * np.sqrt(p_abs_f * p_abs_f + m_sq_f))
    sigma_vac_limit = float(sigma_sq) * I3.copy()
    return DecouplingLimit(
        m_sq=m_sq_f,
        p_abs=p_abs_f,
        sigma_sq=float(sigma_sq),
        sigma_vac_limit=sigma_vac_limit,
    )


@dataclass(frozen=True)
class SmallKappaExpansion:
    """Analytic Taylor expansion of (nu_0, nu_1, d, o) in epsilon = kappa / E^2.

    The expansion is carried out on the stable branch m^2 > 2 kappa > 0
    (so epsilon < 1/2) and truncated at `order`. The stored values are
    the polynomial approximations, NOT the exact nu_k / d / o; compare to
    `compute_vacuum_covariance` for the exact result.

    Attributes
    ----------
    m_sq, kappa, p_abs : float
        The inputs.
    epsilon : float
        kappa / E^2 where E^2 = |p|^2 + m^2.
    sigma_sq : float
        1 / (2 sqrt(|p|^2 + m^2)), the kappa -> 0 common variance.
    order : int
        Truncation order of the expansion (1 or 2).
    nu0_series : float
        sigma^2 * (1 + epsilon + (3/2) epsilon^2 + ...) truncated at `order`.
    nu1_series : float
        sigma^2 * (1 - epsilon/2 + (3/8) epsilon^2 - ...) truncated at `order`.
    diagonal_series : float
        sigma^2 * (1 + (3/4) epsilon^2 + ...) truncated at `order`. The
        O(epsilon) term cancels exactly.
    off_diagonal_series : float
        sigma^2 * (epsilon/2 + (3/8) epsilon^2 + ...) truncated at `order`.
        The leading correction is linear in kappa with coefficient
        sigma^2 / (2 E^2).
    sigma_vac_series : np.ndarray
        The channel-basis matrix diagonal_series * I + off_diagonal_series
        * (S_bar + S_bar^2), truncated at `order`.
    """

    m_sq: float
    kappa: float
    p_abs: float
    epsilon: float
    sigma_sq: float
    order: int
    nu0_series: float
    nu1_series: float
    diagonal_series: float
    off_diagonal_series: float
    sigma_vac_series: np.ndarray


def small_kappa_expansion(
    m_sq: float, kappa: float, p_abs: float, order: int = 2
) -> SmallKappaExpansion:
    """Return the leading-order small-kappa expansion of Sigma_vac (Requirement 8.2).

    Expands the exact mode variances

        nu_0 = sigma^2 / sqrt(1 - 2 epsilon),
        nu_1 = sigma^2 / sqrt(1 + epsilon)

    and the circulant entries d = (nu_0 + 2 nu_1) / 3, o = (nu_0 - nu_1) / 3
    in powers of epsilon = kappa / E^2 with E^2 = |p|^2 + m^2 and
    sigma^2 = 1 / (2 sqrt(E^2)). The expansions, verified symbolically:

        nu_0 / sigma^2 = 1 + eps + (3/2) eps^2 + O(eps^3)
        nu_1 / sigma^2 = 1 - eps/2 + (3/8) eps^2 + O(eps^3)
        d    / sigma^2 = 1 + 0 * eps + (3/4) eps^2 + O(eps^3)
        o    / sigma^2 = eps/2 + (3/8) eps^2 + O(eps^3)

    In particular the leading-order correction to the decoupled limit is

        o = sigma^2 * epsilon / 2 + O(epsilon^2),
        d = sigma^2 + O(epsilon^2),

    i.e. the off-diagonal grows linearly in kappa with slope sigma^2 /
    (2 E^2) while the diagonal correction is O(kappa^2). Supported orders
    are 1 (leading) and 2.

    Requires m^2 > 2 kappa > 0 and |p| >= 0 (stable interior, Requirement 8.4).
    """
    m_sq_f, kappa_f, p_abs_f = _validate_inputs(m_sq, kappa, p_abs)
    if order not in (1, 2):
        raise ValueError(f"order must be 1 or 2, got {order}")

    E_sq = p_abs_f * p_abs_f + m_sq_f
    sigma_sq = 1.0 / (2.0 * np.sqrt(E_sq))
    eps = kappa_f / E_sq

    # Truncated series. The order-1 truncation drops all terms of O(eps^2)
    # and higher; order-2 includes the eps^2 terms.
    if order == 1:
        nu0 = sigma_sq * (1.0 + eps)
        nu1 = sigma_sq * (1.0 - 0.5 * eps)
        d = sigma_sq
        o = sigma_sq * 0.5 * eps
    else:
        eps2 = eps * eps
        nu0 = sigma_sq * (1.0 + eps + 1.5 * eps2)
        nu1 = sigma_sq * (1.0 - 0.5 * eps + 0.375 * eps2)
        d = sigma_sq * (1.0 + 0.75 * eps2)
        o = sigma_sq * (0.5 * eps + 0.375 * eps2)

    sigma_vac_series = float(d) * I3 + float(o) * M

    return SmallKappaExpansion(
        m_sq=m_sq_f,
        kappa=kappa_f,
        p_abs=p_abs_f,
        epsilon=float(eps),
        sigma_sq=float(sigma_sq),
        order=int(order),
        nu0_series=float(nu0),
        nu1_series=float(nu1),
        diagonal_series=float(d),
        off_diagonal_series=float(o),
        sigma_vac_series=sigma_vac_series,
    )


@dataclass(frozen=True)
class StabilityEdgeBehavior:
    """Structured description of the kappa -> (m^2 / 2)^- boundary.

    Implements Requirements 8.3 and 8.4: as kappa approaches m^2 / 2 from
    below, mu_0^2 = m^2 - 2 kappa -> 0^+. At |p| = 0 the mode variance
    nu_0 = 1 / (2 sqrt(|p|^2 + mu_0^2)) = 1 / (2 sqrt(m^2 - 2 kappa))
    diverges; at |p| > 0 it remains finite and approaches 1 / (2 |p|).

    This is a REGIME BOUNDARY, not a physical prediction: the free
    linearized analysis of this module is only trusted in the stable
    interior m^2 > 2 kappa, and at the edge the k = 0 zero-mode
    Gaussian integral is not normalizable. `compute_vacuum_covariance`
    refuses to evaluate at or past the edge; this helper documents the
    behavior analytically without returning a Sigma_vac value.

    Attributes
    ----------
    m_sq : float
        Bare mass squared m^2.
    p_abs : float
        Spatial momentum magnitude |p|.
    kappa_edge : float
        m^2 / 2, the upper end of the stable interval in kappa.
    diverges_at_zero_momentum : bool
        True iff |p| = 0. When True, nu_0 -> +inf as kappa -> kappa_edge.
    nu0_edge_limit : float
        The formal limit value of nu_0 at the edge: +inf when |p| = 0,
        otherwise the finite value 1 / (2 |p|).
    regime_boundary : bool
        Always True. Signals to callers that this is a boundary of the
        validated analysis, not a physical regime.
    description : str
        Human-readable summary suitable for inclusion in diagnostic
        output or derivation notes.
    """

    m_sq: float
    p_abs: float
    kappa_edge: float
    diverges_at_zero_momentum: bool
    nu0_edge_limit: float
    regime_boundary: bool
    description: str


def stability_edge_behavior(m_sq: float, p_abs: float) -> StabilityEdgeBehavior:
    """Describe the kappa -> (m^2 / 2)^- limit without evaluating Sigma_vac.

    Requires m^2 > 0 and |p| >= 0. Does NOT take kappa: at kappa = m^2 / 2
    the validator in `_validate_inputs` refuses to return a Sigma_vac
    (mu_0^2 = 0 takes the analysis off the stable branch); this helper
    only documents the limiting behavior of nu_0 as the edge is
    approached from below. See Requirements 8.3, 8.4.
    """
    try:
        m_sq_f = float(m_sq)
        p_abs_f = float(p_abs)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"m_sq and p_abs must be real scalars; got "
            f"m_sq={m_sq!r}, p_abs={p_abs!r}"
        ) from exc
    if not (np.isfinite(m_sq_f) and np.isfinite(p_abs_f)):
        raise ValueError(
            f"m_sq and p_abs must be finite; got m_sq={m_sq_f}, p_abs={p_abs_f}"
        )
    if m_sq_f <= 0.0:
        raise ValueError(
            f"stability_edge_behavior requires m_sq > 0, got m_sq={m_sq_f}"
        )
    if p_abs_f < 0.0:
        raise ValueError(f"p_abs must be >= 0, got {p_abs_f}")

    kappa_edge = 0.5 * m_sq_f
    diverges = p_abs_f == 0.0
    if diverges:
        nu0_edge_limit = float("inf")
        description = (
            f"At kappa = m^2 / 2 = {kappa_edge:.6g} the k=0 mode mass "
            "squared mu_0^2 = m^2 - 2 kappa vanishes. With |p| = 0 the "
            "mode frequency omega_0 = sqrt(|p|^2 + mu_0^2) -> 0^+ and "
            "nu_0 = 1 / (2 omega_0) diverges. This is a regime boundary "
            "of the free linearized analysis, not a physical prediction: "
            "the zero-mode Gaussian integral fails to be normalizable. "
            "compute_vacuum_covariance is restricted to the stable "
            "interior m^2 > 2 kappa."
        )
    else:
        nu0_edge_limit = 1.0 / (2.0 * p_abs_f)
        description = (
            f"At kappa = m^2 / 2 = {kappa_edge:.6g} the k=0 mode mass "
            "squared mu_0^2 vanishes, but |p| > 0 keeps omega_0 = |p| "
            f"finite so nu_0 -> 1 / (2 |p|) = {nu0_edge_limit:.6g}. "
            "The covariance at this kappa remains formally finite at "
            f"|p| = {p_abs_f:.6g} but still sits on the regime boundary: "
            "compute_vacuum_covariance is restricted to the stable "
            "interior m^2 > 2 kappa."
        )

    return StabilityEdgeBehavior(
        m_sq=m_sq_f,
        p_abs=p_abs_f,
        kappa_edge=float(kappa_edge),
        diverges_at_zero_momentum=bool(diverges),
        nu0_edge_limit=float(nu0_edge_limit),
        regime_boundary=True,
        description=description,
    )


@dataclass(frozen=True)
class RegimeConsistencyReport:
    """Numerical cross-check of the three Requirement-8 regimes.

    Produced by `verify_regime_consistency`. All `*_ok` fields are True
    iff the corresponding numerical check passed within its tolerance.

    Attributes
    ----------
    m_sq, p_abs : float
        The inputs.
    kappa_samples : np.ndarray
        Geometrically spaced sample values of kappa in (0, m^2 / 2).
    decoupling_ok : bool
        True iff the smallest-kappa Sigma_vac agrees with the analytic
        decoupling limit sigma^2 * I within `decoupling_tol`.
    decoupling_residual : float
        max |Sigma_vac(kappa_min) - sigma^2 I|.
    expansion_ok : bool
        True iff the order-2 small-kappa expansion agrees with the exact
        Sigma_vac at the smallest sampled kappa to within a tolerance
        scaling with kappa^3.
    expansion_residual : float
        max |Sigma_vac(kappa_min) - sigma_vac_series(kappa_min, order=2)|.
    edge_monotone_ok : bool
        True iff nu_0(kappa) is strictly increasing in kappa across the
        sample grid, as expected from nu_0 = 1 / (2 sqrt(|p|^2 + m^2
        - 2 kappa)).
    edge_growth_ok : bool
        True iff nu_0 at the largest sampled kappa (inside but near the
        edge) is substantially larger than nu_0 at the smallest sampled
        kappa. At |p| = 0 the ratio tends to infinity; we only require a
        large finite ratio here.
    nu0_min : float
        nu_0 at the smallest sampled kappa.
    nu0_max : float
        nu_0 at the largest sampled kappa.
    """

    m_sq: float
    p_abs: float
    kappa_samples: np.ndarray
    decoupling_ok: bool
    decoupling_residual: float
    expansion_ok: bool
    expansion_residual: float
    edge_monotone_ok: bool
    edge_growth_ok: bool
    nu0_min: float
    nu0_max: float


def verify_regime_consistency(
    m_sq: float,
    p_abs: float,
    n_kappa: int = 20,
    decoupling_tol: float = 1e-6,
) -> RegimeConsistencyReport:
    """Numerically cross-check the three Requirement-8 regimes.

    For a geometrically spaced grid of kappa values in (kappa_min,
    kappa_max) with kappa_min ~ 1e-10 * m^2 and kappa_max ~ 0.49 * m^2:

      1. Decoupling limit (Requirement 8.1). Compute Sigma_vac at
         kappa_min and compare against `decoupling_limit(m_sq, p_abs)`
         within `decoupling_tol`.
      2. Small-kappa expansion (Requirement 8.2). Compare the exact
         Sigma_vac at kappa_min against the order-2 series; expect
         agreement at the level of kappa_min^3 / m^6.
      3. Stability edge (Requirement 8.3). Check that nu_0 is strictly
         increasing in kappa and grows large as kappa approaches the
         edge from below.

    Requires m^2 > 0 and |p| >= 0. n_kappa must be >= 4 so the grid has
    enough points for a meaningful monotonicity check.
    """
    try:
        m_sq_f = float(m_sq)
        p_abs_f = float(p_abs)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"m_sq and p_abs must be real scalars; got "
            f"m_sq={m_sq!r}, p_abs={p_abs!r}"
        ) from exc
    if not (np.isfinite(m_sq_f) and np.isfinite(p_abs_f)):
        raise ValueError(
            f"m_sq and p_abs must be finite; got m_sq={m_sq_f}, p_abs={p_abs_f}"
        )
    if m_sq_f <= 0.0:
        raise ValueError(
            f"verify_regime_consistency requires m_sq > 0, got m_sq={m_sq_f}"
        )
    if p_abs_f < 0.0:
        raise ValueError(f"p_abs must be >= 0, got {p_abs_f}")
    if int(n_kappa) < 4:
        raise ValueError(f"n_kappa must be >= 4, got {n_kappa}")

    kappa_min = 1e-10 * m_sq_f
    kappa_max = 0.49 * m_sq_f  # strictly inside (0, m^2 / 2)
    kappa_samples = np.geomspace(kappa_min, kappa_max, int(n_kappa))

    # --- 8.1: decoupling limit ---
    limit = decoupling_limit(m_sq_f, p_abs_f)
    sigma_at_min = compute_vacuum_covariance(m_sq_f, kappa_min, p_abs_f)
    decoupling_residual = float(
        np.max(np.abs(sigma_at_min - limit.sigma_vac_limit))
    )
    decoupling_ok = bool(decoupling_residual <= decoupling_tol)

    # --- 8.2: order-2 expansion vs exact at kappa_min ---
    # Residual is O(epsilon^3) where epsilon = kappa / (|p|^2 + m^2).
    E_sq = p_abs_f * p_abs_f + m_sq_f
    eps_min = kappa_min / E_sq
    sigma_series = small_kappa_expansion(
        m_sq_f, kappa_min, p_abs_f, order=2
    ).sigma_vac_series
    expansion_residual = float(np.max(np.abs(sigma_at_min - sigma_series)))
    # Tolerance: 10 * sigma^2 * epsilon^3 is a comfortable envelope for the
    # truncation error, with a floor at 1e-15 for machine-precision noise
    # when epsilon is essentially zero.
    expansion_tol = max(
        10.0 * limit.sigma_sq * (eps_min ** 3), 1e-15
    )
    expansion_ok = bool(expansion_residual <= expansion_tol)

    # --- 8.3: monotonicity and growth of nu_0 approaching the edge ---
    nu0_values = np.array(
        [mode_variances(m_sq_f, float(k), p_abs_f)[0] for k in kappa_samples]
    )
    diffs = np.diff(nu0_values)
    edge_monotone_ok = bool(np.all(diffs > 0.0))
    nu0_min_val = float(nu0_values[0])
    nu0_max_val = float(nu0_values[-1])
    # At |p| = 0 the ratio nu0_max / nu0_min is
    #   sqrt(m^2 / (m^2 - 2 kappa_max)) ~ sqrt(1 / 0.02) ~ 7
    # for kappa_max = 0.49 m^2; this is the Requirement-8.3 divergence
    # signature. At |p| > 0 the k = 0 mode stays gapped and nu_0
    # approaches the finite limit 1 / (2 sqrt(|p|^2 + m^2 - 2 kappa_max)),
    # so the ratio is bounded by sqrt((|p|^2 + m^2) / (|p|^2 + m^2
    # - 2 kappa_max)) and we only demand strict monotonic growth.
    if p_abs_f == 0.0:
        edge_growth_ok = bool(nu0_max_val >= 3.0 * nu0_min_val)
    else:
        edge_growth_ok = bool(nu0_max_val > nu0_min_val)

    return RegimeConsistencyReport(
        m_sq=m_sq_f,
        p_abs=p_abs_f,
        kappa_samples=kappa_samples,
        decoupling_ok=decoupling_ok,
        decoupling_residual=decoupling_residual,
        expansion_ok=expansion_ok,
        expansion_residual=expansion_residual,
        edge_monotone_ok=edge_monotone_ok,
        edge_growth_ok=edge_growth_ok,
        nu0_min=nu0_min_val,
        nu0_max=nu0_max_val,
    )


__all__ = [
    "VacuumCovarianceDiagnostics",
    "compute_vacuum_covariance",
    "vacuum_covariance_diagnostics",
    "mode_masses_sq",
    "mode_frequencies",
    "mode_variances",
    "DecouplingLimit",
    "SmallKappaExpansion",
    "StabilityEdgeBehavior",
    "RegimeConsistencyReport",
    "decoupling_limit",
    "small_kappa_expansion",
    "stability_edge_behavior",
    "verify_regime_consistency",
]


# ----------------------------------------------------------------------
# Self-check / CLI
# ----------------------------------------------------------------------


if __name__ == "__main__":
    print("verification.vacuum_propagator")
    print("-" * 60)

    # --- Worked example from design.md / Example 2 --------------------
    # m^2 = 1, kappa = 0.1, |p| = 0
    # mu_0^2 = 0.8, mu_1^2 = 1.1
    # nu_0 = 1 / (2 sqrt(0.8)) ~ 0.5590
    # nu_1 = 1 / (2 sqrt(1.1)) ~ 0.4767
    # off-diagonal = (nu_0 - nu_1) / 3 ~ 0.0274 > 0
    diag_example = vacuum_covariance_diagnostics(
        m_sq=1.0, kappa=0.1, p_abs=0.0
    )
    print()
    print("Worked example (design.md Example 2): m^2 = 1, kappa = 0.1, |p| = 0")
    print(f"  mu_0^2 = {diag_example.mu_sq[0]:.4f}, "
          f"mu_1^2 = {diag_example.mu_sq[1]:.4f}")
    print(f"  omega_0 = {diag_example.omega[0]:.4f}, "
          f"omega_1 = {diag_example.omega[1]:.4f}")
    print(f"  nu_0 = {diag_example.nu[0]:.4f}, "
          f"nu_1 = {diag_example.nu[1]:.4f}")
    print(f"  diagonal d     = {diag_example.diagonal:.4f}")
    print(f"  off-diagonal o = {diag_example.off_diagonal:.4f}")
    print(f"  max |Im(Sigma_vac)| = {diag_example.max_imag:.3e}")
    np.set_printoptions(precision=4, suppress=True)
    print("  Sigma_vac =")
    print(diag_example.sigma_vac)
    np.set_printoptions()

    assert diag_example.off_diagonal > 0.0, (
        "expected positive off-diagonal on stable branch, got "
        f"{diag_example.off_diagonal}"
    )
    # Exact numeric sanity against the worked example figures.
    expected_off = (1.0 / (2.0 * np.sqrt(0.8)) - 1.0 / (2.0 * np.sqrt(1.1))) / 3.0
    assert np.isclose(
        diag_example.off_diagonal, expected_off, atol=1e-12
    ), (
        f"worked-example off-diagonal mismatch: got "
        f"{diag_example.off_diagonal}, expected {expected_off}"
    )
    assert np.isclose(
        diag_example.off_diagonal, 0.02744, atol=5e-5
    ), (
        "worked-example off-diagonal should match design.md figure "
        f"~0.0274; got {diag_example.off_diagonal}"
    )

    # --- Decoupling limit kappa -> 0: Sigma_vac -> sigma^2 * I ---------
    # For kappa very small (but still positive, since kappa > 0 is required),
    # all three modes have mass^2 ~ m^2 and frequency ~ sqrt(|p|^2 + m^2),
    # so Sigma_vac -> (1 / (2 sqrt(|p|^2 + m^2))) * I. Check this at
    # |p| = 0 with m^2 = 1 and kappa = 1e-10.
    diag_decouple = vacuum_covariance_diagnostics(
        m_sq=1.0, kappa=1e-10, p_abs=0.0
    )
    expected_sigma_sq = 1.0 / (2.0 * np.sqrt(1.0))  # = 0.5
    print()
    print(
        "Decoupling limit (kappa = 1e-10, m^2 = 1, |p| = 0): Sigma_vac should "
        "approach sigma^2 * I with sigma^2 = 1 / (2 sqrt(m^2)) = 0.5"
    )
    print(f"  diagonal d     = {diag_decouple.diagonal:.12f} (expected ~0.5)")
    print(
        f"  off-diagonal o = {diag_decouple.off_diagonal:.3e} "
        "(expected ~0, but strictly positive on stable branch)"
    )
    assert np.isclose(
        diag_decouple.diagonal, expected_sigma_sq, atol=1e-8
    ), (
        f"decoupling-limit diagonal should be {expected_sigma_sq}, got "
        f"{diag_decouple.diagonal}"
    )
    assert diag_decouple.off_diagonal > 0.0, (
        "stable-branch off-diagonal should remain strictly positive even "
        "for tiny kappa"
    )
    assert diag_decouple.off_diagonal < 1e-9, (
        "decoupling-limit off-diagonal should be tiny, got "
        f"{diag_decouple.off_diagonal}"
    )
    # Full matrix should be within 1e-9 of sigma^2 * I for kappa = 1e-10.
    assert np.allclose(
        diag_decouple.sigma_vac, expected_sigma_sq * I3, atol=1e-9
    ), (
        "decoupling-limit Sigma_vac should be very close to sigma^2 * I"
    )

    # --- Input validation spot checks ---------------------------------
    for bad_args, description in [
        ((0.1, 0.1, 0.0), "m^2 <= 2 kappa (stability violated)"),
        ((1.0, 0.5, 0.0), "m^2 = 2 kappa (boundary of stability)"),
        ((1.0, -0.1, 0.0), "kappa <= 0 (unphysical coupling)"),
        ((1.0, 0.0, 0.0), "kappa = 0 (decoupled, must be strictly > 0)"),
        ((1.0, 0.1, -0.5), "|p| < 0 (negative momentum magnitude)"),
    ]:
        raised = False
        try:
            compute_vacuum_covariance(*bad_args)
        except ValueError:
            raised = True
        assert raised, (
            f"compute_vacuum_covariance{bad_args} should have raised "
            f"ValueError ({description})"
        )

    # --- Structural guarantees on a nontrivial stable point -----------
    # At m^2 = 4, kappa = 1, |p| = 0.5, all checks should hold.
    sigma_generic = compute_vacuum_covariance(m_sq=4.0, kappa=1.0, p_abs=0.5)
    assert is_c3_circulant_symmetric(sigma_generic), (
        "generic Sigma_vac should be C_3-circulant symmetric"
    )
    assert np.allclose(sigma_generic, sigma_generic.T, atol=TOL), (
        "generic Sigma_vac should be symmetric"
    )
    # Positive definite on the stable branch (all entries positive and
    # structure correct, but confirm eigenvalues directly).
    generic_eigs = np.linalg.eigvalsh(sigma_generic)
    assert np.min(generic_eigs) > 0.0, (
        f"generic Sigma_vac should be PD, got eigenvalues {generic_eigs}"
    )

    # --- Regime analysis (task 9.1 / Requirement 8) -------------------
    print()
    print("Regime analysis (task 9.1 / Requirement 8):")

    # 8.1: analytic decoupling limit at |p| = 0 with m^2 = 1.
    limit = decoupling_limit(m_sq=1.0, p_abs=0.0)
    print(
        f"  decoupling_limit(m^2=1, |p|=0): sigma^2 = {limit.sigma_sq:.6f}, "
        f"Sigma_vac_limit diag = {np.diag(limit.sigma_vac_limit)}"
    )
    assert np.isclose(limit.sigma_sq, 0.5, atol=1e-12), (
        f"decoupling sigma^2 should be 0.5, got {limit.sigma_sq}"
    )
    assert np.allclose(limit.sigma_vac_limit, 0.5 * I3, atol=1e-12), (
        "decoupling Sigma_vac_limit should be 0.5 * I"
    )

    # 8.2: order-1 expansion recovers the leading o ~ sigma^2 * epsilon / 2.
    exp1 = small_kappa_expansion(m_sq=1.0, kappa=1e-4, p_abs=0.0, order=1)
    expected_o_leading = exp1.sigma_sq * 0.5 * exp1.epsilon
    print(
        f"  small_kappa_expansion(m^2=1, kappa=1e-4, |p|=0, order=1): "
        f"epsilon = {exp1.epsilon:.3e}, o_series = {exp1.off_diagonal_series:.3e}, "
        f"expected leading = {expected_o_leading:.3e}"
    )
    assert np.isclose(
        exp1.off_diagonal_series, expected_o_leading, atol=1e-18
    ), (
        "order-1 off-diagonal series should equal sigma^2 * epsilon / 2"
    )
    assert np.isclose(exp1.diagonal_series, exp1.sigma_sq, atol=1e-18), (
        "order-1 diagonal series should equal sigma^2 (no O(eps) correction)"
    )

    # 8.2: order-2 expansion vs exact compute_vacuum_covariance.
    exp2 = small_kappa_expansion(m_sq=1.0, kappa=1e-3, p_abs=0.0, order=2)
    sigma_exact = compute_vacuum_covariance(m_sq=1.0, kappa=1e-3, p_abs=0.0)
    max_exp_dev = float(np.max(np.abs(sigma_exact - exp2.sigma_vac_series)))
    print(
        f"  order-2 expansion vs exact at kappa=1e-3: max deviation "
        f"= {max_exp_dev:.3e} (expected ~ epsilon^3 = {exp2.epsilon**3:.3e})"
    )
    # Residual should be bounded by a small multiple of sigma^2 * eps^3.
    assert max_exp_dev <= 10.0 * exp2.sigma_sq * exp2.epsilon ** 3, (
        f"order-2 expansion residual {max_exp_dev} exceeds expected bound "
        f"{10.0 * exp2.sigma_sq * exp2.epsilon ** 3}"
    )

    # 8.3/8.4: stability edge description at |p| = 0 and at |p| = 1.
    edge_zero = stability_edge_behavior(m_sq=1.0, p_abs=0.0)
    print(
        f"  stability_edge_behavior(m^2=1, |p|=0): kappa_edge "
        f"= {edge_zero.kappa_edge:.3f}, diverges = "
        f"{edge_zero.diverges_at_zero_momentum}, nu0_limit = "
        f"{edge_zero.nu0_edge_limit}"
    )
    assert edge_zero.kappa_edge == 0.5
    assert edge_zero.diverges_at_zero_momentum is True
    assert edge_zero.nu0_edge_limit == float("inf")
    assert edge_zero.regime_boundary is True

    edge_nonzero = stability_edge_behavior(m_sq=1.0, p_abs=1.0)
    assert edge_nonzero.diverges_at_zero_momentum is False
    assert np.isclose(edge_nonzero.nu0_edge_limit, 0.5, atol=1e-12), (
        "at |p| = 1, nu_0 at the edge should be 1 / (2 |p|) = 0.5"
    )

    # 8.4: compute_vacuum_covariance refuses at and past the edge.
    for kappa_bad, desc in (
        (0.5, "kappa = m^2 / 2 (on the edge)"),
        (0.6, "kappa > m^2 / 2 (past the edge)"),
    ):
        raised = False
        try:
            compute_vacuum_covariance(m_sq=1.0, kappa=kappa_bad, p_abs=0.0)
        except ValueError:
            raised = True
        assert raised, f"compute_vacuum_covariance should refuse at {desc}"

    # Combined numerical regime consistency check at |p| = 0 and |p| = 0.7.
    for p_test in (0.0, 0.7):
        report = verify_regime_consistency(m_sq=1.0, p_abs=p_test, n_kappa=25)
        print(
            f"  verify_regime_consistency(m^2=1, |p|={p_test}): "
            f"decoupling_ok={report.decoupling_ok} "
            f"(residual={report.decoupling_residual:.3e}), "
            f"expansion_ok={report.expansion_ok} "
            f"(residual={report.expansion_residual:.3e}), "
            f"edge_monotone_ok={report.edge_monotone_ok}, "
            f"edge_growth_ok={report.edge_growth_ok}, "
            f"nu0 range=[{report.nu0_min:.3e}, {report.nu0_max:.3e}]"
        )
        assert report.decoupling_ok, (
            f"decoupling limit check failed at |p|={p_test}: residual "
            f"{report.decoupling_residual}"
        )
        assert report.expansion_ok, (
            f"small-kappa expansion check failed at |p|={p_test}: residual "
            f"{report.expansion_residual}"
        )
        assert report.edge_monotone_ok, (
            f"nu_0 should be strictly increasing in kappa at |p|={p_test}"
        )
        assert report.edge_growth_ok, (
            f"nu_0 should grow substantially toward the edge at |p|={p_test}"
        )

    print()
    print("all vacuum_propagator self-checks passed")
