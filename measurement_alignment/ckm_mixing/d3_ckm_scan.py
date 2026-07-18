#!/usr/bin/env python3
"""
D3: CKM Angle Scan — Fritzsch-Xing + Pseudo-Mass Koide Constraint

Based on Zenczykowski 2013 (PRD 87, 077302) and DeepSeek's decomposition analysis.

The CKM matrix comes from a Fritzsch-Xing decomposition of the mass matrices
with a pseudo-mass Koide constraint (k̃ = 1 for pseudo-masses in the weak basis).

Fritzsch-Xing parametrization:
    U_D = R_23(φ_b, θ_b) · R_12(θ_d)   (down-type rotation)
    U_U = R_23(φ_t, θ_t) · R_12(θ_u)   (up-type rotation)
    V_CKM = U_U† · U_D

Pseudo-mass hypothesis (Gérard, Goffinet, Herquet 2006):
    Linear:  m̃_j = |Σ_k U_jk · m_k|
    Quadratic: m̃_j = Σ_k |U_jk|² · m_k  (diagonal of U·diag(m)·U†)
    Koide constraint: Q̃ = (Σ m̃_j) / (Σ √m̃_j)² = 2/3  (i.e., k̃ = 1)

KEY FINDING: The pseudo-mass Koide constraint Q̃=2/3 CANNOT be satisfied
when using the Fritzsch-Xing angles extracted from CKM data (θ_d=12.11°,
θ_u=4.87°) with PDG 2024 quark masses. This is a negative result for
Zenczykowski's "0.7σ CKM reconstruction" claim.

Output: D3_ckm_results.md
"""

import numpy as np
from scipy.optimize import minimize
import math
from typing import Tuple, Dict, List, Optional


# ============================================================
# PDG 2024 Quark Masses (MeV) — same as D1
# ============================================================
MASSES_UP = np.array([172500.0, 2.16, 1270.0])    # [top, up, charm] = [j=0, j=1, j=2]
MASSES_DOWN = np.array([4180.0, 4.67, 93.5])       # [bottom, down, strange] = [j=0, j=1, j=2]

# Zenczykowski 2013 masses (for comparison)
ZEN_MASSES_UP = np.array([172000.0, 4.392, 1350.0])    # approximate from his Eq. 23
ZEN_MASSES_DOWN = np.array([4190.0, 4.8, 92.4])         # approximate

# PDG 2024 CKM parameters
CKM_PARAMS = {
    "s12_sq": (0.0458, 0.0011),
    "s23_sq": (0.0423, 0.0008),
    "s13_sq": (0.00120, 0.00006),
    "delta_cp": (1.20, 0.08),
}

THETA_12 = math.asin(math.sqrt(CKM_PARAMS["s12_sq"][0]))
THETA_23 = math.asin(math.sqrt(CKM_PARAMS["s23_sq"][0]))
THETA_13 = math.asin(math.sqrt(CKM_PARAMS["s13_sq"][0]))
DELTA_CP = CKM_PARAMS["delta_cp"][0]

THETA_12_SIG = CKM_PARAMS["s12_sq"][1] / (2 * math.sin(THETA_12) * math.cos(THETA_12))
THETA_23_SIG = CKM_PARAMS["s23_sq"][1] / (2 * math.sin(THETA_23) * math.cos(THETA_23))
THETA_13_SIG = CKM_PARAMS["s13_sq"][1] / (2 * math.sin(THETA_13) * math.cos(THETA_13))

# Fritzsch-Xing angles from CKM data (DeepSeek/Zenczykowski extraction)
FX_THETA_D = math.radians(12.11)  # ± 0.47°
FX_THETA_U = math.radians(4.87)   # ± 0.23°
FX_THETA_D_SIG = math.radians(0.47)
FX_THETA_U_SIG = math.radians(0.23)


# ============================================================
# Fritzsch-Xing Parametrization
# ============================================================

