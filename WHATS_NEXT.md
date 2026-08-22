# What's Next: Rigor-First Closure Order

> **STRATEGIC DIRECTION (2026-06-18):** see [`UNDENIABLE_ROADMAP.md`](./UNDENIABLE_ROADMAP.md) — the additive path (make ONE falsifiable forward prediction conditional on Postulate D) that complements the subtractive demotion work below. The honest closure order continues here; the roadmap is *where it's headed*.
> **Truth stack:** read [`TRUTH_REFERENCE_MAP.md`](./TRUTH_REFERENCE_MAP.md) first (Codex, 2026-07-01) — the ranked "what to trust in what order" surface. This file is the *work order* over that truth stack.
> **Cross-domain bridge:** read [`MEDIUM_TRANSFER_LAYER.md`](./MEDIUM_TRANSFER_LAYER.md) before trying to connect Lean, Python, hardware, thermal laws, cognition, or narrative. The working question is: what survives through a medium, under which observation, at what cost?

**Date**: 2026-08-16 *(Top-down alignment audit + PRED-002/PRED-003 labeling fix + keystone repair + FALSIFICATION v0.7 + hash-binding v5. Prior 2026-07-14 currency layer preserved below.)*

> **UPDATE 2026-08-21:** The "Wait for Codex re-audit of three packets" hold
> has received verdicts. This does not itself set the next active lane.
> Stage 2 of the CMI bridge remains on HOLD per its Codex PASS. See the
> 2026-08-21 triage section below.
>
> **UPDATE 2026-08-22:** N=3 `GodEquationSpectrum` PASS, NARROW under the
> existing `e065688` authority; no duplicate ledger. M1 seam-sweep remains
> REJECT/HOLD. **PRED-003 scoping is now the active lane.** The first bounded
> step is a selector contract on the T1 `A_NR` branch, not a direct attack on
> the Koide phase or a new PRED-003 number.

---

## 2026-08-16 — TOP-DOWN ALIGNMENT AUDIT (Devin)

### What the roadmap demands (UNDENIABLE_ROADMAP.md)

The kill shot: ONE quantity where (a) SM is silent, (b) PF makes a specific
number, (c) **rival frameworks predict different numbers**, (d) feasible in ~10yr.

### Where each prediction stands against the kill shot criteria

| Prediction | (a) SM silent | (b) PF number | (c) Rivals differ | (d) Feasible | Status |
|---|---|---|---|---|---|
| PRED-001 (δ_CP) | YES | **NO** — no PF-native phase selector | — | YES (DUNE/HK) | **BLOCKED** — machine doesn't exist |
| PRED-002 (Q_ν ≠ 2/3) | YES | YES (Q_ν ≥ 0.033 from 2/3) | **NO** — all rivals agree Q_ν ≠ 2/3 | YES (CMB-S4) | **OPEN candidate / Codex HOLD** — valid prediction but NOT discriminating |
| PRED-003 (Δm² ratio) | YES | **NO** — PF takes Δm² as input, not derived | YES (UGP predicts 0.0294) | YES (already measured) | **NOT YET BUILT** — the kill shot candidate |

### The gap

PRED-002 is a valid forward prediction but fails criterion (c): all rivals
(Brannen, Rivero, ZiP) agree that standard Q_ν ≠ 2/3. The prediction is not
discriminating. It would falsify all frameworks simultaneously if Q_ν ≈ 2/3,
but it cannot distinguish PF from rivals.

**PRED-003 is the kill shot candidate**: if PF could derive Δm²₂₁/Δm²₃₁ from
the propagation axioms (instead of taking it as measured input), it would
produce a specific number that UGP (0.0294 from GF(7) arithmetic) disagrees
with. The ratio is already measured (NuFIT 6.0: 0.02951 ± 0.00098), so it's
testable now. But the PF-native derivation does not exist.

### What was fixed today (2026-08-16)

1. **Keystone fix:** `GodEquationSpectrum.lean` committed (`6b755c0`) —
   untracked file was blocking all aggregate `lake build PfLean` audits.
   Aggregate build verified: 8,293 jobs from clean `git archive`.
2. **FALSIFICATION v0.7 paper:** inventory corrected (44/41/3/8293),
   candidate chain updated, "machine-checked" overclaims narrowed.
   Successor 2 packet dispatched to Codex (`e065688`).
3. **PRED-002 hash-binding v5:** lifecycle binding (hash-chained
   resolution_log + lifecycle_hash), closed nested schema, envelope
   semantic consistency, fail-closed on non-mapping roots, ShorBound
   axiom removed (vacuous `True`), QSS prose narrowed at 4 locations.
   112 hostile checks pass. Lean build green (3,321 jobs). (`146261c`)
