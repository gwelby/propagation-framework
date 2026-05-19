# S2 PF-Native Gate Contract
*Date: 2026-05-10*
*Author: Codex*
*Status: route contract, not a proof; no claim-score change*

## Decision

Move next to the **PF-native S2 gate**.

Do not spend the next research cycle optimizing the toy gate beyond keeping it runnable. The toy gate has done its job: it proved the selector-test shape can detect hidden memory without answer-loading. Further speed work on that model will not touch the live G3 obstruction.

The next useful question is:

> Does the actual PF local state, under the `kappa`-coupled Z3 closure object, satisfy the S2 state-sufficiency criterion for the 3-step closure event?

## Truth Anchors

- `CLAIMS.md`: G3 remains `CONDITIONAL 0.88`; the God Equation still needs the primitive-operator / probability bridge.
- `ACTIVE_ISSUES.md`: Path B still lacks a physically justified one-medium probability law on the actual `kappa`-coupled closure object.
- `derivations/z3_extended_propagation_lagrangian.md`: the linearized EOM gives
  `(Box + m^2) delta chi_j = kappa(delta chi_{j-1} + delta chi_{j+1}) + source`.
- `verification/operator_algebra.py`: canonical operator truth is
  `T_sym = 1/2(S_bar + S_bar^2)` and
  `T_sym^3 = 1/4 I + 3/8 S_bar + 3/8 S_bar^2`.
- `derivations/h_prod_joint_model_obligation.md`: Obligation 1 is full local state plus first-order evolution; Obligation 2 is primitive operator; Obligation 3 is the one-medium joint probability law.

## What The PF-Native Gate Must Test

The toy gate tested:

```text
I(X_{t+3}; H_t | state_t) = 0
```

The PF-native gate should test the same shape, but with PF objects:

```text
I(C_{t+3}; H_t | S_t) = 0
```

where:

- `C_{t+3}` is a pre-registered 3-step closure observable for one Z3 medium.
- `H_t` is the simulated local history of the medium.
- `S_t` is a PF-native candidate local state.

This gate only targets **Obligation 1**. Passing it does not prove the primitive operator and does not prove `H_prod` factorization.

## Candidate States

Test these in order.

| State | Contents | Expected role |
|-------|----------|---------------|
| `S_label` | current channel label only | negative control; should fail under actual mixing |
| `S_chi` | current field vector `(delta chi_0, delta chi_1, delta chi_2)` | tests whether configuration alone is enough |
| `S_phase` | `(delta chi, pi)` or `(delta chi, dot chi)` | first serious PF-native Markov candidate |
| `S_spectral` | canonical `(P0, Q)` decomposition of `(delta chi, pi)` | tests operator-native compression without choosing a hidden Q-basis |
| `S_full` | full local history | diagnostic upper bound only |

The key point: the Lagrangian is second-order in time. Axiom 2 gives finite-speed locality, but it does not make `delta chi` alone Markov. The natural PF-native Markov state is phase space: field plus conjugate momentum / time derivative.

## Verification Gate

Minimal v0 implementation:

1. Import canonical matrices from `verification/operator_algebra.py`; do not re-hardcode `S_bar`, `T_sym`, or `T_sym^3` in a drifting copy.
2. Simulate a one-medium linearized Z3 field model around the homogeneous vacuum:

   ```text
   d2/dt2 delta chi = kappa M delta chi - m^2 delta chi + source/noise
   M = S_bar + S_bar^2
   ```

3. Record the local history, candidate states, and the pre-registered 3-step closure observable.
4. Test whether adding `H_t` to each candidate state improves out-of-sample prediction of `C_{t+3}`.
5. Use a conditional permutation or cross-validated log-loss gate. Continuous states must have pre-registered binning or an explicitly stated estimator; no post-hoc bins.
6. Report only:

   ```text
   INSUFFICIENCY DETECTED
   no detected insufficiency
   inconclusive / underpowered
   ```

## Required Controls

- `kappa = 0` or no coupling: null control.
- Actual `T_sym` / `M`: live PF object; simple channel-label state should not pass casually.
- Pure-shift `S_bar`: positive control for diagonal closure, but still not a proof of one-medium `H_prod`.
- Toy S2 gate: regression control for the statistical method only.

## Falsifiers

The PF-native S2 route fails, or at least does not advance, if any of these happen:

- `S_phase` is not sufficient and history still improves prediction after controlling for numerical resolution.
- The only sufficient state uses variables not derivable from the Z3 Lagrangian / Axioms 1-3.
- The gate works only by changing the target from one-medium closure to three replicated experiments.
- The gate passes Obligation 1 but then gets cited as if it closed Obligation 2 or 3.

## Expected First Result

The most likely useful first result is negative/clarifying:

- `S_label` fails.
- `S_chi` may fail because the system is second-order.
- `S_phase = (delta chi, pi)` is the first candidate that has a principled chance.

That would still be progress. It would replace the vague phrase "full local state" with an auditable PF-native object.

## Stop Rule

Do not claim G3 progress from this gate until the result is connected to:

1. a derived primitive closure operator, and
2. a one-medium probability law whose channel events actually factorize.

Until then, G3 stays `CONDITIONAL 0.88`.