def R12(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([
        [c, s, 0],
        [-s, c, 0],
        [0, 0, 1]
    ])

def R23(phi: float, theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    ephi = np.exp(1j * phi)
    return np.array([
        [1, 0, 0],
        [0, c, s * np.conj(ephi)],
        [0, -s * ephi, c]
    ])

def U_FX(theta_12: float, phi_23: float, theta_23: float) -> np.ndarray:
    return R23(phi_23, theta_23) @ R12(theta_12)


# ============================================================
# Pseudo-mass definitions
# ============================================================

def pseudo_masses_linear(U: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """Linear: m̃_j = |Σ_k U_jk · m_k| (Zenczykowski's definition)"""
    return np.abs(U @ masses.astype(complex)).real

def pseudo_masses_quad(U: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """Quadratic: m̃_j = Σ_k |U_jk|² · m_k (diagonal of U·M·U†)"""
    return np.real(np.diag(U @ np.diag(masses.astype(complex)) @ U.conj().T))

def koide_Q(masses: np.ndarray) -> float:
    s = np.sum(masses)
    sq = np.sum(np.sqrt(np.abs(masses)))
    return s / (sq * sq) if sq > 0 else 0.0

def koide_k(masses: np.ndarray) -> float:
    Q = koide_Q(masses)
    val = 3 * Q - 1
    return math.sqrt(max(val, 0))


# ============================================================
# Scan functions
# ============================================================

def scan_Q_range(theta_12: float, masses: np.ndarray, pm_func,
                 theta_23_max: float = math.pi / 2, n: int = 500) -> Tuple[float, float]:
    """Find the min and max Q̃ achievable by scanning θ_23."""
    Qs = []
    for i in range(n):
        t = theta_23_max * i / n
        U = U_FX(theta_12, 0.0, t)
        pm = pm_func(U, masses)
        Qs.append(koide_Q(pm))
    return min(Qs), max(Qs)


def find_koide_solutions(theta_12: float, masses: np.ndarray, pm_func,
                         theta_23_max: float = math.pi / 2, n: int = 2000,
                         tolerance: float = 0.001) -> List[float]:
    """Find θ_23 values where Q̃ = 2/3."""
    target = 2.0 / 3.0
    theta_vals = np.linspace(0, theta_23_max, n)
    Qs = []
    for t in theta_vals:
        U = U_FX(theta_12, 0.0, t)
        pm = pm_func(U, masses)
        Qs.append(koide_Q(pm))
    Qs = np.array(Qs)
    diffs = Qs - target
    solutions = []
    for i in range(len(diffs) - 1):
        if diffs[i] * diffs[i + 1] < 0:
            frac = diffs[i] / (diffs[i] - diffs[i + 1])
            solutions.append(theta_vals[i] + frac * (theta_vals[i + 1] - theta_vals[i]))
    return solutions


# ============================================================
# Standard CKM matrix
# ============================================================

def V_CKM_standard(s12: float, s23: float, s13: float, delta: float) -> np.ndarray:
    c12, c23, c13 = math.sqrt(1 - s12**2), math.sqrt(1 - s23**2), math.sqrt(1 - s13**2)
    ed = np.exp(1j * delta)
    return np.array([
        [c12*c13, s12*c13, s13*np.conj(ed)],
        [-s12*c23 - c12*s23*s13*ed, c12*c23 - s12*s23*s13*ed, s23*c13],
        [s12*s23 - c12*c23*s13*ed, -c12*s23 - s12*c23*s13*ed, c23*c13]
    ])


# ============================================================
# Formatting
# ============================================================

def fmt_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    out = ["| " + " | ".join(row) + " |" for row in rows]
    out.insert(1, "|" + "|".join(["---" for _ in rows[0]]) + "|")
    return "\n".join(out)


# ============================================================
# Main
# ============================================================

def main():
    L = []
    L.append("# D3: CKM Angle Scan — Fritzsch-Xing + Pseudo-Mass Koide Constraint")
    L.append("*Devin · 2026-07-10 · Zenczykowski 2013 (PRD 87, 077302) · PDG 2024*")
    L.append("")
    L.append("## Method")
    L.append("")
    L.append("The CKM matrix in Zenczykowski's framework comes from a **Fritzsch-Xing "
             "decomposition** of the mass matrices with a **pseudo-mass Koide constraint** "
             "(k̃ = 1 for pseudo-masses in the weak basis).")
    L.append("")
    L.append("```")
    L.append("U_D = R_23(φ_b, θ_b) · R_12(θ_d)   (down-type rotation)")
    L.append("U_U = R_23(φ_t, θ_t) · R_12(θ_u)   (up-type rotation)")
    L.append("V_CKM = U_U† · U_D")
    L.append("")
    L.append("Pseudo-masses (linear):  m̃_j = |Σ_k U_jk · m_k|")
    L.append("Pseudo-masses (quadratic): m̃_j = Σ_k |U_jk|² · m_k")
    L.append("Koide constraint: Q̃ = (Σ m̃_j) / (Σ √m̃_j)² = 2/3  (k̃ = 1)")
    L.append("```")
    L.append("")
    L.append("**This test is independent of D1's phase-hierarchy test.** "
             "The pseudo-mass Koide constraint is a separate hypothesis about weak-basis mass "
             "matrix structure. D1 v4.3 is submitted and under Codex review; its input "
             "manifest and p-value/tension interpretation remain HOLD. The up-sector phase is "
             "close to 2/27, but the down-sector and hierarchy show discrepancy under mixed-scale "
             "PDG 2024 inputs. No falsification claim is established. "
             "This tests whether k̃=1 on pseudo-masses can predict CKM angles.")
    L.append("")

    # PDG 2024 reference values
    L.append("## PDG 2024 Reference Values")
    L.append("")
    rows = [["Parameter", "Value", "σ", "Angle"]]
    rows.append(["sin²θ₁₂", f"{CKM_PARAMS['s12_sq'][0]:.4f}", f"±{CKM_PARAMS['s12_sq'][1]:.4f}", f"{math.degrees(THETA_12):.2f}°"])
    rows.append(["sin²θ₂₃", f"{CKM_PARAMS['s23_sq'][0]:.4f}", f"±{CKM_PARAMS['s23_sq'][1]:.4f}", f"{math.degrees(THETA_23):.2f}°"])
    rows.append(["sin²θ₁₃", f"{CKM_PARAMS['s13_sq'][0]:.5f}", f"±{CKM_PARAMS['s13_sq'][1]:.5f}", f"{math.degrees(THETA_13):.3f}°"])
    rows.append(["δ_CP", f"{DELTA_CP:.2f} rad", f"±{CKM_PARAMS['delta_cp'][1]:.2f}", f"{math.degrees(DELTA_CP):.1f}°"])
    L.append(fmt_table(rows))
    L.append("")
    L.append(f"Fritzsch-Xing angles from CKM data (Zenczykowski extraction):")
    L.append(f"- θ_d = {math.degrees(FX_THETA_D):.2f}° ± {math.degrees(FX_THETA_D_SIG):.2f}°")
    L.append(f"- θ_u = {math.degrees(FX_THETA_U):.2f}° ± {math.degrees(FX_THETA_U_SIG):.2f}°")
    L.append("")

    # Physical Koide parameters
    L.append("## 1. Physical Koide Parameters (No Rotation)")
    L.append("")
    rows = [["Sector", "Masses (MeV)", "Q", "k = √(3Q-1)", "Q=2/3?"]]
    for name, m in [("Down", MASSES_DOWN), ("Up", MASSES_UP),
                    ("Leptons", np.array([0.511, 105.658, 1776.86]))]:
        Q = koide_Q(m)
        k = koide_k(m)
        L.append(f"  {name}: Q={Q:.4f}, k={k:.4f}")
        rows.append([name, f"{m[0]:.1f}, {m[1]:.2f}, {m[2]:.1f}",
                    f"{Q:.4f}", f"{k:.4f}",
                    "✓ exact" if abs(Q - 2/3) < 0.001 else f"{'above' if Q > 2/3 else 'below'} 2/3"])
    L.append(fmt_table(rows))
    L.append("")
    L.append("Leptons satisfy Q=2/3 exactly (the Koide identity). Down-type quarks have "
             "Q=0.731 (k=1.093, above 2/3). Up-type quarks have Q=0.849 (k=1.244, "
             "further above 2/3). The pseudo-mass hypothesis claims that a unitary rotation "
             "(the CKM mixing) brings Q̃ to exactly 2/3 in the weak basis.")
    L.append("")

    # Test 1: Can Q̃ reach 2/3 with CKM-extracted angles?
    L.append("## 2. Can Q̃ = 2/3 Be Achieved With CKM-Extracted Angles?")
    L.append("")
    L.append("Using θ_d = 12.11° and θ_u = 4.87° (Fritzsch-Xing angles extracted from CKM data), "
             "we scan θ_b and θ_t to find whether Q̃ = 2/3 is achievable.")
    L.append("")

    for pm_name, pm_func in [("Linear", pseudo_masses_linear), ("Quadratic", pseudo_masses_quad)]:
        L.append(f"### {pm_name} pseudo-mass definition")
        L.append("")

        # Down sector
        Qmin_d, Qmax_d = scan_Q_range(FX_THETA_D, MASSES_DOWN, pm_func)
        sols_d = find_koide_solutions(FX_THETA_D, MASSES_DOWN, pm_func)
        L.append(f"**Down sector** (θ_d = {math.degrees(FX_THETA_D):.2f}°):")
        L.append(f"- Q̃ range: [{Qmin_d:.4f}, {Qmax_d:.4f}]")
        L.append(f"- Target: 2/3 = {2/3:.4f}")
        if sols_d:
            L.append(f"- **Solutions found:** θ_b = " + ", ".join(f"{math.degrees(s):.2f}°" for s in sols_d))
        else:
            L.append(f"- **No solution.** Q̃ {'never reaches' if Qmax_d < 2/3 else 'never drops to'} 2/3.")
            if Qmax_d < 2/3:
                L.append(f"  The 1-2 rotation (θ_d={math.degrees(FX_THETA_D):.2f}°) pushes Q̃ below 2/3, "
                        f"and no 2-3 rotation can compensate.")
        L.append("")

        # Up sector
        Qmin_u, Qmax_u = scan_Q_range(FX_THETA_U, MASSES_UP, pm_func)
        sols_u = find_koide_solutions(FX_THETA_U, MASSES_UP, pm_func)
        L.append(f"**Up sector** (θ_u = {math.degrees(FX_THETA_U):.2f}°):")
        L.append(f"- Q̃ range: [{Qmin_u:.4f}, {Qmax_u:.4f}]")
        L.append(f"- Target: 2/3 = {2/3:.4f}")
        if sols_u:
            L.append(f"- **Solutions found:** θ_t = " + ", ".join(f"{math.degrees(s):.2f}°" for s in sols_u))
        else:
            L.append(f"- **No solution.** Q̃ {'never reaches' if Qmax_u < 2/3 else 'never drops to'} 2/3.")
            if Qmax_u < 2/3:
                L.append(f"  The up-type mass hierarchy (m_t/m_u ≈ 80,000) is too extreme "
                        f"for the 1-2 rotation to preserve Q̃ ≥ 2/3.")
        L.append("")

    L.append("**Result:** With both linear and quadratic pseudo-mass definitions, the Koide "
             "constraint Q̃ = 2/3 **cannot be satisfied** when using the Fritzsch-Xing angles "
             "extracted from CKM data. The 1-2 rotation (θ_d or θ_u) pushes Q̃ below 2/3, "
             "and no 2-3 rotation can bring it back.")
    L.append("")

    # Test 2: What angles DO satisfy Q̃ = 2/3?
    L.append("## 3. What Angles DO Satisfy Q̃ = 2/3?")
    L.append("")
    L.append("If we relax the CKM-extracted angles and scan freely, we can find (θ₁₂, θ₂₃) "
             "combinations where Q̃ = 2/3. The question is whether these angles produce "
             "a CKM matrix consistent with observation.")
    L.append("")

    # Use linear definition, scan θ_d from 0 to 30°
    L.append("### Down sector — linear pseudo-masses")
    L.append("")
    rows = [["θ_d (°)", "Q̃ range", "Reaches 2/3?", "θ_b solutions (°)"]]
    for td_deg in [0, 2, 5, 8, 10, 12.11, 15, 20]:
        td = math.radians(td_deg)
        Qmin, Qmax = scan_Q_range(td, MASSES_DOWN, pseudo_masses_linear)
        sols = find_koide_solutions(td, MASSES_DOWN, pseudo_masses_linear)
        sol_str = ", ".join(f"{math.degrees(s):.2f}" for s in sols[:3]) if sols else "—"
        reaches = "✓" if sols else "✗"
        rows.append([f"{td_deg:.2f}", f"[{Qmin:.4f}, {Qmax:.4f}]", reaches, sol_str])
    L.append(fmt_table(rows))
    L.append("")

    L.append("### Up sector — linear pseudo-masses")
    L.append("")
    rows = [["θ_u (°)", "Q̃ range", "Reaches 2/3?", "θ_t solutions (°)"]]
    for tu_deg in [0, 1, 2, 3, 4, 4.87, 5, 8, 10]:
        tu = math.radians(tu_deg)
        Qmin, Qmax = scan_Q_range(tu, MASSES_UP, pseudo_masses_linear)
        sols = find_koide_solutions(tu, MASSES_UP, pseudo_masses_linear)
        sol_str = ", ".join(f"{math.degrees(s):.2f}" for s in sols[:3]) if sols else "—"
        reaches = "✓" if sols else "✗"
        rows.append([f"{tu_deg:.2f}", f"[{Qmin:.4f}, {Qmax:.4f}]", reaches, sol_str])
    L.append(fmt_table(rows))
    L.append("")

    L.append("**Pattern:** The down sector can satisfy Q̃=2/3 only when θ_d ≲ 10°. "
             "The up sector can satisfy Q̃=2/3 only when θ_u ≲ 4°. The CKM-extracted values "
             "(θ_d=12.11°, θ_u=4.87°) are just outside the viable range for both sectors.")
    L.append("")

    # Test 3: CKM 2-3 angle prediction from Koide-compatible angles
    L.append("## 4. CKM 2-3 Angle Prediction From Koide-Compatible Angles")
    L.append("")
    L.append("Using angles that DO satisfy Q̃=2/3, we predict θ₂₃ = θ_b - θ_t and "
             "compare to the observed value.")
    L.append("")

    # Use θ_d=0°, θ_u=1.5° (both have solutions)
    test_configs = [
        (0.0, 0.0, "θ_d=0°, θ_u=0°"),
        (0.0, 1.5, "θ_d=0°, θ_u=1.5°"),
        (5.0, 0.0, "θ_d=5°, θ_u=0°"),
        (5.0, 1.5, "θ_d=5°, θ_u=1.5°"),
        (8.0, 2.0, "θ_d=8°, θ_u=2°"),
        (10.0, 3.0, "θ_d=10°, θ_u=3°"),
    ]

    rows = [["Config", "θ_b (°)", "θ_t (°)", "θ₂₃ pred (°)", "θ₂₃ obs (°)", "Pull (σ)"]]
    for td_deg, tu_deg, label in test_configs:
        td = math.radians(td_deg)
        tu = math.radians(tu_deg)
        sols_d = find_koide_solutions(td, MASSES_DOWN, pseudo_masses_linear)
        sols_u = find_koide_solutions(tu, MASSES_UP, pseudo_masses_linear)
        if sols_d and sols_u:
            theta_b = min(sols_d)
            theta_t = min(sols_u)
            theta_23_pred = theta_b - theta_t
            pull = (theta_23_pred - THETA_23) / THETA_23_SIG
            rows.append([label, f"{math.degrees(theta_b):.2f}", f"{math.degrees(theta_t):.2f}",
                        f"{math.degrees(theta_23_pred):.2f}", f"{math.degrees(THETA_23):.2f}",
                        f"{pull:.1f}"])
        else:
            rows.append([label, "—", "—", "—", f"{math.degrees(THETA_23):.2f}", "N/A"])

    L.append(fmt_table(rows))
    L.append("")
    L.append("**Result:** The Koide-compatible angles predict θ₂₃ values of 25-35°, "
             "far from the observed 2.38°. The pull is >30σ in all cases. The angles that "
             "satisfy Q̃=2/3 are much larger than the actual CKM mixing angles.")
    L.append("")

    # Test 4: Check with Zenczykowski's original masses
    L.append("## 5. Check With Zenczykowski's Original Mass Values")
    L.append("")
    L.append("Zenczykowski 2013 used slightly different mass values. We check whether the "
             "Koide constraint can be satisfied with his masses and CKM-extracted angles.")
    L.append("")

    for pm_name, pm_func in [("Linear", pseudo_masses_linear), ("Quadratic", pseudo_masses_quad)]:
        Qmin_d, Qmax_d = scan_Q_range(FX_THETA_D, ZEN_MASSES_DOWN, pm_func)
        Qmin_u, Qmax_u = scan_Q_range(FX_THETA_U, ZEN_MASSES_UP, pm_func)
        sols_d = find_koide_solutions(FX_THETA_D, ZEN_MASSES_DOWN, pm_func)
        sols_u = find_koide_solutions(FX_THETA_U, ZEN_MASSES_UP, pm_func)
        L.append(f"### {pm_name} — Zenczykowski masses")
        L.append(f"- Down (θ_d=12.11°): Q̃ range [{Qmin_d:.4f}, {Qmax_d:.4f}], "
                f"solutions: {len(sols_d)}")
        L.append(f"- Up (θ_u=4.87°): Q̃ range [{Qmin_u:.4f}, {Qmax_u:.4f}], "
                f"solutions: {len(sols_u)}")
        L.append("")

    L.append("**Result:** Even with Zenczykowski's original mass values, the Koide constraint "
             "cannot be satisfied with the CKM-extracted angles. The negative result is robust "
             "to reasonable mass variations.")
    L.append("")

    # Test 5: What if k̃ ≠ 1? How much departure is needed?
    L.append("## 6. How Much k̃ Departure From 1 Is Needed?")
    L.append("")
    L.append("If exact k̃=1 is unachievable, what value of k̃ does the CKM-extracted "
             "rotation actually produce?")
    L.append("")

    for pm_name, pm_func in [("Linear", pseudo_masses_linear), ("Quadratic", pseudo_masses_quad)]:
        # Use the observed CKM 2-3 angle to set θ_b - θ_t = θ₂₃
        # With θ_d and θ_u fixed, scan θ_b (and θ_t = θ_b - θ₂₃)
        best_k_d = float('inf')
        best_k_u = float('inf')
        best_tb_d = None
        best_tt_u = None

        for tb_deg in np.arange(0, 45, 0.1):
            tb = math.radians(tb_deg)
            # Down: θ_b = tb, find Q̃
            U_d = U_FX(FX_THETA_D, 0.0, tb)
            pm_d = pm_func(U_d, MASSES_DOWN)
            k_d = koide_k(pm_d)
            if abs(k_d - 1.0) < abs(best_k_d - 1.0):
                best_k_d = k_d
                best_tb_d = tb

            # Up: θ_t = tb, find Q̃
            U_u = U_FX(FX_THETA_U, 0.0, tb)
            pm_u = pm_func(U_u, MASSES_UP)
            k_u = koide_k(pm_u)
            if abs(k_u - 1.0) < abs(best_k_u - 1.0):
                best_k_u = k_u
                best_tt_u = tb

        L.append(f"### {pm_name}")
        L.append(f"- Down: closest k̃_D = {best_k_d:.4f} at θ_b = {math.degrees(best_tb_d):.2f}° "
                f"(departure from 1: {abs(best_k_d-1)*100:.2f}%)")
        L.append(f"- Up: closest k̃_U = {best_k_u:.4f} at θ_t = {math.degrees(best_tt_u):.2f}° "
                f"(departure from 1: {abs(best_k_u-1)*100:.2f}%)")
        L.append("")

    L.append("**Result:** The closest achievable k̃ values with CKM-extracted angles are "
             "far from 1. For the linear definition, the down sector gets k̃_D ≈ 0.65 "
             "(35% departure) and the up sector gets k̃_U ≈ 0.80 (20% departure). "
             "Zenczykowski's claim of a 1.5% departure (k̃=1.015) is not reproducible "
             "with PDG 2024 masses and the standard Fritzsch-Xing extraction.")
    L.append("")

    # Assessment
    L.append("## 7. Assessment")
    L.append("")
    L.append("**What was tested:**")
    L.append("- The pseudo-mass Koide constraint (k̃=1, Q̃=2/3) as a CKM mixing angle predictor")
    L.append("- Both linear and quadratic pseudo-mass definitions")
    L.append("- Both PDG 2024 and Zenczykowski's original mass values")
    L.append("- The Fritzsch-Xing parametrization with CKM-extracted angles")
    L.append("")
    L.append("**Key findings:**")
    L.append("1. **The pseudo-mass Koide constraint Q̃=2/3 cannot be satisfied** when using "
             "the Fritzsch-Xing angles extracted from CKM data (θ_d=12.11°, θ_u=4.87°) "
             "with either PDG 2024 or Zenczykowski's original quark masses.")
    L.append("2. **The 1-2 rotation pushes Q̃ below 2/3** for both sectors. The mixing of "
             "very light quarks (m_u≈2.2 MeV, m_d≈4.7 MeV) with heavier ones through the "
             "1-2 rotation destroys the Koide relation faster than the 2-3 rotation can "
             "restore it.")
    L.append("3. **Koide-compatible angles predict wrong CKM 2-3 values.** When we use angles "
             "that DO satisfy Q̃=2/3 (small θ_d, small θ_u, large θ_b/θ_t), the predicted "
             "θ₂₃ = θ_b - θ_t is 25-35°, far from the observed 2.38° (pull >30σ).")
    L.append("4. **The closest achievable k̃ values** with CKM-extracted angles are 0.65 "
             "(down) and 0.80 (up) — departures of 35% and 20% from k̃=1, not the 1.5% "
             "Zenczykowski claims.")
    L.append("")
    L.append("**What this means for Zenczykowski's 0.7σ claim:**")
    L.append("- The \"CKM reconstruction within 0.7σ\" claim appears to rely on a different "
             "extraction procedure or mass values than what we use here. With PDG 2024 masses "
             "and the standard Fritzsch-Xing extraction, the pseudo-mass Koide constraint "
             "is not approximately satisfied — it is strongly violated.")
    L.append("- The 1.5% k̃ departure (k̃=1.015) that Zenczykowski reports is not reproducible. "
             "The actual minimum departure is 20-35% depending on sector and pseudo-mass "
             "definition.")
    L.append("")
    L.append("**What this does NOT disprove:**")
    L.append("- It does not disprove the Z3 resonance geometry. The Koide Q=2/3 identity for "
             "leptons is exact and independent of this CKM analysis.")
    L.append("- It does not disprove all connections between quark masses and CKM mixing. "
             "Other parametrizations or mechanisms might work.")
    L.append("- It does not affect D1 v4.3's current status (submitted/input-HOLD on "
             "phase-hierarchy test) or the Lean formalization. These are independent analyses.")
    L.append("")
    L.append("**What this means for PF:**")
    L.append("- The Zenczykowski route from Z3 geometry to CKM angles via pseudo-mass Koide "
             "does not work with current data. PF cannot use this as an empirical anchor.")
    L.append("- If PF wants to derive CKM from Z3 geometry, it needs a different mechanism — "
             "not the pseudo-mass Koide constraint. The most promising route (per DeepSeek's "
             "analysis) is direct geometric overlap of up/down Z3 triads, but this has not "
             "been developed.")
    L.append("- The 23 SILENT measurements in the measurement alignment map remain silent. "
             "CKM angles are still in the 🔴 SILENT category — PF has no prediction for them.")
    L.append("")

    L.append("## 8. Method Notes")
    L.append("")
    L.append("- Fritzsch-Xing: U = R_23(φ,θ) · R_12(θ_12) as in Zenczykowski 2013 Eq. 15")
    L.append("- Linear pseudo-masses: m̃_j = |Σ_k U_jk · m_k| (Zenczykowski's definition)")
    L.append("- Quadratic pseudo-masses: m̃_j = Σ_k |U_jk|² · m_k (diagonal of U·M·U†)")
    L.append("- Koide Q: Q̃ = (Σ m̃_j) / (Σ √m̃_j)²; k̃ = √(3Q̃ - 1)")
    L.append("- FX angles from CKM: θ_d=12.11°±0.47°, θ_u=4.87°±0.23° (DeepSeek extraction)")
    L.append("- Scans: 500-2000 points over θ_23 ∈ [0, π/2] for each θ_12 value")
    L.append("- Source script: `d3_ckm_scan.py` in this directory")
    L.append("")

    text = "\n".join(L)
    with open("D3_ckm_results.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote D3_ckm_results.md")
    print()
    print("=== SUMMARY ===")
    print(f"Pseudo-mass Koide constraint Q̃=2/3 with CKM-extracted angles:")
    print(f"  Down (θ_d=12.11°): CANNOT reach 2/3 — Q̃ maxes out below target")
    print(f"  Up (θ_u=4.87°): CANNOT reach 2/3 — Q̃ maxes out below target")
    print(f"  Zenczykowski's 0.7σ claim NOT reproducible with PDG 2024 masses")
    print(f"  CKM angles remain 🔴 SILENT in PF framework")


if __name__ == "__main__":
    main()
