# Propagation Definition Final Audit
*Fundamentals - `/mnt/d/Fundamentals/derivations/propagation_definition_final_audit_2026-04-29.md`*
*Target: `/mnt/d/Fundamentals/definitions/propagation.md`*
*Auditor: Codex*
*Date: 2026-04-29*

---

## Verdict

**PASS.**

`definitions/propagation.md` is safe for canonical status as the formalization of Axiom 1.

The canonical definition is:

> Propagation is the finite-speed causal transmission of a distinguishable state change through the Medium.

This does not derive propagation from the Medium. It closes the bootstrapping loop by restating the original intuitive primitive using the canonical vocabulary built to formalize it.

---

## Corrections Applied During Final Audit

Five precision fixes were required before PASS:

| ID | Issue | Correction |
|----|-------|------------|
| R-01 | Definition made propagation too mode-specific. | Broadened to distinguishable state changes: modes, field disturbances, wave packets, signal fronts, or composite excitations. |
| R-02 | Diffusion/drift were described as having no causal front, which is false microscopically. | Reframed as coarse-grained transport built from underlying causal microscopic dynamics; not propagation claims unless a front/signal/mode is specified. |
| R-03 | Velocity language treated `c` as the only causal-velocity context and underplayed phase/group taxonomy. | Rewritten to use general causal/front-velocity discipline, with `c` as the relativistic-vacuum instance. |
| R-04 | Coherent electron wave packet language implied indefinite stability. | Restricted to finite propagation regimes and stated coherence metrics explicitly. |
| R-05 | Relationship table overclaimed mode/energy/matter/Medium links. | Rewritten to keep propagation as behavior supported by canonical definitions, not as a redefinition of them. |

---

## Audit Questions

### Q1 - Does the bootstrapping section resolve circularity?

**PASS.**

The file distinguishes the original intuitive primitive from the later formal definition. Axiom 1 began with an informal primitive ("propagation"). The canonical definitions then formalized the required vocabulary: Medium, causal velocity, coherence, mode, energy, time, matter, and forces. `propagation.md` is the reverse step: it formalizes the primitive using already-canonical terms.

This is a valid definitional bootstrap, not a derivation. The file says this explicitly and does not claim that propagation is derived from the Medium.

### Q2 - Are diffusion, drift, tunneling, and propagation separated rigorously?

**PASS.**

The file now avoids the false claim that diffusion/drift are acausal. It treats them as coarse-grained transport processes built from causal microscopic dynamics. They become propagation claims only when a front, signal, disturbance, or mode is specified.

Quantum tunneling is correctly treated under causal-velocity discipline: apparent fast tunneling times do not allow controllable FTL signaling.

### Q3 - Is the dispersion math dependency-safe?

**PASS.**

The massless relation is attributed correctly:

```text
omega = ck          from the mode/dispersion relation
E = hbar omega      from energy.md
therefore E = pc
```

The file no longer attributes `E = pc` to `mode.md` alone.

---

## Residual Boundaries

The following are not defects, but must remain bounded:

- `propagation.md` does not derive the Medium.
- `propagation.md` does not derive QFT path integrals.
- `propagation.md` does not solve quantum gravity.
- `propagation.md` does not classify every transport process as propagation.
- `propagation.md` does not make diffusion, drift, phase velocity, group velocity, or tunneling into controllable FTL signals.
- `propagation.md` formalizes Axiom 1; it does not prove the whole PF.

---

## Final Status

`definitions/propagation.md`: **CANONICAL v1.0**.

Recommended next definitions:

1. `gradient.md` - now unblocked by canonical forces/propagation.
2. `observer.md` - still high risk because time/measurement/consciousness depend on it.
