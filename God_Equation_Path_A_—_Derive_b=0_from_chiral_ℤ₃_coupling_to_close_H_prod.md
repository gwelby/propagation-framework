# God Equation Path A — Projected-Sector Closure and the Fourier-to-Position-Space Bridge

⚠ **REFRAMED 2026-04-01** — The original target ("derive b=0 from chirality") was invalidated by the
2026-04-01 chiral projection audit. The actual projected operator `T_L = P_L T_sym P_L` has
`|β/α| = 1`, not `b=0`. The live Path A question is stated below.

---

## What This Is

**Frontier**: God Equation `λ_c` — `CONDITIONAL 0.88`
**This ticket**: Path A — projected-sector closure route to `H_prod`
**Supersedes**: "derive b=0" target (dead; see audit finding in `god_eq_h_prod_model_routes_audit_2026-04-01.md`)
**Source**: `ACTIVE_ISSUES.md`, `god_eq_h_prod_model_routes_audit_2026-04-01.md`, `sandbox/chiral_projection_z3.py`

---

## Why the Old Target Died

The chiral projection `P_L = P₀ + P₁` kills the `k=2` Fourier eigenmode. But in position space:

```
T_L = P_L · T_sym · P_L = cI + aS̄ + bS̄²
c = 1/6,  a = 5/12 + i√3/12,  b = 5/12 − i√3/12
```

`|b/a| = 1`. The S̄² term is **not** eliminated. Fourier-mode killing ≠ position-space `b=0`.

The actual 3-step projected operator has diagonal entries:

```
Fourier eigenvalues of T_L: {1, −1/2, 0}
T_L³ eigenvalues: {1, −1/8, 0}
[T_L³]_{jj} = (1 − 1/8 + 0)/3 = 7/24 ≈ 0.292   (not zero)
```

So "return probability is zero → closure is pure shift → factorization" is a dead chain.

---

## Live Proof Obligations

Two independent obligations remain. Both must be addressed before Path A can move:

### Obligation H-A — Is the projected sector forced?

**Question**: Does the ℤ₃ Lagrangian under left-chiral coupling physically force the system into
the `{k=0, k=1}` projected sector, or is `P_L` an external restriction?

- State the ℤ₃ Lagrangian interaction term for chiral fermion currents (from `z3_extended_propagation_lagrangian.md`)
- Show whether the chiral coupling selects `{k=0,k=1}` as the natural sector or only as an
  imposed projection
- A forced selection would mean `k=2` modes are genuinely suppressed by the dynamics, not only by hand

### Obligation H-B — Does 2D Fourier-sector closure imply position-space H_prod?

**Question**: If we accept the projected `{k=0,k=1}` sector (even as a restriction), does closure
in that 2D Fourier sector imply the position-space joint-law factorization required by `H_prod`?

- The projected operator is diagonal in Fourier space (eigenvalues `{1, −1/2}` restricted to the
  2D sector)
- Map explicitly from "Fourier-sector closure is diagonal" to "position-space joint law factorizes"
- This bridge has not been written yet; it is the core gap

---

## Acceptance Criteria

- [ ] H-A: the physical forcing of the `{k=0,k=1}` sector is derived or definitively killed
- [ ] H-B: the Fourier-to-position-space factorization bridge is proved or killed
- [ ] Neither obligation assumes what it is trying to prove
- [ ] The actual projected operator (`T_L` with `c=1/6`, `a=5/12+i√3/12`, `b=5/12−i√3/12`) is used
- [ ] Codex audits the derivation file and signs off before any confidence upgrade

**Assigned to**: Claude (draft) → Codex (audit)
**Do not promote** without Codex sign-off on both H-A and H-B.

---

## Historical Note

The original "derive b=0" route was:
1. Chiral projection kills `k=2` eigenmode
2. Position-space `b=0` follows
3. `T³` diagonal (Gap B closes positively)
4. `H_prod` closed

Step 2 is false. The `S̄²` term survives with `|β/α|=1` in position space. All subsequent
steps depend on step 2 and are therefore not valid. See `god_eq_h_prod_model_routes_audit_2026-04-01.md` Finding 1.

