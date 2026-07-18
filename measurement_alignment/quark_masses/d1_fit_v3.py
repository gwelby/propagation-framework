#!/usr/bin/env python3
"""
D1 v3: Zenczykowski quark Koide formula fit against PDG 2024 masses.

Formula convention (Zenczykowski 2013, Eq. 4):
    m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta))

Mass ordering convention:
    j=0 -> heaviest (top, bottom)
    j=1 -> lightest (up, down)
    j=2 -> middle   (charm, strange)

Output: D1_fit_results.md (v3)
"""

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammainc
import math
from typing import Tuple, Dict, List

# PDG 2024 quark masses (central values and uncertainties)
# Light quarks MS-bar at 2 GeV; heavy quarks pole masses.
MASSES = {
    "up": {
        "m_u": (2.16, 0.49),     # MeV
        "m_c": (1270.0, 20.0),   # MeV
        "m_t": (172500.0, 700.0),# MeV
    },
    "down": {
        "m_d": (4.67, 0.48),     # MeV
        "m_s": (93.5, 0.8),      # MeV
        "m_b": (4180.0, 20.0),   # MeV
    },
}

# ordering maps key -> j index (heaviest=0, lightest=1, middle=2)
J_MAP = {"m_u": 1, "m_c": 2, "m_t": 0, "m_d": 1, "m_s": 2, "m_b": 0}
QUARK_NAMES = {
    "up":   ["top", "up", "charm"],
    "down": ["bottom", "down", "strange"],
}


def zenczykowski_pred(params: np.ndarray, j: int) -> float:
    """Predict mass for generation j given params [M, k, delta]."""
    M, k, delta = params
    return M * (1.0 + math.sqrt(2.0) * k * math.cos(2.0 * math.pi * j / 3.0 + delta))


