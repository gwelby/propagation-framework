# Path A: Spinor / CP Obstruction Note (2026-04-04)

**Status**: BOUNDED NO-GO / TARGET REFINEMENT  
**Scope**: God Equation Path A only  
**Builds on**: `path_a_chiral_b_to_zero.md`, `god_eq_gap2_no_go_2026-04-04.md`, `h_prod_joint_model_obligation.md`, `sandbox/path_a_spinor_cp_scan.py`

---

## 0. Executive Summary

Path A is not dead, but two common simplifications are now ruled out:

1. **Chirality alone does not suppress the backward coupling.**
2. **A pure CP-odd phase deformation does not suppress the backward coupling magnitude either.**

The executable scan in `sandbox/path_a_spinor_cp_scan.py` shows:

- a left-chiral projector `P_L` acting on spinor space leaves the generation operator
  `alpha S̄ + beta S̄²` unchanged at the coefficient level
- the minimal CP-odd deformation
  `T = (a + i eps) S̄ + (a - i eps) S̄²`
  preserves `|beta/alpha| = 1` exactly for all `eps`
- the first family that actually moves `|beta/alpha|` away from `1` is a **directional amplitude asymmetry**
  `T = (a + delta + i eps) S̄ + (a - delta - i eps) S̄²`

So the surviving Path A target is narrower than "add chirality" or "add a CP phase."

It is:

> derive a physically justified **generation-directional amplitude asymmetry** in the weak / `Z_3` coupling layer.

---

## 1. The Current Path A Target

From `h_prod_joint_model_obligation.md`, the high-leverage Path A route is:

> prove that under left-chiral weak coupling on the `Z_3` Lagrangian, the forward/backward asymmetry `b/a -> 0` in the IR.

The older naive route already failed:

- `chiral_projection_z3.py` kills the `k=2` eigenmode in the Fourier picture
- but in position space the projected operator still has `|beta/alpha| = 1`

That means Path A must distinguish between:

- **spinor-space chirality**
- **generation-space directionality**

Those are not the same thing.

---

## 2. Chirality-Only No-Go

Take a spinor-generation product space:

```text
H_total = H_spinor ⊗ H_gen
```

with:

```text
P_L = left-handed projector on H_spinor
M_gen = alpha S̄ + beta S̄²  on H_gen
```

The minimal weak-coupling operator has the factorized form:

```text
O_weak ∝ P_L ⊗ M_gen
```

But then restricting to the left-handed block leaves the generation operator unchanged:

```text
O_weak |_(left block) = M_gen
```

So `P_L` by itself does **not** alter the relative weights of `S̄` and `S̄²`.

This is exactly what the executable scan confirms.

**Conclusion**: left-chiral weak coupling acting only on spinor space does not imply `beta -> 0`.

---

## 3. Pure CP-Phase No-Go

The natural minimal CP-odd deformation is:

```text
T = (a + i eps) S̄ + (a - i eps) S̄²
```

Then:

```text
|alpha| = |a + i eps| = sqrt(a^2 + eps^2)
|beta|  = |a - i eps| = sqrt(a^2 + eps^2)
```

Hence:

```text
|beta/alpha| = 1
```

for every real `eps`.

So a phase-only CP deformation can change interference structure, but it cannot change the forward/backward **magnitude ratio**.

**Conclusion**: a pure CP-odd phase is not enough to close Path A.

---

## 4. What Actually Can Move `|beta/alpha|`

The first minimal family that can suppress the backward branch is:

```text
T = (a + delta + i eps) S̄ + (a - delta - i eps) S̄²
```

Now:

```text
|alpha|^2 = (a + delta)^2 + eps^2
|beta|^2  = (a - delta)^2 + eps^2
```

So `|beta/alpha| < 1` requires `delta > 0`.

That is the key point:

> the required suppression is controlled by a **directional amplitude asymmetry** `delta`, not by chirality alone and not by a pure phase alone.

The scan shows exactly this behavior.

---

## 5. What Path A Now Really Needs

If Path A is to survive, it needs a derivation of one of the following:

1. A weak-sector coupling term whose **generation operator is already directional**:

```text
M_gen = g_fwd S̄ + g_bwd S̄²
with |g_bwd / g_fwd| -> 0 in the IR
```

2. A CP-violating mechanism that does not merely add phase, but generates a real
   forward/backward amplitude split through interference with another sector.

3. A PF-native selector principle that destabilizes the backward branch at the level
   of effective amplitudes, not just at the level of Fourier labels.

What is **not** enough:

- `P_L` by itself
- `P_L T P_L` by itself
- a pure antisymmetric imaginary deformation `i eps (S̄ - S̄²)` by itself

---

## 6. Repo-Safe Conclusion

The honest Path A update is:

> chirality-only forcing is a no-go, and phase-only CP deformation is also a no-go for suppressing `|beta/alpha|`.

Therefore the live Path A target should be stated as:

> derive a **generation-directional amplitude asymmetry** in the `Z_3` weak coupling layer, and show that it drives `b/a -> 0` in the IR.

That is a sharper target than the older "prove `P_L`" wording, and it matches the executable evidence better.

---

## 7. File Outputs

- Executable scan: `sandbox/path_a_spinor_cp_scan.py`
- CSV output: `sandbox/path_a_spinor_cp_scan.csv`

This note does not upgrade `CLAIMS.md` or `ACTIVE_ISSUES.md`.
