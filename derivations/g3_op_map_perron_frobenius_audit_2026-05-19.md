# G3-OP-MAP Perron-Frobenius Candidate Audit
*Date: 2026-05-19*
*Auditor: Codex*
*Target: DeepSeek Direction 2 from `DEEPSEEK_G3_OP_MAP_CANDIDATES_20260514.md`*
*Status: conditional negative; no claim-score change*

## Verdict

The Perron-Frobenius / positive-cone route does **not** currently survive hostile
audit as a PF-native bridge from the continuous Z3 oscillator to the discrete
closure operator.

Supported statement:

> Perron-Frobenius theory is compatible with treating `T_sym^3` as a positive
> stochastic closure operator after that operator has already been specified.
> It does not derive `T_sym^3`, does not select the signed Q-sector eigenvalue
> `-1/8`, and does not supply the missing oscillator-to-closure map. The proposed
> non-Hermitian positive cone, embedding, irreducibility condition, and collapse
> channel are extra structure unless derived from Axioms 1-3.

G3 remains `CONDITIONAL 0.88`.

## Sources Checked

- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `WHATS_NEXT.md`
- `DEEPSEEK_G3_OP_MAP_CANDIDATES_20260514.md`
- `definitions/medium.md`
- `definitions/coherence.md`
- `definitions/decoherence.md`
- `definitions/axioms.md`
- `definitions/field.md`
- `definitions/coupling.md`
- `verification/operator_algebra.py`
- `derivations/frontier_audit_2026-05-13.md`
- `derivations/g3_op_map_spectral_contract_audit_2026-05-13.md`
- `derivations/g3_op_map_coarse_damping_audit_2026-05-13.md`
- `derivations/g3_op_map_trace_norm_audit_2026-05-16.md`
- `derivations/h_prod_joint_model_obligation.md`
- `derivations/selection_boundary_synthesis_2026-05-08.md`
- `derivations/s2_pf_native_gate_contract_2026-05-10.md`
- `/mnt/d/DeepSeek/REPORTS/oscillator_to_closure_boundary.md`
- `/mnt/d/DeepSeek/REPORTS/measurement_map_exploration.md`
- `/mnt/d/DeepSeek/REPORTS/g3_model_source_card_20260516.md`
- `/mnt/d/Claude/G3_OP_MAP_THREAD.md`

## 1. C*-algebra positivity issue

The candidate says:

```text
Z3-graded C*-algebra with a non-Hermitian positive cone
```

That phrase is not a standard C*-algebra positive cone. In a C*-algebra, positive
elements are self-adjoint elements of the form `a* a` with nonnegative spectrum.
A cone containing non-Hermitian elements may be a useful ordered vector-space or
operator-system construction, but it is no longer the ordinary C*-positive cone.

So the route must choose one:

1. Use standard C*-positivity. Then positive elements are Hermitian, and the
   "non-Hermitian positive cone" claim is wrong.
2. Use a custom cone on a non-Hermitian operator space. Then the cone itself is
   extra structure and must be derived from PF dynamics, measurement, or
   decoherence.

The current submission does neither. It names the cone as if it is already
available.

## 2. Perron-Frobenius does not select the target operator

The canonical target is:

```text
T_sym = 1/2 (S_bar + S_bar^2)
T_sym^3 = P0 - (1/8) Q
```

`T_sym^3` is already an entrywise-positive stochastic matrix:

```text
T_sym^3 =
[[0.25,  0.375, 0.375],
 [0.375, 0.25,  0.375],
 [0.375, 0.375, 0.25 ]]
```

Its Perron-Frobenius eigenvector is the uniform mode `P0`, and its subdominant
Q-sector eigenvalue is `-1/8`.

But Perron-Frobenius theory by itself gives only the dominant positive
eigenvector / spectral radius structure for a positive irreducible operator. It
does not determine the subdominant eigenvalue.

Concrete sanity check: the whole symmetric Z3-positive family

```text
A(lambda) = a I + b S_bar + b S_bar^2
a = (1 + 2 lambda) / 3
b = (1 - lambda) / 3
```

has row sum 1, the same uniform Perron eigenvector, and Q-sector eigenvalue
`lambda`. For many values of `lambda`, the matrix is entrywise positive:

| lambda_Q | a | b | PF dominant mode |
|----------|---:|---:|------------------|
| -0.45 | 0.0333 | 0.4833 | uniform |
| -0.125 | 0.2500 | 0.3750 | uniform |
| 0.0 | 0.3333 | 0.3333 | uniform |
| 0.5 | 0.6667 | 0.1667 | uniform |

So the Perron-Frobenius data do not pick `lambda_Q = -1/8`. That value is one
point in a continuum. Selecting it requires an additional operator-selection
rule, not just positivity and irreducibility.

## 3. PF collapse is asymptotic, while G3 needs a one-step closure object

Perron-Frobenius collapse says that repeated application of a primitive positive
operator converges toward the dominant eigendirection.

The G3 obligation is different. The proof needs the primitive closure operator
or a replacement probability law:

```text
one closure step: Q -> -1/8 Q
```

Asymptotic convergence to `P0` is not enough. If the route says "iterate until
the Q-sector disappears," it has changed the target from the exact
`T_sym^3` closure law to long-time mixing. If the route says "use `T_sym^3` as
the positive operator whose PF theorem applies," it assumes the target operator
instead of deriving it.

