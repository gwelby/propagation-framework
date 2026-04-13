"""
T-022: δ=2/9 Casimir Selector — does the polynomial produce the Koide phase?
==============================================================================
Task:  WHATS_NEXT.md Attack 1 / TASKS.md T-022
Date:  2026-04-12
Agent: Cascade (implementation), Codex (audit), Lumi (physics check)

PRE-REGISTRATION (written before running — do NOT modify after seeing results):
--------------------------------------------------------------------------------
EXPECTED OUTCOME:
  The Weinberg angle derivation uses R = 1 - x+(1/2)/x+(1) = 0.22310.
  The Koide phase δ = 0.22223 rad ≈ 2/9 = 0.22222...
  
  I expect that NO single spin pair (j1, j2) will produce R = 2/9 exactly from
  the same ratio formula R = 1 - x+(j1)/x+(j2), because the Weinberg pair
  (1/2, 1) already gives 0.22310 which is close but NOT 2/9.
  
  However, I expect the SCAN to reveal whether:
  (a) A different functional form of the Casimir roots produces 2/9
  (b) x+(1/2) itself has a fixed-point property related to 2/9
  (c) Some ratio or combination of roots lands within 0.001 of 2/9
  
  If NO combination produces 2/9 ± 0.001 with a geometric interpretation,
  that is an honest negative result: the Casimir polynomial does not naturally
  select the Koide phase, and δ = 2/9 must come from a different mechanism.
  
  PREDICTION: Likely negative (no clean hit), but the gap between 0.22310
  (Weinberg) and 0.22222 (Koide) may yield a structured residual.

FALSIFICATION CRITERION:
  If ANY result below shows 2/9 within 0.1%, record it as a HIT and state
  the geometric interpretation. If the script is adjusted to "find" 2/9 by
  construction, that is not a derivation — note it honestly.
--------------------------------------------------------------------------------

Read first:
  - derivations/g3_casimir_weinberg_angle.md
  - sandbox/casimir_verification.py
  - CLAIMS.md (Koide Phase δ=2/9 row and Weinberg Angle row)
  - WHATS_NEXT.md (Attack 1 section)
"""

from pathlib import Path
import math
import itertools

# ============================================================================
# Core: Casimir polynomial x^2 + C2*x - C2 = 0, C2 = j(j+1)
# ============================================================================

TARGET = 2 / 9  # 0.22222222...
TOLERANCE = 0.001  # 1% of 2/9 — threshold from T-022 spec
SPINS = [0, 0.5, 1, 1.5, 2, 2.5, 3]  # extended scan beyond T-022 minimum


def casimir_c2(j):
    """Quadratic Casimir eigenvalue C2 = j(j+1)."""
    return j * (j + 1)


def casimir_root_positive(j):
    """Positive root of x^2 + C2*x - C2 = 0."""
    c2 = casimir_c2(j)
    if c2 == 0:
        return 0.0
    return (-c2 + math.sqrt(c2**2 + 4 * c2)) / 2


def casimir_root_negative(j):
    """Negative root of x^2 + C2*x - C2 = 0."""
    c2 = casimir_c2(j)
    if c2 == 0:
        return 0.0
    return (-c2 - math.sqrt(c2**2 + 4 * c2)) / 2


# ============================================================================
# Scan 1: All pairwise ratios R = 1 - x+(j1)/x+(j2)
# This is the Weinberg formula generalized to all spin pairs
# ============================================================================

def scan_weinberg_ratios():
    """Scan R = 1 - x+(j1)/x+(j2) for all ordered spin pairs."""
    print("=" * 72)
    print("SCAN 1: Weinberg-type ratio R = 1 - x+(j1)/x+(j2)")
    print("=" * 72)
    print(f"{'j1':>5} {'j2':>5} {'x+(j1)':>12} {'x+(j2)':>12} {'R':>12} {'|R-2/9|':>12} {'HIT?':>6}")
    print("-" * 72)

    hits = []
    for j1, j2 in itertools.permutations(SPINS, 2):
        x1 = casimir_root_positive(j1)
        x2 = casimir_root_positive(j2)
        if x2 == 0:
            continue
        R = 1 - x1 / x2
        gap = abs(R - TARGET)
        is_hit = gap < TOLERANCE
        marker = ">>> HIT" if is_hit else ""
        print(f"{j1:5.1f} {j2:5.1f} {x1:12.8f} {x2:12.8f} {R:12.8f} {gap:12.2e} {marker}")
        if is_hit:
            hits.append(("Weinberg ratio", j1, j2, R, gap))

    return hits


