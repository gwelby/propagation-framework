# State Definition Final Audit
*Codex hostile audit*
*Date: 2026-04-30*
*Target: `definitions/state.md`*

---

## Verdict

**PASS — promote `state.md` to CANONICAL v1.0.**

The definition now safely anchors the most frequently used load-bearing term in the definitions stack. It distinguishes operational state, quantum density operator, classical pointer state, mode state, and information without overcommitting to an interpretation of quantum mechanics.

---

## Findings Closed

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| ST-01 | High | The draft said states are not basis-independent in general, while also using density operators, which are basis-independent mathematical objects. | Rewritten: `ρ` is basis-independent; matrix elements, diagonal representation, and observable probabilities require a specified basis/observable context. |
| ST-02 | High | The draft conflated purity with coherence by saying a pure state is maximally coherent. | Rewritten: pure state means `S(ρ)=0`; coherence is basis-relative and not identical to purity. |
| ST-03 | High | A falsifier incorrectly required every genuine quantum state to have off-diagonal elements in at least one basis. This would mishandle maximally mixed states and decohered density operators. | Replaced with the correct falsifier: basis-independent coherence claims fail; coherence must be specified relative to a basis, observable, pointer structure, or subsystem decomposition. |
| ST-04 | Medium | The definition risked deterministic/ontological wording by saying a state determines distinguishable behavior and is what the system "IS." | Rewritten as an operational configuration sufficient to determine measurement predictions under specified dynamics and measurement context. |
| ST-05 | Medium | Measurement discipline was a claim-status table, not a measurement discipline. | Added a seven-item discipline: boundary, representation, basis/observable, evolution law, preparation/mixedness, access level, and claim status. |
| ST-06 | Medium | The energy relationship row implied `E = H` and used the Schrödinger equation in reversed form. | Rewritten: `H` is the Hamiltonian operator; `iℏ ∂|ψ⟩/∂t = H|ψ⟩`; energy values are expectation values or eigenvalues. |

---

## Residual Boundaries

- The file is operational, not interpretational. It does not choose Copenhagen, Many-Worlds, relational QM, or any other ontology of the density operator.
- The global state of the whole Medium remains open. The file only rejects globally accessible complete state claims under the current PF locality structure.
- Decoherence is treated as necessary for stable pointer records, not as a solution to Born-rule outcome selection.

---

## Promotion Authorized

Update:

- `definitions/state.md` status line to **CANONICAL v1.0**.
- `definitions/README.md` status table and audit log.
