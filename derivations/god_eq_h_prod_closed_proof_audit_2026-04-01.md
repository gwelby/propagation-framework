# God Equation H_prod Closed Proof — Codex Audit (2026-04-01)
*Audit of the replacement draft claiming closure via an “Identity Preservation Selection Rule”*

**Claim under audit**: `derivations/god_eq_h_prod_closed_proof.md` closes `H_prod` and therefore materially closes the God Equation bridge  
**Verdict**: **No sign-off.** The draft overclaims all three live proof obligations.  
**Current truth owner**: `CLAIMS.md`, `ACTIVE_ISSUES.md`, `god_eq_h_prod_model_routes_audit_2026-04-01.md`

---

## Finding 1 — The draft smuggles `b = 0` as a selection rule

The file claims:

> stable matter generations require a purely chiral walk, therefore `b = 0` is forced.

This is not a derivation from the `Z_3` Lagrangian.

It is a selection principle asserted from:

- entropy behavior in a sandbox model
- IBM hardware evidence for identity preservation
- the physical desire that generations remain distinguishable

None of those establishes the theorem

`Z_3` Lagrangian + Axioms 1–3 -> `b = 0`.

The draft therefore reintroduces the dead Path A target under a new verbal label.

---

## Finding 2 — The “independent field model” does not follow from the actual EOM

The actual linearized EOM in `z3_extended_propagation_lagrangian.md` is

`(Box + m^2) delta chi_j = kappa (delta chi_{j-1} + delta chi_{j+1}) + (lambda/3) delta T`.

That is explicitly cross-coupled.

The draft says the fields become independent “under the stability-forced `b = 0` limit,” but that limit is exactly what remains unproved.

So the independence claim is conditional on the very bridge the file is supposed to derive.

---

## Finding 3 — The probability factorization is still built into the setup

The draft proves `H_prod` by defining the joint law as a product of three independent field measures.

That is mathematically fine as an auxiliary experiment model.

It is not yet a proof that the God Equation observables for one three-channel medium factorize.

This is still the Q-C gate:

- one-system reading: not addressed
- replicated-experiment reading: mathematically clean, physically under-justified

So the file relocates the gap rather than closes it.

---

## Finding 4 — The draft ignores the actual Path A / Path B post-audit split

The live route split is:

- **Path A**: projected `{k=0,k=1}` sector -> position-space bridge
- **Path B**: actual non-diagonal closure object -> explicit probability model

The draft collapses that split back into:

- “force `b = 0`”
- “therefore pure shift”
- “therefore factorization”

That is exactly the pre-audit storyline the repo was trying to retire.

---

## Finding 5 — The current route audit already blocks the closure language

See `god_eq_h_prod_model_routes_audit_2026-04-01.md`:

- the zero-diagonal claim for the actual projected operator does not hold
- Model A still needs the Fourier-to-position-space bridge
- Model B still lacks a physically justified single-system probability law
- `kappa` mixing is same-order at closure scale, not a small correction

That is incompatible with “DERIVATION COMPLETE.”

---

## Bottom Line

`derivations/god_eq_h_prod_closed_proof.md` is a **candidate overclaim**, not a signed result.

The honest current state is still:

- `H_prod` open
- God Equation `CONDITIONAL 0.88`

Use:

- `god_eq_h_prod_model_routes_audit_2026-04-01.md` for the live route verdict
- `ACTIVE_ISSUES.md` for the current G3 owner state

Do **not** promote from this draft without a fresh Codex sign-off.
