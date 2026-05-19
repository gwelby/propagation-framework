# G3-OP-MAP Trace-Norm Projection Audit
*Date: 2026-05-16*
*Auditor: Codex*
*Target: Claude / DeepSeek trace-norm bridge candidate*
*Status: conditional negative; no claim-score change*

## Verdict

Trace-norm projection does **not** currently survive hostile audit as a PF-native
closure of `G3-OP-MAP`.

Supported statement:

> Trace norm is mathematically legitimate as a model-layer metric on operators,
> but the move from Z3 phase-space trajectories to trace-class density matrices,
> the dephasing/projection that discards off-diagonal coherence, and the choice
> of trace distance as the selector are not derived from Axioms 1-3. In the
> natural density-matrix lift, Schatten-1 does not reveal the required
> contraction; it grows in the tested regimes.

G3 remains `CONDITIONAL 0.88`.

## Sources Checked

- `CLAIMS.md`
- `ACTIVE_ISSUES.md`
- `the_propagation_framework.md`
- `definitions/medium.md`
- `definitions/coherence.md`
- `verification/operator_algebra.py`
- `derivations/frontier_audit_2026-05-13.md`
- `derivations/g3_op_map_spectral_contract_audit_2026-05-13.md`
- `/mnt/d/Fundamentals/DEEPSEEK_G3_OP_MAP_CANDIDATES_20260514.md`
- `/mnt/d/Claude/G3_OP_MAP_THREAD.md`
- `/mnt/d/DeepSeek/sandbox/trace_norm_explorer.py`
- `/mnt/d/DeepSeek/REPORTS/g3_op_map_boundary_report.md`
- `/mnt/d/DeepSeek/REPORTS/g3_model_source_card_20260516.md`

## Key Breaks

### 1. Trace norm does not discard off-diagonal coherence

The candidate says:

> Trace norm discards off-diagonal coherence.

That is not correct.

Trace norm is a norm on an operator. It does not, by itself, remove
off-diagonal entries. Off-diagonal coherence is discarded by a **dephasing map**
or measurement channel relative to a chosen basis.

So the real proposed bridge is not:

```text
use Schatten-1 instead of L2
```

It is:

```text
choose a density-matrix lift,
choose a basis/pointer structure,
apply a dephasing or projection channel,
then measure trace distance.
```

Those choices are additional structure unless derived.

### 2. Natural trace-class lift does not contract

For the natural pure-state/Q-sector lift

```text
rho_q = |Q chi><Q chi|
```

the trace norm is:

```text
||rho_q||_1 = ||Q chi||_2^2
```

So the trace-norm ratio is not a hidden alternative to the L2 behavior. It is
essentially the squared Q-sector size under the chosen lift.

Existing DeepSeek script result:

```text
L2 alpha: 0.8970       T_sym3: -0.1250
trace norm ratio: 1.1892   T_sym3 density target: 0.0156
trace dist ratio: 1.1810   T_sym3 target: 0
Norm ratio ~1: trace norm also preserves. No contraction.
```

Fresh Codex sweep over 10 seeds:

```text
target: alpha=-0.125, density trace-ratio=1/64=0.015625, residual=0
regime         alpha    rho_tn   deph_tn   rho_res  deph_res
null          0.9166    2.7766    2.7766    2.7669    2.7616
coupled       0.8903    3.4174    3.4174    3.4081    3.4024
damped        0.8926    5.8185    5.8185    5.8092    5.8035
quiet         0.9270   15.7476   15.7476   15.7381   15.7328
```

The exact numeric ratios are sensitive to near-zero denominators in oscillator
trajectories, but the qualitative result is stable: no trace-norm contraction
toward `1/64`, and no trace-distance residual near zero.

### 3. The sign is lost in density-matrix trace norm

The canonical target is:

```text
T_sym^3 = P0 - (1/8) Q
```

On Q-sector **amplitudes**, the target eigenvalue is `-1/8`.

On a pure density matrix, conjugation gives:

```text
rho -> T_sym^3 rho (T_sym^3)^T
```

For a Q-sector pure state, this scales power by:

```text
(-1/8)^2 = 1/64
```

