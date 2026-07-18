#!/usr/bin/env python3
"""
D1: Zenczykowski quark Koide formula fit against PDG masses.
Source-correct square-root mass formula; versioned by output artifacts, not this docstring.

Zenczykowski 2013 (arXiv:1301.4143, PRD 87, 077302), Eq. (4):
    sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))

Therefore:
    m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))^2

The square root structure is essential to the Koide relation:
    Q = sum(m_i) / (sum(sqrt(m_i)))^2 = (1 + k^2) / 3
    k=1  ->  Q = 2/3  (Koide's exact value for charged leptons)

v3 error: implemented m_j = M * (1 + sqrt(2) * k * cos(...)) [missing square].
          This broke the Koide structure and invalidated all v3 results.

Mass ordering convention (same as v3 and Codex sidecar):
    j=0 -> heaviest (top, bottom)
    j=1 -> lightest (up, down)
    j=2 -> middle   (charm, strange)

Input manifest, preflight checks, and honest conditional language per
Codex D1 v3 audit requirements and formula-readiness gate.
"""

import json
import math
import os
import sys
from typing import Tuple, Dict, List, Optional

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2

# Shared D-series validator (per Codex 2026-07-15 formula-readiness gate repair)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from d_series_validator import (
    validate_preflight as _shared_validate,
    Status as _DStatus,
    QStatus as _QStatus,
    Q3DecisionType as _Q3DT,
    check_language as _check_lang,
)


# ============================================================================
# INPUT MANIFEST
# ============================================================================

CL90_TO_1SIGMA = 1.0 / 1.6448536269514722  # exact two-sided 90% CL -> 1-sigma factor

# Per-quark input manifest. Each entry records the exact PDG artifact used,
# its confidence-level label, the conversion rule (if any), the scale, and the scheme.
QUARK_INPUTS = {
    "up": {
        "mass_mev": 2.16,
        "sigma_mev": 0.07 * CL90_TO_1SIGMA,  # 0.0426
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "2.16E-03 GeV",
        "sigma_in_artifact": "0.7E-04 GeV",
        "confidence_label": "90% CL (per PDG 2024 Summary Table header for light quarks)",
        "conversion_rule": "sigma_1s = sigma_90CL / 1.645",
        "scheme": "MS-bar",
        "scale": "2 GeV",
    },
    "down": {
        "mass_mev": 4.70,
        "sigma_mev": 0.07 * CL90_TO_1SIGMA,
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "4.70E-03 GeV",
        "sigma_in_artifact": "0.7E-04 GeV",
        "confidence_label": "90% CL (per PDG 2024 Summary Table header for light quarks)",
        "conversion_rule": "sigma_1s = sigma_90CL / 1.645",
        "scheme": "MS-bar",
        "scale": "2 GeV",
    },
    "strange": {
        "mass_mev": 93.5,
        "sigma_mev": 0.8 * CL90_TO_1SIGMA,  # 0.486
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "9.35E-02 GeV",
        "sigma_in_artifact": "0.8E-03 GeV",
        "confidence_label": "90% CL (per PDG 2024 Summary Table header for light quarks)",
        "conversion_rule": "sigma_1s = sigma_90CL / 1.645",
        "scheme": "MS-bar",
        "scale": "2 GeV",
    },
    "charm": {
        "mass_mev": 1273.0,
        "sigma_mev": 5.0 * CL90_TO_1SIGMA,  # 3.04
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "1.273E+00 GeV",
        "sigma_in_artifact": "5.0E-03 GeV",
        "confidence_label": "90% CL (per PDG 2024 Summary Table header for heavy quarks)",
        "conversion_rule": "sigma_1s = sigma_90CL / 1.645",
        "scheme": "MS-bar",
        "scale": "m_c (~1.27 GeV)",
        "note": "PDG 2024 Summary Table gives m_c = 1273.0 +/- 4.6 MeV; MC file gives 1273.0 +/- 5.0 MeV. This fit uses the MC file value.",
    },
    "bottom": {
        "mass_mev": 4183.0,
        "sigma_mev": 7.0 * CL90_TO_1SIGMA,  # 4.26
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "4.183E+00 GeV",
        "sigma_in_artifact": "7.0E-03 GeV",
        "confidence_label": "90% CL (per PDG 2024 Summary Table header for heavy quarks)",
        "conversion_rule": "sigma_1s = sigma_90CL / 1.645",
        "scheme": "MS-bar",
        "scale": "m_b (~4.18 GeV)",
    },
    "top": {
        "mass_mev": 172570.0,
        "sigma_mev": 290.0,  # NOT converted; see note
        "pdg_artifact": "PDG 2024 MC data file (mass_width_2024.txt), generated 31-May-2024",
        "value_in_artifact": "1.7257E+02 GeV",
        "sigma_in_artifact": "2.9E-01 GeV",
        "confidence_label": "Not labeled as 90% CL by PDG; treated as exploratory 1-sigma Gaussian",
        "conversion_rule": "None — used as-is",
        "scheme": "Direct kinematic average / MC-generator mass parameter",
        "scale": "—",
        "note": "This is the PDG direct-measurement average of LHC and Tevatron kinematic fits. PDG calls this the 'Monte Carlo mass'; it is the mass parameter used in MC generators, distinct from a theoretically well-defined pole mass. The difference between the MC mass and the pole mass is expected to be around 0.5 GeV and is not fully resolved. The 0.29 GeV error is not converted by 1.645 because it is not marked 90% CL.",
    },
}