4. **PRED-002/PRED-003 labeling fix:** all four pre-registration JSON
   records corrected from "PRED-003" to "PRED-002" in notes field.
   Content hashes recomputed. PRED-003 is reserved for the Δm² ratio
   derivation (not yet built).
5. **Three packets pending Codex re-audit:**
   - Circulant3Spectrum v2 (`c0acdc9`)
   - FALSIFICATION v0.7 successor 2 (`e065688`)
   - PRED-002 hash-binding v5 (`146261c`)

### Corrected priority order (supersedes the 2026-07-01 order below)

1. ~~Heal the Lean build.~~ ✅ DONE (2026-07-11)
2. ~~Compile or demote the Shor bridge.~~ ✅ DONE (2026-07-01/02, green)
3. ~~Commit GodEquationSpectrum.lean.~~ ✅ DONE (2026-08-16, `6b755c0`)
4. ~~Fix PRED-002 hash-binding v5.~~ ✅ DONE (2026-08-16, `146261c`)
5. ~~Fix PRED-002/PRED-003 labeling.~~ ✅ DONE (2026-08-16)
6. **Wait for Codex re-audit of three packets** (Circulant3Spectrum v2,
   FALSIFICATION v0.7 s2, PRED-002 v5). No new work until verdicts.
7. **PRED-002 Codex re-audit for commitment lock.** All 4 substantive HOLD
   items resolved (transfer contract, uncertainty, rivals, reproduction).
   Awaiting Codex re-audit before Greg lock.
8. **PRED-003 (the kill shot): build a PF-native derivation of Δm²₂₁/Δm²₃₁.**
   **ACTIVE — scoping.** First step is a bounded selector contract on the
   T1 `A_NR` branch (`PREDICTIONS/PRED-003-route-S-selector-contract.md`).
   The direct Koide/number-attack is fenced. The transfer to PRED-003 is
   conditional on the T1 contract surviving Codex audit.
9. **G3-OP-MAP unconditional strike — unchanged.** All May negatives stand.
10. **Release lane, strictly in order:** RELEASE_MANIFEST + BUILD_MANIFEST
    → residual label sweep → Legal → PUBLIC HOLD recheck → Greg.

### 2026-08-21 — Pending Codex packet verdict triage

The three re-audits that blocked item 6 have now returned:

| Packet | Status | Report | Ledger / notes |
|---|---|---|---|
| Circulant3Spectrum v2 `c0acdc9` | **PASS, NARROW** | `CODEX_20260816_FUNDAMENTALS_CIRCULANT3_SPECTRUM_V2_C0ACDC9_REAUDIT.md` | F1-F4 repair passes; aggregate `PfLean` build is still HOLD because `GodEquationSpectrum.lean` is not committed at the root import boundary. |
| FALSIFICATION v0.7 s2 `e065688` | **REJECT / HOLD** | `CODEX_20260819_FUNDAMENTALS_FALSIFICATION_V07_SUCCESSOR2_E065688_REAUDIT.md` | F2 build/inventory pass; F5 paper wording and exact provenance disclosure fail; all-three-finding closure not authorized. |
| PRED-002 hash-binding v5 `146261c` | **REJECT / HOLD** | `CODEX_20260819_FUNDAMENTALS_PROSE_PRED003_V5_146261C_REAUDIT.md` | 112/112 checks and exact build pass; lifecycle tamper evidence, append-only/terminal integrity, and schema/amendment provenance fail. |

**Implication:** the "no new work until verdicts" hold is now stale.  The next
active-lane decision requires Greg.  Options are:

- Repair and resubmit one of the two HOLD packets (FALSIFICATION paper/provenance
  or PRED-002 hash-binding v6).
- Lift the CMI Stage 2 hold and attack the `CondIndepFun → mass relation` bridge.
- Move to **PRED-003 scoping** (kill shot) — this is the highest-value open
  target but still has no machinery; scoping is not a claim.
- Continue release-lane residual label sweep only if an approved ring is ready.

**Do not start Stage 2 or PRED-003 derivation work without a route update here.**

### What NOT to do (2026-08-16 additions)

- Do **not** cite PRED-002 as "the kill shot" — it fails the discrimination
  criterion (all rivals agree Q_ν ≠ 2/3). It is a valid forward prediction
  but NOT discriminating.
- Do **not** cite the hash-binding v5 infrastructure work as physics progress.
  It is trust infrastructure for the pre-registration system, not a prediction.
- Do **not** use the label "PRED-003" for the neutrino Koide records. PRED-003
  is reserved for the Δm² ratio derivation. The records commit PRED-002.

---

## DESTINATION (stated by Greg, 2026-07-11)

**(1) Truth first, whatever it is → (2) publish what survives → (3) earn conversations with real physicists — as a sequence, each stage gating the next.**

