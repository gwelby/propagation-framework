# Repo Consistency Audit — 2026-03-27

**Audit ID**: HA-20260327-001
**Audit Class**: Repo Coherence
**Auditor**: Codex
**Purpose**: Verify that the live board, sandbox board, and key orientation files tell the same story before theorem-level hostile audit begins.

---

## Exact Scope

Files inspected:

- [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md)
- [ACTIVE_ISSUES.md](/mnt/d/fundamentals/ACTIVE_ISSUES.md)
- [sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md)
- [AGENTS.md](/mnt/d/fundamentals/AGENTS.md)
- [UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md)
- IBM sandbox scripts touched in the latest cleanup

This is not a proof audit.
It is a board-alignment audit.

---

## What Survives

### 1. The main board is materially aligned

The top-level story is now consistent across the live board:

- Weinberg angle: `DERIVED`
- God Equation: `CONDITIONAL`
- Koide phase: still open / empirical frontier

This is stated consistently in:

- [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md)
- [ACTIVE_ISSUES.md](/mnt/d/fundamentals/ACTIVE_ISSUES.md)
- [AGENTS.md](/mnt/d/fundamentals/AGENTS.md)

This is a real improvement over the earlier split-brain state.

### 2. Axiom 3b is now treated explicitly, not smuggled

[CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) defines `DERIVED` as allowing explicitly adopted corollaries like Axiom 3b.
[UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md) explicitly says Axiom 3b is a genuine added axiom/sub-axiom, not derived from Axiom 3 alone.

That means the repo is now saying one coherent thing:

- Weinberg is derived in the **extended framework**
- not in the strict “Axioms 1–3 only, no adopted corollaries” sense

### 3. The God Equation front is honestly frozen

Both board files correctly keep the God Equation at `CONDITIONAL` and identify the remaining exact gaps:

- locality vs coarse Markovity
- primitive operator identification
- true `H_prod` / joint-law factorization

This is the right freeze state.

---

## What Does Not Fully Survive

### 1. Sandbox language still occasionally outruns theorem language

[sandbox_results.md](/mnt/d/fundamentals/sandbox/sandbox_results.md) says, in the Wave 6 chirality section, that:

> stable particle generations require a chiral (one-way) coupling

That is too strong if read as a theorem.

What the sandbox actually shows is narrower:

- in the scanned `Z3` family, two-way nearest-neighbor mixing destroys long-horizon identity
- pure shift preserves it

This is strong sandbox support for the chirality path.
It is **not** yet a derivation from Axioms 1–3.

The same file does include an honesty paragraph that says this explicitly, so the issue is not fraud.
The issue is headline phrasing outrunning the final qualifier.

### 2. Some older sandbox scripts were carrying pre-audit language

The IBM symmetric-circuit script had language implying it proved `H_prod` and even the God Equation.
That was stale and has now been cleaned up.

This is exactly why a sandbox-classification pass is needed:

- scripts drift faster than claim boards
- once a script has stale theorem language, it can silently re-infect the repo narrative

### 3. The book-facing layer still needs a publication audit

[UNDERSTAND.md](/mnt/d/fundamentals/UNDERSTAND.md) is directionally aligned, but it is a teaching document, not a hostile-audit document.
Before publication, every chapter claim in it still needs to be checked against [CLAIMS.md](/mnt/d/fundamentals/CLAIMS.md) line-by-line.

This is not a contradiction.
It is a pending hygiene task.

---

## Exact Risks Going Forward

### Risk A — Sandbox inflation

A good sandbox result gets narrated as “the universe must…”
before the theorem has earned that sentence.

### Risk B — Extended-framework ambiguity

Readers may hear “derived from the axioms” and assume “Axioms 1–3 only.”
The repo now uses a broader rule: adopted corollaries like 3b can support `DERIVED`.
That is defensible, but it must stay explicit.

### Risk C — Script drift

Older scripts may preserve dead proof paths after the board has frozen them.
The IBM symmetric script was an example.

---

## Verdict

**Repo coherence passes at the board level, with two cautions:**

1. sandbox rhetoric must not outrun theorem status
2. publication-facing files still need a dedicated line-by-line status audit

No board-level confidence change is recommended from this audit.

---

## Board Action

### No status changes

Keep:

- Weinberg angle: `DERIVED`
- God Equation: `CONDITIONAL`
- Koide phase: open / empirical frontier

### Required next action

The next hostile audit should be:

**HA-20260327-002 — Axiom 3 -> Bohr-like Quantization**

Reason:

- it is a new high-visibility `DERIVED` claim
- it sits in the public-facing narrative
- it is exactly the kind of result that can look stronger than it is unless the chain is checked cleanly

---

## One-Line Summary

The repo is coherent enough to begin real hostile audit, but the next danger is no longer split-brain claims. The next danger is letting strong sandbox results and strong teaching language quietly outrun theorem-grade closure.
