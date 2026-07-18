#!/usr/bin/env python3
"""
D2: Tau anomalous magnetic moment prediction from PF coherence ceiling.

Formula from PF task spec / PROPAGATION_MANUSCRIPT.md MAX-1:
    delta a_tau = w_max / (m_tau / lambda_c * (hbar c)^-1)

Evaluated in natural units where hbar*c = 1 and lambda_c is measured in MeV^-1:
    delta a_tau = w_max * lambda_c / m_tau

w_max is taken as the maximum topological winding from the Z2 spin structure = 2.

Output: D2_tau_g2_prediction.md
"""

import numpy as np
import math

# Constants
M_TAU_MEV = 1776.86          # PDG 2024 tau mass (MeV)
M_TAU_SIGMA_MEV = 0.12       # PDG uncertainty (MeV)

LAMBDA_C_M = 1.157e-18       # CLAIMS.md ARGUED 0.60 (m)
LAMBDA_C_SIGMA_M = 0.017e-18 # ~1.5% error from God Equation 1.48% mismatch

HBAR_C_MEV_M = 1.97327e-13   # MeV * m
HBAR_C_MEV_FM = 197.327      # MeV * fm

W_MAX = 2.0                  # topological winding from Z2 spin structure
W_MAX_SIGMA = 1.0            # argued integer; ±1 covers Z2/Z3 ambiguity roughly

A_TAU_SM = 1177.21e-6        # Standard Model a_tau = (g-2)/2
A_TAU_SM_SIGMA = 0.05e-6     # SM uncertainty

BELLE_II_TARGET = 1e-5       # manuscript feasibility: 10^-5 precision


def natural_lambda(lambda_si_m: float) -> float:
    """Convert SI length to natural units (MeV^-1)."""
    return lambda_si_m / HBAR_C_MEV_M


def delta_a_tau(w_max: float, lambda_natural: float, m_tau: float) -> float:
    """PF prediction: delta a_tau = w_max * lambda_c / m_tau (natural units)."""
    return w_max * lambda_natural / m_tau


def alternative_delta_a_tau(w_max: float, m_ceiling: float) -> float:
    """Alternative interpretation: delta a_tau = w_max / m_ceiling (natural units)."""
    return w_max / m_ceiling


def monte_carlo_uncertainty(n: int = 50000) -> dict:
    """Propagate uncertainties on m_tau, lambda_c, and w_max."""
    m_samples = np.random.normal(M_TAU_MEV, M_TAU_SIGMA_MEV, n)
    lambda_si_samples = np.random.normal(LAMBDA_C_M, LAMBDA_C_SIGMA_M, n)
    lambda_nat_samples = lambda_si_samples / HBAR_C_MEV_M
    w_samples = np.random.normal(W_MAX, W_MAX_SIGMA, n)

    # Ensure positive samples
    mask = (m_samples > 0) & (lambda_nat_samples > 0) & (w_samples > 0)
    da = delta_a_tau(w_samples[mask], lambda_nat_samples[mask], m_samples[mask])

    return {
        "mean": float(np.mean(da)),
        "std": float(np.std(da)),
        "median": float(np.median(da)),
        "p16": float(np.percentile(da, 16)),
        "p84": float(np.percentile(da, 84)),
        "samples": da,
    }


def format_number(x: float, decimals: int = 3) -> str:
    if x == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / (10 ** exp)
    return f"{mant:.{decimals}f} × 10^{exp}"