INPUT_MANIFEST = {
    "pdg_edition": "2024",
    "primary_source": "https://pdg.lbl.gov/2024/mcdata/mass_width_2024.txt (generated 31-May-2024 by PDG)",
    "secondary_source": "https://pdg.lbl.gov/2024/tables/rpp2024-sum-quarks.pdf (for confidence-level labels)",
    "source_accessed": "2026-07-13",
    "renormalization_scheme": "MS-bar for u,d,s,c,b; top is direct kinematic average (see per-quark notes)",
    "scale_convention": "MIXED — not at a common scale; see per-quark entries",
    "correlation_assumptions": "None — masses treated as independent. PDG does not publish a full quark-mass covariance matrix.",
    "per_quark_inputs": {k: {sk: sv for sk, sv in v.items() if sk not in ("sigma_mev",)} for k, v in QUARK_INPUTS.items()},
    "scale_notes": (
        "Light quarks (u,d,s): MS-bar at 2 GeV. "
        "Charm: MS-bar at m_c scale. "
        "Bottom: MS-bar at m_b scale. "
        "Top: direct kinematic average from tt event kinematics, not run to a common scale with the others. "
        "A scale-consistent test requires QCD running. "
        "Results are CONDITIONAL on the mixed-scale assumption."
    ),
}

# Sector mass vectors built from the per-quark manifest.
MASSES = {
    "up": {
        "quarks": ["top", "up", "charm"],
        "masses_mev": np.array([QUARK_INPUTS["top"]["mass_mev"], QUARK_INPUTS["up"]["mass_mev"], QUARK_INPUTS["charm"]["mass_mev"]]),
        "sigmas_mev": np.array([QUARK_INPUTS["top"]["sigma_mev"], QUARK_INPUTS["up"]["sigma_mev"], QUARK_INPUTS["charm"]["sigma_mev"]]),
        "scale_notes": "Mixed: direct kinematic average (top), MS-bar 2 GeV (up), MS-bar at m_c (charm)",
    },
    "down": {
        "quarks": ["bottom", "down", "strange"],
        "masses_mev": np.array([QUARK_INPUTS["bottom"]["mass_mev"], QUARK_INPUTS["down"]["mass_mev"], QUARK_INPUTS["strange"]["mass_mev"]]),
        "sigmas_mev": np.array([QUARK_INPUTS["bottom"]["sigma_mev"], QUARK_INPUTS["down"]["sigma_mev"], QUARK_INPUTS["strange"]["sigma_mev"]]),
        "scale_notes": "Mixed: MS-bar at m_b (bottom), MS-bar 2 GeV (down, strange)",
    },
}

# Sensitivity: alternate top definition (cross-section pole mass, Codex-cited)
TOP_CROSS_SECTION = {
    "mass_mev": 172400.0,
    "sigma_mev": 700.0,
    "pdg_artifact": "PDG 2024 Summary Table (rpp2024-sum-quarks.pdf)",
    "confidence_label": "Not established; treated as exploratory for sensitivity only",
    "note": "This is a pole-from-cross-section value, distinct from the direct kinematic average used in the main fit.",
}

# Zenczykowski proposed phase values (from abstract: "possibly exact")
# delta_L = 3*delta_D/2 = 3*delta_U = 2/9
# => delta_U = 2/27, delta_D = 4/27
DELTA_U_PRED = 2.0 / 27.0
DELTA_D_PRED = 4.0 / 27.0


# ============================================================================
# Q1/Q2/Q3 PREFLIGHT (Codex formula-readiness gate)
# ============================================================================

