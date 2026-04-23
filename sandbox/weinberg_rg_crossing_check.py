"""Bounded T-021 check for the Koide/Weinberg RG-crossing claim.

Run:
    python sandbox/weinberg_rg_crossing_check.py

Purpose:
    Keep the RG question convention-specific. This helper reports four
    distinct quantities that are often conflated in repo prose:

    1. Direct pole-mass on-shell ratio:
           s2_os = 1 - M_W^2 / M_Z^2
       This is a fixed quantity once the pole masses are chosen. It does not
       "run" with the renormalization scale.

    2. Effective leptonic weak mixing angle:
           sin^2(theta_eff^ell)
       This is an extracted Z-pole observable, not a generic RG trajectory.

    3. The running MS-bar weak angle:
           s_hat^2(mu)
       This is the convention that legitimately runs with mu.

    4. The repo's Casimir value:
           sin^2(theta_W)_PF = 0.223101322300866
       This is an internal PF result, not a Standard Model RG definition.

Sources:
    - PDG 2025 gauge-boson listings for M_W and M_Z:
      https://pdg.lbl.gov/2025/tables/rpp2025-sum-gauge-higgs-bosons.pdf
    - PDG 2025 electroweak review, Table 10.5 and surrounding convention text:
      https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf
    - SM gauge beta-functions (one-loop coefficients used in the helper):
      A. V. Bednyakov, A. F. Pikelner, V. N. Velizhanin,
      JHEP 01 (2013) 017, https://doi.org/10.1007/JHEP01(2013)017

Scope:
    This is a bounded helper, not a full electroweak-fit code. It is good
    enough to test the specific repo sentence:
        "sin^2(theta_W) runs to delta at mu ~= 98 GeV"
    against a legitimate running convention.
"""

from __future__ import annotations

import math

TARGET_DELTA = 2.0 / 9.0
DELTA_EXACT = 0.222229631490
CASIMIR_S2 = 0.223101322300866

# PDG 2025 particle listings (current official central values in this pass).
MW_POLE_GEV = 80.3692
MZ_POLE_GEV = 91.1880

# Legacy repo anchor often used elsewhere in this workspace.
MZ_REPO_GEV = 91.1876

# PDG 2025 electroweak review, Table 10.5.
PDG_S2_EFF_LEPTONIC = 0.23154
PDG_S2_EFF_LEPTONIC_ERR = 0.00006
PDG_HAT_S2_MZ = 0.23122
PDG_HAT_S2_MZ_ERR = 0.00006

# PDG 2025 electroweak review, alpha-hat^(5)(M_Z)^-1.
PDG_ALPHA_HAT_INV_5_MZ = 127.930
PDG_ALPHA_HAT_INV_5_MZ_ERR = 0.008

# Standard Model one-loop gauge beta coefficients in SU(5) normalization.
B1 = 41.0 / 10.0
B2 = -19.0 / 6.0


def direct_on_shell_ratio(mw_gev: float, mz_gev: float) -> float:
    return 1.0 - (mw_gev * mw_gev) / (mz_gev * mz_gev)


def msbar_couplings_at_mz(
    s2_mz: float = PDG_HAT_S2_MZ,
    alpha_hat_inv_mz: float = PDG_ALPHA_HAT_INV_5_MZ,
) -> tuple[float, float]:
    """Return g1^2 and g2^2 at M_Z in SU(5) normalization."""
    alpha_hat = 1.0 / alpha_hat_inv_mz
    g1_sq = (5.0 / 3.0) * 4.0 * math.pi * alpha_hat / (1.0 - s2_mz)
    g2_sq = 4.0 * math.pi * alpha_hat / s2_mz
    return g1_sq, g2_sq