def main():
    lambda_c_natural = natural_lambda(LAMBDA_C_M)
    da = delta_a_tau(W_MAX, lambda_c_natural, M_TAU_MEV)
    mc = monte_carlo_uncertainty()

    # Ceiling mass interpretation: m_t = hbar c / lambda_c
    m_ceiling_mev = HBAR_C_MEV_M / LAMBDA_C_M
    da_alt = alternative_delta_a_tau(W_MAX, m_ceiling_mev)

    # Belle II sensitivity needed to detect PF prediction at 2-sigma
    sigma_needed = da / 2.0
    sigma_needed_conservative = (da + mc["std"]) / 2.0

    lines = []
    lines.append("# D2: Tau Anomalous Magnetic Moment Prediction")
    lines.append("*Devin · 2026-07-10 · PF coherence-ceiling framework · PDG 2024*")
    lines.append("")
    lines.append("## Formula & Conventions")
    lines.append("")
    lines.append("The task specifies the PF prediction:")
    lines.append("")
    lines.append("```")
    lines.append("δa_τ = w_max / (m_τ / λ_c · (ħc)⁻¹)")
    lines.append("```")
    lines.append("")
    lines.append("This evaluates to:")
    lines.append("")
    lines.append("```")
    lines.append("δa_τ = w_max · λ_c · ħc / m_τ")
    lines.append("```")
    lines.append("")
    lines.append("In **natural units** (ħc = 1, length measured in MeV⁻¹):")
    lines.append("")
    lines.append("```")
    lines.append("λ_c^natural = λ_c^SI / (ħc) = 1.157×10⁻¹⁸ m / 1.97327×10⁻¹³ MeV·m")
    lines.append("δa_τ = w_max · λ_c^natural / m_τ")
    lines.append("```")
    lines.append("")
    lines.append("")
    lines.append("## Input Parameters")
    lines.append("")
    lines.append(f"| Parameter | Value | Uncertainty | Source |")
    lines.append(f"|---|---|---|---|")
    lines.append(f"| m_τ | {M_TAU_MEV} MeV | ±{M_TAU_SIGMA_MEV} MeV | PDG 2024 |")
    lines.append(f"| λ_c | 1.157×10⁻¹⁸ m | ±{LAMBDA_C_SIGMA_M:.3e} m | CLAIMS.md, ARGUED 0.60 |")
    lines.append(f"| ħc | 1.97327×10⁻¹³ MeV·m | — | defined |")
    lines.append(f"| w_max | {W_MAX} | ±{W_MAX_SIGMA} | PF manuscript: Z₂ spin structure winding |")
    lines.append(f"| a_τ^SM | 1177.21×10⁻⁶ | ±0.05×10⁻⁶ | Standard Model QED |")
    lines.append("")
    lines.append(f"Natural-unit λ_c = {lambda_c_natural:.6e} MeV⁻¹")
    lines.append(f"Implied ceiling mass m_t = ħc/λ_c = {m_ceiling_mev:.1f} MeV = {m_ceiling_mev/1e3:.2f} GeV")
    lines.append("")

    lines.append("## 1. What λ_c Is in PF (Targeted Search)")
    lines.append("")
    lines.append("I searched the canonical PF documents for a physical definition of λ_c in MeV:")
    lines.append("")
    lines.append("- `/mnt/d/Fundamentals/derivations/lambda_c_from_axioms.md` (the God Equation derivation)")
    lines.append("- `/mnt/d/Fundamentals/definitions/coherence.md` (canonical coherence definition)")
    lines.append("- `/mnt/d/Fundamentals/PROPAGATION_MANUSCRIPT.md` (MAX-1 and surrounding context)")
    lines.append("")
    lines.append("### Finding")
    lines.append("")
    lines.append(f"**λ_c is identified with the top quark Compton wavelength:** λ_c = ħc/m_t ≈ 1.14 × 10⁻¹⁸ m, corresponding to m_t ≈ 173 GeV.")
    lines.append(f"Using the CLAIMS.md value λ_c = 1.157 × 10⁻¹⁸ m gives m_t = ħc/λ_c ≈ {m_ceiling_mev/1e3:.2f} GeV.")
    lines.append("")
    lines.append("This identification is **calibrated / empirical**, not derived from PF axioms. The `lambda_c_from_axioms.md` document explicitly states:")
    lines.append("")
    lines.append("> λ_c ≈ 1.14 × 10⁻¹⁸ m (matter coherence scale) is currently calibrated to the top quark mass, not derived from axioms.")
    lines.append("")
    lines.append("The `definitions/coherence.md` file lists the open question:")
    lines.append("")
    lines.append("> Can 'coherence ceiling' be defined as a precise functional rather than a phrase? | OPEN")
    lines.append("")
    lines.append("### Consequence for D2")
    lines.append("")
    lines.append("- λ_c is pinned as the top Compton wavelength, but **the formula that uses it is not dimensionally closed**. See Section 5.")
    lines.append("- The literal-formula numerics are ~6.6 × 10⁻⁹; the ceiling-mass numerics are ~1.17 × 10⁻⁵. These differ by a factor of m_τ and **both are unit-stripped outputs, not dimensionally valid predictions of a dimensionless anomalous magnetic moment.")
    lines.append("")

    lines.append("## 2. PF Prediction (Formula As Written)")
    lines.append("")
    lines.append(f"**δa_τ = {format_number(da, 3)}**")
    lines.append("")
    lines.append(f"Monte Carlo uncertainty (m_τ, λ_c, w_max): **{format_number(mc['std'], 2)}** (68% interval)")
    lines.append(f"68% interval: [{format_number(mc['p16'], 2)}, {format_number(mc['p84'], 2)}]")
    lines.append("")
    lines.append(f"Relative to SM: δa_τ / a_τ^SM = {da / A_TAU_SM:.2e}")
    lines.append(f"Relative to SM uncertainty: δa_τ / σ_SM = {da / A_TAU_SM_SIGMA:.2f}σ")
    lines.append("")

    lines.append("## 3. Alternative Interpretation (Coherence Ceiling Mass)")
    lines.append("")
    lines.append("The PF manuscript prose says the correction is 'proportional to the topological winding number divided by the coherence ceiling mass.' If the coherence ceiling mass is m_t = ħc/λ_c, the formula would be:")
    lines.append("")
    lines.append("```")
    lines.append("δa_τ = w_max / m_t")
    lines.append("```")
    lines.append("")
    lines.append(f"**δa_τ^alt = {format_number(da_alt, 3)}**")
    lines.append("")
    lines.append(f"This is {da_alt / A_TAU_SM:.2e} of the SM value and {da_alt / A_TAU_SM_SIGMA:.1f}σ of the SM uncertainty.")
    lines.append("")

    lines.append("## 4. Comparison with Belle II Sensitivity")
    lines.append("")
    lines.append(f"Belle II feasibility target (PF manuscript): **σ(a_τ) ≈ {BELLE_II_TARGET}**")
    lines.append("")
    lines.append("### Formula-as-written prediction")
    lines.append(f"- PF δa_τ = {format_number(da, 3)}")
    lines.append(f"- Belle II σ = {BELLE_II_TARGET}")
    lines.append(f"- PF signal / Belle II precision = {da / BELLE_II_TARGET:.2e}")
    lines.append(f"- **Conclusion:** Belle II at 10⁻⁵ would measure a_τ consistent with pure QED; the PF correction is ~{BELLE_II_TARGET/da:.0f}× below the projected precision.")
    lines.append(f"- Sensitivity needed for 2σ detection: **σ(a_τ) < {format_number(sigma_needed, 2)}**")
    lines.append("")
    lines.append("### Alternative ceiling-mass interpretation")
    lines.append(f"- PF δa_τ^alt = {format_number(da_alt, 3)}")
    lines.append(f"- PF signal / Belle II precision = {da_alt / BELLE_II_TARGET:.2f}")
    lines.append(f"- **Conclusion:** Belle II at 10⁻⁵ could detect or constrain this correction.")
    lines.append("")

    lines.append("## 5. Dimensional Analysis")
    lines.append("")
    lines.append("An anomalous magnetic moment `a = (g-2)/2` is **dimensionless**. The PF formula must produce a dimensionless number. It does not, under either reading.")
    lines.append("")
    lines.append("In natural units (ħc = 1), λ_c has dimensions of inverse mass. The formula as written is:")
    lines.append("")
    lines.append("```")
    lines.append("δa_τ = w_max / (m_τ / λ_c)")
    lines.append("```")
    lines.append("")
    lines.append("Since λ_c ~ 1/m_t, this becomes:")
    lines.append("")
    lines.append("```")
    lines.append("δa_τ ~ w_max / (m_τ · m_t)")
    lines.append("```")
    lines.append("")
    lines.append("If `w_max` is a pure winding number (dimensionless), the right-hand side has dimensions **mass⁻²**, not dimensionless. The reported number 6.6 × 10⁻⁹ is what remains after stripping the units.")
    lines.append("")
    lines.append("The ceiling-mass reading `δa_τ = w_max / m_t` has dimensions **mass⁻¹**, still not dimensionless. The reported number 1.17 × 10⁻⁵ is likewise unit-stripped.")
    lines.append("")
    lines.append("**Conclusion:** PF has not yet dimensionally closed lepton g-2. Neither reading of the stated formula yields a dimensionless prediction. The two numbers are not competing interpretations of a valid formula; they are two different ways of mishandling the same dimensional gap.")
    lines.append("")

    lines.append("## 6. Assessment")
    lines.append("")
    lines.append("**What the calculation shows:**")
    lines.append(f"- Evaluating the given formula literally with w_max = 2 gives a tiny number: **{format_number(da, 2)}**.")
    lines.append(f"- Evaluating the ceiling-mass reading gives a larger number: **{format_number(da_alt, 2)}**.")
    lines.append("- **Neither is a valid prediction of a dimensionless anomalous magnetic moment.** See Section 5.")
    lines.append("")
    lines.append("**What the λ_c search found:**")
    lines.append("- λ_c is canonically identified with the top quark Compton wavelength (~1.14 × 10⁻¹⁸ m).")
    lines.append("- This identification is **calibrated/empirical**, not derived from PF axioms (`lambda_c_from_axioms.md` is explicit about this).")
    lines.append("- The 'coherence ceiling' is not yet a precise functional in `definitions/coherence.md`; it is listed as OPEN.")
    lines.append("")
    lines.append("**Honest ambiguity:**")
    lines.append("- The formula as written is dimensionally inconsistent. A dimensionless `a_τ` cannot equal `w_max / (mass²)` or `w_max / mass` unless `w_max` carries compensating units that the PF manuscript does not specify.")
    lines.append("- The ceiling-mass reading gives ~1.2 × 10⁻⁵, which sits near Belle II's projected 10⁻⁵ reach. This coincidence is not a successful prediction; it is the signature of a free factor-of-m_τ ambiguity landing near an experimental threshold.")
    lines.append("- The '234σ of SM theory uncertainty' framing is misleading: it is 234 × the tiny SM theory uncertainty (~5×10⁻⁸), not 234σ of detectability. At Belle II's actual precision (~10⁻⁵), a 1.17 × 10⁻⁵ effect is a ~1σ hint, not a slam dunk.")
    lines.append("")
    lines.append("**What this does not prove:**")
    lines.append("- It does not prove or disprove the PF coherence-ceiling mechanism. It shows that the current formula for lepton g-2 is not dimensionally closed and therefore not yet a prediction.")
    lines.append("- It does not resolve the gap; that requires a field-theoretic derivation of how the coherence ceiling contributes to the lepton magnetic moment.")
    lines.append("")
    lines.append("**Next step for PF:**")
    lines.append("- Derive a dimensionally closed formula for lepton g-2 from the PF Lagrangian or coherence functional, or admit the gap openly in the PREMISE_LEDGER.")
    lines.append("- Do not present the 6.6 × 10⁻⁹ or 1.17 × 10⁻⁵ numbers as predictions until the dimensional scaffolding is fixed.")
    lines.append("- TASK-051/052 (muon/electron g-2) will hit the same undefined formula and should not be started.")
    lines.append("")

    lines.append("## 7. Method Notes")
    lines.append("")
    lines.append("- Natural-unit conversion: λ_c(MeV⁻¹) = λ_c(m) / (ħc in MeV·m).")
    lines.append("- Uncertainty propagation: 50,000 Monte Carlo samples perturbing m_τ, λ_c, and w_max within their stated uncertainties.")
    lines.append("- Source script: `d2_tau_g2.py` in this directory.")
    lines.append("")

    text = "\n".join(lines)
    with open("D2_tau_g2_prediction.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote D2_tau_g2_prediction.md")

    print(f"\nPF δa_τ (formula as written) = {da:.3e}")
    print(f"PF δa_τ (ceiling-mass interpretation) = {da_alt:.3e}")
    print(f"SM a_τ = {A_TAU_SM:.3e}")


if __name__ == "__main__":
    main()