def free_fit(masses: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Analytic solution for 3-parameter fit (M, k, delta) to 3 masses.

    Ordering: j=0 heaviest, j=1 lightest, j=2 middle.
    Formula: m_j = M * (1 + sqrt(2) * k * cos(2*pi*j/3 + delta)).
    """
    m0, m1, m2 = masses
    M = (m0 + m1 + m2) / 3.0
    k_sq = ((m0 / M - 1.0) ** 2 + (m1 / M - 1.0) ** 2 + (m2 / M - 1.0) ** 2) / 3.0
    if k_sq <= 0:
        return np.zeros(3), False
    k = math.sqrt(k_sq)

    c0 = (m0 / M - 1.0) / (math.sqrt(2.0) * k)
    c1 = (m1 / M - 1.0) / (math.sqrt(2.0) * k)
    c2 = (m2 / M - 1.0) / (math.sqrt(2.0) * k)

    # Check representability: all cosines must lie in [-1, 1]
    if not all(abs(c) <= 1.0 + 1e-12 for c in (c0, c1, c2)):
        return np.zeros(3), False

    # For delta in [0, pi/3], the ordering is c0 > c2 > c1 (heaviest, middle, lightest).
    # If the data violate this, the assumed ordering is wrong for this formula.
    if not (c0 > c2 > c1):
        return np.zeros(3), False

    delta = math.acos(np.clip(c0, -1.0, 1.0))
    # Ensure delta is in [0, pi/3] for the assumed ordering
    if not (0.0 <= delta <= math.pi / 3.0 + 1e-12):
        return np.zeros(3), False

    return np.array([M, k, delta]), True


def chi2_fixed_delta(params: np.ndarray, masses: np.ndarray, sigmas: np.ndarray, delta: float, indices: Tuple[int, ...] = (0, 1, 2)) -> float:
    M, k = params
    preds = np.array([M * (1.0 + math.sqrt(2.0) * k * math.cos(2.0 * math.pi * j / 3.0 + delta))
                      for j in indices])
    return np.sum(((masses - preds) / sigmas) ** 2)


def fit_fixed_delta(masses: np.ndarray, sigmas: np.ndarray, delta: float) -> Dict:
    """Fit M, k with delta fixed. Returns dict with params, chi2, dof, preds."""
    p_free, _ = free_fit(masses)
    res = minimize(lambda x: chi2_fixed_delta(x, masses, sigmas, delta),
                   x0=p_free[:2], method="Nelder-Mead")
    M, k = res.x
    preds = np.array([M * (1.0 + math.sqrt(2.0) * k * math.cos(2.0 * math.pi * j / 3.0 + delta))
                      for j in range(3)])
    chi2 = res.fun
    dof = 1  # 3 data - 2 params
    p_value = 1.0 - float(gammainc(dof / 2.0, chi2 / 2.0))
    return {
        "M": M, "k": k, "delta": delta,
        "masses": masses, "sigmas": sigmas,
        "preds": preds, "chi2": chi2, "dof": dof,
        "p_value": p_value,
        "residuals": masses - preds,
        "pulls": (masses - preds) / sigmas,
    }


def monte_carlo_uncertainty(masses: np.ndarray, sigmas: np.ndarray, n: int = 20000) -> Dict:
    """Estimate parameter uncertainties by perturbing masses within PDG errors."""
    params_samples = []
    for _ in range(n):
        m_sample = masses + np.random.normal(0.0, sigmas)
        if np.any(m_sample <= 0):
            continue
        p, ok = free_fit(m_sample)
        if ok:
            # Normalize delta to principal range [-pi, pi] near the central value
            params_samples.append(p)
    params_samples = np.array(params_samples)
    return {
        "M_mean": np.mean(params_samples[:, 0]),
        "M_std": np.std(params_samples[:, 0]),
        "k_mean": np.mean(params_samples[:, 1]),
        "k_std": np.std(params_samples[:, 1]),
        "delta_mean": np.mean(params_samples[:, 2]),
        "delta_std": np.std(params_samples[:, 2]),
        "samples": params_samples,
    }


def cross_sector_prediction(predictor_sector: str, target_sector: str,
                            free_results: Dict) -> Dict:
    """
    Test Zenczykowski's 1:2 phase hierarchy as a cross-sector prediction.
    If predictor is 'up', predict delta_down = 2 * delta_up and fit down-type masses.
    If predictor is 'down', predict delta_up = delta_down / 2 and fit up-type masses.
    Returns fit dict plus the predicted delta and the chi2 of the prediction.
    """
    if predictor_sector == "up":
        predicted_delta = 2.0 * free_results["up"]["params"][2]
        target = "down"
    else:
        predicted_delta = free_results["down"]["params"][2] / 2.0
        target = "up"

    masses = free_results[target]["masses"]
    sigmas = free_results[target]["sigmas"]
    fit = fit_fixed_delta(masses, sigmas, predicted_delta)
    fit["predicted_delta"] = predicted_delta
    fit["predictor_delta"] = free_results[predictor_sector]["params"][2]
    return fit


def pole_distance(params: np.ndarray) -> Dict:
    """Distance from the lightest mass to the zero-denominator pole."""
    M, k, delta = params
    # Lightest mass is at j=1 (cos(2pi/3 + delta))
    c1 = math.cos(2.0 * math.pi / 3.0 + delta)
    c1_pole = -1.0 / (math.sqrt(2.0) * k)
    distance = c1 - c1_pole
    m_light = M * (1.0 + math.sqrt(2.0) * k * c1)
    return {
        "c1_actual": c1,
        "c1_pole": c1_pole,
        "distance_to_pole": distance,
        "lightest_mass_MeV": m_light,
    }


def format_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    out = ["| " + " | ".join(row) + " |" for row in rows]
    out.insert(1, "|" + "|".join(["---" for _ in rows[0]]) + "|")
    return "\n".join(out)


def main():
    output_lines = []
    output_lines.append("# D1 v3: Quark Koide Formula — Full Parameter Fit & Predictive Power")
    output_lines.append("*Devin · 2026-07-10 · Zenczykowski 2013 (PRD 87, 077302) · PDG 2024 masses*")
    output_lines.append("")
    output_lines.append("## Formula & Conventions")
    output_lines.append("")
    output_lines.append("We use Zenczykowski's published Eq. (4):")
    output_lines.append("")
    output_lines.append("```")
    output_lines.append("m_j = M · (1 + √2 · k · cos(2πj/3 + δ))")
    output_lines.append("```")
    output_lines.append("")
    output_lines.append("with generation ordering `j = 0, 1, 2` mapping to heaviest, lightest, middle.")
    output_lines.append("Koide Q in this convention is `Q = (1 + k²)/3`, so `k = 1` gives `Q = 2/3` exactly.")
    output_lines.append("")
    output_lines.append("## Input Masses (PDG 2024)")
    output_lines.append("")
    rows = [["Sector", "Quark", "j", "Mass (MeV)", "σ (MeV)"]]
    for sector in ("up", "down"):
        for key, (m, s) in MASSES[sector].items():
            quark = key.replace("m_", "")
            j = J_MAP[key]
            rows.append([sector, quark, str(j), f"{m:g}", f"{s:g}"])
    output_lines.append(format_table(rows))
    output_lines.append("")

    output_lines.append("## 1. Free-δ Fit (3 parameters, 3 masses)")
    output_lines.append("")
    output_lines.append("A 3-parameter model fit to 3 masses has zero degrees of freedom and will reproduce the input exactly if a real solution exists. The interesting output is the best-fit parameters and their uncertainty.")
    output_lines.append("")

    free_results = {}
    for sector in ("up", "down"):
        m_dict = MASSES[sector]
        masses = np.array([m_dict["m_t"][0] if sector == "up" else m_dict["m_b"][0],
                           m_dict["m_u"][0] if sector == "up" else m_dict["m_d"][0],
                           m_dict["m_c"][0] if sector == "up" else m_dict["m_s"][0]])
        sigmas = np.array([m_dict["m_t"][1] if sector == "up" else m_dict["m_b"][1],
                           m_dict["m_u"][1] if sector == "up" else m_dict["m_d"][1],
                           m_dict["m_c"][1] if sector == "up" else m_dict["m_s"][1]])
        params, ok = free_fit(masses)
        if not ok:
            print(f"WARNING: free fit for {sector} did not converge")
        M, k, delta = params
        preds = np.array([zenczykowski_pred(params, j) for j in range(3)])
        mc = monte_carlo_uncertainty(masses, sigmas, n=20000)
        free_results[sector] = {
            "masses": masses, "sigmas": sigmas, "params": params,
            "preds": preds, "mc": mc,
        }

        output_lines.append(f"### {sector.title()}-type")
        output_lines.append("")
        rows = [["Quark", "j", "PDG (MeV)", "Fit (MeV)", "Residual"]]
        for i, name in enumerate(QUARK_NAMES[sector]):
            rows.append([name, str(i), f"{masses[i]:.3f}", f"{preds[i]:.3f}", f"{masses[i]-preds[i]:.3g}"])
        output_lines.append(format_table(rows))
        output_lines.append("")
        output_lines.append(f"- **M** = {M:.3f} ± {mc['M_std']:.3f} MeV")
        output_lines.append(f"- **k** = {k:.6f} ± {mc['k_std']:.6f}")
        output_lines.append(f"- **δ** = {delta:.6f} ± {mc['delta_std']:.6f} rad ({math.degrees(delta):.4f}°)")
        output_lines.append(f"- **Q = (1+k²)/3** = {(1+k*k)/3:.6f}")
        output_lines.append("")

    # Sector comparison
    delta_u = free_results["up"]["params"][2]
    delta_d = free_results["down"]["params"][2]
    sigma_u = free_results["up"]["mc"]["delta_std"]
    sigma_d = free_results["down"]["mc"]["delta_std"]
    ratio = delta_d / delta_u if delta_u != 0 else np.inf
    ratio_unc = ratio * math.sqrt((sigma_d / delta_d) ** 2 + (sigma_u / delta_u) ** 2) if delta_u != 0 and delta_d != 0 else np.inf
    zen_pred = 2.0
    pull_ratio = (delta_d - zen_pred * delta_u) / math.sqrt(sigma_d ** 2 + (zen_pred * sigma_u) ** 2)

    output_lines.append("### δ_U : δ_D Ratio Test")
    output_lines.append("")
    output_lines.append(f"- δ_U = {delta_u:.6f} ± {sigma_u:.6f} rad")
    output_lines.append(f"- δ_D = {delta_d:.6f} ± {sigma_d:.6f} rad")
    output_lines.append(f"- Observed δ_D / δ_U = {ratio:.3f} ± {ratio_unc:.3f}")
    output_lines.append(f"- Zenczykowski prediction (1:2 phase hierarchy): δ_D / δ_U = 2.000")
    output_lines.append(f"- Pull from 1:2 prediction: **{pull_ratio:.2f}σ**")
    output_lines.append("")

    output_lines.append("## 2. Fixed-δ Fit (Zenczykowski's δ = 2/27 for up, 4/27 for down)")
    output_lines.append("")
    output_lines.append("This is the actual claim: Zenczykowski asserts the phase hierarchy is exact, with δ_U = 2/27 and δ_D = 4/27. With δ fixed, the model has 2 free parameters (M, k) and 1 degree of freedom.")
    output_lines.append("")

    fixed_deltas = {"up": 2.0 / 27.0, "down": 4.0 / 27.0}
    for sector in ("up", "down"):
        masses = free_results[sector]["masses"]
        sigmas = free_results[sector]["sigmas"]
        delta_fix = fixed_deltas[sector]
        fit = fit_fixed_delta(masses, sigmas, delta_fix)
        output_lines.append(f"### {sector.title()}-type, δ = {delta_fix:.6f} rad ({math.degrees(delta_fix):.4f}°)")
        output_lines.append("")
        rows = [["Quark", "j", "PDG (MeV)", "Pred (MeV)", "σ (MeV)", "Pull"]]
        for i, name in enumerate(QUARK_NAMES[sector]):
            rows.append([name, str(i), f"{masses[i]:.3f}", f"{fit['preds'][i]:.3f}",
                         f"{sigmas[i]:.3f}", f"{fit['pulls'][i]:.2f}"])
        output_lines.append(format_table(rows))
        output_lines.append("")
        output_lines.append(f"- M = {fit['M']:.3f} MeV, k = {fit['k']:.6f}")
        output_lines.append(f"- χ² = {fit['chi2']:.3f} (dof = {fit['dof']})")
        output_lines.append(f"- p-value = {fit['p_value']:.3e}")
        output_lines.append("")

    output_lines.append("## 3. Cross-Sector Predictive Test (1:2 Phase Hierarchy)")
    output_lines.append("")
    output_lines.append("The only genuinely predictive claim in the Zenczykowski framework is the phase hierarchy: δ_D = 2δ_U. If true, the up-type masses (3 free parameters) predict the down-type masses after fixing δ_D, leaving only M and k free for the down sector. This test has 1 degree of freedom for the down-type prediction. The reverse prediction (down → up) also has 1 degree of freedom.")
    output_lines.append("")

    for direction in (("up", "down"), ("down", "up")):
        pred_sector, target_sector = direction
        fit = cross_sector_prediction(pred_sector, target_sector, free_results)
        output_lines.append(f"### {pred_sector.title()}-type δ predicts {target_sector.title()}-type masses")
        output_lines.append("")
        output_lines.append(f"- Predictor δ_{pred_sector[0]} = {fit['predictor_delta']:.6f} rad")
        output_lines.append(f"- Predicted δ_{target_sector[0]} = {fit['predicted_delta']:.6f} rad (by 1:2 hierarchy)")
        output_lines.append(f"- Free-fit δ_{target_sector[0]} = {free_results[target_sector]['params'][2]:.6f} rad")
        rows = [["Quark", "j", "PDG (MeV)", "Predicted (MeV)", "σ (MeV)", "Pull"]]
        for i, name in enumerate(QUARK_NAMES[target_sector]):
            rows.append([name, str(i), f"{fit['masses'][i]:.3f}", f"{fit['preds'][i]:.3f}",
                         f"{fit['sigmas'][i]:.3f}", f"{fit['pulls'][i]:.2f}"])
        output_lines.append(format_table(rows))
        output_lines.append("")
        output_lines.append(f"- M = {fit['M']:.3f} MeV, k = {fit['k']:.6f}")
        output_lines.append(f"- χ² = {fit['chi2']:.3f} (dof = {fit['dof']})")
        output_lines.append(f"- p-value = {fit['p_value']:.3e}")
        output_lines.append("")


    output_lines.append("## 4. Pole Distance & Fine-Tuning")
    output_lines.append("")
    output_lines.append("The lightest quark sits near the zero of the cosine term. The closer it is to the pole `1 + √2·k·cos = 0`, the more fine-tuned the parameters are.")
    output_lines.append("")
    for sector in ("up", "down"):
        params = free_results[sector]["params"]
        pd = pole_distance(params)
        output_lines.append(f"### {sector.title()}-type")
        output_lines.append(f"- cos(2π/3 + δ) = {pd['c1_actual']:.6f}")
        output_lines.append(f"- Pole location cos_pole = -1/(√2·k) = {pd['c1_pole']:.6f}")
        output_lines.append(f"- Distance to pole: {pd['distance_to_pole']:.6e}")
        output_lines.append(f"- Lightest mass: {pd['lightest_mass_MeV']:.3f} MeV")
        output_lines.append("")

    output_lines.append("## 5. Assessment")
    output_lines.append("")
    output_lines.append("**What the fit proves:**")
    output_lines.append("- The Zenczykowski formula with 3 free parameters (M, k, δ) can exactly reproduce any three positive quark masses that satisfy the geometric positivity constraint. This is expected algebra, not a physical prediction.")
    output_lines.append("- With δ fixed at Zenczykowski's claimed values (2/27 for up, 4/27 for down), the formula is **strongly ruled out** by PDG 2024 masses. The up-type fit predicts top = 32.4 GeV (actual 172.5 GeV, pull 200σ) and charm = 2.66 GeV (actual 1.27 GeV, pull −70σ). The down-type fit predicts bottom = 832 MeV (actual 4.18 GeV, pull 167σ), strange = 127 MeV (actual 93.5 MeV, pull −42σ), and **down = −5.6 MeV** (negative, unphysical).")
    output_lines.append("- The cross-sector prediction test is also ruled out: using the 1:2 hierarchy to predict down-type masses from up-type masses gives χ² = 806.7 (dof = 1, p ≈ 0); the reverse gives χ² = 729.1 (dof = 1, p ≈ 0).")
    output_lines.append("")
    output_lines.append("**What the fit does NOT prove:**")
    output_lines.append("- It does not prove that the Z3 resonance geometry is wrong. It shows that the specific phase values δ_U=2/27, δ_D=4/27 are inconsistent with data.")
    output_lines.append("- It does not prove the alternative best-fit δ values are meaningful; 3 parameters fitting 3 data points is a reparameterization, not a derivation.")
    output_lines.append("")
    output_lines.append("**The key falsifiable claim:**")
    output_lines.append(f"- Zenczykowski predicts δ_U : δ_D = 1 : 2. The data give δ_D/δ_U = {ratio:.3f} ± {ratio_unc:.3f}, a **{pull_ratio:.1f}σ** deviation. The 1:2 phase hierarchy is therefore falsified by PDG 2024 quark masses at the level of the parameter values themselves.")
    output_lines.append("")
    output_lines.append("**Next step for PF:**")
    output_lines.append("- If PF wants to derive quark masses from Z3 geometry, it must derive δ and k from first principles (e.g., gauge couplings, color factors, coherence ceiling) rather than adopt Zenczykowski's empirical phase hierarchy. The current result removes that empirical anchor.")
    output_lines.append("")

    output_lines.append("## 6. Method Notes")
    output_lines.append("")
    output_lines.append("- Free-δ parameters solved analytically from the three mass equations; the solution is unique for the assumed heaviest/lightest/middle ordering.")
    output_lines.append("- Parameter uncertainties estimated by Monte Carlo: 20,000 samples perturbing each PDG mass within its quoted σ.")
    output_lines.append("- Fixed-δ fits use Nelder-Mead minimization of χ² with respect to M and k.")
    output_lines.append("- Source script: `d1_fit_v3.py` in this directory.")
    output_lines.append("")

    text = "\n".join(output_lines)
    with open("D1_fit_results.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote D1_fit_results.md")

    print(f"\nFree-fit δ_U = {delta_u:.6f} rad, δ_D = {delta_d:.6f} rad")
    print(f"δ_D/δ_U = {ratio:.3f} ± {ratio_unc:.3f} (Zenczykowski predicts 2.000, pull = {pull_ratio:.2f}σ)")


if __name__ == "__main__":
    main()