def sin2_hat_msbar(
    mu_gev: float,
    s2_mz: float = PDG_HAT_S2_MZ,
    alpha_hat_inv_mz: float = PDG_ALPHA_HAT_INV_5_MZ,
) -> float:
    """One-loop running helper for s_hat^2(mu) above M_Z."""
    if mu_gev <= 0.0:
        raise ValueError("mu_gev must be positive")

    g1_sq_mz, g2_sq_mz = msbar_couplings_at_mz(
        s2_mz=s2_mz,
        alpha_hat_inv_mz=alpha_hat_inv_mz,
    )

    log_mu_over_mz = math.log(mu_gev / MZ_POLE_GEV)
    inv_g1_sq = 1.0 / g1_sq_mz - B1 * log_mu_over_mz / (8.0 * math.pi**2)
    inv_g2_sq = 1.0 / g2_sq_mz - B2 * log_mu_over_mz / (8.0 * math.pi**2)

    g1_sq = 1.0 / inv_g1_sq
    g2_sq = 1.0 / inv_g2_sq
    return (3.0 * g1_sq) / (5.0 * g2_sq + 3.0 * g1_sq)


def d_sin2_hat_d_log_mu(
    mu_gev: float,
    s2_mz: float = PDG_HAT_S2_MZ,
    alpha_hat_inv_mz: float = PDG_ALPHA_HAT_INV_5_MZ,
) -> float:
    """One-loop derivative d s_hat^2 / d ln(mu)."""
    g1_sq_mz, g2_sq_mz = msbar_couplings_at_mz(
        s2_mz=s2_mz,
        alpha_hat_inv_mz=alpha_hat_inv_mz,
    )

    log_mu_over_mz = math.log(mu_gev / MZ_POLE_GEV)
    inv_g1_sq = 1.0 / g1_sq_mz - B1 * log_mu_over_mz / (8.0 * math.pi**2)
    inv_g2_sq = 1.0 / g2_sq_mz - B2 * log_mu_over_mz / (8.0 * math.pi**2)
    g1_sq = 1.0 / inv_g1_sq
    g2_sq = 1.0 / inv_g2_sq

    numerator = 15.0 * g1_sq * g2_sq * (B1 * g1_sq - B2 * g2_sq)
    denominator = 8.0 * math.pi**2 * (5.0 * g2_sq + 3.0 * g1_sq) ** 2
    return numerator / denominator


def sensitivity_window(mu_gev: float) -> tuple[float, float]:
    """Scan PDG 1-sigma corners for s_hat^2(M_Z) and alpha_hat^-1(M_Z)."""
    samples = []
    for s2 in (PDG_HAT_S2_MZ - PDG_HAT_S2_MZ_ERR, PDG_HAT_S2_MZ + PDG_HAT_S2_MZ_ERR):
        for alpha_inv in (
            PDG_ALPHA_HAT_INV_5_MZ - PDG_ALPHA_HAT_INV_5_MZ_ERR,
            PDG_ALPHA_HAT_INV_5_MZ + PDG_ALPHA_HAT_INV_5_MZ_ERR,
        ):
            samples.append(sin2_hat_msbar(mu_gev, s2_mz=s2, alpha_hat_inv_mz=alpha_inv))
    return min(samples), max(samples)


def crossing_statement(value: float) -> str:
    gap = value - TARGET_DELTA
    if abs(gap) < 1.0e-6:
        return "hits 2/9 within 1e-6"
    if gap > 0.0:
        return f"above 2/9 by {gap:.9f}"
    return f"below 2/9 by {-gap:.9f}"


def print_rule(char: str = "-") -> None:
    print(char * 100)


def print_inputs() -> None:
    print("T-021 RG audit helper: Koide/Weinberg crossing check")
    print_rule("=")
    print("Repo anchors")
    print(f"  delta_target = 2/9                = {TARGET_DELTA:.12f}")
    print(f"  delta_exact  = delta_Koide        = {DELTA_EXACT:.12f}")
    print(f"  Casimir PF value                  = {CASIMIR_S2:.12f}")
    print()
    print("PDG / external inputs")
    print(f"  M_W pole (2025 listings)          = {MW_POLE_GEV:.4f} GeV")
    print(f"  M_Z pole (2025 listings)          = {MZ_POLE_GEV:.4f} GeV")
    print(f"  legacy repo M_Z anchor            = {MZ_REPO_GEV:.4f} GeV")
    print(f"  sin^2(theta_eff^ell)              = {PDG_S2_EFF_LEPTONIC:.5f} +/- {PDG_S2_EFF_LEPTONIC_ERR:.5f}")
    print(f"  s_hat^2(M_Z)                      = {PDG_HAT_S2_MZ:.5f} +/- {PDG_HAT_S2_MZ_ERR:.5f}")
    print(f"  alpha_hat^(5)(M_Z)^-1             = {PDG_ALPHA_HAT_INV_5_MZ:.3f} +/- {PDG_ALPHA_HAT_INV_5_MZ_ERR:.3f}")
    print()


