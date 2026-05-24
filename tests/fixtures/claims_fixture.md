# CLAIMS.md — TEST FIXTURE (NOT THE REAL CLAIMS BOARD)
#
# This file is a minimal parser test fixture.
# It exercises every status tier but does NOT make any claims about the framework.
# Do not cite, link, or copy rows from this file. The language is intentionally
# generic and uses placeholder variable names (X, Y, W_foo) so that no content
# here can be mistaken for a real PF result.

**Last Updated**: 2099-01-01
**Status**: Synthetic fixture for `verification/claim_parser.py` unit tests. All numerical values are fabricated. Every row below is a parser test case, not a scientific claim.
**Audit Agent**: Fixture (🧪)

---

## ⦿ The Grading Scale

| Status | Definition | Confidence Range |
| :--- | :--- | :--- |
| **DERIVED** | Follows from the fixture axioms by logic/math alone. | 0.90 - 1.00 |
| **CONDITIONAL** | Formally proved but rests on a named hypothesis that is not yet derived. | 0.75 - 0.89 |
| **PARTIAL DERIVATION** | Core lemma proven; remaining physical-realization bridge is stated but open. | 0.75 - 0.89 |
| **ARGUED** | Plausible reasoning, mechanism identified, formal proof pending. | 0.70 - 0.89 |
| **EMPIRICAL** | Matches synthetic experimental data, derivation pending. | 0.60 - 0.95 |
| **INTUITION** | Insight-driven pattern, currently being modeled. | 0.30 - 0.59 |
| **OPEN** | Unresolved gap. | 0.00 - 0.29 |
| **NO_GO** | Documented failed approach; retained as a negative signpost. | 0.00 - 0.29 |

---

## ⦿ The Audit Scoreboard

### 1. Fundamental Physics