# ============================================================================
# Scan 2: Root values themselves — does any x+(j) ≈ 2/9?
# ============================================================================

def scan_root_values():
    """Check if any x+(j) value is close to 2/9."""
    print("\n" + "=" * 72)
    print("SCAN 2: Root values x+(j) — does any equal 2/9?")
    print("=" * 72)
    print(f"{'j':>5} {'C2':>10} {'x+(j)':>14} {'|x-2/9|':>14} {'HIT?':>6}")
    print("-" * 72)

    hits = []
    for j in SPINS:
        x = casimir_root_positive(j)
        gap = abs(x - TARGET)
        is_hit = gap < TOLERANCE
        marker = ">>> HIT" if is_hit else ""
        print(f"{j:5.1f} {casimir_c2(j):10.4f} {x:14.10f} {gap:14.2e} {marker}")
        if is_hit:
            hits.append(("Root value", j, None, x, gap))

    return hits


# ============================================================================
# Scan 3: Ratio of roots x+(j1)/x+(j2) — does any ratio equal 2/9?
# ============================================================================

def scan_root_ratios():
    """Check if x+(j1)/x+(j2) ≈ 2/9 for any pair."""
    print("\n" + "=" * 72)
    print("SCAN 3: Root ratio x+(j1)/x+(j2) — does any equal 2/9?")
    print("=" * 72)
    print(f"{'j1':>5} {'j2':>5} {'x+(j1)/x+(j2)':>16} {'|ratio-2/9|':>14} {'HIT?':>6}")
    print("-" * 72)

    hits = []
    for j1, j2 in itertools.permutations(SPINS, 2):
        x1 = casimir_root_positive(j1)
        x2 = casimir_root_positive(j2)
        if x2 == 0 or x1 == 0:
            continue
        ratio = x1 / x2
        gap = abs(ratio - TARGET)
        is_hit = gap < TOLERANCE
        marker = ">>> HIT" if is_hit else ""
        print(f"{j1:5.1f} {j2:5.1f} {ratio:16.10f} {gap:14.2e} {marker}")
        if is_hit:
            hits.append(("Root ratio", j1, j2, ratio, gap))

    return hits


# ============================================================================
# Scan 4: Difference of roots x+(j2) - x+(j1) — does any equal 2/9?
# ============================================================================

def scan_root_differences():
    """Check if x+(j2) - x+(j1) ≈ 2/9 for any pair."""
    print("\n" + "=" * 72)
    print("SCAN 4: Root difference x+(j2) - x+(j1) — does any equal 2/9?")
    print("=" * 72)
    print(f"{'j1':>5} {'j2':>5} {'x+(j2)-x+(j1)':>16} {'|diff-2/9|':>14} {'HIT?':>6}")
    print("-" * 72)

    hits = []
    for j1, j2 in itertools.combinations(SPINS, 2):
        x1 = casimir_root_positive(j1)
        x2 = casimir_root_positive(j2)
        diff = x2 - x1
        gap = abs(diff - TARGET)
        is_hit = gap < TOLERANCE
        marker = ">>> HIT" if is_hit else ""
        print(f"{j1:5.1f} {j2:5.1f} {diff:16.10f} {gap:14.2e} {marker}")
        if is_hit:
            hits.append(("Root difference", j1, j2, diff, gap))

    return hits


# ============================================================================
# Scan 5: Products, sums, and algebraic combinations of roots
# ============================================================================

