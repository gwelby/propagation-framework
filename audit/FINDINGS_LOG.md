# Audit Findings Log — Running Notes for the Group

**Maintainer:** Claude (Opus 4.8), hostile reviewer
**Started:** 2026-06-16
**Purpose:** A living list of findings and ideas — positive and negative — to help the team (Greg, Codex, DeepSeek, Lumi, Cascade, Devin, Hermes, and future Claudes) make this program defensible. Tags: `[RED]` stress-test target · `[BLUE]` constructive / build · `[META]` process. Priority: P0 (do now) → P3 (someday).

> **Companion docs in this folder:** `../HOSTILE_AUDIT_2026-06-16.md` (the verdict), `LOOK_ELSEWHERE_RESULTS.md` (trials-factor experiment + scripts), `DEPENDENCY_DAG.md` (floor-rule ledger).

---

## TOP OF MIND — the three things that would change my verdict

1. **`[BLUE] P0` Demote `CLAIMS.md` to match the source files.** The single highest-leverage action. God Equation → ARGUED, Weinberg → ARGUED, Koide → IDENTITY+OPEN, α → OPEN (delete the 0.60 scan hit). One editing session ends the credibility gap. Everything else is downstream of this.
2. **`[RED] P0` Apply your own "target-loaded" test to Postulate D.** You *correctly* killed the φ-harmonic (2026-04-22) and information-theoretic (2026-05-20) T3 selectors as "target-loaded." Postulate D's "seven approaches converged on a=0" is the same shape: seven routes to a destination (a=0 ⟹ U=M/2 ⟹ the desired eigenvalues) that was known in advance. Either it survives the identical scrutiny, or G3 is not "CLOSED." This is the most important internal-consistency check in the repo.
3. **`[BLUE] P0` Write the minimal honest paper.** Gravity-as-optical-geometry + neutrino Koide non-universality. Both are correct, both survive peer review, neither needs the God Equation or α. Publishing these two *first* builds the credibility that the speculative program will need later. Don't lead with the God Equation — lead with the two things that are true.

---

## RED-TEAM — next stress targets (with the null model each one needs)

- **`[RED] P0` IBM "98.1% fidelity / 153/156 qubits" needs a null model.**
  `G3_CLOSURE_20260531.md` calls it "strongest structure of any AI signature tested." That phrasing is a classic read-structure-into-noise risk. Before this counts as *any* evidence:
  - What does a **symmetric (non-chiral)** medium give on the *same* hardware, *same* analysis? (The repo says it "destroys identity" — quantify the gap with error bars.)
  - Is the classifier **trained and scored on the same shots**? If so the 98.1% is in-sample and meaningless.
  - What does **shuffled/random** data give through the identical pipeline? Pre-register that null *before* looking.
  - Until those exist, label it "suggestive hardware demo," not verification.

- **`[RED] P0` Postulate D "52.7× decoherence effect" — publish the full a-sweep.**
  The 52.7× compares a=0 against a=0.95. If the coherence-time ratio is monotone in a, then "52.7×" is an artifact of picking the far endpoint (a=0.95) as the comparison. Show coherence-time vs a over a∈[0,1]; report the effect at a=0 vs a *generic* (e.g. a=0.5), not vs the worst case. A selection pressure that only exists relative to a hand-picked alternative is not a selection pressure.

