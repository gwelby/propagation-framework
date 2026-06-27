#!/usr/bin/env python3
"""
Trials-factor / coverage estimate for the Casimir-root menu.

Cleanest look-elsewhere metric: what fraction of a generic target constant in
[0.05, 0.70] lands within 0.5% of SOME value reachable by {spin pair x simple
functional} on the fixed polynomial x^2 + C2 x - C2 = 0?

That fraction = the probability a RANDOM physics constant gets a "sub-percent
derivation" from this machinery by chance. It is the honest denominator behind
any single 0.13-sigma headline.
"""
import math, itertools, random

def xplus(s):
    C2 = s*(s+1)
    return (-C2 + math.sqrt(C2**2 + 4*C2)) / 2

spins = [0.5*k for k in range(1, 13)]
roots = {s: xplus(s) for s in spins}

def functionals(xa, xb):
    out = []
    if xb: out += [1 - xa/xb, xa/xb]
    if xa: out += [1 - xb/xa, xb/xa]
    if (xa+xb): out += [xa/(xa+xb), xb/(xa+xb)]
    return out

# collect every reachable value in [0,1]
vals = []
for s1, s2 in itertools.combinations(spins, 2):
    for v in functionals(roots[s1], roots[s2]):
        if 0 <= v <= 1:
            vals.append(v)
vals = sorted(set(round(v, 9) for v in vals))
print(f"Reachable distinct values in [0,1]: {len(vals)}")

TOL = 0.005  # 0.5% relative
# Monte Carlo: random targets uniform in a realistic constant band
band = (0.05, 0.70)
N = 200000
hits = 0
for _ in range(N):
    t = random.uniform(*band)
    if any(abs(v - t)/t < TOL for v in vals):
        hits += 1
p = hits / N
print(f"Band {band}, tolerance {TOL*100:.1f}% relative")
print(f"P(random target gets a sub-percent hit from this menu) = {p:.3f}")
print(f"  => roughly 1 in {1/p:.1f} arbitrary constants is 'derivable' by chance")
print(f"  => a single 0.13-sigma headline must be discounted by ~this trials factor\n")

# Fairness check: is (1/2,1) genuinely the BEST sin2W hit on the chosen functional?
target = 0.22337
cand = []
for s1, s2 in itertools.combinations(spins, 2):
    v = 1 - roots[s1]/roots[s2]
    cand.append((abs(v-target)/target*100, s1, s2, v))
cand.sort()
print("Best sin2_W (on-shell) hits with functional 1 - x(a)/x(b):")
for err, s1, s2, v in cand[:4]:
    star = "  <-- repo choice" if (s1,s2)==(0.5,1) else ""
    print(f"  s=({s1:g},{s2:g}) = {v:.5f}  ({err:.2f}% off){star}")
