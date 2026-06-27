# PREDICTIONS/ — The Forward-Prediction Ledger
*Created 2026-06-18. This is the structure that guides the family from postdiction to truth. Born from the demotion audit + the `framework-toward-true` sweep (5 maps → synthesis → 3 adversarial cooling lenses). Read `../UNDENIABLE_ROADMAP.md` first.*

## Why this exists (the diagnosis)
The family kept drifting back to overclaiming **not from dishonesty but from structure.** The scoreboard was `CLAIMS.md` — a count of "how many known constants did we derive." That metric **has no wrong answer**: you can always find another combination, and every promotion looks like progress. Postdiction of things we already know cannot falsify you, so it drifts toward overclaim forever. Exhortation ("be honest") failed because it never changed the scoreboard.

**This ledger changes the scoreboard.** From *"how many constants did we match?"* (unfalsifiable) to *"what did we commit to BEFORE the experiment, and did it land?"* (failure is possible → success means something). A framework that can be wrong and isn't is undeniable. A framework that can't be wrong is just elegant.

`CLAIMS.md` is hereby **supporting evidence**, not the claim. The claim is what's in this ledger.

## The hard truth this ledger must hold (2026-06-18)
**PF cannot make a discriminating forward prediction today.** Verified by the sweep:
- δ = 2/9 (the Koide phase) is a **postdiction** (read off data; every PF-native selector route — T-021, T-022, 4 audit lanes — FAILED) **and DEGENERATE** (rivals ZiP/Brannen/Rivero also land on ~2/9). Committing it would not count and would not distinguish PF.
- Every other candidate (neutrino ordering, Σmν, δ_CP, 3-generations, dark matter) fails the test **"can PF compute a number today?"** — No.
- So the first ledger entry is not a prediction. It is the **one machine to build** (a PF-native phase selector), logged honestly as **BLOCKED**, so the family cannot mistake an aspiration for a commitment.

That negative result IS the deliverable. The honest map of where the framework actually stands is worth more than a fake number.

## Entry schema (commitment block = git-timestamp-LOCKED, never edited)
```
id:             PRED-NNN
status:         OPEN | BLOCKED | RESOLVED-HIT | RESOLVED-MISS | DEGENERATE | WITHDRAWN
committed:      <git commit timestamp — the lock; you cannot pre-date>
committed_by:   <agent> @ <commit SHA>
claim:          a NUMBER or functional-form + the parameter to be fixed (vague claims REJECTED)
error_bar:      explicit (e.g. "<3σ vs PDG best-fit")
conditional_on: EVERY unresolved premise named (Postulate D; EM-sector-specificity; …)
resolution:     a REAL planned measurement + date window (must be able to resolve)
sm_says:        "silent" | a specific SM value
rivals_say:     each named rival's number — OR a time-boxed task to find them (NOT "assumed different")
falsifier:      the exact observation that kills it
--- (everything below this line is append-only resolution log) ---
```

## Anti-gaming rules (from the cooling pass — these are what make it stick)
1. **Number-or-form, never prose.** "PF predicts normal ordering" with no error bar is REJECTED. A claim must be falsifiable by a measurement.
2. **The git timestamp is the lock.** Like clinical-trial pre-registration — you cannot back-date a commitment. The commitment block is never edited; resolution only appends.
3. **`conditional_on` is mandatory at the point of maximum temptation.** Every inherited premise (Postulate D especially) must be named at the prediction site, or it doesn't land.
4. **`rivals_say` empty → DEGENERATE-risk flag.** If you haven't found what rivals predict, it's a time-boxed task, not an assumption. If all rivals give the same number → **DEGENERATE** (lands but doesn't distinguish PF → does not count toward undeniability).
5. **BLOCKED ≠ OPEN.** A prediction contingent on machinery that doesn't exist is BLOCKED, never OPEN. The family must not mistake "we could predict this IF we build X" for "we predict this."
6. **Clock-enforced, or it dies like the claim-guard.** A periodic check (Pi/cron) surfaces OPEN entries nearing their resolution window and BLOCKED entries with their blocker — so the ledger cannot be quietly forgotten. *Resolution is enforced by a clock the family does not control.* This is the single property that keeps it from becoming another orphaned file.

## Status today
- `PRED-001` — δ_CP via a PF-native phase selector — **BLOCKED** (the machine doesn't exist; 4 derivation routes failed). Status report: `/mnt/d/Fundamentals/predictions/PRED-001-H8-Z3-STATUS-20260626.md`.
- `PRED-002` — Neutrino Koide non-universality — **OPEN candidate** (PF predicts neutrino masses do NOT satisfy Q=2/3; DUNE/Hyper-K can resolve ~2029–2033). Awaiting Codex audit and Greg lock. Gate packet: `/mnt/d/Fundamentals/outbox/CLAIM_PACKET_PRED-002_20260626.md`.
- The day a PRED entry goes OPEN with a real number, a named experiment, and rivals_say filled in differing — that is the day PF stops being numerology and becomes physics.