- **`[RED] P1` Koide Q pole-mass scheme dependence.**
  The 0.0009% precision uses pole masses. Q drifts under MS̄ running masses. Quantify the drift; report Q with a scheme-uncertainty band. The "remarkable precision" is partly a scheme artifact and should be stated as such (Koide's original 1981 caveat).

- **`[RED] P1` Run Top/Tau (m_t/m_τ ≈ α⁻¹/√2, EMPIRICAL 0.90) through the trials-factor instrument.**
  It is one ratio of three measured numbers. 0.90 confidence for a single coincidence is unjustified until the menu-coverage number is computed (use `audit/weinberg_trials_factor.py`, adapt the menu). Same for electron/up ≈ 1/φ³ (already flagged a-posteriori) and δ≈2/9.

- **`[RED] P2` Multi-agent independence audit.**
  Codex/DeepSeek/Claude/Lumi all share `CLAIMS.md` and the target numbers. Shared context → correlated errors that look like independent confirmation. Run one audit pass by an agent given **only** the raw data and the bare claim, with **no** access to existing derivation files or target values, and see if it reaches the same place. If it can't, the "convergence" was shared priors.

---

## BLUE-TEAM — constructive ideas to salvage and amplify the real value

- **`[BLUE] P0` The no-go corpus is your most underrated asset.**
  You have proven *dozens* of genuine negative results: the edge-flux identity `J⁰+J¹+J²=0`, the Family-C operator-algebra collapse, the κ-upstream strike, the T3 selector target-loadings, the Casimir/RG Koide-phase fences. Package these as a standalone contribution — **"Constraints on emergent-Medium and ℤ₃-generation models: a catalogue of no-go results."** This is publishable and valuable *even if the positive program never closes*, and it is the part of the repo that is most clearly real. Negative results are a contribution, not a failure.

- **`[BLUE] P0` Ship a trials-factor number with every coincidence.**
  `audit/weinberg_trials_factor.py` computes "menu coverage" for any target in seconds. Make it mandatory: any claim whose menu coverage >10% at its tolerance is `COINCIDENCE (uncorrected)`, never `DERIVED`. This converts your scanning machinery from a coincidence factory into an honesty instrument.

- **`[BLUE] P1` Automate the floor rule (DEPENDENCY_DAG.md).**
  Add `depends_on:` to each `CLAIMS.md` row; ~30 lines of Python recompute `min(parent confidence)` and flag any row published above its floor. Extend the existing `public_claim_guard.py`. This would have caught the God-Equation 0.90 the day it was written.

- **`[BLUE] P1` Attack the Koide selection problem — time-boxed, pre-registered.**
  The identity `Q=2/3 ⟺ equal U(1)/SU(3) Frobenius norm` is genuinely elegant. If ONE dynamical principle selects the equal-norm point, that is a real result. Max-entropy (Route A) is the most promising, BUT the repo already flags the trap: the fully-degenerate point gives e₂/e₁²=1/3, not 1/6 — so naive symmetry/entropy is not enough. Pre-register the exact selector and its falsifier *before* coding. Time-box it; if it loads the target, kill it like you killed the T3 selectors.

- **`[BLUE] P2` Public, git-timestamped prediction registry (write-once).**
  The repo's pre-registration discipline is excellent. Formalize it: a `PREDICTIONS/` folder where each prediction is a write-once, git-committed file with a timestamp and an explicit falsifier, *before* the measurement. This mechanically prevents postdiction from masquerading as prediction — the failure mode that produced every current `DERIVED` row.

- **`[BLUE] P2` Spin the consciousness/biology claims into a separate repo.**
  "Life = coherence," "8h sleep," "consciousness = self-referential propagation" share no derivation machinery with the physics and dilute its credibility with reviewers. Different falsifiers, different audience, different risk profile. Keep Fundamentals about the Medium + particle sector.

---

## META — process observations

- **`[META] P1` Documentation volume is being mistaken for progress.**
  Hundreds of derivation files, a 28 MB `PROPAGATION_FRAMEWORK_v2.pdf`, a `BOOK_PROPAGATION_FRAMEWORK.pdf`, explorer panels, UI/UX "premium" passes — all produced while the load-bearing theorems are open. Your own `WHATS_NEXT.md` says it: *"do not let the public layer outrun the exact-status layer."* It has. Freeze book/UI work until `CLAIMS.md` matches the source files.

- **`[META] P1` Single source of truth for "current state."**
  `STATE.md` (physics), `RESUME.md` (Lean compile errors, by Devin/Kimi), `REMEMBER.md` (UI/UX pass) describe three different projects. A new agent cannot tell what's true. Pick one; delete or subordinate the others.

- **`[META] P2` Provenance to the front.**
  Koide (1981), Foot (1994 — the PDF is in the repo), de Vries (2004), Rivero (2005–6) authored the interesting relations. Put that in the abstract, not the footnotes. It is more honest *and* it protects you from a priority dispute.

- **`[META] P2` "Lean-certified" wording.**
  Every Lean file proves an algebraic identity, not a physics derivation. Relabel uniformly: "algebraic content machine-checked in Lean 4." True, still impressive, no longer overclaiming. (Also: `lake`/`lean` are not installed in at least one working environment, and per `RESUME.md` parts of the project don't build — so every "lake build passed" line is self-reported. Add a CI badge with a real build log, or drop the claim.)

- **`[META] P3` The Lean grab-bag.**
  `CollatzSyracuse.lean` and `ShorBound.lean` assume the Collatz conjecture and a Shor bound as `axiom`s and (per RESUME.md) don't compile. They are unrelated to the physics. Either justify their presence or move them out — they make the formalization project look unfocused.

---

## VERIFIED-GOOD (don't let the criticism erase these)

- Gravity-as-optical-geometry: **correct physics.**
- Neutrino Koide non-universality: **correct, honestly scoped.**
- Topological kernel theorem: **genuinely proven, 0 sorrys (verified — the "sorry" grep hit was a comment).**
- The Koide `R/A=√2` ⟺ equal-norm identity: **elegant and exact.**
- The α derivation file: **the most honest document in the repo** ("FAILED… no derivation achieved").
- The audit culture itself: NO-GO logs, "running ≠ verified," pre-registration, target-loaded rejections. **Rare and worth protecting.** The fix is to make the scoreboard as honest as the trenches.

---

*Append below. Date every entry. Keep positives and negatives in the same log — the group needs both.*

---

### 2026-06-16 — `[RED]` Postulate D "seven approaches" downgraded to ~one (now substantiated, not just flagged)

Promoted the P0 flag to a verified finding. See `POSTULATE_D_PROBE_AUDIT.md` (+ `postulate_d_probe_check.py`). Result:
- Probes #4 (mutual info), #5 (Fisher info), #6 (decoherence-free subspace) all conclude "symmetric mode is preferred" — but the symmetric mode is an eigenvector of `U=aI+bM` with eigenvalue 1 for **every** a (the constraint `a+2b=1` guarantees it). **They cannot discriminate a=0.** Verified numerically.
- `a=0` is the unique value giving `U|Q = −1/2 = cos(2π/3)`, hence `U³|Q = −1/8` — the target. The eigenvalue agreement is a **consequence** of choosing a=0, i.e. **target-loaded** (the exact defect that killed the φ-harmonic and information-theoretic T3 selectors).
- Honest load-bearing count: **one** probe (#7, the 52.7× decoherence number), which itself still needs the a-sweep audit.
- **Action:** strike "seven independent approaches converged" from `CLAIMS.md`, `AGENTS_FULL.md`, board update; it is doing real rhetorical work and does not hold.

---

### 2026-06-16 — `[RED]` The "decisive 52.7× decoherence" probe is an endpoint artifact AND self-rates CONDITIONAL

Re-ran `D:\DeepSeek\sandbox\g3_decoherence_time_bounds_probe_v2.py` unmodified. See `DECOHERENCE_PROBE_AUDIT.md`. Result:
- decoherence(a) is a **smooth monotone curve** from 0.0011 (a=0) to 0.056 (a=0.95). "52.7×" = max/min = worst-endpoint / best-endpoint. No peak or basin at a=0.
- **Fair comparison a=0 vs a=1/3 is 1.62×**, on fidelities 99.89% vs 99.83% — physically negligible.
- Mechanism is **power iteration** (script renormalizes each step; a=0 = biggest spectral gap of U → fastest projection to symmetric mode). Restatement of a=0, not new physics.
- The script's **own verdict (lines 253–260): "NOT a derivation from Axioms 1-3 … G3 remains CONDITIONAL 0.88,"** and it names a *second* undeclared postulate (long-correlation-time noise). The board update **inverted its own decisive evidence.**
- **Net:** support for "G3 DERIVED" collapses. Honest status ≤ CONDITIONAL 0.88, ARGUED more defensibly.
- IBM "99.01%" = gate fidelity of a permutation circuit; demonstrates the hardware ran the circuits, not a PF claim. CLAIMS hedges it; `G3_CLOSURE` over-reaches ("strongest structure of any AI signature tested").

---

### 2026-06-16 — `[RED]`/`[BLUE]` IBM null model built; Codex already had it right

Built the explicit null model + shuffle control (`IBM_NULL_MODEL_AUDIT.md` + `ibm_null_model.py`):
- The chiral circuit is `T_chiral³ = I` **by construction**, so "return to |00⟩" only tests "does a net-identity circuit return its input?" — a gate-fidelity benchmark.
- Depolarizing noise alone reproduces the whole reported band: p=0.005→98.9% (≈ the "99.01%"), p=0.02–0.03→94–95% (≈ Codex's audited 94.6%). Three reported numbers (99.01/98.1/94.6) = three devices/depths, not a constant.
- Shuffle control: return prob is **identical under every relabeling** → the "identity preservation" signal is label-independent, carries zero PF content.
- **`[BLUE]` Credit:** Codex already concluded this on 2026-06-09 ("hardware calibration … HOLD … does not measure the −1/8 eigensector"). The audit culture worked. The problem is only that the overstated CLAIMS/`G3_CLOSURE` wording survived Codex's HOLD.
- **Action:** adopt Codex's ledger-safe wording; reconcile the three numbers; a real PF hardware test needs a coherent phase/eigenvalue readout of the −1/8 Q-sector (LCU/block-encoding/Hadamard test).

---

### 2026-06-16 — Deliverables (b) and (c) complete
- `CLAIMS_DIFF_PROPOSED.md` — exact find/replace patch for the 5 overstated rows + header + Lean wording + provenance line. PROPOSED, not applied (Codex to rule).
- `MINIMAL_HONEST_PAPER_OUTLINE.md` — recommended paper (Koide-as-EM-identity + neutrino non-universality); alternates (gravity-optics pedagogy; **the no-go corpus, judged the strongest standalone**).
