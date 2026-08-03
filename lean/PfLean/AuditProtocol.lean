/-
  PfLean.AuditProtocol — Machine-Checked Audit of Claim Ledgers
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-08-01

  This module formalizes the **audit process itself** inside the Lean 4
  kernel.  It defines what it means for a `ClaimLedger` to be *structurally
  honest* — internally consistent, dependencies resolved, tiers respected,
  falsifiers present, no circular dependencies, and status gates enforced.

  The audit formalizes **structural** honesty.  It does NOT formalize
  **semantic** honesty (whether the evidence string actually supports the
  claim, whether the prose overclaims, whether the source says what we
  attribute to it).  Semantic audit requires a human or LLM in the loop
  (Codex hostile review).  Both are needed.

  Checks formalized:
  1. TierConsistency      — confidence in the tier's allowed range
  2. DependenciesResolved — every dependency name exists in the ledger
  3. UniqueEntryNames     — no two positions share a name
  4. FalsifierNonEmpty    — every claim has a stated falsifier
  5. EvidenceNonEmpty     — every claim has an evidence string
  6. StatusGateConsistency — no OK claim depends on a HOLD/NOGO claim
  7. NoSelfDependency     — no claim lists itself as a dependency
  8. NoCyclicDependencies — the dependency graph is acyclic (2-cycle check)

  The result type `AuditResult` is a structured certificate listing which
  checks passed and which failed, with detail strings for failures.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import PfLean.ClaimLedger
import PfLean.MeasurementContract

namespace PfLean

open ClaimLedger ClaimEntry ClaimRecord

-- ---------------------------------------------------------------------------
-- 1. Check identifiers and result types
-- ---------------------------------------------------------------------------

/-- The structural audit checks. -/
inductive AuditCheck
  | tierConsistency
  | dependenciesResolved
  | uniqueEntryNames
  | falsifierNonEmpty
  | evidenceNonEmpty
  | statusGateConsistency
  | noSelfDependency
  | noCyclicDependencies
  | measurementOutcomeConsistent
  | acyclic
  deriving DecidableEq, BEq, Repr

namespace AuditCheck

/-- Human-readable name for each check. -/
def name : AuditCheck → String
  | tierConsistency               => "TierConsistency"
  | dependenciesResolved          => "DependenciesResolved"
  | uniqueEntryNames              => "UniqueEntryNames"
  | falsifierNonEmpty             => "FalsifierNonEmpty"
  | evidenceNonEmpty              => "EvidenceNonEmpty"
  | statusGateConsistency         => "StatusGateConsistency"
  | noSelfDependency              => "NoSelfDependency"
  | noCyclicDependencies          => "NoCyclicDependencies"
  | measurementOutcomeConsistent  => "MeasurementOutcomeConsistent"
  | acyclic                       => "Acyclic"

end AuditCheck

/-- The result of a single audit check. -/
inductive CheckResult
  | pass : AuditCheck → String → CheckResult
  | fail : AuditCheck → String → String → CheckResult
  deriving Repr

namespace CheckResult

/-- The check this result is for. -/
def check : CheckResult → AuditCheck
  | pass c _ => c
  | fail c _ _ => c

/-- Did this check pass? -/
def passed : CheckResult → Bool
  | pass _ _ => true
  | fail _ _ _ => false

/-- Human-readable summary. -/
def summary : CheckResult → String
  | pass c detail => s!"PASS: {c.name} — {detail}"
  | fail c detail reason => s!"FAIL: {c.name} — {detail} — {reason}"

end CheckResult

/-- The full audit result: a list of check results and whether all passed. -/
structure AuditResult where
  results : List CheckResult
  deriving Repr

namespace AuditResult

/-- All checks in the result passed. -/
def allPassed (r : AuditResult) : Bool :=
  r.results.all CheckResult.passed

/-- Number of checks that passed. -/
def passCount (r : AuditResult) : ℕ :=
  r.results.countP CheckResult.passed

/-- Number of checks that failed. -/
def failCount (r : AuditResult) : ℕ :=
  r.results.length - r.passCount

/-- Human-readable summary of the full audit. -/
def summary (r : AuditResult) : String :=
  let header := s!"Audit Result: {r.passCount}/{r.results.length} checks passed"
  let failures := r.results.filter (fun cr => ¬ cr.passed)
  let failLines := failures.map (fun cr => "  " ++ cr.summary)
  if failures.isEmpty then
    header ++ " — ALL PASS"
  else
    String.intercalate "\n" (header :: failLines)

end AuditResult

-- ---------------------------------------------------------------------------
-- 2. Individual audit check predicates
-- ---------------------------------------------------------------------------

namespace Check

/-- **Check 1: TierConsistency** — Every entry's confidence lies in the range
    prescribed by its tier.

    This is structurally enforced by the `tier_bound` field in `ClaimRecord`,
    so it holds for any well-typed ledger.  The audit verifies it explicitly
    to make the check visible and to catch any future code path that might
    bypass the constructor. -/