| Claim | Status | Evidence | What Falsifies It | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha Derived From X** | **DERIVED** | Fixture theorem: from the toy axioms A1-A3, the ratio `R_alpha = X / (X + Y)` is uniquely pinned to `1/2` by a closure argument on a three-element cyclic group. The result follows by logic/math alone and has a sandbox regression in `sandbox/fixture_alpha_check.py` that reproduces `R_alpha = 0.50000` to machine precision. See [fixture_alpha_derivation.md](derivations/fixture_alpha_derivation.md) and the Codex-style audit in [fixture_alpha_audit.md](derivations/fixture_alpha_audit.md). No external data is needed; this row is a pure theorem island with a local regression pin. | Proof that the closure argument on the three-element cyclic group does not pin `R_alpha`, or a sandbox regression showing `R_alpha != 1/2` outside floating-point tolerance. | 0.95 |
| **Beta Conditional On H_foo** | **CONDITIONAL** | Fixture bridge: the local lemma `L_beta: W(psi) = alpha * Q(psi)` is proven inside a `2x2` toy Hamiltonian ansatz. The full claim `Beta = alpha` then follows **pending closure of H_foo**, the named hypothesis that the toy ansatz is the correct low-energy representative of the fixture medium. Code support: `sandbox/fixture_beta_check.py` computes `W = 0.4999` on synthetic input, consistent with the lemma. Gap: `H_foo` (ansatz sufficiency) is open; the current draft derivation [fixture_beta_draft.md](derivations/fixture_beta_draft.md) states the hypothesis but does not derive it from A1-A3. This row stays CONDITIONAL until `H_foo` is closed by a Codex-audited derivation. | Proof that the `2x2` toy ansatz is not the correct low-energy representative, or a sandbox rerun showing `W / Q` drifting outside `[0.48, 0.52]`. | 0.85 |
| **Gamma Numerator Theorem** | **PARTIAL DERIVATION** | Fixture audit: the covering-space part of the Gamma theorem survives as a conditional lemma — specifically, the `SU(2)` lift step is exact, and the closure-order sector admits exactly two lift classes (`k = 1` and `k = 2`). The physical-realization bridge, however, is not yet derived: the chain rule gives only `F^{tot} >= F^{(1)}`, while the strict deficit needed for the claim requires the extra non-redundancy hypothesis `H_nr` (named hypothesis), and `H_nr` is not yet derived from A1-A3. A proposed route using a winding term `C[psi] = integral |psi|^2 dmu + kappa * winding` does not close the gap because `kappa`, its sign, and a two-local-maxima stability claim are inserted rather than derived. See [fixture_gamma_audit.md](derivations/fixture_gamma_audit.md). This row therefore stays PARTIAL DERIVATION until `H_nr` is closed. | Proof that the covering-space lift is wrong, or a Codex-audited derivation of `H_nr` from A1-A3 (which would promote the row to DERIVED), or a counter-example showing only the trivial lift class is physically realizable. | 0.85 |
| **Delta Coupling Ratio** | **ARGUED** | Fixture reasoning: the ratio `g' / g` between the two fixture couplings is plausibly fixed by a medium-geometry argument invoking the `U(1) x U(1)` splitting of the toy sector. A pressure-test script `sandbox/fixture_delta_pressure.py` returns `g' / g = 0.577 +/- 0.01`, consistent with the argued value `1 / sqrt(3)`. **Gap: the medium-geometry argument is not yet derived** — it is currently a motivational sketch, not a theorem, and the scheme-selection step (on-shell vs. a toy MS-bar analogue) is not yet derived either. Row stays ARGUED until the medium-geometry step is closed. See [fixture_delta_notes.md](derivations/fixture_delta_notes.md). | A pressure-test rerun returning `g' / g` outside `[0.55, 0.60]`, or an audited proof that the `U(1) x U(1)` splitting does not pin this ratio. | 0.80 |
| **Epsilon Mass Coincidence** | **EMPIRICAL** | Fixture numerical match: the ratio `m_A / m_B` equals `phi^3` to `0.2%` in the synthetic dataset shipped with the fixture. Monte Carlo significance: `p ~ 0.007` over 10,000 trials in `sandbox/fixture_epsilon_mc.py`. The coincidence is treated as a real signal in the fixture taxonomy, but no derivation from A1-A3 is claimed. See [fixture_epsilon_notes.md](derivations/fixture_epsilon_notes.md). | A precision update to the synthetic `m_B` value shifting the ratio outside `[phi^3 - 0.01, phi^3 + 0.01]`, or a revised trials-factor analysis pushing the coincidence back to `p > 0.1`. | 0.70 |
| **Zeta Perpetual Motion Fixture** | **NO_GO** | Documented failed approach: attempts to extract net work from the fixture's closed coherence cycle have been repeatedly shown to violate the fixture's energy-conservation axiom A1. Every proposed cycle has been audited and rejected — see [fixture_zeta_no_go.md](derivations/fixture_zeta_no_go.md). This row is retained as a negative signpost so that the verification harness' No_Go library can recognize and block any re-attempt. No score movement is possible from inside this tier. | A derivation from A1-A3 producing net work over a closed cycle (which would falsify A1 itself and invalidate the rest of the fixture, not promote this row). | 0.05 |

### 2. Biological & Cognitive Systems

| Claim | Status | Evidence | What Falsifies It | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Eta Pattern Insight** | **INTUITION** | Pattern observation: across the synthetic cognition dataset in `sandbox/fixture_eta_cognition.py`, a `2/3` duty-cycle pattern recurs in the encode/recover traces. The pattern is suggestive but no quantitative PF-specific variable has been defined that dissociates it from classical synchrony metrics. Row stays INTUITION pending a dissociating measurement. See [fixture_eta_notes.md](derivations/fixture_eta_notes.md). | A pre-registered dissociation experiment in which the `2/3` pattern fails to track the target variable after controlling for synchrony and task structure. | 0.45 |
| **Theta Frontier Gap** | **OPEN** | Currently unresolved in the fixture taxonomy: no mechanism, no sandbox script, and no proposed derivation route. This row is a placeholder so the parser exercises the OPEN tier. It carries the lowest confidence the scale allows and no evidence beyond a short description of why the question matters. | Any credible derivation route, sandbox result, or external measurement that would move this row out of OPEN — at which point the row's status would be updated by a future audit, not by the verification harness. | 0.10 |
