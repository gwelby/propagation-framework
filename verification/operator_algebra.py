"""
Foundational canonical operator algebra for the God Equation Path B / Family C
and the exact Z_3 vacuum propagator notes.

Role
----
This module is the single source of truth for the 3x3 channel-space algebra
shared by:

  * derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md
    (canonical Family C no-go)
  * derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md
    (exact Z_3 vacuum propagator)

Every downstream Python module in `verification/` (family_c_kernels,
support_constraint, gaussian_factorization, vacuum_propagator,
escape_comparison, consistency_check, guardrail_check, ...) imports its
matrices, projectors, and spectral data from here so the two notes cannot
drift apart at the numerical level.

Truth sources
-------------
The canonical closure object is

    T_sym = (1/2) * ( S_bar + S_bar^2 )

with the cyclic shift

    S_bar[e_j] = e_{j+1 mod 3},   S_bar = [[0,0,1],[1,0,0],[0,1,0]].

The exact third power is

    T_sym^3 = (1/4) * I + (3/8) * S_bar + (3/8) * S_bar^2,

with diagonal 1/4 and off-diagonal 3/8. Its spectral decomposition is

    T_sym^3 = 1 * P0  -  (1/8) * Q,

where

    P0 = (1/3) * 1 * 1^T     (symmetric-mode projector)
    Q  = I - P0              (degenerate (-1/8) eigenspace projector, rank 2).

Eigenvalues:
    T_sym   has spectrum {  1, -1/2, -1/2 }
    T_sym^3 has spectrum {  1, -1/8, -1/8 }

Non-canonicity of any Q-sector basis split
------------------------------------------
The -1/8 eigenspace of T_sym^3 (equivalently the -1/2 eigenspace of T_sym)
is two-dimensional and degenerate. There is NO canonical split of Q into
one-dimensional projectors P_1, P_2. Any such split requires choosing a
direction inside the Q-sector, which is an extra basis hypothesis that is
not operator-native.

Downstream code that wants a "channel projector" triple therefore MUST
declare that extra hypothesis explicitly; this module exposes only the
canonical, operator-native data.

Self-check
----------
All assertions listed in the Family C / vacuum note task specs are executed
at module import time, so

    import verification.operator_algebra  # noqa

doubles as a numerical regression test of the canonical algebra. Run this
file directly for a concise human-readable summary.
"""

from __future__ import annotations

import numpy as np

# ----------------------------------------------------------------------
# Tolerances and shared conventions
# ----------------------------------------------------------------------

# Matches the tolerance used elsewhere in verification/ (see
# counterexample_search.py).
TOL: float = 1e-12

# ----------------------------------------------------------------------
# Core matrices: cyclic shift, its square, identity
# ----------------------------------------------------------------------

# S_bar acts on the standard basis as S_bar e_j = e_{j+1 mod 3}.
# Matrix form: [[0,0,1],[1,0,0],[0,1,0]].
S_bar: np.ndarray = np.array(
    [[0.0, 0.0, 1.0],
     [1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0]],
    dtype=float,
)

S_bar_sq: np.ndarray = S_bar @ S_bar

I3: np.ndarray = np.eye(3)

# Sanity: S_bar is a genuine 3-cycle.
assert np.allclose(S_bar @ S_bar @ S_bar, I3, atol=TOL), \
    "S_bar is not a 3-cycle: S_bar^3 != I"
assert np.allclose(S_bar_sq, S_bar.T, atol=TOL), \
    "S_bar^2 should equal S_bar.T for a real cyclic shift"

# ----------------------------------------------------------------------
# Canonical closure operator T_sym and its third power
# ----------------------------------------------------------------------

T_sym: np.ndarray = 0.5 * (S_bar + S_bar_sq)
T_sym_cu: np.ndarray = np.linalg.matrix_power(T_sym, 3)

# T_sym must be symmetric by construction.
assert np.allclose(T_sym, T_sym.T, atol=TOL), "T_sym is not symmetric"