def tierConsistency (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries,
    EpistemicTier.minConfidence e.record.tier ≤ e.record.confidence.value ∧
    e.record.confidence.value ≤ EpistemicTier.maxConfidence e.record.tier

/-- **Check 2: DependenciesResolved** — Every dependency name of every entry
    names an existing entry in the ledger.

    Reuses `ClaimLedger.dependenciesResolved`. -/
def dependenciesResolved (cl : ClaimLedger) : Prop :=
  cl.dependenciesResolved

/-- **Check 3: UniqueEntryNames** — No two positions in the entry list share
    the same name (occurrence-level uniqueness).

    Reuses `ClaimLedger.uniqueEntryNames`. -/
def uniqueEntryNames (cl : ClaimLedger) : Prop :=
  cl.uniqueEntryNames

/-- **Check 4: FalsifierNonEmpty** — Every entry has a non-empty falsifier
    string.  A claim without a falsifier is not testable and therefore not
    scientific. -/
def falsifierNonEmpty (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries, e.falsifier ≠ ""

/-- **Check 5: EvidenceNonEmpty** — Every entry has a non-empty evidence
    string.  A claim without evidence is an assertion, not a claim. -/
def evidenceNonEmpty (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries, e.evidence ≠ ""

/-- **Check 6: StatusGateConsistency** — No claim with status `OK` depends on
    a claim with status `HOLD` or `NOGO`.  If a dependency is gated, the
    dependent claim must also be gated — you cannot build on a blocked
    foundation. -/
def statusGateConsistency (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries,
    e.status = .OK →
    ∀ d ∈ e.dependencies,
      ∀ e' ∈ cl.entries,
        e'.name = d →
        e'.status = .OK

/-- **Check 7: NoSelfDependency** — No entry lists itself as a dependency.
    A self-dependency is a trivial cycle and indicates a construction error. -/
def noSelfDependency (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries, e.name ∉ e.dependencies

/-- **Check 8: NoCyclicDependencies** — No two entries depend on each other
    (2-cycle check).  A 2-cycle means A depends on B and B depends on A,
    which is a circular foundation.

    This is the simplest non-trivial cycle check.  The stronger
    `acyclic` check (Check 10) catches cycles of any length. -/
def noCyclicDependencies (cl : ClaimLedger) : Prop :=
  ∀ e₁ ∈ cl.entries,
    ∀ e₂ ∈ cl.entries,
      e₁.name ∈ e₂.dependencies →
      e₂.name ∉ e₁.dependencies

/-- **Check 9: MeasurementOutcomeConsistent** — For every measurement contract
    that has a known outcome, the corresponding claim's status matches the
    outcome: `Confirmed → OK`, `Inconclusive → HOLD`, `Falsified → NOGO`.

    This is the genuinely new invariant that connects the measurement layer
    to the claim status layer.  A claim with a falsified measurement must
    not be in status `OK`; a claim with an inconclusive measurement must
    not be in status `OK` either.

    This is the Lean-native formalization of the "evidence_ready vs.
    resolved" distinction: a claim can have a measurement contract (the
    measurement is planned) without the outcome having been applied (the
    measurement hasn't been run).  This check verifies that when the
    outcome IS known, the status reflects it.

    The `outcomes` parameter maps claim names to their known measurement
    outcomes.  A mapping to `none` means the measurement hasn't been run
    yet — the check is vacuously satisfied for that contract. -/
def measurementOutcomeConsistent (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) : Prop :=
  ∀ c ∈ contracts, ∀ e ∈ cl.entries,
    e.name = c.claimName →
    match outcomes c.claimName with
    | some .Confirmed => e.status = .OK
    | some .Inconclusive => e.status = .HOLD
    | some .Falsified => e.status = .NOGO
    | none => True

/-- **Check 10: Acyclic** — The dependency graph has no cycles of any length.

    This is strictly stronger than `noCyclicDependencies` (which only
    catches 2-cycles).  A graph with a 3-cycle (A→B→C→A) passes the
    2-cycle check but fails this one.

    Uses a bounded reachability check: since the graph has `n` nodes,
    any cycle must have length ≤ `n`.  We check that no node reaches
    itself in 1..n steps. -/
def directDeps (cl : ClaimLedger) (name : String) : List String :=
  (cl.entries.filterMap (fun e => if e.name = name then some e.dependencies else none)).flatten

/-- Can `src` reach `target` in exactly `n` steps through the dependency graph? -/
def reachesIn (cl : ClaimLedger) (src target : String) : ℕ → Bool
  | 0 => src = target
  | n+1 => (directDeps cl src).any (fun d => reachesIn cl d target n)

/-- Does `name` participate in a cycle of length 1..n? -/
def hasCycleThrough (cl : ClaimLedger) (name : String) : Bool :=
  let n := cl.entries.length
  (List.range (n + 1)).drop 1 |>.any (fun k => reachesIn cl name name k)

/-- The dependency graph is acyclic: no node participates in any cycle. -/
def acyclic (cl : ClaimLedger) : Prop :=
  ∀ e ∈ cl.entries, hasCycleThrough cl e.name = false

end Check

-- ---------------------------------------------------------------------------
-- 3. The full audit predicate
-- ---------------------------------------------------------------------------

/-- A ledger passes the structural audit when all nine ledger-only checks hold.

    This does NOT include the measurement-outcome check, which requires
    additional parameters (contracts and outcomes).  See
    `auditPassesWithMeasurements` for the full audit including measurements. -/
def auditPasses (cl : ClaimLedger) : Prop :=
  Check.tierConsistency cl ∧
  Check.dependenciesResolved cl ∧
  Check.uniqueEntryNames cl ∧
  Check.falsifierNonEmpty cl ∧
  Check.evidenceNonEmpty cl ∧
  Check.statusGateConsistency cl ∧
  Check.noSelfDependency cl ∧
  Check.noCyclicDependencies cl ∧
  Check.acyclic cl

/-- A ledger passes the full audit (including measurement outcomes) when all
    ten checks hold.  This is the complete audit certificate. -/
def auditPassesWithMeasurements (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) : Prop :=
  auditPasses cl ∧
  Check.measurementOutcomeConsistent cl contracts outcomes

-- ---------------------------------------------------------------------------
-- 4. Theorems about individual checks
-- ---------------------------------------------------------------------------

namespace Check

/-- **TierConsistency holds for any well-typed ClaimLedger.**

    This is the structural guarantee: because `tier_bound` is a proof field
    in `ClaimRecord`, any constructed record already satisfies the tier
    bounds.  The audit check is therefore always satisfied, but we state it
    explicitly to make the invariant visible. -/
theorem tierConsistency_holds (cl : ClaimLedger) :
    tierConsistency cl := by
  intro e he
  exact e.record.tier_bound

/-- **DependenciesResolved and UniqueEntryNames together imply
    StatusGateConsistency is vacuously true when all entries are OK.**

    If every entry has status OK, then the status gate check is trivially
    satisfied (there are no gated dependencies to violate). -/
theorem statusGateConsistency_when_all_OK
    (cl : ClaimLedger) (h_all_OK : ∀ e ∈ cl.entries, e.status = .OK) :
    statusGateConsistency cl := by
  intro e he h_OK d hd e' he' h_name
  exact h_all_OK e' he'

/-- **NoSelfDependency is implied by NoCyclicDependencies** when combined with
    DependenciesResolved.

    If the ledger has no 2-cycles and every dependency resolves, then no
    entry can depend on itself (a self-dependency would be a 1-cycle, which
    is a special case of a 2-cycle where e₁ = e₂).

    This is not strictly true — a self-dependency is e.name ∈ e.dependencies,
    which is a 1-cycle, not a 2-cycle.  The 2-cycle check catches e₁ ≠ e₂
    pairs.  So NoSelfDependency is an independent check.  We keep both. -/
theorem noSelfDependency_independent :
    True := trivial

end Check

-- ---------------------------------------------------------------------------
-- 5. Audit result construction (computable)
-- ---------------------------------------------------------------------------

/-- Run the tier consistency check and produce a `CheckResult`.

    Since `tierConsistency` holds for any well-typed ledger (by
    `tierConsistency_holds`), this always produces a pass result. -/
def runTierConsistency (_cl : ClaimLedger) : CheckResult :=
  CheckResult.pass .tierConsistency
    "tier_bound is structurally enforced in ClaimRecord"

/-- Run the dependencies resolved check. -/
def runDependenciesResolved (cl : ClaimLedger) : CheckResult :=
  if cl.entries.all (fun e =>
    e.dependencies.all (fun d =>
      cl.entries.any (fun e' => e'.name = d)) && true) then
    -- The && true is to force the if-then-else to typecheck as Bool
    CheckResult.pass .dependenciesResolved
      s!"{cl.entries.length} entries, all dependencies resolve"
  else
    CheckResult.fail .dependenciesResolved
      s!"{cl.entries.length} entries"
      "some dependencies do not resolve to entries in the ledger"

/-- Run the unique entry names check. -/
def runUniqueEntryNames (cl : ClaimLedger) : CheckResult :=
  if (cl.entries.map ClaimEntry.name).Nodup then
    CheckResult.pass .uniqueEntryNames
      s!"{cl.entries.length} entries, all names unique"
  else
    CheckResult.fail .uniqueEntryNames
      s!"{cl.entries.length} entries"
      "duplicate entry names found"

/-- Run the falsifier non-empty check. -/
def runFalsifierNonEmpty (cl : ClaimLedger) : CheckResult :=
  if cl.entries.all (fun e => e.falsifier ≠ "") then
    CheckResult.pass .falsifierNonEmpty
      s!"{cl.entries.length} entries, all have falsifiers"
  else
    CheckResult.fail .falsifierNonEmpty
      s!"{cl.entries.length} entries"
      "some entries have empty falsifiers"

/-- Run the evidence non-empty check. -/
def runEvidenceNonEmpty (cl : ClaimLedger) : CheckResult :=
  if cl.entries.all (fun e => e.evidence ≠ "") then
    CheckResult.pass .evidenceNonEmpty
      s!"{cl.entries.length} entries, all have evidence"
  else
    CheckResult.fail .evidenceNonEmpty
      s!"{cl.entries.length} entries"
      "some entries have empty evidence strings"

/-- Run the status gate consistency check. -/
def runStatusGateConsistency (cl : ClaimLedger) : CheckResult :=
  let violations := cl.entries.filter (fun e =>
    e.status = .OK ∧
    e.dependencies.any (fun d =>
      cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK)))
  if violations.isEmpty then
    CheckResult.pass .statusGateConsistency
      s!"{cl.entries.length} entries, no OK claim depends on gated claim"
  else
    CheckResult.fail .statusGateConsistency
      s!"{cl.entries.length} entries, {violations.length} violations"
      "some OK claims depend on HOLD/NOGO claims"

/-- Run the no self dependency check. -/
def runNoSelfDependency (cl : ClaimLedger) : CheckResult :=
  let violations := cl.entries.filter (fun e => e.name ∈ e.dependencies)
  if violations.isEmpty then
    CheckResult.pass .noSelfDependency
      s!"{cl.entries.length} entries, no self-dependencies"
  else
    CheckResult.fail .noSelfDependency
      s!"{cl.entries.length} entries, {violations.length} violations"
      "some entries list themselves as dependencies"

/-- Run the no cyclic dependencies check (2-cycle detection). -/
def runNoCyclicDependencies (cl : ClaimLedger) : CheckResult :=
  let violations := cl.entries.filter (fun e₁ =>
    e₁.dependencies.any (fun d =>
      cl.entries.any (fun e₂ =>
        e₂.name = d ∧ e₁.name ∈ e₂.dependencies)))
  if violations.isEmpty then
    CheckResult.pass .noCyclicDependencies
      s!"{cl.entries.length} entries, no 2-cycles"
  else
    CheckResult.fail .noCyclicDependencies
      s!"{cl.entries.length} entries, {violations.length} violations"
      "2-cycles detected in dependency graph"

/-- Expected claim status for a given measurement outcome. -/
def expectedStatus (o : MeasurementOutcome) : ClaimStatus :=
  match o with
  | .Confirmed => .OK
  | .Inconclusive => .HOLD
  | .Falsified => .NOGO

/-- Run the measurement outcome consistency check.

    This check verifies that for every contract with a known outcome, the
    corresponding claim's status matches the expected status for that
    outcome.  Contracts without a known outcome (`none`) are skipped. -/
def runMeasurementOutcomeConsistent (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) : CheckResult :=
  let violations := contracts.filter (fun c =>
    match outcomes c.claimName with
    | some o => cl.entries.any (fun e =>
      e.name = c.claimName ∧ e.status ≠ expectedStatus o)
    | none => false)
  if violations.isEmpty then
    let known := contracts.filter (fun c => outcomes c.claimName |>.isSome)
    CheckResult.pass .measurementOutcomeConsistent
      s!"{contracts.length} contracts, {known.length} with known outcomes, all consistent"
  else
    CheckResult.fail .measurementOutcomeConsistent
      s!"{contracts.length} contracts, {violations.length} violations"
      "some claims have status inconsistent with their measurement outcome"

/-- Run the acyclicity check (general cycle detection). -/
def runAcyclic (cl : ClaimLedger) : CheckResult :=
  let violations := cl.entries.filter (fun e => Check.hasCycleThrough cl e.name)
  if violations.isEmpty then
    CheckResult.pass .acyclic
      s!"{cl.entries.length} entries, dependency graph is acyclic"
  else
    CheckResult.fail .acyclic
      s!"{cl.entries.length} entries, {violations.length} nodes in cycles"
      "cycles detected in dependency graph"

/-- Run the structural audit on a `ClaimLedger`, producing an `AuditResult`
    with 9 checks (excluding measurement outcome, which requires extra
    parameters). -/
def runAudit (cl : ClaimLedger) : AuditResult :=
  ⟨[ runTierConsistency cl
    , runDependenciesResolved cl
    , runUniqueEntryNames cl
    , runFalsifierNonEmpty cl
    , runEvidenceNonEmpty cl
    , runStatusGateConsistency cl
    , runNoSelfDependency cl
    , runNoCyclicDependencies cl
    , runAcyclic cl ]⟩

/-- Run the full audit including measurement outcomes, producing an
    `AuditResult` with 10 checks. -/
def runAuditWithMeasurements (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) : AuditResult :=
  ⟨(runAudit cl).results ++ [runMeasurementOutcomeConsistent cl contracts outcomes]⟩

-- ---------------------------------------------------------------------------
-- 6. Soundness bridge: computable checks imply propositional predicates
-- ---------------------------------------------------------------------------
--
-- For each computable check `runX`, we prove:
--   If `(runX cl).passed = true`, then `Check.X cl` holds.
--
-- This is the soundness direction: the computable audit function is a
-- faithful reporter of the propositional audit predicate.  If the
-- computable check says PASS, the propositional invariant holds.

/-- Tier consistency is always sound (holds by construction). -/
theorem runTierConsistency_sound (cl : ClaimLedger) :
    (runTierConsistency cl).passed = true → Check.tierConsistency cl := by
  intro _
  exact Check.tierConsistency_holds cl

/-- The tier consistency check in `runAudit` always passes, because
    `tier_bound` is structurally enforced. -/
theorem runTierConsistency_always_passes (cl : ClaimLedger) :
    (runTierConsistency cl).passed = true := by
  simp [runTierConsistency, CheckResult.passed]

/-- **Soundness of runFalsifierNonEmpty**: if the computable check passes,
    then every entry has a non-empty falsifier. -/
theorem runFalsifierNonEmpty_sound (cl : ClaimLedger)
    (h : (runFalsifierNonEmpty cl).passed = true) : Check.falsifierNonEmpty cl := by
  unfold runFalsifierNonEmpty at h
  split at h
  · -- Condition true: all entries have non-empty falsifier
    intro e he
    have h_all := ‹cl.entries.all (fun e => e.falsifier ≠ "") = true›
    rw [List.all_eq_true] at h_all
    have := h_all e he
    -- this : (e.falsifier ≠ "") = true  [Bool form via decide]
    -- Need: e.falsifier ≠ ""  [Prop form]
    exact decide_eq_true_iff.mp this
  · -- Condition false: fail.passed = false, contradiction
    simp [CheckResult.passed] at h

/-- **Soundness of runEvidenceNonEmpty**: if the computable check passes,
    then every entry has a non-empty evidence string. -/
theorem runEvidenceNonEmpty_sound (cl : ClaimLedger)
    (h : (runEvidenceNonEmpty cl).passed = true) : Check.evidenceNonEmpty cl := by
  unfold runEvidenceNonEmpty at h
  split at h
  · intro e he
    have h_all := ‹cl.entries.all (fun e => e.evidence ≠ "") = true›
    rw [List.all_eq_true] at h_all
    have := h_all e he
    exact decide_eq_true_iff.mp this
  · simp [CheckResult.passed] at h

/-- **Soundness of runNoSelfDependency**: if the computable check passes,
    then no entry lists itself as a dependency. -/
theorem runNoSelfDependency_sound (cl : ClaimLedger)
    (h : (runNoSelfDependency cl).passed = true) : Check.noSelfDependency cl := by
  intro e he
  by_contra h_self
  by_cases h_cond : (cl.entries.filter (fun e => e.name ∈ e.dependencies)).isEmpty = true
  · -- Filter is empty, but e is in it → contradiction
    have h_mem : e ∈ cl.entries.filter (fun e => e.name ∈ e.dependencies) := by
      simp [he, h_self]
    have h_not_empty : (cl.entries.filter (fun e => e.name ∈ e.dependencies)).isEmpty = false := by
      rw [List.isEmpty_eq_false_iff]
      intro h_eq
      rw [h_eq] at h_mem
      simp at h_mem
    rw [h_not_empty] at h_cond
    simp at h_cond
  · -- isEmpty ≠ true → fail → passed = false
    simp only [runNoSelfDependency, h_cond, CheckResult.passed] at h
    simp at h

/-- **Soundness of runUniqueEntryNames**: if the computable check passes,
    then all entry names are unique. -/
theorem runUniqueEntryNames_sound (cl : ClaimLedger)
    (h : (runUniqueEntryNames cl).passed = true) : Check.uniqueEntryNames cl := by
  unfold runUniqueEntryNames at h
  split at h
  · -- Nodup is Prop, so split gives us the Prop directly
    exact ‹(cl.entries.map ClaimEntry.name).Nodup›
  · simp [CheckResult.passed] at h

/-- **Soundness of runDependenciesResolved**: if the computable check passes,
    then all dependencies resolve. -/
theorem runDependenciesResolved_sound (cl : ClaimLedger)
    (h : (runDependenciesResolved cl).passed = true) : Check.dependenciesResolved cl := by
  unfold runDependenciesResolved at h
  split at h
  · unfold Check.dependenciesResolved ClaimLedger.dependenciesResolved
    intro e he d hd
    have h_all := ‹cl.entries.all (fun e =>
      e.dependencies.all (fun d => cl.entries.any (fun e' => e'.name = d)) && true) = true›
    rw [List.all_eq_true] at h_all
    have h_e := h_all e he
    simp at h_e
    -- h_e is now ∀ x ∈ e.dependencies, ∃ x_1 ∈ cl.entries, x_1.name = x
    have h_d := h_e d hd
    exact h_d
  · simp [CheckResult.passed] at h

/-- **Soundness of runStatusGateConsistency**: if the computable check passes,
    then no OK claim depends on a gated claim. -/
theorem runStatusGateConsistency_sound (cl : ClaimLedger)
    (h : (runStatusGateConsistency cl).passed = true) : Check.statusGateConsistency cl := by
  intro e he h_OK d hd e' he' h_name
  by_contra h_not_OK
  by_cases h_cond : (cl.entries.filter (fun e =>
    e.status = .OK ∧
    e.dependencies.any (fun d =>
      cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK)))).isEmpty = true
  · have h_mem : e ∈ cl.entries.filter (fun e =>
      e.status = .OK ∧
      e.dependencies.any (fun d =>
        cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK))) := by
      simp only [List.mem_filter, decide_eq_true_iff]
      refine ⟨he, ⟨h_OK, ?_⟩⟩
      rw [List.any_eq_true]
      refine ⟨d, hd, ?_⟩
      rw [List.any_eq_true]
      refine ⟨e', he', ?_⟩
      simp only [decide_eq_true_iff]
      exact ⟨h_name, h_not_OK⟩
    have h_not_empty : (cl.entries.filter (fun e =>
      e.status = .OK ∧
      e.dependencies.any (fun d =>
        cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK)))).isEmpty = false := by
      rw [List.isEmpty_eq_false_iff]
      intro h_eq
      rw [h_eq] at h_mem
      simp at h_mem
    rw [h_not_empty] at h_cond
    simp at h_cond
  · simp only [runStatusGateConsistency, h_cond, CheckResult.passed] at h
    simp at h

/-- **Soundness of runNoCyclicDependencies**: if the computable check passes,
    then no 2-cycles exist. -/
theorem runNoCyclicDependencies_sound (cl : ClaimLedger)
    (h : (runNoCyclicDependencies cl).passed = true) : Check.noCyclicDependencies cl := by
  intro e₁ he₁ e₂ he₂ h_dep
  by_contra h_back
  by_cases h_cond : (cl.entries.filter (fun e₁ =>
    e₁.dependencies.any (fun d =>
      cl.entries.any (fun e₂ =>
        e₂.name = d ∧ e₁.name ∈ e₂.dependencies)))).isEmpty = true
  · have h_mem : e₁ ∈ cl.entries.filter (fun e₁ =>
      e₁.dependencies.any (fun d =>
        cl.entries.any (fun e₂ =>
          e₂.name = d ∧ e₁.name ∈ e₂.dependencies))) := by
      simp only [List.mem_filter]
      refine ⟨he₁, ?_⟩
      rw [List.any_eq_true]
      -- d = e₂.name, which is in e₁.dependencies (h_back)
      refine ⟨e₂.name, h_back, ?_⟩
      rw [List.any_eq_true]
      refine ⟨e₂, he₂, ?_⟩
      simp only [decide_eq_true_iff]
      exact ⟨trivial, h_dep⟩
    have h_not_empty : (cl.entries.filter (fun e₁ =>
      e₁.dependencies.any (fun d =>
        cl.entries.any (fun e₂ =>
          e₂.name = d ∧ e₁.name ∈ e₂.dependencies)))).isEmpty = false := by
      rw [List.isEmpty_eq_false_iff]
      intro h_eq
      rw [h_eq] at h_mem
      simp at h_mem
    rw [h_not_empty] at h_cond
    simp at h_cond
  · simp only [runNoCyclicDependencies, h_cond, CheckResult.passed] at h
    simp at h

/-- **Soundness of runAcyclic**: if the computable check passes,
    then the dependency graph is acyclic. -/
theorem runAcyclic_sound (cl : ClaimLedger)
    (h : (runAcyclic cl).passed = true) : Check.acyclic cl := by
  intro e he
  -- Goal: hasCycleThrough cl e.name = false
  by_contra h_cycle
  -- h_cycle : hasCycleThrough cl e.name ≠ false
  -- Convert to = true
  have h_cycle_true : Check.hasCycleThrough cl e.name = true := by
    by_cases h_eq : Check.hasCycleThrough cl e.name = true
    · exact h_eq
    · -- Not true and not false → contradiction
      have : Check.hasCycleThrough cl e.name = false := by
        cases h : Check.hasCycleThrough cl e.name
        · rfl
        · exact absurd h h_eq
      exact absurd this h_cycle
  by_cases h_cond : (cl.entries.filter (fun e => Check.hasCycleThrough cl e.name)).isEmpty = true
  · have h_mem : e ∈ cl.entries.filter (fun e => Check.hasCycleThrough cl e.name) := by
      rw [List.mem_filter]
      exact ⟨he, h_cycle_true⟩
    have h_not_empty : (cl.entries.filter (fun e => Check.hasCycleThrough cl e.name)).isEmpty = false := by
      rw [List.isEmpty_eq_false_iff]
      intro h_eq
      rw [h_eq] at h_mem
      simp at h_mem
    rw [h_not_empty] at h_cond
    simp at h_cond
  · simp only [runAcyclic, h_cond, CheckResult.passed] at h
    simp at h

/-- The structural audit always runs exactly 9 checks. -/
theorem runAudit_length (cl : ClaimLedger) :
    (runAudit cl).results.length = 9 := by
  simp [runAudit]

/-- The full audit with measurements runs exactly 10 checks. -/
theorem runAuditWithMeasurements_length (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) :
    (runAuditWithMeasurements cl contracts outcomes).results.length = 10 := by
  simp only [runAuditWithMeasurements, List.length_append,
             runAudit_length]
  simp

/-- Helper: extract the i-th check's passed result from allPassed. -/
private theorem allPassed_get (results : List CheckResult) (i : ℕ)
    (hi : i < results.length)
    (h : results.all CheckResult.passed = true) :
    (results.get ⟨i, hi⟩).passed = true := by
  rw [List.all_eq_true] at h
  exact h _ (List.get_mem results ⟨i, hi⟩)

/-- **Full soundness theorem**: if `runAudit` produces a result where all
    checks passed, then the `auditPasses` predicate holds.

    This is the capstone soundness theorem: the computable audit function
    is a faithful reporter of the propositional audit predicate. -/
theorem runAudit_allPassed_implies_auditPasses (cl : ClaimLedger)
    (h : (runAudit cl).allPassed = true) : auditPasses cl := by
  unfold auditPasses
  -- Extract each check's pass result using the helper
  have h0 : (runTierConsistency cl).passed = true := by
    have := allPassed_get _ 0 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h1 : (runDependenciesResolved cl).passed = true := by
    have := allPassed_get _ 1 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h2 : (runUniqueEntryNames cl).passed = true := by
    have := allPassed_get _ 2 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h3 : (runFalsifierNonEmpty cl).passed = true := by
    have := allPassed_get _ 3 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h4 : (runEvidenceNonEmpty cl).passed = true := by
    have := allPassed_get _ 4 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h5 : (runStatusGateConsistency cl).passed = true := by
    have := allPassed_get _ 5 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h6 : (runNoSelfDependency cl).passed = true := by
    have := allPassed_get _ 6 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h7 : (runNoCyclicDependencies cl).passed = true := by
    have := allPassed_get _ 7 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  have h8 : (runAcyclic cl).passed = true := by
    have := allPassed_get _ 8 (by simp [runAudit]) h
    simp [runAudit] at this; exact this
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact runTierConsistency_sound cl h0
  · exact runDependenciesResolved_sound cl h1
  · exact runUniqueEntryNames_sound cl h2
  · exact runFalsifierNonEmpty_sound cl h3
  · exact runEvidenceNonEmpty_sound cl h4
  · exact runStatusGateConsistency_sound cl h5
  · exact runNoSelfDependency_sound cl h6
  · exact runNoCyclicDependencies_sound cl h7
  · exact runAcyclic_sound cl h8

/-- **Full soundness with measurements**: if the 10-check audit passes,
    then `auditPassesWithMeasurements` holds. -/
theorem runAuditWithMeasurements_allPassed_implies_auditPasses
    (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome)
    (h : (runAuditWithMeasurements cl contracts outcomes).allPassed = true) :
    auditPassesWithMeasurements cl contracts outcomes := by
  unfold auditPassesWithMeasurements
  refine ⟨?_, ?_⟩
  · -- The first 9 checks pass (from runAudit)
    have h9 : (runAudit cl).allPassed = true := by
      unfold AuditResult.allPassed at h ⊢
      unfold runAuditWithMeasurements at h
      rw [List.all_append, Bool.and_eq_true] at h
      exact h.1
    exact runAudit_allPassed_implies_auditPasses cl h9
  · -- The measurement check passes
    intro c hc e he h_name
    -- Goal: match outcomes c.claimName with ...
    -- Handle each case of the outcome
    cases h_out : outcomes c.claimName with
    | none => trivial
    | some o =>
      -- Need to case on o to reduce the match
      cases o with
      | Confirmed =>
        -- Goal: e.status = .OK  (expectedStatus .Confirmed = .OK)
        by_contra h_mismatch
        -- Extract the measurement check's pass result
        have h_pass : (runMeasurementOutcomeConsistent cl contracts outcomes).passed = true := by
          unfold AuditResult.allPassed at h
          unfold runAuditWithMeasurements at h
          rw [List.all_append, Bool.and_eq_true] at h
          simp only [List.all_cons, List.all_nil, Bool.and_eq_true] at h
          exact h.2.1
        -- The violation exists
        by_cases h_cond : (contracts.filter (fun c =>
          match outcomes c.claimName with
          | some o => cl.entries.any (fun e =>
            e.name = c.claimName ∧ e.status ≠ expectedStatus o)
          | none => false)).isEmpty = true
        · have h_mem : c ∈ contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false) := by
            simp only [List.mem_filter]
            refine ⟨hc, ?_⟩
            simp only [h_out]
            rw [List.any_eq_true]
            refine ⟨e, he, ?_⟩
            rw [decide_eq_true_iff, expectedStatus]
            exact ⟨h_name, h_mismatch⟩
          have h_not_empty : (contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false)).isEmpty = false := by
            rw [List.isEmpty_eq_false_iff]
            intro h_eq
            rw [h_eq] at h_mem
            simp at h_mem
          rw [h_not_empty] at h_cond
          simp at h_cond
        · simp only [runMeasurementOutcomeConsistent, h_cond
                     , CheckResult.passed] at h_pass
          simp at h_pass
      | Inconclusive =>
        by_contra h_mismatch
        have h_pass : (runMeasurementOutcomeConsistent cl contracts outcomes).passed = true := by
          unfold AuditResult.allPassed at h
          unfold runAuditWithMeasurements at h
          rw [List.all_append, Bool.and_eq_true] at h
          simp only [List.all_cons, List.all_nil, Bool.and_eq_true] at h
          exact h.2.1
        by_cases h_cond : (contracts.filter (fun c =>
          match outcomes c.claimName with
          | some o => cl.entries.any (fun e =>
            e.name = c.claimName ∧ e.status ≠ expectedStatus o)
          | none => false)).isEmpty = true
        · have h_mem : c ∈ contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false) := by
            simp only [List.mem_filter]
            refine ⟨hc, ?_⟩
            simp only [h_out]
            rw [List.any_eq_true]
            refine ⟨e, he, ?_⟩
            rw [decide_eq_true_iff, expectedStatus]
            exact ⟨h_name, h_mismatch⟩
          have h_not_empty : (contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false)).isEmpty = false := by
            rw [List.isEmpty_eq_false_iff]
            intro h_eq
            rw [h_eq] at h_mem
            simp at h_mem
          rw [h_not_empty] at h_cond
          simp at h_cond
        · simp only [runMeasurementOutcomeConsistent, h_cond
                     , CheckResult.passed] at h_pass
          simp at h_pass
      | Falsified =>
        by_contra h_mismatch
        have h_pass : (runMeasurementOutcomeConsistent cl contracts outcomes).passed = true := by
          unfold AuditResult.allPassed at h
          unfold runAuditWithMeasurements at h
          rw [List.all_append, Bool.and_eq_true] at h
          simp only [List.all_cons, List.all_nil, Bool.and_eq_true] at h
          exact h.2.1
        by_cases h_cond : (contracts.filter (fun c =>
          match outcomes c.claimName with
          | some o => cl.entries.any (fun e =>
            e.name = c.claimName ∧ e.status ≠ expectedStatus o)
          | none => false)).isEmpty = true
        · have h_mem : c ∈ contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false) := by
            simp only [List.mem_filter]
            refine ⟨hc, ?_⟩
            simp only [h_out]
            rw [List.any_eq_true]
            refine ⟨e, he, ?_⟩
            rw [decide_eq_true_iff, expectedStatus]
            exact ⟨h_name, h_mismatch⟩
          have h_not_empty : (contracts.filter (fun c =>
            match outcomes c.claimName with
            | some o => cl.entries.any (fun e =>
              e.name = c.claimName ∧ e.status ≠ expectedStatus o)
            | none => false)).isEmpty = false := by
            rw [List.isEmpty_eq_false_iff]
            intro h_eq
            rw [h_eq] at h_mem
            simp at h_mem
          rw [h_not_empty] at h_cond
          simp at h_cond
        · simp only [runMeasurementOutcomeConsistent, h_cond
                     , CheckResult.passed] at h_pass
          simp at h_pass