def run_preflight() -> Dict:
    """Run Q1/Q2/Q3 preflight checks per Codex formula-readiness gate.

    Wired through the shared d_series_validator (per 2026-07-15 repair contract).
    Q3 decision type is COMPUTATIONAL_DIAGNOSTIC: numerical chi^2/p-values are
    computational outputs of the declared model, not physical sigma,
    compatibility, or falsification decisions.
    """
    preflight = {}

    # Q1: Units and normalization close in the actual implementation
    preflight["Q1_units"] = {
        "check": "sqrt(m_j) = sqrt(M) * (1 + sqrt(2)*k*cos(...)) — sqrt(mass) = sqrt(mass) * dimensionless",
        "status": "CLOSED",
        "notes": "Dimensionally consistent. M in MeV, k and delta dimensionless.",
    }

    # Q2: Inputs have physical definitions; all calibration declared
    preflight["Q2_inputs"] = {
        "check": "All inputs from PDG 2024 with declared scheme, scale, and confidence convention.",
        "status": "DECLARED",
        "notes": (
            "Per-quark manifest records exact PDG artifact, value, uncertainty, confidence label, "
            "conversion rule, scheme, and scale. u,d,s,c,b: 90% CL converted to 1-sigma. "
            "top: direct kinematic average 172.57 +/- 0.29 GeV; uncertainty not labeled 90% CL by PDG, "
            "used as exploratory 1-sigma Gaussian. No calibration or target selection reused. "
            "WARNING: mixed scales and unresolved top confidence convention mean results are "
            "CONDITIONAL exploratory outputs, not a closed PDG-2024 statistical test."
        ),
    }

    # Q3: Observable, control/null, and decision threshold written before the run
    # Decision type: COMPUTATIONAL_DIAGNOSTIC — chi^2/p-values are numerical
    # outputs of the declared model, NOT physical sigma/compatibility/falsification.
    preflight["Q3_observable"] = {
        "observable": "Best-fit phase delta_f for each sector (f=up, down) under Eq. (4)",
        "null_model": "Zenczykowski proposed values: delta_U=2/27, delta_D=4/27",
        "decision_threshold": (
            "No sigma-based falsification claim and no compatibility/tension verdict labels. "
            "Report only numerical chi^2 and p-value outputs for fixed-phase fits, labeled as "
            "computational diagnostics of the declared exploratory Gaussian input model. "
            "Do not claim 'falsification at N sigma' or 'compatible at N sigma'."
        ),
        "decision_type": "computational_diagnostic",
        "status": "DECLARED",
        "notes": (
            "Following Codex D1 v3 audit and 2026-07-15 formula-readiness gate repair: "
            "numerical discrepancies under mixed-scale inputs are computational "
            "diagnostics, not physical conclusions. This run uses mixed-scale inputs, "
            "so all results are CONDITIONAL exploratory outputs."
        ),
    }

    # Overall status via shared validator
    vr = _shared_validate(
        task_id="D1",
        q1_status=preflight["Q1_units"]["status"],
        q2_status=preflight["Q2_inputs"]["status"],
        q3_status=preflight["Q3_observable"]["status"],
        q3_decision_type=_Q3DT.COMPUTATIONAL_DIAGNOSTIC,
    )

    preflight["overall_status"] = str(vr.overall_status)
    preflight["overall_notes"] = vr.allowed_language
    preflight["disallowed_language"] = vr.disallowed_language
    preflight["reducer_reason"] = vr.reducer_reason
    preflight["validator"] = "d_series_validator.validate_preflight"

    return preflight


# ============================================================================
# FORMULA IMPLEMENTATION (source-correct)
# ============================================================================

def cosines(delta: float) -> np.ndarray:
    """Three cosine values for j=0,1,2 at phase delta."""
    return np.array([math.cos(2.0 * math.pi * j / 3.0 + delta) for j in range(3)])


def predict_masses(M: float, k: float, delta: float) -> np.ndarray:
    """
    Predict masses using Zenczykowski Eq. (4):
        sqrt(m_j) = sqrt(M) * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))
        m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))^2
    """
    factors = 1.0 + math.sqrt(2.0) * k * cosines(delta)
    return M * factors**2


def koide_Q(k: float) -> float:
    """Koide Q parameter: Q = (1+k^2)/3. k=1 -> Q=2/3."""
    return (1.0 + k**2) / 3.0


def free_fit(masses: np.ndarray) -> Tuple[float, float, float, np.ndarray]:
    """
    Analytic solution for 3-parameter fit (M, k, delta) to 3 masses
    using the CORRECT square-root formula.

    Given sqrt(m_j) = sqrt(M) * (1 + sqrt(2)*k*cos(2*pi*j/3 + delta)):
    - Sum of sqrt(m_j) = 3*sqrt(M)  (since sum of cosines = 0)
    - So sqrt(M) = mean(sqrt(m_j))
    - Normalized: (sqrt(m_j)/sqrt(M) - 1) = sqrt(2)*k*cos(2*pi*j/3 + delta)
    - k = sqrt(sum(normalized^2) / 3)  (since sum(cos^2) = 3/2)
    - delta = acos(normalized[0] / (sqrt(2)*k))
    """
    roots = np.sqrt(masses)
    sqrt_M = float(roots.mean())
    M = sqrt_M**2

    normalized = roots / sqrt_M - 1.0  # = sqrt(2)*k*cos(2*pi*j/3 + delta)

    k_sq = float(np.dot(normalized, normalized) / 3.0)
    if k_sq <= 0:
        raise ValueError(f"k^2 <= 0 for masses {masses}")
    k = math.sqrt(k_sq)

    # cos(delta) from j=0 (heaviest): normalized[0] = sqrt(2)*k*cos(delta)
    c0 = float(normalized[0]) / (math.sqrt(2.0) * k)
    c0 = max(-1.0, min(1.0, c0))  # numerical safety
    delta = math.acos(c0)

    predictions = predict_masses(M, k, delta)
    return M, k, delta, predictions