## 4. The sign problem is not solved by positivity

The trace-norm audit already separated three codomains:

- amplitude/operator target: `Q -> -1/8 Q`,
- density/power target: Q-sector power contraction by `1/64`,
- probability target: channel law matching `T_sym^3`.

Perron-Frobenius can tolerate a positive matrix with negative subdominant
eigenvalues. So it is not mathematically impossible for a positive stochastic
operator to have the signed Q-sector action.

But that is weaker than the candidate needs. Perron-Frobenius does not explain
why the subdominant Q-sector eigenvalue is negative, why it equals exactly
`-1/8`, or why the Q-sector remains a two-dimensional degenerate eigenspace.

If the route moves to positive density matrices or norms, it has the same
sign-loss problem as the trace-norm route: the signed amplitude action becomes a
power contraction such as `1/64`. If it stays at the probability-deviation level,
the sign can exist, but it is not selected by PF theory.

## 5. Embedding the oscillator as a positive irreducible operator imports an open-system map

The current G3 evidence says the linearized Z3 dynamics are a conservative
second-order phase-space oscillator. The Q-sector tracker gives growth /
alignment around `alpha ~= +0.89`, not `-1/8`.

To make a Perron-Frobenius theorem applicable, the route must provide a map from
that reversible/conservative oscillator to a positive irreducible transfer
operator. That map is the missing bridge. It would likely require one of:

- a measurement channel,
- a decoherence / pointer-basis mechanism,
- a coarse-graining or RG map,
- a nonlinear completion,
- or an environment coupling.

Those are exactly the live `G3-OP-MAP` candidate classes. Naming Perron-Frobenius
does not derive any of them.

The canonical definitions reinforce this boundary:

- `field.md` requires field type, domain, representation, transformation law,
  dynamics, and observable status.
- `coupling.md` requires subsystem boundaries, interaction structure, affected
  degrees of freedom, regime, and outcome.
- `decoherence.md` requires environment-selected basis and coupling model.
- `coherence.md` requires the metric and layer of coherence to be named.

The Perron-Frobenius candidate supplies none of those details.

## Answers to Kiro's Questions

### Does the non-Hermitian extension violate Axiom 3 or the Medium definition?

Not automatically.

A non-Hermitian transfer operator can be a legitimate effective open-system,
measurement, or Markov representation. It can also be compatible with the
Medium definition if it is given a field/coupling/decoherence interpretation.

But it is not derived here. As submitted, the non-Hermitian cone is an imported
model layer. It also conflicts with standard C*-algebra positivity unless the
route explicitly leaves ordinary C*-positivity for a custom cone.

### Does Perron-Frobenius reproduce the signed `-1/8` Q-sector eigenvalue?

No.

It can describe a positive matrix that already has that eigenvalue, but it does
not select that eigenvalue. The continuum `A(lambda)` above has the same
Perron-Frobenius dominant mode for many Q-sector eigenvalues. The target
`lambda_Q = -1/8` must come from some additional PF-native operator derivation.

### What is the falsification gate?

A valid Perron-Frobenius route would need:

```text
D = continuous Z3 oscillator states plus a PF-derived observable/coarse-graining domain
F = a PF-derived positive transfer operator or cone map, not containing T_sym^3 by definition
R = the unique realized closure operator has entries diag=1/4, offdiag=3/8, equivalently Q -> -1/8 Q
V = analytical derivation or script showing this operator is uniquely selected from the stated domain
X = failure if the same PF premises allow a continuum of lambda_Q values, if T_sym^3 is inserted into F, or if the map only produces asymptotic P0 collapse
```

The simple symmetric Z3-positive family already triggers the falsifier for
uniqueness unless the route adds a new constraint that selects `lambda_Q = -1/8`.

## If This Route Were To Pass Later

A future passing route would need to state all of the following without loading
the answer:

1. **Cone definition.** Is this standard C*-positivity or a custom ordered cone?
   If custom, derive the cone from PF dynamics.
2. **Embedding.** Give the map from `(chi, v)` trajectories into the ordered
   operator space.
3. **Transfer operator.** Derive the positive irreducible operator from the
   Z3 Lagrangian, coupling, measurement, environment, or coarse-graining.
4. **Exact selection.** Prove why the Q-sector eigenvalue is exactly `-1/8`,
   not just any value in a positive Z3-circulant family.
5. **Codomain.** Declare whether the target is operator amplitude, density/power,
   or channel probability. Do not switch between them.
6. **Falsifier.** Include a gate that can return `NO BRIDGE FOUND`.

## Board Impact

No confidence-score change.

Recommended wording:

```text
The Perron-Frobenius positive-cone route was audited as a conditional negative.
PF theory is compatible with T_sym^3 once the closure operator is supplied, but
it does not derive that operator, does not select the signed -1/8 Q-sector
eigenvalue, and imports a non-Hermitian/custom cone plus an oscillator-to-positive
transfer map not derived from Axioms 1-3. G3-OP-MAP remains open.
```

Recommended next move:

```text
Stop treating positivity/collapse as a selector until the transfer operator is
derived. Move upstream to the same real bridge identified by the trace-norm
audit: a PF-native measurement, decoherence, environment, nonlinear, or RG map
from the continuous oscillator to a discrete closure operator. If no such map is
available, record the primitive closure operator as extra structure.
```