-- ---------------------------------------------------------------------------
-- 6b. Completeness bridge: propositional predicates imply computable checks pass
-- ---------------------------------------------------------------------------

/-- **Completeness of runFalsifierNonEmpty**: if every entry has a non-empty
    falsifier, then the computable check passes. -/
theorem runFalsifierNonEmpty_complete (cl : ClaimLedger)
    (h : Check.falsifierNonEmpty cl) :
    (runFalsifierNonEmpty cl).passed = true := by
  unfold runFalsifierNonEmpty
  have h_cond : cl.entries.all (fun e => e.falsifier ≠ "") = true := by
    rw [List.all_eq_true]
    intro e he
    exact decide_eq_true_iff.mpr (h e he)
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runEvidenceNonEmpty**: if every entry has non-empty
    evidence, then the computable check passes. -/
theorem runEvidenceNonEmpty_complete (cl : ClaimLedger)
    (h : Check.evidenceNonEmpty cl) :
    (runEvidenceNonEmpty cl).passed = true := by
  unfold runEvidenceNonEmpty
  have h_cond : cl.entries.all (fun e => e.evidence ≠ "") = true := by
    rw [List.all_eq_true]
    intro e he
    exact decide_eq_true_iff.mpr (h e he)
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runNoSelfDependency**: if no entry lists itself as a
    dependency, then the computable check passes. -/