def maximum_positive_k(delta: float) -> float:
    """Maximum k before any bracket factor goes non-positive (ensuring sqrt(m) > 0)."""
    cos_vals = cosines(delta)
    negative_cos = [c for c in cos_vals if c < 0.0]
    if not negative_cos:
        return float('inf')
    return min(-1.0 / (math.sqrt(2.0) * c) for c in negative_cos)


def fixed_delta_fit(masses: np.ndarray, sigmas: np.ndarray, delta: float, sector_name: str = "") -> Dict:
    """
    Fit M and k with delta fixed, using the CORRECT square-root formula.
    2 free parameters, 3 data points -> 1 degree of freedom.
    Enforces positivity: all bracket factors must be > 0.

    Uses a 1D grid search over k with analytic optimal M for each k. This avoids
    the 2D boundary-gradient problems that made L-BFGS-B return ABNORMAL.
    """
    k_max = maximum_positive_k(delta) * (1.0 - 1e-12)
    if k_max <= 0.0 or not math.isfinite(k_max):
        raise ValueError(f"No positive-k region for {sector_name} delta={delta}")

    factors_grid = np.array([1.0 + math.sqrt(2.0) * k * cosines(delta) for k in np.linspace(0, k_max, 20001)])
    # Remove any k where positivity is lost (should be none up to k_max, but numerical safety)
    valid = np.all(factors_grid > 0.0, axis=1)
    ks_valid = np.linspace(0, k_max, 20001)[valid]
    factors_valid = factors_grid[valid]

    if len(ks_valid) == 0:
        raise ValueError(f"No positive-k samples for {sector_name} delta={delta}")

    # Analytic optimal M for each k: M = sum(m_i * f_i^2 / sigma_i^2) / sum(f_i^4 / sigma_i^2)
    m = masses[:, np.newaxis]
    f = factors_valid.T  # shape (3, n_samples)
    s = sigmas[:, np.newaxis]
    numerator = np.sum(m * f**2 / s**2, axis=0)
    denominator = np.sum(f**4 / s**2, axis=0)
    M_opt = numerator / denominator
    M_opt = np.where(M_opt > 0.0, M_opt, 1e-300)

    preds = M_opt[np.newaxis, :] * f**2
    chi2_vals = np.sum(((m - preds) / s) ** 2, axis=0)

    best_idx = int(np.argmin(chi2_vals))
    k_fit = float(ks_valid[best_idx])
    M_fit = float(M_opt[best_idx])
    chisq = float(chi2_vals[best_idx])

    # Local refinement: quadratic interpolation around the best grid point
    if 0 < best_idx < len(ks_valid) - 1:
        k_local = ks_valid[best_idx - 1 : best_idx + 2]
        c_local = chi2_vals[best_idx - 1 : best_idx + 2]
        # Fit parabola c = a*k^2 + b*k + c0 and find vertex
        A = np.vstack([k_local**2, k_local, np.ones_like(k_local)]).T
        try:
            a, b, c0 = np.linalg.lstsq(A, c_local, rcond=None)[0]
            if a > 0.0:
                k_vertex = -b / (2.0 * a)
                if k_local[0] < k_vertex < k_local[-1]:
                    f_vertex = 1.0 + math.sqrt(2.0) * k_vertex * cosines(delta)
                    if np.all(f_vertex > 0.0):
                        M_vertex = float(np.sum(masses * f_vertex**2 / sigmas**2) / np.sum(f_vertex**4 / sigmas**2))
                        if M_vertex > 0.0:
                            preds_vertex = M_vertex * f_vertex**2
                            chi2_vertex = float(np.sum(((masses - preds_vertex) / sigmas) ** 2))
                            if chi2_vertex < chisq:
                                k_fit = float(k_vertex)
                                M_fit = M_vertex
                                chisq = chi2_vertex
        except (np.linalg.LinAlgError, ValueError):
            pass

    preds = predict_masses(M_fit, k_fit, delta)

    return {
        "M": M_fit,
        "k": k_fit,
        "delta": delta,
        "Q": koide_Q(k_fit),
        "k_max_positive": k_max,
        "chi2": chisq,
        "dof": 1,
        "p_value": float(chi2.sf(chisq, 1)),
        "predictions_mev": preds.tolist(),
        "pulls": ((masses - preds) / sigmas).tolist(),
        "residuals": (masses - preds).tolist(),
        "optimizer_success": True,
        "optimizer_message": f"1D grid search + analytic M; {len(ks_valid)} k samples; quadratic refinement",
    }


def monte_carlo_delta(masses: np.ndarray, sigmas: np.ndarray, seed: int, n_draws: int = 20000) -> Tuple[float, float, float, float]:
    """
    Monte Carlo over mass uncertainties to get delta and k distributions.
    Returns (delta_mean, delta_sigma, k_mean, k_sigma).
    """
    rng = np.random.default_rng(seed)
    deltas = []
    ks = []
    for draw in rng.normal(masses, sigmas, (n_draws, 3)):
        if np.all(draw > 0.0):
            try:
                M, k, delta, _ = free_fit(draw)
                # Check positivity
                factors = 1.0 + math.sqrt(2.0) * k * cosines(delta)
                if np.all(factors > 0.0):
                    deltas.append(delta)
                    ks.append(k)
            except (ValueError, FloatingPointError):
                continue

    if len(deltas) < 100:
        return float('nan'), float('nan'), float('nan'), float('nan')

    delta_arr = np.array(deltas)
    k_arr = np.array(ks)
    return float(delta_arr.mean()), float(delta_arr.std()), float(k_arr.mean()), float(k_arr.std())


