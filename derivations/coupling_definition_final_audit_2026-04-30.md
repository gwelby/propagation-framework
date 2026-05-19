# Coupling Definition Final Audit
*Codex hostile audit*
*Date: 2026-04-30*
*Target: `definitions/coupling.md`*

---

## Verdict

**PASS — promote `coupling.md` to CANONICAL v1.0.**

The file now defines coupling as dynamical dependence through a specified interaction structure, not as correlation itself. This is the correct primitive for measurement, decoherence, force-like interactions, observer records, and information transfer without overclaiming a universal coupling-strength formula.

---

## Findings Closed

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| CPL-01 | Critical | The draft made post-coupling correlation mandatory by requiring the joint state to be non-factorable. This fails for eigenstates, dark states, symmetry-protected states, and interactions that are present but inactive for a specific preparation. | Rewritten: coupling is dynamical dependence; under some allowed preparations it can alter states, transition probabilities, conserved-quantity exchange, or correlations. |
| CPL-02 | Critical | Thermodynamic coupling was described as "no environmental phase loss," contradicting decoherence and measurement regimes. | Rewritten: thermodynamic coupling is interaction where no stable accessible record survives; correlations may thermalize or disperse. |
| CPL-03 | High | The dependency graph was backwards: a primitive coupling definition should not depend on measurement/decoherence/forces. | Core dependencies now stop at Medium, field, state, mode, coherence, information, causal velocity, minimum substrate, and propagation. Measurement/decoherence/forces/observer are related definitions. |
| CPL-04 | High | Decoherence was described as irreversible without the effective-irreversibility caveat from `decoherence.md`. | Rewritten: decoherence makes phase relations inaccessible to the reduced system; falsifier distinguishes reduced-system decoherence from reversible unitary dephasing. |
| CPL-05 | Medium | Coupling strength wording over-focused on `H_int` and closed Hamiltonian systems. | Expanded to Hamiltonian terms, Lagrangian terms, gauge couplings, boundary conditions, scattering channels, update rules, rates, cross sections, and effective open-system dynamics. |
| CPL-06 | Medium | Causal language risked implying pre-existing entanglement is a new coupling channel or signal. | Rewritten: controllable influence through coupling is bounded by causal velocity; pre-existing correlations do not constitute a new signal channel. |
| CPL-07 | Medium | Measurement discipline was only a status table. | Added a seven-item discipline covering subsystem boundaries, interaction structure, coupled degrees of freedom, strength/rate measure, regime, causal domain, and claimed outcome. |

---

## Residual Boundaries

- Coupling is not identical to correlation. Correlation is a possible result or evidence of prior coupling.
- Coupling is not necessarily measurement, decoherence, or force; those require additional conditions.
- No universal coupling-strength formula is canonical.
- Quantum-gravity-scale coupling remains open.

---

## Promotion Authorized

Update:

- `definitions/coupling.md` status line to **CANONICAL v1.0**.
- `definitions/README.md` status table and audit log.
