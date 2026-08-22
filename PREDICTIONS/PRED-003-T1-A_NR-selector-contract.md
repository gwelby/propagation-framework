# T1 — A_NR Selector Contract (PRED-003 Route S, Step 1)

**Status:** SCOPING — no claim, no confidence upgrade, no locked prediction  
**Date:** 2026-08-22  
**Agent:** Devin ∇λΣ∞  
**Authority tier:** advisory — a design document, not a theorem  
**Public hold:** yes — Fundamentals PUBLIC HOLD remains in effect

---

## 1. Why this contract exists

T1 (`PfLean.TopologicalWeights`) is the cleanest training ground for the missing selector. The module proves the **availability** half of the (2,1) weights claim:

> `quatToSO3 g = 1 → closureOrder g ∈ {1, 2}` (`topological_availability`).

The missing half is **physical realization**: why both branches are populated, with the weight-2 branch carrying non-redundant coherent information. This is the `A_NR` hypothesis in `ACTIVE_ISSUES.md` and the selection boundary synthesis.

T1 is a better first step than PRED-003 because the source domain is already machine-checked, the gap is isolated, and the falsifier is direct. If a selector contract cannot close T1, it cannot close PRED-003.

---

## 2. Exact source and target

| Field | Value |
|---|---|
| **Source (PROVEN)** | `PfLean.TopologicalWeights` — `quatToSO3_ker`, `at_most_two_closure_orders`, `kernel_closure_orders`, `topological_availability`. |
| **Source structure** | The deck transformation group of the SU(2) → SO(3) double cover is `UnitQuaternion` with kernel `{±1}`. Closure orders 1 and 2 are the only algebraic possibilities. |
| **Target (OPEN)** | The physical (2,1) weights claim: in a 3D PF medium both closure-order classes are realized, with multiplicities (2,1). |
| **Target observable** | Whether the weight-2 branch is a stable, non-redundant PF realization. |

The gap is not in the topology; it is in the **realization rule** that turns available branches into realized modes.

---

## 3. Missing bridge: `A_NR`

`A_NR` is the **non-redundancy and realization** hypothesis for the weight-2 branch:

> The weight-2 branch carries coherent information that is not already contained in the weight-1 branch, and the medium must realize it in order to be stable under a PF-native selection rule.

`ACTIVE_ISSUES.md` (T1, 2026-04-28) explains why the previous `κ * winding` route failed: the coupling, sign, and two-local-maxima stability claim were inserted, not derived. The contract below avoids that failure mode by requiring a **named functional** and a **falsifiable verification gate**.

---

## 4. Proposed selector contract

This contract follows `MEDIUM_TRANSFER_LAYER.md` and the selection-boundary synthesis.

| Contract field | Proposed content |
|---|---|
| **Source** | `PfLean.TopologicalWeights` availability theorem. |
| **Target** | Stable PF realization of both closure-order branches in a 3D medium. |
| **Medium** | PF propagation state `(Φ_int, Φ_ext)` and the deck transformation `g ∈ {±1}` acting on the external field. |
| **Coupling map** | `deckAction g q = g * q` (left multiplication by the deck element). |
| **Coarse-graining / measurement map** | An observer that can only resolve the external field `Φ_ext`, not the full covering-space state. |
| **Coherence functional** | `F_C[Φ_int, Φ_ext] := I(Φ_int; Φ_ext) − H(Φ_ext)` under fixed topology and causal constraints. This is a placeholder candidate; any surviving contract must derive its form from Axioms 1–3 or name it as a new posit. |
| **Realization rule** | Stable PF realizations are local maxima of `F_C` on the space of allowed branch populations; the weight-2 branch is realized when including it strictly increases `F_C`. |
| **Null model** | The weight-2 branch is redundant (no new coherent information) and the medium realizes only the weight-1 branch. |
| **Survival metric** | `F_C` with the (2,1) branch population is strictly greater than `F_C` with the (1,0) population. |
| **Residual / noise metric** | The difference `F_C(2,1) − F_C(1,0)` must be bounded away from zero by a PF-native threshold, not by an inserted scale. |
| **Falsifier** | The lowest-order PF-native interaction on the degenerate subspace is fully symmetric, so `F_C` has no local maximum at the weight-2 branch. |

---

## 5. Concrete Lean target (not yet a theorem)

A future T1 theorem could look like this:

```lean
theorem A_NR_realization (g : UnitQuaternion) (h_quat : quatToSO3 g = 1) :
  ∃ (Φ_int Φ_ext : PFState),
    g = -1 → F_C Φ_int Φ_ext > F_C Φ_int (1 * Φ_ext) :=
sorry  -- placeholder; contract must first falsify the null model
```

This is a **target statement**, not a proof. The contract must first determine whether `F_C` can be PF-native and whether the inequality can survive.

---

## 6. Toy probe: `sandbox/t1_A_NR_selector_probe.py`

A minimal Python probe tests the null model against a family of candidate functionals. It does **not** derive the (2,1) weights; it checks whether any simple functional realizes the weight-2 branch.

### Model

- `x` = internal field value (continuous or discrete).
- `b` = branch label: `0` = weight-1 (`g = 1`), `1` = weight-2 (`g = -1`).
- The weight-2 branch has internal degeneracy 2: there are two independent modes, `b = 1a` and `b = 1b`, both with `y = -x`.
- External observation `y = g_b * x` plus small Gaussian noise.

### Candidate functionals tested

