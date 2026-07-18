# Askability Audit — first pass (Claude, 2026-07-11)
*Generalizes the D2/PREMISE-001 catch: before any quantitative PF formula gets a compute task, three questions. (1) **Dimensionally closed?** (2) **Every input defined as a specific physical quantity?** (3) **Gradable — does a stated experiment/measurement exist that can separate the claim's variables?***
*Scope: every formula-bearing row in `CLAIMS.md` as of 2026-07-11. First pass by one reviewer; **not authoritative until Codex verifies** — dispatch in `/mnt/d/Codex/inbox/`. My known calibration: algebra/structure reliable, statistics not — no sigma judgments are made here.*

## Verdicts

| # | Claim (CLAIMS.md row) | Q1 closed? | Q2 inputs defined? | Q3 gradable? | Verdict |
|---|----------------------|-----------|--------------------|--------------|---------|
| 1 | Lepton g-2 `δa = w_max/(m/λ_c·(ħc)⁻¹)` | **NO** — mass⁻² or mass⁻¹ under either reading; never dimensionless | λ_c pinned (top Compton, calibrated); w_max dimension unclear | no — non-prediction | **BROKEN** (= PREMISE_LEDGER 001; blocks D2/051/052) |
| 2 | α structural: `α = Z₀/2R_K` | yes (Ω/Ω) | yes (measured constants) | **NO** — `Z₀/(2R_K) = e²μ₀c/2h = α` is an **exact SI algebraic identity**; it holds by definition of the constants, so no measurement can ever grade the PF content | **UNGRADABLE AS STATED** — tautology risk. Becomes a claim only if PF derives Z₀ or R_K *independently*. Stated falsifier ("proof of no PF-native origin") is not a measurement. ⚠️ verify my algebra (Codex) |
| 3 | α numeric (Casimir combo → 1/137.119) | yes (dimensionless) | combo not principled (look-elsewhere P≈0.46) | gradable but target-loaded | correctly parked OPEN — no action |
| 4 | Weinberg `R = 1−x₊(1/2)/x₊(1) = 0.22310` | yes (root ratio) | yes (Casimir C₂; k=1 via Axiom 3b) | **PARTIAL** — formula gives ONE number but the comparison target is scheme-dependent (on-shell 0.22337 vs MS-bar ~0.231) and scheme selection is NOT derived. The grade depends on an undefined choice | **PARTIAL** — askable once the scheme rule is pre-registered (or derived). Matches existing ARGUED 0.65 |
| 5 | λ_c scale: `√2·l_P·exp(4π²N^{D/2}/b₀)` | yes (length) | **NO** — `N^{D/2}` fit-selected (N=3,D=3 chosen to match); H_prod not derived | **CIRCULAR-RISK** — the "observed" λ_c it is graded against is itself calibrated to m_t; formula-vs-calibration is not formula-vs-measurement | **PARTIAL** — honest at ARGUED 0.60; flag: grading target needs an independent λ_c measurement to mean anything |
| 6 | Variable c: `c_local = 1/√(1+λχ)` | conditionally — requires λχ dimensionless; with λ~1/M_Pl, χ must carry mass dimension | **VERIFY** — is χ's field normalization pinned in the derivation file, or free? | yes (Cassini bound now; SKA/LISA forward) | **VERIFY-INPUT** — one definedness check away from GOOD |
| 7 | QCD confinement `r_conf = λ_c·exp(2π/b₀α_s)` | yes (length) | λ_c calibrated + α_s empirical (borrowed, declared) | yes — and honestly graded (2.2 fm vs 0.9 fm overshoot stated) | **GOOD askability** (independent of its 0.72 truth-confidence) |
| 8 | Koide Q=2/3 geometric identity | yes (dimensionless) | yes (equal-amplitude premise explicit) | yes — 3σ mass-drift falsifier stated | **GOLD STANDARD** — the row every other row should look like |
| 9 | Koide phase δ=2/9 | yes | yes | yes — pre-registered (2026-04-01) with promotion/demotion rules | **GOLD STANDARD** |
| 10 | Three Generations `Q(N)=2N/(2N+3)` | yes | conditional premises explicit (T1/T2 owed) | yes, as conditional | GOOD (conditional askability, honestly labeled) |
| 11 | Top/Tau `m_t/m_τ ≈ α⁻¹/√2` | yes (ratio) | yes | yes (0.5% falsifier) | GOOD askability; note tier is EMPIRICAL-numerological — askable ≠ explained |
| 12 | Coulomb eikonal → `E_k = −1/2k²` | yes (natural units, internally consistent model) | yes | yes — graded (0.00% phase-closure, all e) | GOOD |
| 13 | Neutrino Koide Q_NO/Q_IO + PRED-002 | yes | yes | yes — 1% falsifier + forward window (DUNE/HK) | GOOD — PRED-002 is the flagship askable claim |
| 14 | 8h sleep 2/3 fraction | yes (fraction) | mapping analogical (declared) | **WEAK** — no stated measurement separates the PF mechanism from mundane explanations | PARTIAL — askability gap is the falsifier design, not the number |
| 15 | CKM pseudo-mass θ₂₃ (D3 lane) | yes (angle) | yes (external model) | **PARTIAL** — gradable ONLY with pre-registered branch rule + consistent covariance (Codex v3 requirements = exactly the missing askability conditions) | PARTIAL — v3 requirements ARE the fix |

## The pattern (three sentences)
Dimensionless-ratio claims are structurally immune to Q1 failure — their askability risk migrates to **input-definedness** (fit-selected exponents) and **target-selection** (which scheme, which branch, which calibration). The two failure archetypes found: **dimensional non-closure** (g-2 — the only Q1 failure) and **identity-grading** (α structural, λ_c-vs-calibrated-λ_c — formulas graded against things that cannot disagree with them). Refines DeepSeek's computability map: *ratios are computable, but computable ≠ gradable — check what the number is compared TO.*

## Recommended actions (pending Codex verification)
1. **PREMISE_LEDGER Entry candidate 003:** α structural identification is an exact SI identity (`Z₀ = 2αR_K`) — ungradable without an independent PF derivation of Z₀ or R_K. (Codex: verify the algebra first.)
2. **PREMISE_LEDGER Entry candidate 004:** λ_c scale formula is graded against a calibrated target — needs an independent λ_c estimate or explicit "internal-consistency only" label.
3. **VERIFY task (small):** pin χ's normalization in the variable-c derivation; if free, the Cassini bound constrains λχ jointly, not λ.
4. **Rule for new D-tasks (proposed for WHATS_NEXT):** no compute task on a formula that hasn't passed Q1–Q3. Cost: minutes of reading. Prevented losses this month: D2's Monte Carlo, marrakesh n=5–7, D3 v1/v2 sigma language.

## Boundary
No claim tier changed by this audit — it assesses *askability*, not truth. No PUBLIC HOLD, Lean, Legal, or Greg boundary touched. First pass by Claude (structure/algebra lane); statistical judgments deliberately absent. Authoritative only after Codex replay.