# Exact entries of T_sym^3: diagonal 1/4, off-diagonal 3/8.
_expected_T_sym_cu = (
    0.25 * I3
    + (3.0 / 8.0) * S_bar
    + (3.0 / 8.0) * S_bar_sq
)
assert np.allclose(T_sym_cu, _expected_T_sym_cu, atol=TOL), (
    "T_sym^3 disagrees with the closed form "
    "(1/4) I + (3/8) S_bar + (3/8) S_bar^2"
)

_diag_T_sym_cu = np.diag(T_sym_cu)
assert np.allclose(_diag_T_sym_cu, 0.25, atol=TOL), (
    f"T_sym^3 diagonal is {_diag_T_sym_cu}, expected all 1/4"
)

# Off-diagonal entries: mask out the diagonal and check every remaining
# entry equals 3/8.
_offdiag_mask = ~np.eye(3, dtype=bool)
_offdiag_T_sym_cu = T_sym_cu[_offdiag_mask]
assert np.allclose(_offdiag_T_sym_cu, 3.0 / 8.0, atol=TOL), (
    f"T_sym^3 off-diagonal entries are {_offdiag_T_sym_cu}, expected all 3/8"
)

# ----------------------------------------------------------------------
# Canonical spectral projectors P0 (symmetric mode) and Q (degenerate)
# ----------------------------------------------------------------------

P0: np.ndarray = np.ones((3, 3)) / 3.0
Q: np.ndarray = I3 - P0

# P0 + Q = I, P0 Q = 0, P0^2 = P0, Q^2 = Q  (to machine precision).
assert np.allclose(P0 + Q, I3, atol=TOL), "P0 + Q != I"
assert np.allclose(P0 @ Q, np.zeros((3, 3)), atol=TOL), "P0 @ Q != 0"
assert np.allclose(Q @ P0, np.zeros((3, 3)), atol=TOL), "Q @ P0 != 0"
assert np.allclose(P0 @ P0, P0, atol=TOL), "P0 is not idempotent (P0^2 != P0)"
assert np.allclose(Q @ Q, Q, atol=TOL), "Q is not idempotent (Q^2 != Q)"

# Ranks: P0 is rank 1 (symmetric mode), Q is rank 2 (degenerate sector).
assert np.linalg.matrix_rank(P0, tol=TOL) == 1, "P0 should have rank 1"
assert np.linalg.matrix_rank(Q, tol=TOL) == 2, "Q should have rank 2"

# Spectral identity: T_sym^3 = 1 * P0 - (1/8) * Q.
assert np.allclose(T_sym_cu, P0 - (1.0 / 8.0) * Q, atol=TOL), (
    "T_sym^3 does not equal 1*P0 - (1/8)*Q"
)

# ----------------------------------------------------------------------
# Spectra of T_sym and T_sym^3
# ----------------------------------------------------------------------

# T_sym has eigenvalues { 1, -1/2, -1/2 }.
_eigs_T = np.sort(np.linalg.eigvalsh(T_sym))
_expected_eigs_T = np.sort(np.array([1.0, -0.5, -0.5]))
assert np.allclose(_eigs_T, _expected_eigs_T, atol=TOL), (
    f"T_sym eigenvalues are {_eigs_T}, expected {{1, -1/2, -1/2}}"
)

# T_sym^3 has eigenvalues { 1, -1/8, -1/8 }.
_eigs_T_cu = np.sort(np.linalg.eigvalsh(T_sym_cu))
_expected_eigs_T_cu = np.sort(np.array([1.0, -1.0 / 8.0, -1.0 / 8.0]))
assert np.allclose(_eigs_T_cu, _expected_eigs_T_cu, atol=TOL), (
    f"T_sym^3 eigenvalues are {_eigs_T_cu}, expected {{1, -1/8, -1/8}}"
)