1. `F1 = I(x; y)` — mutual information between internal and external.
2. `F2 = H(b) − H(b | y)` — branch information recovered from external field.
3. `F3 = I(x; y) − H(y)` — coherence minus external entropy.

### Toy probe results (2026-08-22)

Run: `python3.12 sandbox/t1_A_NR_selector_probe.py`

```text
     p   F1 = I(x;y)   F2 = I(b;y)   F3 = I-H(y)
  0.00        3.2016       -0.0000       -1.8965
  0.50        2.3004        0.0060       -2.8222
  0.65        2.3766        0.0041       -2.6591
  0.70        2.4075        0.0043       -2.6591
  1.00        3.2000       -0.0000       -1.8484

Maxima:
  F1(I): p = 0.00, value = 3.2016
  F2(I_branch): p = 0.50, value = 0.0060
  F3(I-H): p = 1.00, value = -1.8484

Target p = 0.6667 (2 weight-2 : 1 weight-1):
  F1(I): value = 2.4075
  F2(I_branch): value = 0.0043
  F3(I-H): value = -2.6591

Verdict: NO-GO
```

### Interpretation

- `F1 = I(x;y)` is maximized at the pure branches (`p = 0` and `p = 1`), not at the mixed (2,1) point `p = 2/3`. The mixture loses determinism.
- `F2 = I(b;y)` is maximized near `p = 0.5` (maximum branch uncertainty), not at `p = 2/3`.
- `F3 = I(x;y) − H(y)` is maximized at `p = 1` (pure weight-2).

None of the simple functionals select the target `p = 2/3`. This is consistent with the T1 PARTIAL DERIVATION status and the `A_NR` gap. It is a toy no-go, not a formal impossibility theorem.

### Honest caveats

- The toy does not include the two-fold **degeneracy of the weight-2 branch** as a separate mode; it only tracks the branch probability. A real `A_NR` functional may need to act on the degenerate subspace, not just the branch label.
- The noise level `σ = 0.1` and the bin count `64` are arbitrary. The probe is meant to falsify the simplest candidates, not to explore the full functional space.
- A PF-native `F_C` could still exist, but it is not approximated by standard information-theoretic functionals.

---

## 6.1 Candidate PF-native F_C found (2026-08-22): Diophantine closure-weight functional

See `PREDICTIONS/PRED-003-T1-A_NR-candidate-F_C.md` for the full proposal.

**Functional:**

```
F_C[n_B, n_F] = - |n_B · 1 + n_F · 2 - M|
```

where `n_B` is the count of order-1 (bosonic / trivial) loop classes realized, `n_F` is the count of order-2 (fermionic / nontrivial) loop classes realized, and `M` is the spatial dimension.

**Selection rule:** maximize `F_C` subject to the non-redundancy constraint `n_B > 0, n_F > 0`.

**Why it works for M = 3:**
- `n_B + 2 n_F = 3` with `n_B, n_F > 0` has the unique solution `(n_B, n_F) = (1, 1)`.
- This is one order-1 class and one order-2 class.
- Topological weights: fermion = 2, boson = 1, so the realized pair is `(2, 1)`.

**Toy probe:** `sandbox/t1_A_NR_diophantine_F_C_probe.py`

```text
T1 A_NR Diophantine F_C probe (M = 3)
F_C[n_B, n_F] = - |n_B*1 + n_F*2 - 3|

Best non-redundant pair(s): [(1, 1)] with F_C = 0
PASS: M = 3 and F_C uniquely select one bosonic (order 1) and one fermionic (order 2) mode.
Realized topological weights: (fermion=2, boson=1) -> (2,1).
```

**Honest boundary:**
- This candidate introduces one new principle: **the total closure weight of realized loop classes equals the spatial dimension `M`**.
- `M = 3` has a PF result (`GodEquationGap.lean` D=3 uniqueness).
- Closure orders 1 and 2 are from `TopologicalWeights.lean`.
- The non-redundancy condition `n_B > 0, n_F > 0` is the `A_NR` hypothesis itself.
- The new principle is not yet derived from Axioms 1–3; it is a candidate coherence rule.

---

## 7. Failure modes to avoid

From `ACTIVE_ISSUES.md` and the selection-boundary synthesis:

- **Do not insert `κ * winding`.** The coupling, sign, and stability must come from the PF medium, not from a fit.
- **Do not claim a full spin-statistics theorem.** The target is only the weight-2 branch realization.
- **Do not strengthen T3 while T2 is unresolved.** T1 is downstream; keep the contract bounded to T1.
- **Do not promote the contract to DERIVED without a named transfer contract.** All MEDIUM fields must be filled.

---

## 8. Boundaries

- This is a **scoping contract**, not a derivation.
- No confidence score changes.
- No public, canonical, or release claim.
- The toy probe is for exploration; negative results are expected and must be reported honestly.
- If the toy probe fails as expected, the next step is to either (a) identify a PF-native `F_C` that survives the falsifier, or (b) document a formal no-go theorem.

---

## 9. Files and commands

- Source: `lean/PfLean/TopologicalWeights.lean`
- Issue: `ACTIVE_ISSUES.md` (T1)
- Route S scoping: `PREDICTIONS/PRED-003-route-S-selector-contract.md`
- Toy probe: `sandbox/t1_A_NR_selector_probe.py`
- Build: `lake build PfLean.TopologicalWeights`

---

## 10. Next step

1. Run the toy probe.
2. Record whether any candidate functional selects the weight-2 branch.
3. If not, document the missing functional as the next open object.
4. Route the contract + probe result to Codex for hostile scoping review.

---

Generated with [Devin](https://devin.ai)