# ============================================================================
# REGRESSION TEST: delta_U = 2/27 under correct formula
# ============================================================================

def regression_test_delta_u_2_27() -> Dict:
    """
    Codex required: 'Add a direct test showing the expected up-sector behavior
    at delta_U = 2/27 under the actual formula.'

    This test reports the up-sector fixed-phase diagnostic at delta_U = 2/27
    under the correct square-root formula.
    """
    masses = MASSES["up"]["masses_mev"]
    sigmas = MASSES["up"]["sigmas_mev"]

    # Free fit
    M_free, k_free, delta_free, preds_free = free_fit(masses)

    # Fixed delta = 2/27
    fixed = fixed_delta_fit(masses, sigmas, DELTA_U_PRED, sector_name="up")

    # Compare
    return {
        "test": "delta_U = 2/27 fixed-phase up-sector diagnostic",
        "formula": "sqrt(m_j) = sqrt(M) * (1 + sqrt(2)*k*cos(2*pi*j/3 + delta))",
        "free_fit_delta": delta_free,
        "free_fit_delta_deg": math.degrees(delta_free),
        "proposed_delta": DELTA_U_PRED,
        "proposed_delta_deg": math.degrees(DELTA_U_PRED),
        "delta_difference": delta_free - DELTA_U_PRED,
        "delta_difference_percent": (delta_free - DELTA_U_PRED) / DELTA_U_PRED * 100,
        "fixed_delta_chi2": fixed["chi2"],
        "fixed_delta_p_value": fixed["p_value"],
        "fixed_delta_k": fixed["k"],
        "fixed_delta_M": fixed["M"],
        "fixed_delta_Q": fixed["Q"],
        "notes": (
            f"Free fit gives delta_U = {delta_free:.6f} rad. "
            f"Zenczykowski proposes {DELTA_U_PRED:.6f} rad. "
            f"Difference: {abs(delta_free - DELTA_U_PRED):.6f} rad "
            f"({abs(delta_free - DELTA_U_PRED)/DELTA_U_PRED*100:.2f}%). "
            f"Fixed-delta chi^2 = {fixed['chi2']:.4f} (p = {fixed['p_value']:.4f}). "
            f"No compatibility/tension verdict is assigned; these are exploratory model outputs."
        ),
    }


def regression_test_optimizer() -> Dict:
    """
    Regression fixture: verify fixed_delta_fit can recover a known synthetic solution.
    Generate masses from known (M, k, delta), add small Gaussian noise, and check
    that the optimizer finds the correct chi2 minimum and recovers the known delta.
    """
    M_true = 10000.0
    k_true = 1.2
    delta_true = 0.07
    sigmas = np.array([1.0, 0.001, 0.1])  # tiny noise so known solution is near optimum
    preds = predict_masses(M_true, k_true, delta_true)
    masses = preds + np.array([0.5, -0.0003, 0.05])  # small perturbations

    result = fixed_delta_fit(masses, sigmas, delta_true, sector_name="synthetic")
    chi2_expected = float(np.sum(((masses - preds) / sigmas) ** 2))

    # The optimum should be very close to the known (M_true, k_true) because the noise is small
    M_err = abs(result["M"] - M_true) / M_true
    k_err = abs(result["k"] - k_true) / k_true

    return {
        "test": "optimizer regression on synthetic data",
        "M_true": M_true,
        "k_true": k_true,
        "delta_true": delta_true,
        "M_recovered": result["M"],
        "k_recovered": result["k"],
        "M_relative_error": M_err,
        "k_relative_error": k_err,
        "chi2_found": result["chi2"],
        "chi2_expected_at_true": chi2_expected,
        "optimizer_success": result["optimizer_success"],
        "pass": (M_err < 1e-5 and k_err < 1e-5 and result["optimizer_success"]),
    }