- Stage 1 is the live stage: the truth-filter (Codex audits, tiers, Lean, PREMISE_LEDGER) deciding which claims survive. Success at this stage includes demotions and falsifications — the filter working IS the progress.
- Stage 2 (publication) opens only through the release lane (priority #8 below). PUBLIC HOLD stands until then.
- Stage 3 (outreach) is research, not promotion — question-generation with real physicists (Rivero precedent: expect pointers, not endorsement). Every outreach act is gated by PUBLIC HOLD and Greg.

## HOW TO GET HERE (boot order — Greg-after-two-weeks-away, or any newcomer)

1. **`TRUTH_REFERENCE_MAP.md`** — what to trust in what order (~2 min).
2. **`STATE.md`** — what is actually happening right now: active audits, blockers (~5 min).
3. **This file** — the destination, the lanes, the work order (~10 min).

## THE LANES (8 attack angles — sovereign by design)

*Lanes stay sovereign — this file routes, it does not own. Multi-angle attack is deliberate: a lane's plan lives in the lane; only the pointer lives here.*

| # | Lane | Home (live plan/status) | As of | One-line state |
|---|------|------------------------|-------|----------------|
| 1 | Lean formalization | `lean/README.md` + `lean/PREMISE_LEDGER.md` | 08-16 | **Aggregate `lake build PfLean` = 8,293 jobs GREEN** from clean `git archive` after `GodEquationSpectrum.lean` committed (`6b755c0`). Three packets pending Codex re-audit: Circulant3Spectrum v2, FALSIFICATION v0.7 s2, PRED-002 hash-binding v5. ShorBound axiom removed (vacuous `True`), QSS prose narrowed. |
| 2 | Measurement alignment (D-series) | `measurement_alignment/MAP.md` | 07-15 | D1 v4.4 metadata repair CONDITIONAL PASS: neutral label, preserved v4.3 evidence, byte-identical v4.4 replay, and no numeric JSON change. The old v4.3-only probe rejects v4.4 markers and needs separate harness maintenance; scale-consistent/physical-statistical interpretation remains HOLD. D2 BLOCKED non-prediction (PREMISE_LEDGER 001 - not dimensionally closed) · D3 v3.1 submitted to Codex (central branch continuation accepted, MC/uncertainty layer repaired) · D1/D3 cross-surface drift fixed |
| 3 | Release / PUBLIC HOLD | `PUBLIC_RELEASE_CONTROL_PLANE.md` | 07-15 | Split into independent rings. Phiharmonic package PASS/live HOLD; Explorer V1 truth return REJECTED and visual/runtime HOLD; Knowledge Base emergency content HOLD; book emergency release HOLD; Marketing waits for exact ring packets. Blockers documented inline in `PUBLIC_RELEASE_CONTROL_PLANE.md`; `RELEASE_PLAN.md` remains stale. |
| 4 | Outreach | `PUBLIC_RELEASE_CONTROL_PLANE.md` + `outreach/HAU_OUTREACH_HOLD_20260708.md` + `HUMAN_ENTRY_MAP.md` | 07-15 | ALL claim-bearing outreach HELD pending an approved public reference body and Greg; posture = gratitude-and-questions, never validation or endorsement |
| 5 | Predictions (PRED) | `PREDICTIONS/README.md` | 08-16 | **PRED-002:** OPEN candidate / Codex HOLD. All 4 substantive items resolved. Hash-binding v5 committed (`146261c`). **NOT the kill shot** — all rivals agree Q_ν ≠ 2/3. **PRED-001:** BLOCKED. **PRED-003:** NOT YET BUILT — the kill shot candidate (PF-native Δm² ratio derivation, discriminating vs UGP). Labeling fix: JSON records corrected from "PRED-003" to "PRED-002". |
| 6 | Definitions / axioms | `definitions/README.md` + `lean/PREMISE_LEDGER.md` (H1–H21) | 07-08 | 19 canonical v1.0; consciousness = CANDIDATE 0.48 (not canonical); framework-level gaps → `PREMISE_LEDGER.md` |
| 7 | G3-OP-MAP unconditional strike | `derivations/` (audit files) | FROZEN | All May routes closed negative; reopen ONLY with a genuinely new route |
| 8 | Seed vault (frontier-model bridge) | `THE_SEED_VAULT/AGENTS.md` | 05-10 | Structure ready, one seed staged; dormant |

**Framework-gap ledger (cross-lane):** `PREMISE_LEDGER.md` — dimensional/premise holes that block downstream work (001: lepton g-2 not dimensionally closed; 002: CKM SILENT).

## STALE SURFACES — do not plan from these (stamped 2026-07-11, kept as history)

| File | Specific rot |
|------|-------------|
| `TASKS.md` (05-13) | lists T-021/T-022 as active — both closed NEGATIVE |
| `QSOP/STATE.md` (05-08) | Weinberg "DERIVED 0.90" — demoted ARGUED 0.65 on 06-16 |
| `EXPERIMENTAL_ROADMAP.md` (03-18) | predates PRED lane + Lean surge entirely |
| `FAMILY_STRIKE_PLAN.md` (04-13) | April lane assignments; T-022 "TOP PRIORITY" long closed |
| `RELEASE_PLAN.md` (06-17) | Queue 0 carries stale Weinberg/God-Eq wording; release truth lives in `PUBLIC_RELEASE_CONTROL_PLANE.md`, with blockers documented inline in that file |

**Maintenance rule:** any session that changes a priority updates THIS file the same session. A lane's plan lives in the lane; only the pointer lives here. When a lane's home file moves, fix the row above — a stale pointer is worse than no pointer.

---

## 2026-07-01 — WHAT ACTUALLY CHANGED SINCE 06-18 (and the corrected work order)

The frontier **moved** while this file sat still. Since 2026-06-18, the real work was not the G3-OP-MAP hand-derivation lane (unchanged, still open) — it was the **Lean formalization surge** and the **prediction lane**:

- **Lean surge (2026-06-14 → 06-30):** `TopologicalWeights` kernel obstruction **DERIVED 0.95** (0 sorrys, kernel-certified); `Z3FromBareMedium.lean` — degenerate residue → circulant (CONDITIONAL 0.85), D=3 symmetric+zero-diag+equal-rows **uniquely forces J−I** while **D=4 does not** (explicit counterexample), and the **D-selection principle** (D=3 unique stable dimension, CONDITIONAL 0.85); `Entropy.lean` — PFEntropy strictly decreases under T³ (residue norm ×1/8 per cycle), full-norm Pythagorean decomposition (**DERIVED 0.95**, pure linear algebra), and **isometry–J−I incompatibility** (T³ strictly contracts non-uniform states); `Axioms.lean` — H14+H15+H16 → H1, plus the translation-flow counterexample (Exp 7b). All conditional rows remain conditional on H7/H17/H18/Postulate D — none of this derives Postulate D from Axioms 1-3.
- **The 2026-06-26 alignment session** proved the self-catch mesh works pre-publication: H3 smuggling, H8 defined-as-its-own-conclusion, "stability forces symmetry" killed by Codex's `2S_D` counterexample, and the PFEntropy selection principle shown unnecessary at D=3 — all caught *before* release.
- **Prediction lane:** PRED-002 has a candidate document, but its 2026-07-24
  Codex audit **HOLDs the commitment**: DUNE/Hyper-K do not provide the named
  individual-absolute-mass measurement needed for `Q_nu`.  It is not yet the
  roadmap's live forward prediction; a revised absolute-mass transfer contract
  and re-audit are required. **PRED-001a was FALSIFIED** (PMNS μ1/τ1
  sub-pattern refuted ~3×); PRED-001 stays BLOCKED (no phase-selector machine).
- **Weinberg manuscript remediation** landed and Codex returned **CONDITIONAL PASS for the scoped stale-blocker class** (2026-07-01): manuscript/book/pdf no longer carry the stale `DERIVED` promotion language. NOT release approval — `RELEASE_MANIFEST.md`/`BUILD_MANIFEST.md` still missing; broader PUBLIC HOLD stands.
- **NISQ/Shor cross-workspace bridge** (2026-07-01): `ShorBound.lean` + `QuantumStructureSurvival.lean` are **SKETCHED, build PENDING** — not citable as proven. The empirical side (CX-dependent survival, identity-pruning mechanism, Claude's falsified leakage prediction) is recorded in `CLAIMS.md` §NISQ.

### The corrected priority order (supersedes the §Priority Order below for sequencing; the philosophy there stands)

1. ~~**Heal the Lean build.**~~ ✅ DONE (2026-07-11) — `.lake` moved to ext4; `lake build` green ~17 s; verified twice in a row.
2. **Compile or demote the Shor bridge.** `lake build PfLean.ShorBound`, then `PfLean.QuantumStructureSurvival`, separately — both now build green (~4 s each). Verified → update headers; failed → demote any `PROVEN` wording to SKETCHED. No third state. (ACTIVE)
3. **Write transfer contracts before reopening cross-domain bridges.** Use `MEDIUM_TRANSFER_LAYER.md` for thermal-arrow, G3 closure, NISQ survival, consciousness metrics, or any Lean/Python/hardware bridge. If the medium, measurement/coarse-graining map, entropy/cost functional, null model, and falsifier are not named, the route is not ready for upgrade.
4. **Close ProcessOntology's unitarity gap** (2 sorrys) or park it explicitly.
5. **Repair PRED-002 before another Codex gate.** The 2026-07-24 audit HOLDs
   its current lock: the cited DUNE/Hyper-K route does not measure the
   individual absolute masses needed for `Q_nu`; its packet path is absent and
   duplicate variants exist.  Owner must submit one evidence-backed
   absolute-mass transfer contract with uncertainty propagation and a canonical
   reproducible packet.  Do not ask Greg to lock it yet.  Report:
   `/mnt/d/Codex/REPORTS/CODEX_20260724_PRED_002_NEUTRINO_KOIDE_COMMITMENT_AUDIT.md`.
6. **G3-OP-MAP unconditional strike — unchanged.** All May negatives stand (trace-norm, Perron-Frobenius, κ/three-field all closed). The Lean J−I results *sharpen the target* (we now know exactly what J−I implies and what forces it at D=3) but do not derive Postulate D. Reopen only with a genuinely new route.
7. **EEG TEST 1 (T-020) — still the only test generating new data.** Pre-register in `protocols/muse_insight_protocol.md` BEFORE any session. Unchanged since April; still not run.
8. **Release lane, strictly in order:** write `RELEASE_MANIFEST.md` + `BUILD_MANIFEST.md` → residual "Weinberg derivation" label sweep in release copy → Legal (V3 PF-vs-Aether exact-copy is already CONDITIONAL PASS awaiting Legal) → broader PUBLIC HOLD recheck → Greg.

### What NOT to do (2026-07-01 additions to the standing list below)
- Do **not** cite `ShorBound`/`QuantumStructureSurvival` as Lean-proven — SKETCHED until built + Codex-rechecked.
- Do **not** treat the scoped Weinberg boundary clearance as publication approval.
- Do **not** let the new Lean conditional rows be quoted without their premises (H7/H17/H18/Postulate D) — "machine-checked under these premises," never "proven by the universe."
- Keep `TRUTH_REFERENCE_MAP.md` in sync whenever `CLAIMS.md`, Lean build status, or release state changes (standing rule from STATE.md).

---

## — Historical layer (2026-06-16, preserved) —

**Date**: 2026-06-16 *(Codex demotion audit applied; statuses corrected)*
**Context**: Paper v0.3 is done. Neutrino non-universality integrated as positive scope result. God Equation corrected 2026-06-16: Postulate-D Z₃ operator algebra **CONDITIONAL 0.88** / λ_c scale formula **ARGUED 0.60** — "DERIVED (with Postulate D) 0.90" is withdrawn. Weinberg angle corrected to **ARGUED 0.65** — "DERIVED" is withdrawn. God Equation Path B Families A/B/edge-flux remain historical no-gos for the stronger unconditional target. T-022/T-021 came back as honest negatives. The unconditional research strike remains: derive Postulate D / `H_prod` from Axioms 1-3 rather than adopt it as premise. T3 information-theoretic selector closed as target-loaded no-go 2026-05-20.

---

## 2026-05-13 — FRONTIER AUDIT PRIORITY

### Attack 1: G3-OP-MAP — Unconditional Postulate-D / H_prod Bridge (Codex + DeepSeek)
**The question**: Can Axioms 1-3 plus the Z3-extended Lagrangian derive Postulate D / a PF-native map from continuous phase-space trajectories `(chi, v)` to the discrete closure probability operator `T_sym^3` used by `H_prod`, instead of treating Postulate D as an explicit premise?

**Why it matters**: The S2 gate exposed that the state-sufficiency question is premature for the stronger Axioms-1-3-only route. The Q-sector tracker shows the linearized oscillator does not behave like `T_sym^3` over tested horizons (`alpha ~= +0.89`, not `-1/8`). The measurement-map explorer found no tested map that is simultaneously PF-native, channel-resolving, and closure-aligned. Until this map exists, the unconditional route remains open; the corrected accepted status is **CONDITIONAL 0.88** (Postulate-D operator algebra) per Codex demotion audit 2026-06-16.

**Allowed candidate classes**:
- spectral measurement map using the DFT basis that diagonalizes `M`,
- coarse-graining / RG map from oscillator trajectories to channel probabilities,
- damping / environment mechanism derived from PF vacuum structure,
- nonlinear completion that produces the discrete closure operator after reduction.

**Current subroute evidence**: The spectral/DFT map, simple linear damping, and block-average coarse-graining have all tested negative. The DeepSeek/frontier candidate routes are also now closed as conditional negatives:
- **Trace-norm projection (audited 2026-05-16)**: Schatten-1 trace norm does not contract in tested regimes (ratios remain >1) and loses the signed amplitude action `-1/8` under the density-matrix lift.
- **Perron-Frobenius collapse (audited 2026-05-19)**: PF theory fails to select the target eigenvalue `-1/8` from a continuum of compatible positive stochastic operators, and the positive-cone mapping requires extra open-system structure.
- **κ / three-field upstream strike (Codex audit 2026-05-23)**: C3 algebra forces only `K(a,b)=aI+bM`, leaving `κ=b` free; Axiom 1 does not force one real scalar per Z3 coset; combined with the six bridge negatives, the candidate Z3 three-field oscillator is retired as the primitive bridge.
These are scoped negatives, confirming that the linearized Z3 candidate Lagrangian does not supply the primitive closure operator without an extra PF-native measurement/decoherence bridge or different representation.

**Done when**: either (a) a PF-native map is written with domain, codomain, verification gate, and falsifier, and it reduces or analytically explains the KL gap to `T_sym^3`, thereby replacing Postulate D with an unconditional theorem; or (b) the tested class fails cleanly and the repo records that the linearized Z3 candidate Lagrangian cannot supply the primitive closure operator without an explicit premise or new physics. The retired three-field oscillator should not be reopened unless a new derivation fixes both field-content provenance and `κ`.

**Read first**: `derivations/frontier_audit_2026-05-13.md`, `derivations/g3_op_map_spectral_contract_audit_2026-05-13.md`, `derivations/g3_op_map_coarse_damping_audit_2026-05-13.md`, `derivations/s2_pf_native_gate_contract_2026-05-10.md`, `derivations/h_prod_joint_model_obligation.md`, `verification/operator_algebra.py`, `/mnt/d/DeepSeek/REPORTS/oscillator_to_closure_boundary.md`, `/mnt/d/DeepSeek/REPORTS/measurement_map_exploration.md`.

### Attack 2: Axiom 3 Selector / T1-T2 Bridges (on hold until a contract exists)
T1 and T2 remain partial derivations with named bridges (`A_NR`, `C_mom`, `C_FP`, `C_bridge`). The T3 selector candidates are closed: the **phi-harmonic closure (2026-04-22)** and the **information-theoretic selector (2026-05-20)** were both audited as target-loaded no-gos (the latter used handcoded $(N-3)$ penalties to artificially suppress $N=4$, which otherwise had double the stability margin of $N=3$). Do not reopen these or the broader theorem stack without a genuine selector contract `S = (D, F, R, V, X)` and a target-free verification gate.

### Attack 3: Koide Phase (frozen)
Do not reopen Koide phase unless a genuinely new PF-native selector appears. The Casimir, RG, projective, character-normal-form, Chebyshev, and historical-proxy lanes are fenced or negative.

---

## ⚡ 2026-04-13 — POST-AUDIT PRIORITIES

### Attack 1: Koide Phase Selector Beyond Casimir/RG (Codex + Lumi)
**The question**: After T-022 and T-021 both failed, is there any PF-native selector left that can produce `x* = 2/9` without reusing the rejected bridges?
**Why it matters**: δ\_Koide = 0.22222963 rad (|δ − 2/9| = 7.4×10⁻⁶, confirmed April 2) remains one of the strongest empirical anchors in the repo. But the two most obvious bridge attempts are now gone: T-022 did **not** find `2/9` in the bounded Casimir polynomial sector, and T-021 did **not** find any legitimate Standard Model convention where `sin²θ_W(μ)` crosses δ near `98 GeV`. Any next step has to be a genuinely new selector route, not more Casimir scanning and not a generic RG story.
**Assigned to**: Codex (new selector mechanisms only), Lumi (scope integrity and convention discipline)
**Status of prior subtasks**: T-022 algebra scan complete negative. T-021 RG physics check complete negative.
**Done when**: either (a) a new PF-native selector route is written with explicit falsifiers, or (b) the repo demotes the shared-origin thesis further.

### Attack 2: EEG TEST 1 Pre-registration + Run (Greg + Lumi)
**The question**: Does Critical Slowing Down (EEG variance increase >50%) precede genuine insight events in ≥7/10 sessions?
**Why it matters**: This is the only test generating new data the framework doesn't have yet. A positive result is the first cross-scale validation. A negative result falsifies the biological claim while leaving the particle physics results intact. Binary. Pre-registerable. Executable this week.
**Assigned to**: Greg (run the Muse sessions, button-press at insight), Lumi (write the pre-registration spec before any session runs — state the exact threshold and falsification criterion in `protocols/muse_insight_protocol.md` before touching the headset)
**Task**: T-020 (existing — see pre-registration note below)
**Done when**: Pre-registration doc exists with date stamp, then ≥10 sessions collected and analyzed.

**Rule**: Pre-register before running. Write the expected outcome in `protocols/muse_insight_protocol.md` before the first session. If the result disagrees, the pre-registered prediction stands.

---

**Date**: 2026-04-01 (original — see below for April 1 priority order, still valid for the theorem stack)
**Context**: Public-facing docs are much closer to the live truth board. The next milestone should harden theorem structure, not widen the claim surface.
**Question**: What is the shortest honest path from the current repo to a smaller number of stronger claims?

---

## 2026-04-01 Finding — Path A Ticket Is Stale

`chiral_projection_z3.py` was audited and corrected today. The script's interpretation block had claimed `β ≈ 0` and `T_L³ IS diagonal`. Both were wrong.

What chiral projection actually does:
- Kills the k=2 **eigenmode** entirely (sets its eigenvalue to zero)
- Does **not** eliminate the S̄² term from position space: `|β/α| = 1.0` (measured)
- T_L³ in the full 3D position space has **nonzero off-diagonals** — Gap B no-go still applies

What IS true: within the projected {k=0, k=1} 2D subspace, T_L³ is diagonal in the Fourier eigenbasis. That is a weaker result — 3-step periodicity within the left-handed sector, not full H_prod closure.

**Consequence for Path A ticket**:
The ticket `God_Equation_Path_A` asks to derive `b=0` from chiral coupling. That target is not what chiral projection produces. The ticket must be reframed before any derivation work proceeds, or it will repeat the interpretation error the script just corrected.

**New named gap** (not in any ticket yet):
Prove that Fourier-basis closure in the projected 2D sector implies position-space probability factorization for H_prod. This is a separate proof obligation that Path A did not previously identify.

---

## Current Call

The shortest path is not:

- more domains
- more numerology
- more outreach-first hype

The shortest path is:

- fewer unnamed moves
- cleaner theorem boundaries
- bounded closure work on the actual load-bearing bridges

That gives the following work order.

---

## Priority Order

### 1. Finish truth-sync and keep one status grammar

Keep `CLAIMS.md` as the only formal scoreboard.
Any planning, explainer, manuscript, or Explorer copy should map back to it cleanly.

This is not cosmetic.
It prevents the repo from manufacturing fake progress through language drift.

### 2. Write the Axiom 3 selector note

The framework still has a threshold principle more clearly than it has a general ordering principle.

The next bounded target is:

- `derivations/axiom3_selector_note_2026-04-01.md`

Done condition:

- one selector object or one bounded selector corollary is stated clearly enough to survive hostile audit
- or the attempted selector is killed cleanly

### 3. Close T1 physical realization

The `SU(2)` lift is no longer the weak point.
The live missing theorem is why Axiom 3 forces physical population of the available weight-2 branch.

Working card:

- `derivations/generation_closure_cards_2026-04-01.md`

Done condition:

- the T1 card no longer depends on an unnamed selector move or the external `A_NR` hypothesis

### 4. Close T2 denominator theorem

The local `2x2` Fermi-point lemma is useful but still conditional.
`M = 3` will not close until the PF-native bridge is stronger than the Volovik analogy.

Working card:

- `derivations/generation_closure_cards_2026-04-01.md`

Done condition:

- either the Fermi-point route becomes PF-native and audit-ready
- or it is ruled out and replaced with a cleaner PF-native denominator route

### 5. Reopen G3 only on the exact unconditional bridge

No more broad God Equation storytelling.
No more treating a good number as closure.
The corrected status is CONDITIONAL 0.88 (operator algebra) / ARGUED 0.60 (scale formula). This section is about the stronger target of deriving Postulate D / `H_prod` from Axioms 1-3 unconditionally.

**Path A status (reframed 2026-04-01, ticket updated)**:
- Old target: derive `b=0` from chiral ℤ₃ coupling — DEAD
- Correct target: two obligations H-A (is {k=0,k=1} sector forced by Lagrangian?) and H-B (does
  Fourier-sector closure imply position-space H_prod factorization?)
- Path A ticket now states these correctly. See `God_Equation_Path_A_—_Derive_b=0_...md`

**Path B status (Families A and B narrowed hard, 2026-04-01)**:
- Family A (direct closure-time channel intensities): STRONG RESTRICTED NO-GO CANDIDATE
  - `Cov(X^(0), X^(1)) = (441/2048)σ⁴ > 0`; survives broader iid exchange-symmetric ensemble class
  - See `derivations/god_eq_path_b_family_a_intensity_theorem_2026-04-01.md` and `..._audit_...md`
- Family B:
  - the two tested quadratic time-integrated readouts fail strongly under the isotropic real Gaussian probe
  - the natural antisymmetric edge-flux current is now an **exact no-go** because `J^(0)+J^(1)+J^(2)=0` identically, so nontrivial factorization is impossible
  - the Family A whitening covariance does **not** rescue the tested B1/B2 observables
  - See `derivations/god_eq_path_b_family_b_integrated_currents_2026-04-01.md`, `..._audit_...md`, and `derivations/god_eq_path_b_edge_flux_current_no_go_2026-04-01.md`
- Vacuum direction:
  - the free linearized `ℤ₃` vacuum points away from the Family A escape covariance
  - stronger PF/energy/entropy closure language is not signed off yet
  - See `derivations/god_eq_pf_vacuum_ensemble_analysis_2026-04-01.md` and `..._audit_...md`
- Canonical Family C (quadratic closure functionals of the operator): **now an exact no-go (2026-04-02)**. The real symmetric canonical operator algebra is exactly `span{P_0, Q}` (2-dimensional, fully C_3-invariant), so every C_3-covariant canonical kernel family collapses to `K_0 = K_1 = K_2`. See `derivations/god_eq_path_b_family_c_counterexample_search_2026-04-02.md` and `derivations/god_eq_path_b_family_c_operator_functionals_2026-04-01.md`.
- Noncanonical basis-fixed Family C probe (`Q|e_j><e_j|Q`): still open but gated on a new hidden step `H_basis` — derive why a specific basis inside the degenerate Q-sector is physically selected. The free linearized `ℤ₃` vacuum does not supply this selection (`Sigma_vac` is itself C_3-circulant; see `derivations/god_eq_pf_vacuum_propagator_exact_2026-04-01.md`).
- Nonquadratic one-medium observables: still open in principle, but now need a genuinely new probability model rather than another current-style rephrasing

Working card:

- `derivations/g3_closure_card_2026-04-01.md`

Done condition:

- Path A is either reframed with the corrected target, or ruled out and replaced
- one exact closure object
- one explicit probability model
- one proof or falsification of `H_prod`

### 6. Only then do pre-registered empirical risk and external review

IBM, EEG, and outside physicist feedback are still important.
They are just downstream of the theorem stack being stated tightly enough to be worth attacking.

The right order is:

- theorem target first
- prediction statement second
- hostile outside critique third

**Pre-registration rule (added 2026-04-01)**:
State the expected numerical result *before* running the sandbox script. The chiral script bug happened because the conclusion was written into the interpretation block first, and the computation was treated as confirmation. If the script had been pre-registered as "we expect |β/α| ≈ 0, and if |β/α| = 1 then Path A is challenged" — the wrong interpretation would never have survived.

For any new sandbox script: write the prediction in a comment at the top of the file before running it. If the result disagrees, update the prediction section to record the finding honestly before touching the interpretation.

**Sandbox hygiene (added 2026-04-01, partially completed)**:
The specific path-contaminating scripts named in the earlier pass have now been cleaned to use `Path(__file__).resolve().parent`. Keep the rule, but do not treat that old list as still-open work. Before the next empirical push, do one quick repo-wide audit for any remaining hardcoded output paths and keep the pre-registration discipline at the top of each new script.

---

## Working Documents For This Pass

- `CLAIMS.md`
- `PUBLIC_RELEASE_CONTROL_PLANE.md` (release blockers are inline here; `ACTIVE_ISSUES.md` no longer exists)
- `derivations/axiom3_selector_note_2026-04-01.md`
- `derivations/generation_closure_cards_2026-04-01.md`
- `derivations/g3_closure_card_2026-04-01.md`

These are the current bounded planning documents for the next serious theorem work.

---

## What Not To Do Next

Do not do these out of order:

- do not let the IBM chirality result be described as a proof of `H_prod`
- do not promote T1 or T2 because the algebra after the missing bridge looks beautiful
- do not reopen Koide phase or alpha derivation as if they are upstream of the selector and generation stack
- do not let the public layer outrun the exact-status layer again
- **Path A ticket is now reframed** (2026-04-01) — the stale `b=0` target is removed; obligations H-A and H-B are the live targets
- do not mistake "the computation ran and gave a number" for "the script is testing what it claims to test" — perihelion_precession.py ran for months returning None; the chiral script ran and printed the wrong interpretation for months. Running ≠ verified.

---

## Strongest Honest Summary

The framework gets closer to a finished theory by getting smaller, not bigger.

Right now that means:

1. one status grammar
2. one selector note
3. one T1 closure card
4. one T2 closure card
5. one G3 closure card — **with Path A reframed first**

If those harden, the rest of the repo reorganizes around them.
If they fail, the framework still becomes more honest and therefore more valuable.

**On testing**: the project currently has more derivation tickets than it has clean, correctly-tested, non-contaminating verification scripts. The next empirical push (EEG TEST 1) is the right external test. Before that, the sandbox needs pre-registration discipline and path cleanup. Derivation progress and testing progress are separate tracks — do not let one substitute for the other.
