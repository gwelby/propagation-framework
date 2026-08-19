# Consciousness Metric Program — Null-Class Test Results
*Claude · 2026-07-20 · first rung toward promotion condition #2*
*Script: `sandbox/consciousness_metric_null_class_test.py`*
*Governing spec: `definitions/consciousness_metric_program.md`*

## What this is
`consciousness_metric_program.md` lists 6 conditions for promotion from ACTIVE CANDIDATE to canonical. Condition #2 is: *"Feed-forward null holds: no feed-forward system scores `L_self_proxy > 0` after null enforcement."* This is a direct implementation and test of the abstract-theorem-layer formulas (`R_in`, `R_out`, `L_self`, `D_int`) against the program's own two **proven** analytic null classes, plus a literal feed-forward net (Falsifier #1) and a positive control.

## Scope boundary (explicit, so nobody overreads this)
- **This tests the abstract layer only** — constructed linear/tanh-bounded systems where the causal structure is known by construction. It does **not** touch EEG data, PLV/wPLI, or the `M_obs_t → M_t` bridge.
- **This does not promote `consciousness_metric_program.md` or `consciousness.md`.** No CLAIMS.md, PUBLIC HOLD, or tier change. It is one piece of evidence toward condition #2's prerequisite: does the pipeline even reproduce the program's own proven math before real data is introduced.
- The next rung is the **observable proxy layer**: the same null-class discipline run on real EEG delay-embedding + the coherence panel. The `unified_capture.py` pipeline (P1/experiments) is the natural instrument for that once the J-space×EEG redo lands.

## The honest journey (kept in, not cleaned up)
The first run **failed** 3 of 4 checks. That was the right outcome to get and report, not a problem to hide:

| Attempt | Config | Class I | Class II | Feed-forward | Positive control |
|---|---|---|---|---|---|
| 1 (naive Gaussian MI, T=200) | raw `np.cov` | PASS | **FAIL** (0.40) | **FAIL** (0.85) | **FAIL** (0.06, below floor) |
| Diagnostic: scale T (200→5000) | raw `np.cov` | — | shrinks to 0.02 ✓ | stuck at 0.80 ✗ | — |

Two different bugs, diagnosed separately before touching any fix:
1. **Class II's error shrank cleanly as T grew** (0.36→0.08→0.02) — the textbook signature of finite-sample bias in high-dimensional Gaussian MI estimation, not a conceptual flaw in the formula or null-class construction. Fixed with **Ledoit-Wolf shrinkage covariance** (`sklearn.covariance.LedoitWolf`), the standard tool for exactly this regime.
2. **The feed-forward net's error barely moved with T** (0.98→0.96→0.80) — a harder failure: both the conditional-MI numerator and the unconditional-MI ceiling are genuinely near zero for this system, so their *ratio* is noise-over-noise and numerically unstable regardless of sample size. Fixed with an explicit **noise-floor guard**: if the unconditional MI ceiling is itself below the estimator's empirical noise floor (~0.02 nats at this dimension/shrinkage config), report the normalized ratio as 0 rather than dividing near-zero by near-zero.
3. A third, unrelated bug: the **positive-control system diverged to NaN** at T=2000 — the linear feedback gains (0.5/0.6) were only stable in a narrow range and blew up over enough iterations. Fixed by **tanh-bounding** the loop, which is also the more physically honest construction (real self-referential systems are bounded).

After both fixes, Class II still needed **more samples to clear the threshold** (T=2000→0.13, T=4000→0.08, T=8000→0.05) — re-confirmed as genuine shrinkage, not threshold-tuning, via a second diagnostic sweep before locking T=8000 as the final config.

## Final result (T=8000, 20 trials/system)