def scan_algebraic_combinations():
    """Check various algebraic combinations of roots for 2/9."""
    print("\n" + "=" * 72)
    print("SCAN 5: Algebraic combinations of roots")
    print("=" * 72)

    hits = []
    roots = {j: casimir_root_positive(j) for j in SPINS if j > 0}

    # 5a: x+(j)^2 for each j
    print("\n--- 5a: x+(j)^2 ---")
    for j, x in roots.items():
        val = x**2
        gap = abs(val - TARGET)
        marker = ">>> HIT" if gap < TOLERANCE else ""
        print(f"  x+({j})^2 = {val:.10f}  |gap| = {gap:.2e}  {marker}")
        if gap < TOLERANCE:
            hits.append(("x^2", j, None, val, gap))

    # 5b: 1 - x+(j) for each j
    print("\n--- 5b: 1 - x+(j) ---")
    for j, x in roots.items():
        val = 1 - x
        gap = abs(val - TARGET)
        marker = ">>> HIT" if gap < TOLERANCE else ""
        print(f"  1-x+({j}) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
        if gap < TOLERANCE:
            hits.append(("1-x", j, None, val, gap))

    # 5c: x+(j1) * x+(j2) for pairs
    print("\n--- 5c: x+(j1) * x+(j2) ---")
    for (j1, x1), (j2, x2) in itertools.combinations(roots.items(), 2):
        val = x1 * x2
        gap = abs(val - TARGET)
        marker = ">>> HIT" if gap < TOLERANCE else ""
        if gap < 0.01:  # only print close ones
            print(f"  x+({j1})*x+({j2}) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
        if gap < TOLERANCE:
            hits.append(("product", j1, j2, val, gap))

    # 5d: x+(j1) * (1-x+(j2)) for pairs
    print("\n--- 5d: x+(j1) * (1 - x+(j2)) ---")
    for j1, x1 in roots.items():
        for j2, x2 in roots.items():
            if j1 == j2:
                continue
            val = x1 * (1 - x2)
            gap = abs(val - TARGET)
            marker = ">>> HIT" if gap < TOLERANCE else ""
            if gap < 0.01:
                print(f"  x+({j1})*(1-x+({j2})) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
            if gap < TOLERANCE:
                hits.append(("x*(1-y)", j1, j2, val, gap))

    # 5e: (1-x+(j1)) * (1-x+(j2)) for pairs
    print("\n--- 5e: (1-x+(j1)) * (1-x+(j2)) ---")
    for (j1, x1), (j2, x2) in itertools.combinations(roots.items(), 2):
        val = (1 - x1) * (1 - x2)
        gap = abs(val - TARGET)
        marker = ">>> HIT" if gap < TOLERANCE else ""
        if gap < 0.01:
            print(f"  (1-x+({j1}))*(1-x+({j2})) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
        if gap < TOLERANCE:
            hits.append(("(1-x)(1-y)", j1, j2, val, gap))

    # 5f: x+(j)/(1+x+(j)) — "normalized root"
    print("\n--- 5f: x+(j)/(1+x+(j)) ---")
    for j, x in roots.items():
        val = x / (1 + x)
        gap = abs(val - TARGET)
        marker = ">>> HIT" if gap < TOLERANCE else ""
        print(f"  x+({j})/(1+x+({j})) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
        if gap < TOLERANCE:
            hits.append(("x/(1+x)", j, None, val, gap))

    # 5g: C2(j) / (C2(j) + k) for small integers k — fixed-point forms
    print("\n--- 5g: C2(j)/(C2(j)+k) for k=1..6 ---")
    for j in SPINS:
        c2 = casimir_c2(j)
        if c2 == 0:
            continue
        for k in range(1, 7):
            val = c2 / (c2 + k)
            gap = abs(val - TARGET)
            marker = ">>> HIT" if gap < TOLERANCE else ""
            if gap < 0.01:
                print(f"  C2({j})/(C2({j})+{k}) = {val:.10f}  |gap| = {gap:.2e}  {marker}")
            if gap < TOLERANCE:
                hits.append((f"C2/(C2+{k})", j, None, val, gap))

    return hits


# ============================================================================
# Scan 6: The Weinberg-Koide gap analysis
# ============================================================================

def analyze_weinberg_koide_gap():
    """Analyze the structured gap between sin²θ_W = 0.22310 and δ = 2/9."""
    print("\n" + "=" * 72)
    print("SCAN 6: Weinberg-Koide gap analysis")
    print("=" * 72)

    sin2_W = 1 - casimir_root_positive(0.5) / casimir_root_positive(1)
    delta_koide = 2 / 9
    gap = sin2_W - delta_koide

    print(f"  sin²θ_W (Casimir) = {sin2_W:.10f}")
    print(f"  δ_Koide = 2/9     = {delta_koide:.10f}")
    print(f"  Gap               = {gap:.10f}")
    print(f"  Gap / (2/9)       = {gap / delta_koide:.6f}  ({gap / delta_koide * 100:.4f}%)")
    print(f"  Gap / α           = {gap / (1/137.036):.6f}")
    print(f"  Gap * 9           = {gap * 9:.10f}")
    print(f"  Gap * 9 * 137     = {gap * 9 * 137:.6f}")

    # Check if gap matches any simple Casimir expression
    print("\n  Checking gap against Casimir root expressions:")
    for j in SPINS:
        if j == 0:
            continue
        x = casimir_root_positive(j)
        for label, val in [
            (f"x+({j})/π²", x / math.pi**2),
            (f"x+({j})²/π", x**2 / math.pi),
            (f"(1-x+({j}))/π²", (1 - x) / math.pi**2),
            (f"x+({j})/9", x / 9),
            (f"α*x+({j})", (1/137.036) * x),
            (f"α*(1-x+({j}))", (1/137.036) * (1 - x)),
        ]:
            ratio = abs(gap / val) if val != 0 else float('inf')
            if 0.8 < ratio < 1.2:
                print(f"    {label} = {val:.10f}  gap/val = {ratio:.6f}  {'CLOSE' if 0.95 < ratio < 1.05 else ''}")


# ============================================================================
# Scan 7: Fixed-point check — does x+(1/2) have a 2/9 property?
# ============================================================================

def scan_fixed_point():
    """Check if x+(1/2) has an algebraic relationship to 2/9."""
    print("\n" + "=" * 72)
    print("SCAN 7: Fixed-point properties of x+(1/2)")
    print("=" * 72)

    x_half = casimir_root_positive(0.5)
    print(f"  x+(1/2) = (-3 + √57) / 8 = {x_half:.15f}")
    print(f"  2/9                       = {TARGET:.15f}")
    print(f"  x+(1/2) - 2/9             = {x_half - TARGET:.15f}")
    print(f"  x+(1/2) / (2/9)           = {x_half / TARGET:.15f}")

    # Check algebraic identities
    print("\n  Algebraic checks:")
    checks = [
        ("x^2 + (3/4)x - 3/4 at x=2/9", (2/9)**2 + (3/4)*(2/9) - 3/4),
        ("x^2/(1-x) at x=2/9", (2/9)**2 / (1 - 2/9)),
        ("x^2/(1-x) at x=x+(1/2)", x_half**2 / (1 - x_half)),
        ("C2 at j=1/2", 3/4),
        ("2/9 satisfies polynomial?", (2/9)**2 + (3/4)*(2/9) - 3/4),
    ]
    for label, val in checks:
        print(f"    {label} = {val:.10f}")

    # What spin j would make x+(j) = 2/9 exactly?
    # From x^2 + C2*x - C2 = 0: C2 = x^2/(1-x)
    x_target = 2/9
    c2_needed = x_target**2 / (1 - x_target)
    j_needed = (-1 + math.sqrt(1 + 4 * c2_needed)) / 2
    print(f"\n  For x+ = 2/9 exactly:")
    print(f"    C2 needed = (2/9)^2 / (1-2/9) = {c2_needed:.10f}")
    print(f"    j needed  = {j_needed:.10f}")
    print(f"    Is j a half-integer? {abs(2*j_needed - round(2*j_needed)) < 0.001}")
    print(f"    Nearest half-integer: {round(2*j_needed)/2}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("T-022: δ=2/9 Casimir Selector Scan")
    print("Date: 2026-04-12")
    print(f"Target: 2/9 = {TARGET:.15f}")
    print(f"Tolerance: ±{TOLERANCE} ({TOLERANCE/TARGET*100:.1f}% of target)")
    print()

    all_hits = []
    all_hits.extend(scan_weinberg_ratios())
    all_hits.extend(scan_root_values())
    all_hits.extend(scan_root_ratios())
    all_hits.extend(scan_root_differences())
    all_hits.extend(scan_algebraic_combinations())
    analyze_weinberg_koide_gap()
    scan_fixed_point()

    # ========================================================================
    # VERDICT
    # ========================================================================
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    if all_hits:
        print(f"\n  {len(all_hits)} HIT(S) FOUND within ±{TOLERANCE} of 2/9:\n")
        for scan_type, j1, j2, value, gap in all_hits:
            j2_str = f", j2={j2}" if j2 is not None else ""
            print(f"    [{scan_type}] j1={j1}{j2_str}: value={value:.10f}, |gap|={gap:.2e}")
        print("\n  NEXT STEP: Each hit needs a geometric interpretation.")
        print("  If interpretable → candidate for Koide phase selector.")
        print("  If numerical coincidence → record honestly and close T-022.")
    else:
        print("\n  NO HITS within ±0.001 of 2/9.")
        print("  The Casimir polynomial x^2 + C2*x - C2 = 0 does NOT naturally")
        print("  produce 2/9 as a fixed point, root value, ratio, difference,")
        print("  or simple algebraic combination for any spin j in [0, 3].")
        print("\n  This is an honest negative result. δ = 2/9 must come from a")
        print("  different mechanism than the Casimir polynomial sector.")

    print("\n  Pre-registered prediction: Likely negative (no clean hit).")
    print(f"  Actual result: {'POSITIVE — hits found' if all_hits else 'NEGATIVE — confirmed'}.")

    # Write result summary to stdout for appending to sandbox_results.md
    print("\n" + "=" * 72)
    print("END T-022 SCAN")
    print("=" * 72)


if __name__ == "__main__":
    main()