# ----------------------------------------------------------------------
# Coupling matrix M = S_bar + S_bar^2 and its DFT diagonalization
# ----------------------------------------------------------------------
#
# The coupling matrix M appears directly in the linearized Z_3-extended
# equations of motion (z3_extended_propagation_lagrangian.md Section 4.2,
# god_eq_pf_vacuum_propagator_exact_2026-04-01.md Section 2):
#
#     (Box + m^2) delta_chi_j = kappa ( delta_chi_{j-1} + delta_chi_{j+1} )
#
# which in matrix form reads (Box + m^2) f = kappa * M * f with
#
#     M = S_bar + S_bar^2 = [[0,1,1],[1,0,1],[1,1,0]].
#
# M is the real symmetric circulant with zero diagonal and unit off-diagonal.
# Its eigenvalues are { 2, -1, -1 }, diagonalized exactly by the 3x3 unitary
# discrete Fourier transform
#
#     F[j,k] = (1/sqrt(3)) * omega^(j*k),   omega = exp(2*pi*i/3)
#
# via F^dagger @ M @ F = diag(2, -1, -1) with the k=0 (symmetric) mode on
# eigenvalue 2 and k=1, k=2 on the degenerate -1 eigenspace.

M: np.ndarray = S_bar + S_bar_sq

# Symmetric, zero diagonal, unit off-diagonal.
assert np.allclose(M, M.T, atol=TOL), "M is not symmetric"
assert np.allclose(np.diag(M), 0.0, atol=TOL), (
    f"M diagonal is {np.diag(M)}, expected all zeros"
)
_M_offdiag = M[_offdiag_mask]
assert np.allclose(_M_offdiag, 1.0, atol=TOL), (
    f"M off-diagonal entries are {_M_offdiag}, expected all 1"
)

# Spectrum: { 2, -1, -1 }.
_eigs_M = np.sort(np.linalg.eigvalsh(M))
_expected_eigs_M = np.sort(np.array([2.0, -1.0, -1.0]))
assert np.allclose(_eigs_M, _expected_eigs_M, atol=TOL), (
    f"M eigenvalues are {_eigs_M}, expected {{2, -1, -1}}"
)

# 3x3 unitary DFT matrix F with F[j,k] = (1/sqrt(3)) * omega^(j*k).
_omega: complex = np.exp(2.0j * np.pi / 3.0)
_jk = np.outer(np.arange(3), np.arange(3))
F: np.ndarray = (_omega ** _jk) / np.sqrt(3.0)

# F is unitary: F @ F^dagger = F^dagger @ F = I.
_F_dag = F.conj().T
assert np.allclose(F @ _F_dag, I3, atol=TOL), "F @ F^dagger != I (F not unitary)"
assert np.allclose(_F_dag @ F, I3, atol=TOL), "F^dagger @ F != I (F not unitary)"

# DFT diagonalization: F^dagger @ M @ F = diag(2, -1, -1).
# The k=0 column of F is the symmetric mode (eigenvalue 2); k=1, k=2 span
# the degenerate -1 eigenspace.
_M_diag = _F_dag @ M @ F
_expected_M_diag = np.diag([2.0 + 0.0j, -1.0 + 0.0j, -1.0 + 0.0j])
# Diagonal entries must match exactly up to machine precision, and the
# imaginary part must vanish (M is real symmetric).
assert np.allclose(np.diag(_M_diag), np.diag(_expected_M_diag), atol=TOL), (
    f"diag(F^dagger M F) = {np.diag(_M_diag)}, expected (2, -1, -1)"
)
assert np.max(np.abs(np.imag(np.diag(_M_diag)))) < TOL, (
    "Diagonal of F^dagger M F has nonzero imaginary part"
)
# Off-diagonal residual of F^dagger M F must vanish to machine precision.
_M_diag_offdiag = _M_diag[_offdiag_mask]
assert np.max(np.abs(_M_diag_offdiag)) < 1e-10, (
    f"F^dagger M F off-diagonal residual {np.max(np.abs(_M_diag_offdiag))} "
    "exceeds machine-precision tolerance"
)