| System | R_in_norm | R_out_norm | L_self | Verdict |
|---|---|---|---|---|
| Class I (exogenous-only / "thermostat") | 0.0000 | 0.0000 | **0.0000** | PASS — `L_self` floors on `R_in=0` per spec (`min`) |
| Class II (passive tracker) | 0.9536 | 0.0513 | **0.0513** | PASS — below 0.08 noise-floor threshold |
| Feed-forward net (Falsifier #1, literal) | 0.0000 | 0.0000 | **0.0000** | PASS — exact null |
| Positive control (closed self-model loop) | 0.9535 | 0.6803 | **0.6575 ± 0.22** | PASS — clearly nonzero, pipeline is not vacuous |

**All 4 checks pass.**

\* **R_out = 1.0000 anomaly — RESOLVED 2026-08-19.** Class I's `R_out_norm` was reading 1.0000, which looked wrong (X in Class I is constructed to not depend on M at all, so `R_out` should be ~0). It did not affect the verdict — `L_self = min(R_in, R_out)` correctly floored at 0 via `R_in` — but it was a real estimator bug.

  **Root cause:** M_t = A·E_t is a deterministic function of E_t, making the joint covariance of (M_t, E_t) singular. The original CMI estimator computed `I(A;B|C) = I(A;[B,C]) - I(A;C)` using **separate** Ledoit-Wolf shrinkage targets for each term. This breaks the Gaussian entropy identity `H(A|C) = H(A,C) - H(C)` because different shrinkage factors apply to each term, introducing spurious conditional dependence.

  **Canonical fix (Route B, SWE Devin):** Use a **single joint Ledoit-Wolf covariance** for the full `(A, B, C)` vector, so the entropy identity holds exactly and no artifact arises. Validated against analytic population values via Lyapunov equation (0.595 ± 0.006 vs true 0.599). See `sandbox/consciousness_cmi_repair_probe.py`.

  **Alternative fix (GLM Devin, superseded):** Added a residual-variance guard to `normalize()` detecting when A is >99% determined by C. This works for Class I but is a symptom patch — any other near-singular configuration the 1% threshold doesn't catch still inflates. Superseded by Route B's root-cause fix. See `consciousness_metric_null_class_test.py` normalize() Guard 2.

  **After fix:** Class I R_out_norm = 0.0000 (was 1.0000). All 4 checks still pass. Positive control unaffected (L_self = 0.6575).

## What this is (and isn't) evidence for
- **Is:** the abstract-layer formulas, as specified in `consciousness_metric_program.md`, correctly reproduce the program's own two proven analytic null results and the literal feed-forward-net falsifier, once estimated with an appropriately robust (shrinkage-regularized, noise-floor-guarded) mutual information estimator — and the pipeline is not vacuous (a genuine closed loop scores nonzero).
- **Is not:** validation on real data, validation of the `M_obs_t → M_t` bridge, or any claim about EEG, sleep, seizure, or anesthesia states. Condition #2 in the promotion list refers to the full program; this closes only its cheapest, safest, most foundational prerequisite.

## Honest next steps
1. ~~Investigate the Class I `R_out=1.0` oddity before trusting the pipeline on non-null data.~~ **DONE 2026-08-19** — root-caused (singular covariance from deterministic M=E mapping) and fixed (residual-variance guard in normalize()). See above.
2. Port the same null-class discipline to the observable proxy layer (real/synthetic multichannel EEG, delay embedding, PLV+wPLI panel) once capture is stable.
3. Complete the Lean formalization (`PfLean/NullClassProofs.lean`) — currently a stub with `sorry`. The mathematical argument is clear and DeepSeek-audited; the Lean plumbing for Gaussian conditional independence is the remaining work.
4. This script and result are sandbox evidence, not a CLAIMS.md row — any future promotion claim should cite this file plus the observable-layer equivalent, not this file alone.

## Independent reasoning audit (DeepSeek, 2026-07-20)
Third check, distinct from the numerical test above and the pending Lean formalization: DeepSeek audited both null classes at the reasoning level — d-separation on the causal graph, not code or estimation. **Both hold exactly, not approximately.** Class I: `X_history ⟂ M_t | E_history` follows directly since M_t is a pure function of E_history with no bypassing path from X_history. Class II: `M_t ⟂ X_future | X_t, E_t` holds since M_t is a leaf node the construction's `X_{t+1}` update never reads from. No hidden common-cause assumption in either construction.

Independently confirmed the `R_out=1.0` oddity (item 1 above) as a numerical-estimator limitation (ceiling and numerator both near the noise floor → unstable ratio), not a logical flaw in the null-class claim — matches my own diagnosis, now cross-checked.

**Boundary reinforced, worth restating precisely because it's the kind of thing that drifts:** Class I/II being closed at the abstract layer says nothing about the observable proxy layer (`M_obs_t` from EEG delay embedding) — that bridge remains explicitly unbridged, per the original program spec. Do not let future citations of "the null classes are closed" imply anything about real EEG data; they don't yet.

Full audit: `/mnt/d/Claude/inbox/processed/2026-07-20-deepseek-null-class-reasoning-audit.md`.