def print_definition_table() -> None:
    current_os = direct_on_shell_ratio(MW_POLE_GEV, MZ_POLE_GEV)
    legacy_os = direct_on_shell_ratio(MW_POLE_GEV, MZ_REPO_GEV)

    print("Definition audit")
    print_rule()
    print(f"{'quantity':34} {'value':>16} {'can run?':>10}  note")
    print_rule()
    print(
        f"{'1 - M_W^2/M_Z^2 (current pole masses)':34} "
        f"{current_os:16.12f} {'no':>10}  fixed once pole masses are chosen"
    )
    print(
        f"{'1 - M_W^2/M_Z^2 (repo M_Z=91.1876)':34} "
        f"{legacy_os:16.12f} {'no':>10}  legacy anchor; still fixed, not RG flow"
    )
    print(
        f"{'sin^2(theta_eff^ell)':34} "
        f"{PDG_S2_EFF_LEPTONIC:16.12f} {'no':>10}  Z-pole extracted observable"
    )
    print(
        f"{'s_hat^2(M_Z)':34} "
        f"{PDG_HAT_S2_MZ:16.12f} {'yes':>10}  MS-bar running definition"
    )
    print(
        f"{'Casimir sin^2(theta_W)':34} "
        f"{CASIMIR_S2:16.12f} {'no':>10}  PF internal value"
    )
    print_rule()
    print()


def print_running_table() -> None:
    print("MS-bar running check (one-loop helper anchored at PDG s_hat^2(M_Z))")
    print_rule()
    print(f"{'mu [GeV]':>12} {'s_hat^2(mu)':>16} {'vs 2/9':>26}")
    print_rule()
    for mu in (MW_POLE_GEV, MZ_POLE_GEV, 98.0, 100.0, 172.61, 1000.0, 10000.0):
        value = sin2_hat_msbar(mu)
        print(f"{mu:12.4f} {value:16.9f} {crossing_statement(value):>26}")
    print_rule()
    print()

    at_98 = sin2_hat_msbar(98.0)
    min_98, max_98 = sensitivity_window(98.0)
    slope_98 = d_sin2_hat_d_log_mu(98.0)

    print("Sensitivity")
    print_rule()
    print(f"  s_hat^2(98 GeV) central           = {at_98:.9f}")
    print(f"  PDG 1-sigma corner window         = [{min_98:.9f}, {max_98:.9f}]")
    print(f"  d s_hat^2 / d ln(mu) at 98 GeV    = {slope_98:.9f}")
    print()
    print(
        "  PDG states the scale dependence of s_hat^2(mu) reaches its minimum near mu = M_W."
    )
    print(
        "  Since the helper already gives s_hat^2(M_W) = "
        f"{sin2_hat_msbar(MW_POLE_GEV):.9f} > 2/9,"
    )
    print("  the standard MS-bar trajectory does not cross 2/9 in the electroweak region audited here.")
    print()


def print_verdict() -> None:
    current_os = direct_on_shell_ratio(MW_POLE_GEV, MZ_POLE_GEV)
    at_98 = sin2_hat_msbar(98.0)

    print("Final verdict")
    print_rule()
    print(
        f"- Direct pole-mass on-shell ratio = {current_os:.12f}; it is fixed, not a running definition."
    )
    print(
        f"- Effective leptonic angle = {PDG_S2_EFF_LEPTONIC:.5f}; it is a Z-pole extracted observable, not a generic RG trajectory."
    )
    print(
        f"- Running MS-bar value at 98 GeV = {at_98:.9f}; this is well above 2/9 = {TARGET_DELTA:.12f}."
    )
    print(
        f"- Casimir value = {CASIMIR_S2:.12f}; it stays a separate PF result and is not an RG definition."
    )
    print()
    print(
        "Therefore no legitimate definition audited here supports the sentence "
        "\"sin^2(theta_W) runs to delta at mu ~= 98 GeV\"."
    )


def main() -> None:
    print_inputs()
    print_definition_table()
    print_running_table()
    print_verdict()


if __name__ == "__main__":
    main()