def top_mass_sensitivity() -> Dict:
    """
    Sensitivity check: the PDG summary table lists a different top definition
    (pole-from-cross-section: 172.4 +/- 0.7 GeV) than the direct-measurement
    average (172.57 +/- 0.29 GeV) used in the main fit. Re-run the up-sector
    free fit with the cross-section value and compare.
    """
    masses = MASSES["up"]["masses_mev"].copy()
    masses[0] = TOP_CROSS_SECTION["mass_mev"]

    M, k, delta, preds = free_fit(masses)
    return {
        "top_definition_used": "pole-from-cross-section (172.4 +/- 0.7 GeV)",
        "M": M,
        "k": k,
        "delta": delta,
        "delta_deg": math.degrees(delta),
        "Q": koide_Q(k),
        "delta_difference_from_main": delta - free_fit(MASSES["up"]["masses_mev"])[2],
        "notes": (
            "Using the cross-section top definition instead of the direct-measurement "
            "average shifts the up-sector free-fit phase. This check varies only the central "
            "mass; it does not carry the alternate uncertainty through the fixed-phase or "
            "Monte-Carlo outputs. A full sensitivity study is future work."
        ),
    }


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    print("=" * 80)
    print("D1 v4.4: Zenczykowski Quark Koide Formula — Source-Correct Fit")
    print("Formula: sqrt(m_j) = sqrt(M) * (1 + sqrt(2)*k*cos(2*pi*j/3 + delta))")
    print("Source: arXiv:1301.4143 (PRD 87, 077302), Eq. (4)")
    print("=" * 80)
    print()

    # --- Preflight ---
    print("--- Q1/Q2/Q3 PREFLIGHT (Codex formula-readiness gate) ---")
    preflight = run_preflight()
    print(f"Overall status: {preflight['overall_status']}")
    print(f"  Q1 (units): {preflight['Q1_units']['status']}")
    print(f"  Q2 (inputs): {preflight['Q2_inputs']['status']}")
    print(f"  Q3 (observable): {preflight['Q3_observable']['status']}")
    print(f"  Notes: {preflight['overall_notes']}")
    print()

    # --- Input manifest ---
    print("--- INPUT MANIFEST ---")
    print(f"PDG edition: {INPUT_MANIFEST['pdg_edition']}")
    print(f"Primary source: {INPUT_MANIFEST['primary_source']}")
    print(f"Secondary source: {INPUT_MANIFEST['secondary_source']}")
    print(f"Source accessed: {INPUT_MANIFEST['source_accessed']}")
    print(f"Scheme: {INPUT_MANIFEST['renormalization_scheme']}")
    print(f"Scale: {INPUT_MANIFEST['scale_convention']}")
    print(f"Correlations: {INPUT_MANIFEST['correlation_assumptions']}")
    print(f"Scale notes: {INPUT_MANIFEST['scale_notes'][:120]}...")
    print()
    print("  Per-quark inputs used in this fit:")
    for qname, qdata in QUARK_INPUTS.items():
        print(f"    {qname:8s}: {qdata['mass_mev']:12.3f} ± {qdata['sigma_mev']:8.4f} MeV")
        print(f"              PDG artifact: {qdata['pdg_artifact']}")
        print(f"              Value in artifact: {qdata['value_in_artifact']} ± {qdata['sigma_in_artifact']}")
        print(f"              Confidence: {qdata['confidence_label']}")
        print(f"              Conversion: {qdata['conversion_rule']}")
        print(f"              Scheme/scale: {qdata['scheme']} / {qdata['scale']}")
        if "note" in qdata:
            print(f"              Note: {qdata['note']}")
    print()

    # --- Free fit ---
    print("--- FREE-delta FIT (3 parameters, 3 masses, 0 dof) ---")
    print("Note: 3-param fit to 3 masses reproduces inputs exactly if solution exists.")
    print("      The interesting output is the best-fit parameters and their MC uncertainties.")
    print()

    free_results = {}
    mc_results = {}

    for i, (sector, data) in enumerate(MASSES.items()):
        masses = data["masses_mev"]
        sigmas = data["sigmas_mev"]

        M, k, delta, preds = free_fit(masses)
        Q = koide_Q(k)

        free_results[sector] = {
            "M": M, "k": k, "delta": delta, "Q": Q,
            "predictions": preds.tolist(),
            "residuals": (masses - preds).tolist(),
        }

        print(f"  {sector}-type ({'/'.join(data['quarks'])}):")
        print(f"    M     = {M:12.4f} MeV")
        print(f"    k     = {k:12.6f}")
        print(f"    delta = {delta:12.6f} rad ({math.degrees(delta):.4f}°)")
        print(f"    Q     = {Q:12.6f}  (Koide: 2/3 = {2/3:.6f})")
        print(f"    Fitted-model values: {[f'{p:.6f}' for p in preds]}")
        print(f"    Residuals:   {[f'{r:.2e}' for r in (masses - preds)]}")
        print()

        # Monte Carlo for uncertainties
        d_mean, d_sigma, k_mean, k_sigma = monte_carlo_delta(masses, sigmas, 20260712 + i)
        mc_results[sector] = {
            "delta_mean": d_mean, "delta_sigma": d_sigma,
            "k_mean": k_mean, "k_sigma": k_sigma,
        }
        print(f"    Monte Carlo (20,000 draws):")
        print(f"      delta = {d_mean:.6f} ± {d_sigma:.6f} rad")
        print(f"      k     = {k_mean:.6f} ± {k_sigma:.6f}")
        print()

    # --- Phase comparison ---
    print("--- PHASE COMPARISON ---")
    delta_u = free_results["up"]["delta"]
    delta_d = free_results["down"]["delta"]
    ratio = delta_d / delta_u

    print(f"  Free fit:  delta_U = {delta_u:.6f} rad, delta_D = {delta_d:.6f} rad")
    print(f"  Zenczykowski: delta_U = {DELTA_U_PRED:.6f} rad, delta_D = {DELTA_D_PRED:.6f} rad")
    print(f"  Ratio delta_D/delta_U = {ratio:.4f}  (Zenczykowski proposes 2.000)")
    print()

    # MC uncertainty on ratio
    d_u_mean = mc_results["up"]["delta_mean"]
    d_u_sig = mc_results["up"]["delta_sigma"]
    d_d_mean = mc_results["down"]["delta_mean"]
    d_d_sig = mc_results["down"]["delta_sigma"]
    ratio_mc = d_d_mean / d_u_mean
    ratio_sigma = ratio_mc * math.sqrt((d_d_sig/d_d_mean)**2 + (d_u_sig/d_u_mean)**2)
    print(f"  MC ratio: {ratio_mc:.4f} ± {ratio_sigma:.4f}")
    print(f"  Difference from 2:1 = {(ratio_mc - 2.0):.4f}")
    print(f"  NOTE: This is a parameter-ratio discrepancy under mixed-scale inputs. Not a falsification claim.")
    print()

    # --- Fixed-delta fits ---
    print("--- FIXED-delta FITS (Zenczykowski's claimed values) ---")
    print("  2 free params (M, k), 3 masses, 1 dof")
    print()

    fixed_results = {}
    for sector, data in MASSES.items():
        masses = data["masses_mev"]
        sigmas = data["sigmas_mev"]
        delta_fixed = DELTA_U_PRED if sector == "up" else DELTA_D_PRED

        result = fixed_delta_fit(masses, sigmas, delta_fixed, sector_name=sector)
        fixed_results[sector] = result

        print(f"  {sector}-type (delta = {delta_fixed:.6f} rad = {math.degrees(delta_fixed):.4f}°):")
        print(f"    M = {result['M']:.4f} MeV, k = {result['k']:.6f}, Q = {result['Q']:.6f}")
        print(f"    chi^2 = {result['chi2']:.4f} (dof=1, p = {result['p_value']:.6f})")
        print(f"    Fitted-model values: {[f'{p:.4f}' for p in result['predictions_mev']]}")
        print(f"    Pulls:       {[f'{p:.2f}' for p in result['pulls']]}")
        print(f"    (chi^2 and p-value are outputs of the declared exploratory Gaussian input model.")
        print(f"     They are not a closed PDG-2024 statistical test.")
        print()

    # --- Cross-sector 1:2 hierarchy test ---
    print("--- CROSS-SECTOR 1:2 HIERARCHY TEST ---")
    print("  If delta_D = 2*delta_U, up-type fit reconstructs down-type phase")
    print()

    cross_results = {}
    # Up reconstructs down: delta_D = 2 * delta_U_free
    delta_d_pred_from_up = 2.0 * delta_u
    cross_up_to_down = fixed_delta_fit(
        MASSES["down"]["masses_mev"], MASSES["down"]["sigmas_mev"], delta_d_pred_from_up, sector_name="down_from_up"
    )
    cross_results["up_to_down"] = cross_up_to_down
    print(f"  Up -> Down (delta_D = 2*delta_U = {delta_d_pred_from_up:.6f} rad):")
    print(f"    chi^2 = {cross_up_to_down['chi2']:.4f} (dof=1, p = {cross_up_to_down['p_value']:.6f})")
    print(f"    (Exploratory model output; not a closed statistical test.)")
    print()

    # Down reconstructs up: delta_U = delta_D_free / 2
    delta_u_pred_from_down = delta_d / 2.0
    cross_down_to_up = fixed_delta_fit(
        MASSES["up"]["masses_mev"], MASSES["up"]["sigmas_mev"], delta_u_pred_from_down, sector_name="up_from_down"
    )
    cross_results["down_to_up"] = cross_down_to_up
    print(f"  Down -> Up (delta_U = delta_D/2 = {delta_u_pred_from_down:.6f} rad):")
    print(f"    chi^2 = {cross_down_to_up['chi2']:.4f} (dof=1, p = {cross_down_to_up['p_value']:.6f})")
    print(f"    (Exploratory model output; not a closed statistical test.)")
    print()

    # --- Regression tests ---
    print("--- REGRESSION TEST: delta_U = 2/27 ---")
    reg = regression_test_delta_u_2_27()
    print(f"  {reg['notes']}")
    print(f"  Verdict label removed; chi2/p are exploratory model outputs only.")
    print()

    print("--- REGRESSION TEST: optimizer fixture ---")
    opt_reg = regression_test_optimizer()
    print(f"  M relative error: {opt_reg['M_relative_error']:.6e}")
    print(f"  k relative error: {opt_reg['k_relative_error']:.6e}")
    print(f"  Optimizer success: {opt_reg['optimizer_success']}")
    print(f"  Pass: {opt_reg['pass']}")
    print()

    print("--- SENSITIVITY CHECK: top mass definition ---")
    top_sens = top_mass_sensitivity()
    print(f"  Using {top_sens['top_definition_used']}")
    print(f"  delta_U = {top_sens['delta']:.6f} rad ({top_sens['delta_deg']:.4f}°)")
    print(f"  Shift from main fit: {top_sens['delta_difference_from_main']:.6f} rad")
    print(f"  {top_sens['notes']}")
    print()

    # --- Summary ---
    print("=" * 80)
    print("SUMMARY — CONDITIONAL RESULTS (mixed-scale inputs)")
    print("=" * 80)
    print()
    print(f"1. Free-fit phases:")
    print(f"   delta_U = {delta_u:.6f} rad ({math.degrees(delta_u):.4f}°) — "
          f"Zenczykowski: {DELTA_U_PRED:.6f} rad ({math.degrees(DELTA_U_PRED):.4f}°)")
    print(f"   delta_D = {delta_d:.6f} rad ({math.degrees(delta_d):.4f}°) — "
          f"Zenczykowski: {DELTA_D_PRED:.6f} rad ({math.degrees(DELTA_D_PRED):.4f}°)")
    print()
    print(f"2. Up-sector fixed delta_U = 2/27:")
    print(f"   chi^2 = {fixed_results['up']['chi2']:.4f}, p = {fixed_results['up']['p_value']:.4f}")
    print(f"   Free fit differs from proposed value by {abs(delta_u - DELTA_U_PRED)/DELTA_U_PRED*100:.2f}%")
    print(f"   NOTE: p-value is an output of the declared exploratory Gaussian input model.")
    print(f"   It is not a closed PDG-2024 statistical test.")
    print()
    print(f"3. Down-sector fixed delta_D = 4/27:")
    print(f"   chi^2 = {fixed_results['down']['chi2']:.4f}, p = {fixed_results['down']['p_value']:.6f}")
    print(f"   NOTE: p-value is an output of the declared exploratory Gaussian input model.")
    print()
    print(f"4. 1:2 hierarchy: delta_D/delta_U = {ratio:.4f} (proposed 2.000)")
    print(f"   Cross-sector chi^2 values are large under the exploratory model.")
    print(f"   This is a parameter-ratio discrepancy, not a falsification claim.")
    print()
    print(f"5. Koide Q values: up = {free_results['up']['Q']:.6f}, down = {free_results['down']['Q']:.6f}")
    print(f"   (Charged leptons: Q = 2/3 = {2/3:.6f} with k=1)")
    print()
    print("IMPORTANT: All results are CONDITIONAL on mixed-scale inputs.")
    print("A scale-consistent test requires QCD running to a common scale.")
    print("No falsification claim is made. No sigma-based claim is made.")
    print("This is EXPLORATORY per the Codex formula-readiness gate.")
    print()

    # --- JSON output for audit ---
    output = {
        "schema": "devin-d1-v4-4-results",
        "formula": "sqrt(m_j) = sqrt(M) * (1 + sqrt(2)*k*cos(2*pi*j/3 + delta))",
        "source": "arXiv:1301.4143 Eq. (4)",
        "input_manifest": INPUT_MANIFEST,
        "preflight": preflight,
        "free_fit": {
            sector: {
                "M": r["M"], "k": r["k"], "delta": r["delta"],
                "Q": r["Q"], "predictions": r["predictions"],
            }
            for sector, r in free_results.items()
        },
        "monte_carlo": mc_results,
        "fixed_delta": {
            sector: {
                "delta": r["delta"], "M": r["M"], "k": r["k"], "Q": r["Q"],
                "chi2": r["chi2"], "p_value": r["p_value"],
                "predictions": r["predictions_mev"], "pulls": r["pulls"],
                "optimizer_success": r["optimizer_success"],
            }
            for sector, r in fixed_results.items()
        },
        "cross_sector": {
            "up_to_down": {
                "delta": cross_up_to_down["delta"], "chi2": cross_up_to_down["chi2"],
                "p_value": cross_up_to_down["p_value"],
            },
            "down_to_up": {
                "delta": cross_down_to_up["delta"], "chi2": cross_down_to_up["chi2"],
                "p_value": cross_down_to_up["p_value"],
            },
        },
        "regression_test_delta_u_2_27": reg,
        "regression_test_optimizer": opt_reg,
        "top_mass_sensitivity": top_sens,
        "phase_ratio": {
            "observed": ratio,
            "mc_mean": ratio_mc,
            "mc_sigma": ratio_sigma,
            "proposed": 2.0,
        },
        "status": "EXPLORATORY",
        "claim_boundary": (
            "No falsification claim. No sigma-based statistical claim. "
            "p-values and chi2 are outputs of the declared exploratory Gaussian input model only. "
            "Results conditional on mixed-scale inputs. "
            "Scale-consistent test requires QCD running to a common scale."
        ),
    }

    # Write JSON for Codex audit
    json_path = "/mnt/d/Fundamentals/measurement_alignment/quark_masses/d1_v4_4_results.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nJSON output written to: {json_path}")


if __name__ == "__main__":
    main()