# ----------------------------------------------------------------------
# Family A escape covariance Sigma_escape = (A A^T)^{-1}, A = T_sym^3
# ----------------------------------------------------------------------
#
# This block installs the reference Family A escape covariance from
# derivations/god_eq_path_b_family_a_intensity_audit_2026-04-01.md.
#
# With A = T_sym^3 (diagonal 1/4, off-diagonal 3/8), the Gram matrix
#
#     A A^T = [[22/64, 21/64, 21/64],
#              [21/64, 22/64, 21/64],
#              [21/64, 21/64, 22/64]]
#
# is C_3-circulant symmetric with diagonal 22/64 = 11/32 and off-diagonal
# 21/64. Its inverse
#
#     Sigma_escape = (A A^T)^{-1} = [[ 43, -21, -21],
#                                    [-21,  43, -21],
#                                    [-21, -21,  43]]
#
# is exactly integer-valued (det(A A^T) = 1/4096 and adj(A A^T) has integer
# entries after the scale cancellation), is C_3-circulant symmetric, and
# has strictly NEGATIVE off-diagonal entries. This is the covariance that
# would whiten the Family A closure amplitudes to iid standard normals --
# the Gaussian escape hatch identified in the audit that makes the
# Family A no-go a restricted rather than a universal result.
#
# The whitening identity
#
#     A @ Sigma_escape @ A^T = I
#
# holds exactly in rationals and to machine precision in floating point.
# It is also verified at module import time below.
#
# Sign contrast with Sigma_vac: the exact free linearized Z_3 vacuum
# covariance (god_eq_pf_vacuum_propagator_exact_2026-04-01.md) has
# POSITIVE off-diagonals on the stable branch, so the natural vacuum
# points opposite to Sigma_escape in C_3-circulant sign space. That
# contrast is the content of Requirement 7.3.

AA_T: np.ndarray = T_sym_cu @ T_sym_cu.T

# Exact entries: AA^T is C_3-circulant symmetric with diagonal 22/64 and
# off-diagonal 21/64. Note: derivations/god_eq_path_b_family_a_intensity_audit
# reports the off-diagonal explicitly as 21/64 (via the row inner product
# a . b = 21/64); the diagonal 22/64 follows from a . a = (1/4)^2 + 2*(3/8)^2.
_diag_AA_T = np.diag(AA_T)
assert np.allclose(_diag_AA_T, 22.0 / 64.0, atol=TOL), (
    f"A A^T diagonal is {_diag_AA_T}, expected all 22/64 = 11/32"
)
_offdiag_AA_T = AA_T[_offdiag_mask]
assert np.allclose(_offdiag_AA_T, 21.0 / 64.0, atol=TOL), (
    f"A A^T off-diagonal entries are {_offdiag_AA_T}, expected all 21/64"
)

Sigma_escape: np.ndarray = np.linalg.inv(AA_T)


def is_c3_circulant_symmetric(M: np.ndarray, tol: float = TOL) -> bool:
    """
    Return True iff M is a real C_3-circulant symmetric 3x3 matrix,
    i.e. has the form a * I + b * (S_bar + S_bar^2) with real a, b.

    Equivalently: M is real, 3x3, symmetric, has equal diagonal entries,
    and has equal off-diagonal entries, all to tolerance `tol`.

    Parameters
    ----------
    M : np.ndarray
        Candidate matrix.
    tol : float, optional
        Absolute tolerance for the equality checks. Defaults to module TOL.

    Returns
    -------
    bool
        True iff M is real symmetric, 3x3, with constant diagonal and
        constant off-diagonal.
    """
    arr = np.asarray(M)
    if arr.shape != (3, 3):
        return False
    # Real-valued (no nontrivial imaginary part).
    if np.iscomplexobj(arr) and np.max(np.abs(np.imag(arr))) > tol:
        return False
    arr = np.real(arr)
    # Symmetric.
    if not np.allclose(arr, arr.T, atol=tol):
        return False
    diag = np.diag(arr)
    if not np.allclose(diag, diag[0], atol=tol):
        return False
    offdiag_mask = ~np.eye(3, dtype=bool)
    off = arr[offdiag_mask]
    if not np.allclose(off, off[0], atol=tol):
        return False
    return True


# Sigma_escape is C_3-circulant symmetric.
assert is_c3_circulant_symmetric(Sigma_escape, tol=TOL), (
    "Sigma_escape = inv(A A^T) is not C_3-circulant symmetric"
)