theorem runNoSelfDependency_complete (cl : ClaimLedger)
    (h : Check.noSelfDependency cl) :
    (runNoSelfDependency cl).passed = true := by
  unfold runNoSelfDependency
  have h_filter : (cl.entries.filter (fun e => e.name ∈ e.dependencies)) = [] := by
    rw [List.filter_eq_nil_iff]
    intro e he
    rw [decide_eq_true_iff]
    intro h_self
    exact absurd h_self (h e he)
  have h_cond : (cl.entries.filter (fun e => e.name ∈ e.dependencies)).isEmpty = true := by
    rw [h_filter]
    rfl
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runUniqueEntryNames**: if all entry names are unique,
    then the computable check passes. -/
theorem runUniqueEntryNames_complete (cl : ClaimLedger)
    (h : Check.uniqueEntryNames cl) :
    (runUniqueEntryNames cl).passed = true := by
  unfold runUniqueEntryNames
  split
  · simp [CheckResult.passed]
  · exact absurd h ‹¬(cl.entries.map ClaimEntry.name).Nodup›

/-- **Completeness of runDependenciesResolved**: if all dependencies resolve,
    then the computable check passes. -/
theorem runDependenciesResolved_complete (cl : ClaimLedger)
    (h : Check.dependenciesResolved cl) :
    (runDependenciesResolved cl).passed = true := by
  unfold runDependenciesResolved
  have h_cond : cl.entries.all (fun e =>
    e.dependencies.all (fun d => cl.entries.any (fun e' => e'.name = d)) && true) = true := by
    rw [List.all_eq_true]
    intro e he
    simp only [Bool.and_true]
    rw [List.all_eq_true]
    intro d hd
    rw [List.any_eq_true]
    obtain ⟨e', he'_mem, h_name'⟩ := h e he d hd
    exact ⟨e', he'_mem, decide_eq_true_iff.mpr h_name'⟩
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runStatusGateConsistency**: if no OK claim depends on a
    gated claim, then the computable check passes. -/
