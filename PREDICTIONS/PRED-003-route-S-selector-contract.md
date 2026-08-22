# PRED-003 — Route S: Bounded Selector-Contract Training Ground

**Status:** SCOPING — no locked number, no pre-registration hash  
**Date:** 2026-08-22  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory — route map, not a theorem or claim  
**Public hold:** yes — Fundamentals PUBLIC HOLD remains in effect

---

## 1. The problem this route addresses

The multi-angle PRED-003 sweep (Route A, B, C, D, U) converged on one fact:

> PF has the right number of modes (three) and the right degenerate residue eigenvalue (−1/8), but it has **no mechanism to split that degeneracy**, no eV-scale bridge, and no map to the SM neutrino mass eigenstates.

`selection_boundary_synthesis_2026-05-08.md` shows the same pattern across four fronts (T1, T2, G3/H_prod, Koide). The missing object is the same: a **PF-native selector contract** that turns an available topological degeneracy into a physically realized, distinct outcome.

Route S proposes to build **one** such contract on the cleanest bounded domain first, then test whether it transfers to PRED-003.

---

## 2. Why T1 / `A_NR` is the best training ground

The selection-boundary synthesis names two tracks:

1. **Primary track:** T1 / `A_NR` — the weight-2 branch of the SU(2) lift for `π₁(SO(3)) ≅ Z₂`.
2. **Parallel fallback:** S2 / minimal-sufficient-state on G3 Obligation 1.

T1 is the best first choice because:

- It is the **cleanest expression** of the availability-versus-realization gap.
- It does **not** require the full G3 probability model or the Koide ansatz.
- It has a **direct falsifier**: if the lowest-order PF-native interaction remains symmetric in the target subspace, the contract fails.
- It has a **Codex-audited Lean base** (`PfLean.TopologicalWeights`) with `at_most_two_closure_orders` and `topological_availability`.

The T1 arena is: topology makes a weight-2 branch *available*, but a theorem is needed to say it is *realized* and *non-redundant*.

The PRED-003 arena is: topology makes a twofold `−1/8` residue *available*, but a theorem is needed to say it is *split* into two distinct mass-squared values.

If a selector contract closes T1, the same contract pattern can be tested on the PRED-003 degeneracy. If it fails, the framework becomes sharper because the boundary is named.

---

## 3. Proposed selector contract

| Field | Content |
|---|---|
| **Domain** | T1: the weight-2 branch of the SU(2) lift over `π₁(SO(3)) ≅ Z₂` (already available in `PfLean.TopologicalWeights`). |
| **PF-native functional** | A coherence functional `F_C = I(Φ_int; Φ_ext)` on local PF states, or an equivalent minimal-sufficient-state functional `S₂` derived from Axiom 2 locality. |
| **Realization rule** | Stable PF realizations are **local maxima** of `F_C` under fixed topology and causal constraints; the weight-2 branch is selected when it carries non-redundant coherent information. |
| **Verification gate** | Compute the lowest-order allowed PF-native interaction on the stated degenerate subspace and verify that its extrema select the claimed branch without inserting that target into the interaction. |
| **Falsifier** | The lowest-order PF-native interaction remains fully symmetric in the target subspace, or selects a value/branch different from the claimed physical one. |

This is the same contract shape as the **S3 / Degeneracy-Breaking Vacuum Selector** in `selection_boundary_synthesis_2026-05-08.md`, but trained on T1 first.

---

## 4. Transfer to PRED-003 — only if T1 contract survives

If the T1 selector contract passes hostile audit, the next step is to apply it to the PRED-003 Q-sector degeneracy `μ₁² = μ₂² = m² + κ`.

The transfer contract fields from `MEDIUM_TRANSFER_LAYER.md` would then be:

| Field | Proposed content |
|---|---|
| **Source domain** | PF propagation geometry; T1-proven selector contract. |
| **Source structure** | Twofold `−1/8` residue degeneracy in the 3-cycle God Equation spectrum. |
| **Target domain** | SM neutrino mass eigenstates. |
| **Target observable** | `r_ν = Δm²₂₁ / Δm²₃₁`. |
| **Medium** | The T1 selector functional, now acting on the Q-sector degeneracy. |
| **Coupling map** | `PF residue modes → mass eigenstates m₁, m₂, m₃` (to be named). |
| **Coarse-graining / measurement map** | `SM neutrino mass-squared differences` (to be named). |
| **Entropy / cost functional** | The same `F_C` or `S₂` that selected the T1 branch. |
| **Null model** | The mass-squared differences are free Lagrangian parameters (SM view). |
| **Falsifier** | No PF-native, dimensionally closed functional selects `r_ν = 0.02951`; or the selected value is wrong. |

This is a **conditional transfer**. It only makes sense if the T1 contract is real.

---

## 5. What this route is not

- **Not a new axiom.** The contract must be derivable from Axioms 1–3 + Postulate D, not inserted by hand.
- **Not a general selector theorem.** It is one contract for one bounded domain.
- **Not a PRED-003 derivation.** It is a training-ground route. The PRED-003 transfer is step two.
- **Not a public or canonical claim.** It is scoping under PUBLIC HOLD.

---

## 6. Concrete next actions

1. **Write a one-page T1 selector contract** with exact Lean theorem targets in `PfLean.TopologicalWeights`.
2. **Identify the candidate functional** `F_C` or `S₂` and express it in PF terms.
3. **Run a toy Python probe** on the T1 branch to see if any natural functional selects the weight-2 branch.
4. **If the toy probe fails, document the no-go** and update this file.
5. **If it succeeds, route to Codex hostile audit** before applying to PRED-003.

---

## 7. References

- `selection_boundary_synthesis_2026-05-08.md` — the cross-front selector contract pattern.
- `PREDICTIONS/PRED-003-neutrino-mass-squared-ratio.md` — the PRED-003 multi-angle sweep.
- `MEDIUM_TRANSFER_LAYER.md` — transfer-contract fields.
- `lean/PfLean/TopologicalWeights.lean` — Codex-audited T1 formalization.

---

Generated with [Devin](https://devin.ai)