# Off-diagonal entries of Sigma_escape are strictly negative (anti-correlated
# channels). This is the sign contrast with Sigma_vac used in Requirement 7.3.
_offdiag_Sigma_escape = Sigma_escape[_offdiag_mask]
assert np.all(_offdiag_Sigma_escape < -TOL), (
    f"Sigma_escape off-diagonal entries {_offdiag_Sigma_escape} are not "
    "strictly negative"
)

# Exact integer entries after inversion: diag = 43, off-diag = -21.
assert np.allclose(np.diag(Sigma_escape), 43.0, atol=1e-10), (
    f"Sigma_escape diagonal is {np.diag(Sigma_escape)}, expected all 43"
)
assert np.allclose(_offdiag_Sigma_escape, -21.0, atol=1e-10), (
    f"Sigma_escape off-diagonal entries are {_offdiag_Sigma_escape}, "
    "expected all -21"
)

# Whitening property: A @ Sigma_escape @ A^T = I to machine precision.
_whitened = T_sym_cu @ Sigma_escape @ T_sym_cu.T
assert np.allclose(_whitened, I3, atol=1e-10), (
    "Whitening identity A @ Sigma_escape @ A^T = I failed; got\n"
    f"{_whitened}"
)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

__all__ = [
    "TOL",
    "I3",
    "S_bar",
    "S_bar_sq",
    "T_sym",
    "T_sym_cu",
    "P0",
    "Q",
    "M",
    "F",
    "AA_T",
    "Sigma_escape",
    "is_c3_circulant_symmetric",
]


# ----------------------------------------------------------------------
# CLI summary
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("verification.operator_algebra")
    print("-" * 60)
    print("S_bar (cyclic shift):")
    print(S_bar)
    print()
    print("T_sym = (1/2)(S_bar + S_bar^2):")
    print(T_sym)
    print()
    print("T_sym^3 (diagonal 1/4, off-diagonal 3/8):")
    print(T_sym_cu)
    print()
    print(f"eig(T_sym)   = {np.sort(np.linalg.eigvalsh(T_sym))}")
    print(f"eig(T_sym^3) = {np.sort(np.linalg.eigvalsh(T_sym_cu))}")
    print()
    print("Projectors: P0 (symmetric mode, rank 1), Q = I - P0 (rank 2).")
    print("Q sector is degenerate; any split into one-dimensional projectors")
    print("is noncanonical and must be declared as an extra hypothesis.")
    print()
    print("Coupling matrix M = S_bar + S_bar^2 (zero diagonal, unit off-diag):")
    print(M)
    print()
    print(f"eig(M) = {np.sort(np.linalg.eigvalsh(M))}   (expected {{2, -1, -1}})")
    print()
    print("3x3 unitary DFT matrix F (F[j,k] = omega^(j*k) / sqrt(3)):")
    np.set_printoptions(precision=4, suppress=True)
    print(F)
    np.set_printoptions()
    print()
    print("F^dagger @ M @ F (should be diag(2, -1, -1) up to machine eps):")
    np.set_printoptions(precision=4, suppress=True)
    print(F.conj().T @ M @ F)
    np.set_printoptions()
    print()
    print("Family A escape covariance:")
    print("  A = T_sym^3; A A^T has diagonal 22/64 and off-diagonal 21/64:")
    print(AA_T)
    print()
    print("  Sigma_escape = inv(A A^T)  (diag 43, off-diag -21, NEGATIVE):")
    print(Sigma_escape)
    print(
        f"  is_c3_circulant_symmetric(Sigma_escape) = "
        f"{is_c3_circulant_symmetric(Sigma_escape)}"
    )
    off = Sigma_escape[~np.eye(3, dtype=bool)]
    print(f"  off-diagonal entries {np.unique(off)} are strictly negative")
    print()
    print("  Whitening identity A @ Sigma_escape @ A^T (should be I):")
    np.set_printoptions(precision=4, suppress=True)
    print(T_sym_cu @ Sigma_escape @ T_sym_cu.T)
    np.set_printoptions()
    print()
    print("all operator_algebra checks passed")