theorem runStatusGateConsistency_complete (cl : ClaimLedger)
    (h : Check.statusGateConsistency cl) :
    (runStatusGateConsistency cl).passed = true := by
  unfold runStatusGateConsistency
  have h_filter : (cl.entries.filter (fun e =>
    e.status = .OK ∧
    e.dependencies.any (fun d =>
      cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK)))) = [] := by
    rw [List.filter_eq_nil_iff]
    intro e he
    rw [decide_eq_true_iff]
    intro ⟨h_OK, h_any⟩
    rw [List.any_eq_true] at h_any
    obtain ⟨d, hd, h_inner⟩ := h_any
    rw [List.any_eq_true] at h_inner
    obtain ⟨e', he'_mem, h_pair⟩ := h_inner
    rw [decide_eq_true_iff] at h_pair
    obtain ⟨h_name, h_not_OK⟩ := h_pair
    exact absurd (h e he h_OK d hd e' he'_mem h_name) h_not_OK
  have h_cond : (cl.entries.filter (fun e =>
    e.status = .OK ∧
    e.dependencies.any (fun d =>
      cl.entries.any (fun e' => e'.name = d ∧ e'.status ≠ .OK)))).isEmpty = true := by
    rw [h_filter]
    rfl
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runNoCyclicDependencies**: if no 2-cycles exist, then
    the computable check passes. -/
theorem runNoCyclicDependencies_complete (cl : ClaimLedger)
    (h : Check.noCyclicDependencies cl) :
    (runNoCyclicDependencies cl).passed = true := by
  unfold runNoCyclicDependencies
  have h_filter : (cl.entries.filter (fun e₁ =>
    e₁.dependencies.any (fun d =>
      cl.entries.any (fun e₂ =>
        e₂.name = d ∧ e₁.name ∈ e₂.dependencies)))) = [] := by
    rw [List.filter_eq_nil_iff]
    intro e₁ he₁ h_any
    rw [List.any_eq_true] at h_any
    obtain ⟨d, hd, h_inner⟩ := h_any
    rw [List.any_eq_true] at h_inner
    obtain ⟨e₂, he₂_mem, h_pair⟩ := h_inner
    rw [decide_eq_true_iff] at h_pair
    obtain ⟨h_name, h_back⟩ := h_pair
    have h_in : e₂.name ∈ e₁.dependencies := h_name ▸ hd
    exact absurd h_in (h e₁ he₁ e₂ he₂_mem h_back)
  have h_cond : (cl.entries.filter (fun e₁ =>
    e₁.dependencies.any (fun d =>
      cl.entries.any (fun e₂ =>
        e₂.name = d ∧ e₁.name ∈ e₂.dependencies)))).isEmpty = true := by
    rw [h_filter]
    rfl
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runAcyclic**: if the dependency graph is acyclic, then
    the computable check passes. -/
theorem runAcyclic_complete (cl : ClaimLedger)
    (h : Check.acyclic cl) :
    (runAcyclic cl).passed = true := by
  unfold runAcyclic
  have h_filter : (cl.entries.filter (fun e => Check.hasCycleThrough cl e.name)) = [] := by
    rw [List.filter_eq_nil_iff]
    intro e he h_cycle
    rw [h e he] at h_cycle
    simp at h_cycle
  have h_cond : (cl.entries.filter (fun e => Check.hasCycleThrough cl e.name)).isEmpty = true := by
    rw [h_filter]
    rfl
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Completeness of runTierConsistency**: the check always passes. -/
theorem runTierConsistency_complete (cl : ClaimLedger)
    (_h : Check.tierConsistency cl) :
    (runTierConsistency cl).passed = true := by
  exact runTierConsistency_always_passes cl

/-- **Full completeness theorem**: if `auditPasses` holds, then `runAudit`
    produces a result where all checks passed.

    This is the converse of `runAudit_allPassed_implies_auditPasses`,
    establishing the exact correspondence:
    `runAudit_allPassed ↔ auditPasses`. -/
theorem auditPasses_implies_runAudit_allPassed (cl : ClaimLedger)
    (h : auditPasses cl) :
    (runAudit cl).allPassed = true := by
  unfold auditPasses at h
  obtain ⟨h_tier, h_dep, h_uniq, h_fals, h_evid, h_gate, h_self, h_cyc, h_acyc⟩ := h
  have h0 := runTierConsistency_complete cl h_tier
  have h1 := runDependenciesResolved_complete cl h_dep
  have h2 := runUniqueEntryNames_complete cl h_uniq
  have h3 := runFalsifierNonEmpty_complete cl h_fals
  have h4 := runEvidenceNonEmpty_complete cl h_evid
  have h5 := runStatusGateConsistency_complete cl h_gate
  have h6 := runNoSelfDependency_complete cl h_self
  have h7 := runNoCyclicDependencies_complete cl h_cyc
  have h8 := runAcyclic_complete cl h_acyc
  unfold AuditResult.allPassed runAudit
  simp only [List.all_cons, List.all_nil, Bool.and_true,
             h0, h1, h2, h3, h4, h5, h6, h7, h8]

/-- **Exact correspondence (iff)**: the computable audit passes if and only if
    the propositional audit predicate holds.

    This is the capstone theorem combining soundness (Wave 5) and
    completeness (Wave 6) into a single iff. -/
theorem runAudit_allPassed_iff_auditPasses (cl : ClaimLedger) :
    (runAudit cl).allPassed = true ↔ auditPasses cl := by
  refine ⟨runAudit_allPassed_implies_auditPasses cl, auditPasses_implies_runAudit_allPassed cl⟩

-- ---------------------------------------------------------------------------
-- 6c. Completeness bridge with measurements
-- ---------------------------------------------------------------------------

/-- **Completeness of runMeasurementOutcomeConsistent**: if the propositional
    measurement-outcome consistency check holds, then the computable check
    passes.

    Strategy: prove the filter of violations is empty (no contract has a
    mismatched status), then `isEmpty = true` and the `if` takes the pass
    branch. -/
theorem runMeasurementOutcomeConsistent_complete (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome)
    (h : Check.measurementOutcomeConsistent cl contracts outcomes) :
    (runMeasurementOutcomeConsistent cl contracts outcomes).passed = true := by
  unfold runMeasurementOutcomeConsistent
  -- Prove the filter of violations is empty
  have h_filter : (contracts.filter (fun c =>
    match outcomes c.claimName with
    | some o => cl.entries.any (fun e =>
      e.name = c.claimName ∧ e.status ≠ expectedStatus o)
    | none => false)) = [] := by
    rw [List.filter_eq_nil_iff]
    intro c hc
    -- Need: ¬ (match outcomes c.claimName with ...)
    -- Case on the outcome
    cases h_out : outcomes c.claimName with
    | none => simp
    | some o =>
      -- Reduce the match first
      simp only
      -- Goal: (cl.entries.any ...) = false
      -- Prove by contradiction: if any = true, some entry has mismatched status
      by_contra h_any
      rw [List.any_eq_true] at h_any
      obtain ⟨e, he_mem, h_pair⟩ := h_any
      rw [decide_eq_true_iff] at h_pair
      obtain ⟨h_name, h_mismatch⟩ := h_pair
      have h_expected := h c hc e he_mem h_name
      rw [h_out] at h_expected
      cases o with
      | Confirmed =>
        simp [expectedStatus] at h_expected h_mismatch
        exact h_mismatch h_expected
      | Inconclusive =>
        simp [expectedStatus] at h_expected h_mismatch
        exact h_mismatch h_expected
      | Falsified =>
        simp [expectedStatus] at h_expected h_mismatch
        exact h_mismatch h_expected
  have h_cond : (contracts.filter (fun c =>
    match outcomes c.claimName with
    | some o => cl.entries.any (fun e =>
      e.name = c.claimName ∧ e.status ≠ expectedStatus o)
    | none => false)).isEmpty = true := by
    rw [h_filter]
    rfl
  simp only [h_cond, if_true, CheckResult.passed]

/-- **Full completeness with measurements**: if `auditPassesWithMeasurements`
    holds, then `runAuditWithMeasurements` produces a result where all checks
    passed.

    This is the converse of `runAuditWithMeasurements_allPassed_implies_auditPasses`,
    establishing the exact correspondence for the 10-check audit. -/
theorem auditPassesWithMeasurements_implies_runAuditWithMeasurements_allPassed
    (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome)
    (h : auditPassesWithMeasurements cl contracts outcomes) :
    (runAuditWithMeasurements cl contracts outcomes).allPassed = true := by
  unfold auditPassesWithMeasurements at h
  obtain ⟨h_audit, h_meas⟩ := h
  -- First 9 checks pass (from auditPasses)
  have h9 : (runAudit cl).allPassed = true :=
    auditPasses_implies_runAudit_allPassed cl h_audit
  -- 10th check passes (from measurement consistency)
  have h10 : (runMeasurementOutcomeConsistent cl contracts outcomes).passed = true :=
    runMeasurementOutcomeConsistent_complete cl contracts outcomes h_meas
  -- Combine: allPassed = (runAudit.results ++ [meas]).all = true
  unfold AuditResult.allPassed runAuditWithMeasurements
  rw [List.all_append, Bool.and_eq_true]
  refine ⟨?_, ?_⟩
  · -- (runAudit cl).results.all CheckResult.passed = true
    -- This is h9 after unfolding allPassed
    exact h9
  · -- [meas].all CheckResult.passed = true
    simp only [List.all_cons, List.all_nil, h10, Bool.and_true]

/-- **Exact correspondence with measurements (iff)**: the computable 10-check
    audit passes if and only if the propositional audit predicate (including
    measurements) holds.

    This is the full capstone theorem combining soundness (Wave 5) and
    completeness (Wave 8) for the complete 10-check audit. -/
theorem runAuditWithMeasurements_allPassed_iff_auditPassesWithMeasurements
    (cl : ClaimLedger)
    (contracts : List MeasurementContract)
    (outcomes : String → Option MeasurementOutcome) :
    (runAuditWithMeasurements cl contracts outcomes).allPassed = true ↔
    auditPassesWithMeasurements cl contracts outcomes := by
  refine ⟨runAuditWithMeasurements_allPassed_implies_auditPasses cl contracts outcomes,
          auditPassesWithMeasurements_implies_runAuditWithMeasurements_allPassed cl contracts outcomes⟩

-- ---------------------------------------------------------------------------
-- 7. Negative fixtures: the audit catches violations
-- ---------------------------------------------------------------------------

/-- **Negative fixture 1**: A ledger with an empty falsifier fails the
    falsifier check.

    We construct a minimal ledger with one entry whose falsifier is empty
    and show the audit catches it. -/
def emptyFalsifierEntry : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "empty_falsifier_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence"
      falsifier := ""
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def emptyFalsifierLedger : ClaimLedger :=
  ⟨[emptyFalsifierEntry]⟩

/-- The empty-falsifier ledger fails the falsifier check. -/
theorem emptyFalsifierLedger_fails_falsifierCheck :
    ¬ Check.falsifierNonEmpty emptyFalsifierLedger := by
  intro h
  have : emptyFalsifierEntry ∈ emptyFalsifierLedger.entries := by simp [emptyFalsifierLedger]
  have := h emptyFalsifierEntry this
  simp [emptyFalsifierEntry, ClaimEntry.falsifier] at this

/-- **Negative fixture 2**: A ledger with a self-dependency fails the
    self-dependency check. -/
def selfDepEntry : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "self_dep_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence"
      falsifier := "test falsifier"
      dependencies := ["self_dep_test"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def selfDepLedger : ClaimLedger :=
  ⟨[selfDepEntry]⟩

/-- The self-dependency ledger fails the self-dependency check. -/
theorem selfDepLedger_fails_selfDepCheck :
    ¬ Check.noSelfDependency selfDepLedger := by
  intro h
  have he : selfDepEntry ∈ selfDepLedger.entries := by simp [selfDepLedger]
  have := h selfDepEntry he
  -- selfDepEntry.name = "self_dep_test", selfDepEntry.dependencies = ["self_dep_test"]
  -- this : "self_dep_test" ∉ ["self_dep_test"] → contradiction
  simp [selfDepEntry, ClaimEntry.dependencies] at this

/-- **Negative fixture 3**: A ledger with a 2-cycle fails the cycle check.

    Two entries that depend on each other form a 2-cycle. -/
def cycleEntryA : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "cycle_a" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence A"
      falsifier := "test falsifier A"
      dependencies := ["cycle_b"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def cycleEntryB : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "cycle_b" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence B"
      falsifier := "test falsifier B"
      dependencies := ["cycle_a"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def cyclicLedger : ClaimLedger :=
  ⟨[cycleEntryA, cycleEntryB]⟩

/-- The cyclic ledger fails the 2-cycle check. -/
theorem cyclicLedger_fails_cycleCheck :
    ¬ Check.noCyclicDependencies cyclicLedger := by
  intro h
  have hA : cycleEntryA ∈ cyclicLedger.entries := by simp [cyclicLedger]
  have hB : cycleEntryB ∈ cyclicLedger.entries := by simp [cyclicLedger]
  -- noCyclicDependencies: ∀ e₁ e₂, e₁.name ∈ e₂.dependencies → e₂.name ∉ e₁.dependencies
  -- e₁ = cycleEntryA (name="cycle_a"), e₂ = cycleEntryB (name="cycle_b")
  -- e₁.name ∈ e₂.dependencies → "cycle_a" ∈ cycleEntryB.dependencies → TRUE
  have hA_name_in_B : "cycle_a" ∈ cycleEntryB.dependencies := by
    simp [cycleEntryB, ClaimEntry.dependencies]
  -- h gives: e₂.name ∉ e₁.dependencies → "cycle_b" ∉ cycleEntryA.dependencies
  have h_contra := h cycleEntryA hA cycleEntryB hB hA_name_in_B
  -- But "cycle_b" IS in cycleEntryA.dependencies
  have hB_name_in_A : "cycle_b" ∈ cycleEntryA.dependencies := by
    simp [cycleEntryA, ClaimEntry.dependencies]
  exact h_contra hB_name_in_A

/-- **Negative fixture 4**: A claim with a falsified measurement but status OK
    fails the measurement-outcome consistency check.

    This is the genuinely new invariant: a falsified measurement must set
    the claim to NOGO, not leave it as OK. -/
noncomputable def falsifiedContract : MeasurementContract :=
  { claimName := "falsified_outcome_test"
    predictedValue := (1 : ℝ)
    tolerance := (0.01 : ℝ)
    tolerance_nonneg := by norm_num
    falsificationThreshold := (0.05 : ℝ)
    falsification_nonneg := by norm_num
    tolerance_le_falsification := by norm_num }

def falsifiedOutcomeEntry : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "falsified_outcome_test" P
    { proof := h
      tier := .DERIVED
      status := .OK  -- WRONG: should be NOGO after falsification
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence"
      falsifier := "test falsifier"
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def falsifiedOutcomeLedger : ClaimLedger :=
  ⟨[falsifiedOutcomeEntry]⟩

/-- The outcome map says the measurement was Falsified. -/
def falsifiedOutcomes : String → Option MeasurementOutcome :=
  fun name => if name = "falsified_outcome_test" then some .Falsified else none

/-- The ledger with a falsified measurement but OK status fails the
    measurement-outcome consistency check. -/
theorem falsifiedOutcomeLedger_fails_measurementCheck :
    ¬ Check.measurementOutcomeConsistent falsifiedOutcomeLedger
        [falsifiedContract] falsifiedOutcomes := by
  intro h
  have h_contract : falsifiedContract ∈ [falsifiedContract] := by simp
  have h_entry : falsifiedOutcomeEntry ∈ falsifiedOutcomeLedger.entries := by
    simp [falsifiedOutcomeLedger]
  have h_name : falsifiedOutcomeEntry.name = falsifiedContract.claimName := by
    simp [falsifiedOutcomeEntry, falsifiedContract]
  have := h falsifiedContract h_contract falsifiedOutcomeEntry h_entry h_name
  -- Evaluate the outcome function and reduce the match
  -- The if-then-else evaluates to some .Falsified, match gives .OK = .NOGO
  -- which is false, closing the goal
  simp [falsifiedOutcomes, falsifiedContract, falsifiedOutcomeEntry,
        ClaimEntry.status] at this

/-- **Negative fixture 5**: A 3-cycle passes the 2-cycle check but fails the
    general acyclicity check.

    A → B → C → A is a 3-cycle.  No two entries form a 2-cycle, so
    `noCyclicDependencies` passes.  But `acyclic` catches it. -/
def cycle3EntryA : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "c3_a" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence A"
      falsifier := "test falsifier A"
      dependencies := ["c3_b"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def cycle3EntryB : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "c3_b" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence B"
      falsifier := "test falsifier B"
      dependencies := ["c3_c"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def cycle3EntryC : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "c3_c" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence C"
      falsifier := "test falsifier C"
      dependencies := ["c3_a"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def cycle3Ledger : ClaimLedger :=
  ⟨[cycle3EntryA, cycle3EntryB, cycle3EntryC]⟩

/-- The 3-cycle ledger passes the 2-cycle check (no 2-cycles exist). -/
theorem cycle3Ledger_passes_2cycleCheck :
    Check.noCyclicDependencies cycle3Ledger := by
  intro e₁ he₁ e₂ he₂ h_dep
  simp [cycle3Ledger, ClaimEntry.dependencies] at he₁ he₂ h_dep ⊢
  rcases he₁ with rfl | rfl | rfl
  all_goals
    rcases he₂ with rfl | rfl | rfl
    all_goals
      simp [cycle3EntryA, cycle3EntryB, cycle3EntryC] at h_dep ⊢

/-- The 3-cycle ledger fails the general acyclicity check.

    `hasCycleThrough` detects the 3-cycle because c3_a reaches c3_a in 3
    steps: c3_a → c3_b → c3_c → c3_a. -/
theorem cycle3Ledger_fails_acyclicCheck :
    ¬ Check.acyclic cycle3Ledger := by
  intro h
  have hA : cycle3EntryA ∈ cycle3Ledger.entries := by simp [cycle3Ledger]
  have hA_no_cycle : Check.hasCycleThrough cycle3Ledger "c3_a" = false :=
    h cycle3EntryA hA
  -- Direct computation: hasCycleThrough evaluates to true
  -- because c3_a → c3_b → c3_c → c3_a is a 3-step cycle
  have h_has_cycle : Check.hasCycleThrough cycle3Ledger "c3_a" = true := by
    native_decide
  -- hA_no_cycle : true = false after rewrite
  rw [h_has_cycle] at hA_no_cycle
  simp at hA_no_cycle

/-- **Negative fixture 6**: A ledger with an unresolved dependency fails the
    dependencies-resolved check.

    Entry A depends on "nonexistent", but no entry has that name. -/
def unresolvedDepEntry : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "unresolved_dep_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence"
      falsifier := "test falsifier"
      dependencies := ["nonexistent_entry"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def unresolvedDepLedger : ClaimLedger :=
  ⟨[unresolvedDepEntry]⟩

/-- The unresolved-dependency ledger fails the dependencies-resolved check. -/
theorem unresolvedDepLedger_fails_depResolvedCheck :
    ¬ Check.dependenciesResolved unresolvedDepLedger := by
  intro h
  have he : unresolvedDepEntry ∈ unresolvedDepLedger.entries := by
    simp [unresolvedDepLedger]
  have hd : "nonexistent_entry" ∈ unresolvedDepEntry.dependencies := by
    simp [unresolvedDepEntry, ClaimEntry.dependencies]
  have := h unresolvedDepEntry he "nonexistent_entry" hd
  -- this : ∃ e' ∈ entries, e'.name = "nonexistent_entry"
  -- But the only entry has name "unresolved_dep_test"
  simp [unresolvedDepLedger, unresolvedDepEntry] at this

/-- **Negative fixture 7**: A ledger with duplicate entry names fails the
    unique-entry-names check.

    Two entries with the same name "dup_test". -/
def dupNameEntryA : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "dup_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence A"
      falsifier := "test falsifier A"
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def dupNameEntryB : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "dup_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence B"
      falsifier := "test falsifier B"
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def dupNamesLedger : ClaimLedger :=
  ⟨[dupNameEntryA, dupNameEntryB]⟩

/-- The duplicate-names ledger fails the unique-entry-names check. -/
theorem dupNamesLedger_fails_uniqueNamesCheck :
    ¬ Check.uniqueEntryNames dupNamesLedger := by
  -- Check.uniqueEntryNames = (entries.map name).Nodup
  -- entries = [dupNameEntryA, dupNameEntryB], both have name "dup_test"
  -- map = ["dup_test", "dup_test"], not Nodup
  intro h
  -- h : Check.uniqueEntryNames dupNamesLedger
  -- definionally equal to (dupNamesLedger.entries.map ClaimEntry.name).Nodup
  have h_nodup : (dupNamesLedger.entries.map ClaimEntry.name).Nodup := h
  have h_map : dupNamesLedger.entries.map ClaimEntry.name = ["dup_test", "dup_test"] := by
    simp [dupNamesLedger, dupNameEntryA, dupNameEntryB]
  rw [h_map] at h_nodup
  -- h_nodup : List.Nodup ["dup_test", "dup_test"]
  exact absurd h_nodup (by native_decide)

/-- **Negative fixture 8**: A ledger with empty evidence fails the
    evidence-non-empty check. -/
def emptyEvidenceEntry : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "empty_evidence_test" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := ""
      falsifier := "test falsifier"
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def emptyEvidenceLedger : ClaimLedger :=
  ⟨[emptyEvidenceEntry]⟩

/-- The empty-evidence ledger fails the evidence-non-empty check. -/
theorem emptyEvidenceLedger_fails_evidenceCheck :
    ¬ Check.evidenceNonEmpty emptyEvidenceLedger := by
  intro h
  have he : emptyEvidenceEntry ∈ emptyEvidenceLedger.entries := by
    simp [emptyEvidenceLedger]
  have := h emptyEvidenceEntry he
  simp [emptyEvidenceEntry, ClaimEntry.evidence] at this

/-- **Negative fixture 9**: An OK claim depending on a HOLD claim fails the
    status-gate-consistency check.

    Entry A (OK) depends on entry B (HOLD).  An OK claim should not depend
    on a gated (non-OK) claim. -/
def gatedDepEntryA : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "gate_a" P
    { proof := h
      tier := .DERIVED
      status := .OK
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence A"
      falsifier := "test falsifier A"
      dependencies := ["gate_b"]
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def gatedDepEntryB : ClaimEntry :=
  let P : Prop := True
  let h : P := trivial
  ClaimEntry.mk "gate_b" P
    { proof := h
      tier := .DERIVED
      status := .HOLD  -- gated!
      confidence := ⟨0.95, by constructor <;> norm_num⟩
      evidence := "test evidence B"
      falsifier := "test falsifier B"
      dependencies := []
      tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

def gatedDepLedger : ClaimLedger :=
  ⟨[gatedDepEntryA, gatedDepEntryB]⟩

/-- The gated-dependency ledger fails the status-gate-consistency check. -/
theorem gatedDepLedger_fails_statusGateCheck :
    ¬ Check.statusGateConsistency gatedDepLedger := by
  intro h
  have hA : gatedDepEntryA ∈ gatedDepLedger.entries := by
    simp [gatedDepLedger]
  have hA_OK : gatedDepEntryA.status = .OK := by
    simp [gatedDepEntryA, ClaimEntry.status]
  have hB : gatedDepEntryB ∈ gatedDepLedger.entries := by
    simp [gatedDepLedger]
  have hB_name : gatedDepEntryB.name = "gate_b" := by
    simp [gatedDepEntryB]
  have hB_not_OK : gatedDepEntryB.status ≠ .OK := by
    simp [gatedDepEntryB, ClaimEntry.status]
  -- h : ∀ e ∈ entries, e.status = .OK → ∀ d ∈ e.dependencies,
  --       ∀ e' ∈ entries, e'.name = d → e'.status = .OK
  -- Apply to e = A, d = "gate_b", e' = B
  have hd : "gate_b" ∈ gatedDepEntryA.dependencies := by
    simp [gatedDepEntryA, ClaimEntry.dependencies]
  have := h gatedDepEntryA hA hA_OK "gate_b" hd gatedDepEntryB hB hB_name
  exact absurd this hB_not_OK

end PfLean