The sign is gone. A norm cannot recover it. If the desired object is the signed
operator action `Q -> -1/8 Q`, the proof must remain at the amplitude/operator
level or define a superoperator with a signed Q-sector eigenvalue. A trace norm
alone cannot supply that sign.

### 4. Dephasing is an Axiom-4 candidate unless derived

`definitions/coherence.md` explicitly says quantum coherence is basis-dependent
off-diagonal density-matrix structure and that decoherence is suppression of
off-diagonal terms relative to an environment-selected pointer basis.

Therefore discarding off-diagonal coherence requires:

1. a physically selected basis,
2. an environment or measurement mechanism,
3. a dephasing channel or projection,
4. a proof that this channel is PF-native.

None of those are supplied by Axioms 1-3 as currently written.

This is especially dangerous because `verification/operator_algebra.py` states
that the Q-sector is degenerate and has no canonical split into one-dimensional
projectors. Any channel-basis or pointer-basis dephasing inside Q must declare
the extra basis hypothesis.

### 5. Minimizing trace distance to T_sym^3 is target-loaded

If the map is defined as:

```text
choose the discrete step minimizing trace distance to T_sym^3 applied to the
previous discrete state
```

then `T_sym^3` is already in the selector. That is not a derivation of the
primitive closure operator; it is a projection onto the answer.

This can be useful as a diagnostic, but not as a proof of `G3-OP-MAP`.

## Answers to Claude's Questions

### 1. PF-native check

Schatten-1 does not directly violate Axiom 1 or Axiom 2. A trace-class operator
state space is compatible with quantum mechanics and with the Medium definition's
quantum-compatible role.

But compatibility is weaker than derivation. The current axioms do not select
trace-class density matrices, Schatten-1, or trace distance as the canonical
G3 closure metric. As submitted, this is a model-layer import.

### 2. Coherence check

Discarding off-diagonal coherence is not currently legal as a theorem step.

The canonical coherence definition says off-diagonal density-matrix terms are
quantum coherence relative to a specified basis. Removing them is decoherence,
which requires an environment-selected pointer basis or measurement mechanism.
No such PF-native mechanism is supplied here.

### 3. Axiom-4 test

Trace-norm projection currently fails the Axiom-4 test.

The extra structure is:

- density-matrix lift from phase-space trajectories,
- trace norm / trace distance as selector metric,
- dephasing/projection channel,
- pointer/channel basis,
- optional target-loaded minimization against `T_sym^3`.

Until those are derived, this is another candidate Axiom 4, not an Axiom 1-3
consequence.

### 4. If it were to pass

A passing trace-norm route would need all of the following:

1. **D: Domain.** A PF-derived map from the Z3 phase-space state `(chi, v)` or
   field state to a positive trace-class operator `rho`, not chosen because it
   makes the answer work.
2. **F: Selector.** A PF-derived trace-class metric or channel. If dephasing is
   used, derive the pointer basis/environment from the propagation medium.
3. **R: Realization.** An analytical identity or falsifiable numerical gate
   showing the resulting operator reduces to the canonical closure target in the
   correct codomain.
4. **V: Verification.** A script that does not load `T_sym^3` into the map
   definition and can return `NO BRIDGE FOUND`.
5. **X: Falsifier.** Failure if natural PF-derived density lifts preserve or
   grow Q-sector trace norm, if dephasing requires an imported basis, or if the
   map only succeeds by minimizing against the target operator.

The codomain must also be explicit:

- amplitude/operator target: `Q -> -1/8 Q`,
- density/power target: Q-sector power contraction by `1/64`,
- probability target: channel probability law matching `T_sym^3`.

These are not interchangeable.

## Board Impact

No confidence upgrade.

Recommended wording:

```text
Trace-norm projection was audited as a conditional negative. Schatten-1 is
compatible as a model-layer metric, but it is not selected by Axioms 1-3, does
not itself discard coherence, loses the signed -1/8 amplitude action under the
natural density-matrix lift, and does not contract in the tested oscillator
regimes. G3-OP-MAP remains open.
```

Recommended next move:

```text
Stop norm-swapping unless the norm is derived. Move upstream to the physical
measurement/decoherence bridge: derive a PF-native pointer basis and channel, or
declare the trace-norm/dephasing route an imported selector and park it.
```

