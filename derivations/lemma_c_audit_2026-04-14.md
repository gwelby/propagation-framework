# Lemma C Audit — 2026-04-14
*Codex hostile audit of the spinorial population argument*

**Audit target:** "A coherence-maximizing medium must populate all available rotational branches; therefore the weight-2 spinorial branch is physically realized."

**Status before audit:** CANDIDATE  
**Verdict:** **NO SIGN-OFF. No T1 upgrade.**  
**Effect on board:** T1 remains `PARTIAL DERIVATION 0.85`.

Builds on:

- `derivations/topological_weights_t1_audit_2026-03-28.md`
- `derivations/t1_physical_realization_theorem.md`
- `derivations/t1_physical_realization_theorem_audit_2026-03-31.md`
- `derivations/t1_non_redundancy_lemma.md`
- `derivations/axiom3_coherence_functional_spec.md`
- `ACTIVE_ISSUES.md`
- `CLAIMS.md`

---

## 1. Exact Claim Audited

Lemma C tries to close the remaining T1 gap by arguing:

1. `pi_1(SO(3)) ~= Z_2` makes the weight-2 branch topologically available
2. Axiom 3 should make a coherence-seeking medium populate all available branches
3. therefore the weight-2 branch is physically realized

The proposed upgrade path was:

> if "available but unpopulated" is a strict coherence deficit, T1 upgrades from `PARTIAL DERIVATION 0.85` to `DERIVED 0.93`.

That upgrade does **not** survive audit.

---

## 2. What Actually Survives

### 2.1 The topology survives

This part is unchanged and solid:

- `pi_1(SO(3)) ~= Z_2`
- there are exactly two loop classes
- the only minimal lifted closure orders are `1` and `2`

### 2.2 The `SU(2)` lift survives conditionally

If a genuine weight-2 rotational mode is physically admitted, it must live on the `SU(2)` double cover rather than on `SO(3)` alone.

That is a clean covering-space statement. It is **not** the physical-population theorem.

### 2.3 The Family C chain-rule lower bound survives

The valid information-theoretic statement is still:

`F_C^tot >= F_C^(1)`

This means the sector-complete candidate score is not lower than the weight-1-only score.

It does **not** prove strict deficit for leaving branch 2 empty.

---

## 3. Exact Reason Lemma C Fails

Lemma C needs two things, not one:

1. a **selector principle**
2. a **strict gain principle**

The current repo still lacks both in derived form.

### 3.1 Missing piece A: selector

Lemma C assumes that Axiom 3 does more than impose a coherence threshold.
It assumes Axiom 3 orders coherent candidates and pushes the medium to the maximizer of the Family C functional.

That is not currently derived.

The design spec already names this as the open frontier:

> Axiom 3 currently gives threshold, not ordering.

So Lemma C does not get a selector "for free" from Axiom 3 as written.

### 3.2 Missing piece B: strict gain

Even if one grants the Family C candidate language and an extremal principle, Lemma C still needs:

`A_NR: I(Phi_int^(2); Phi_ext^(2) | Phi_int^(1), Phi_ext^(1)) > 0`

or an equivalent branch-faithfulness statement.

Without that, the chain rule gives only:

`F_C^tot >= F_C^(1)`

not

`F_C^tot > F_C^(1)`.

So "available but unpopulated" is not yet a theorem-grade strict coherence deficit.

---

## 4. Existing No-Go Already Covers This

The 2026-04-04 file `t1_non_redundancy_lemma.md` already proves the relevant no-go:

### Countermodel A — available but unpopulated

Weight-2 branch is topologically available but physically constant / unpopulated.

Then:

`I(X_2; Y_2 | X_1, Y_1) = 0`

This violates no current PF axiom.

### Countermodel B — populated but redundant

Weight-2 branch is present but fully recoverable from branch 1:

`X_2 = f(X_1, Y_1), Y_2 = g(X_1, Y_1)`

Then again:

`I(X_2; Y_2 | X_1, Y_1) = 0`

So topological distinctness does **not** imply information-theoretic non-redundancy.

That is the exact reason Lemma C fails as a derivation.

---

## 5. Strongest Honest Verdict

Lemma C is **not** a new closure of T1.
It is a more intuitive restatement of the same missing bridge already isolated in prior audits.

The honest summary is:

> topology gives availability; covering-space theory gives the conditional `SU(2)` lift; the Family C route gives a non-decrease bound; but physical population of the weight-2 branch still requires a derived selector plus a derived branch-faithfulness / non-redundancy statement.

So the repo should **not** say:

- "Lemma C confirmed"
- "T1 upgrades to DERIVED 0.93"
- "Axiom 3 forces population of all available rotational branches"

---

## 6. What Would Actually Close T1

The weakest honest closure package remains:

### A_BF — Branch Faithfulness

After conditioning on branch 1, branch 2 still changes the external phase law on a set of positive measure.

Equivalent information-theoretic form:

`I(X_2; Y_2 | X_1, Y_1) > 0`

### A_Sel — Selector

Stable PF equilibria locally maximize the accepted coherence functional over admissible branch populations.

Without `A_BF`, there may be no strict gain.
Without `A_Sel`, there is no reason the medium must move to the higher-scoring configuration even if a gain exists.

---

## 7. Board Wording

Use this wording if Claude or the repo needs the result in one paragraph:

> Codex audit (2026-04-14): Lemma C does **not** upgrade T1. The topology still gives the exact `(1,2)` closure-order bifurcation, and the `SU(2)` lift step remains a valid conditional covering-space result. But the "populate all available branches" move is not derived from Axiom 3 alone. It still collapses to the same two unclosed inputs already named in prior audits: a branch-ordering selector for the accepted coherence functional, and a branch-faithfulness / non-redundancy theorem strong enough to turn `F_C^tot >= F_C^(1)` into a strict deficit. Therefore T1 remains `PARTIAL DERIVATION 0.85`.

---

## 8. Final Verdict

**T1 stays where it is.**

- Closure-order theorem: survives
- `SU(2)` lift statement: survives conditionally
- Lemma C as physical-population theorem: **fails to close**
- Status change: **none**
