#!/usr/bin/env python3
"""
Look-elsewhere stress test of the Weinberg "unique among 582 alternatives" claim.

The repo claim (g3_casimir_weinberg_angle.md):
  "A systematic scan of 582 polynomial alternatives ... confirms uniqueness:
   no other equation of this class reproduces sin2_W to sub-percent accuracy
   at (s1,s2)=(1/2,1)."

We do NOT dispute that statement on its own terms. We ask the question that
matters for whether the match is evidence: HOW MANY sub-percent hits on a
famous physics constant does the SAME search machinery produce when we let
the other hand-fixed choices vary -- spin pair, functional form, and target?

If the menu is dense with sub-percent hits, then finding one at (1/2,1) is
expected, not surprising, and carries little evidential weight.

Pre-registration (written BEFORE running, per repo rule):
  Prediction: the spin/functional menu will yield MANY sub-percent hits on
  sin2_W and on other O(0.1-1) constants. We expect the (1/2,1) hit to be
  one of several, not unique once the functional form is also free.
"""
import math, itertools

def xplus(s):
    C2 = s*(s+1)
    return (-C2 + math.sqrt(C2**2 + 4*C2)) / 2

# ---- the menu of root values for half-integer spins ----
spins = [0.5*k for k in range(1, 13)]   # 1/2 .. 6
roots = {s: xplus(s) for s in spins}

# ---- targets: famous dimensionless constants in the 0.1-1 band ----
targets = {
    "sin2W_onshell": 0.22337,
    "sin2W_MSbar":   0.23122,
    "delta_Koide":   2/9,          # 0.2222
    "Koide_Q":       2/3,          # 0.6667
    "alpha_s(MZ)":   0.1179,
    "Cabibbo_sin2":  0.0505,       # sin^2(theta_C)
    "sin2_th23":     0.55,         # atmospheric nu mixing
    "g_minus2_ish":  0.5,
}
TOL = 0.005   # 0.5% relative  (their "sub-percent")

# ---- functional forms a human could plausibly write down ----
def functionals(xa, xb):
    out = {}
    if xb != 0:
        out["1 - xa/xb"] = 1 - xa/xb
        out["xa/xb"]     = xa/xb
    if xa != 0:
        out["1 - xb/xa"] = 1 - xb/xa
        out["xb/xa"]     = xb/xa
    out["xa - xb"]   = xa - xb
    if (xa+xb) != 0:
        out["xa/(xa+xb)"] = xa/(xa+xb)
        out["xb/(xa+xb)"] = xb/(xa+xb)
    return out

hits = []
total_combos = 0
for s1, s2 in itertools.combinations(spins, 2):
    xa, xb = roots[s1], roots[s2]
    for fname, val in functionals(xa, xb).items():
        total_combos += 1
        for tname, tval in targets.items():
            if tval != 0 and abs(val - tval)/abs(tval) < TOL:
                hits.append((tname, s1, s2, fname, val, abs(val-tval)/abs(tval)*100))

print(f"Fixed polynomial x^2 + C2 x - C2 = 0  (the repo's chosen one)")
print(f"Spin menu: {[f'{s:g}' for s in spins]}")
print(f"Functional forms per pair: 7 | spin pairs: {math.comb(len(spins),2)}")
print(f"Total (pair x functional) combinations scanned: {total_combos}")
print(f"Targets: {len(targets)} famous constants | tolerance: {TOL*100:.1f}% relative\n")
print(f"=== SUB-PERCENT HITS: {len(hits)} ===")
for tname, s1, s2, fname, val, err in sorted(hits, key=lambda h: h[0]):
    print(f"  {tname:14s}  s=({s1:g},{s2:g})  {fname:14s} = {val:.5f}  ({err:.2f}% off)")

# focused: how many ways hit sin2W specifically (either scheme)?
sw = [h for h in hits if h[0].startswith("sin2W")]
print(f"\n=== sin2_W hits specifically (either scheme): {len(sw)} ===")
for h in sw:
    print(f"  {h[0]:14s}  s=({h[1]:g},{h[2]:g})  {h[3]:14s} = {h[4]:.5f}  ({h[5]:.2f}% off)")
