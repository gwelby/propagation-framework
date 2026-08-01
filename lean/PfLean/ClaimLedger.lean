/-
  PfLean.ClaimLedger — Epistemic Claim Ledger
  Authors: Devin (Cognition AI), Greg Welby, PF Research Team
  Date: 2026-07-23

  This module formalizes the CLAIMS.md epistemic architecture inside the
  Lean 4 kernel.  A `ClaimRecord` bundles a theorem proof with its
  epistemic tier, confidence interval, evidence statement, falsifier, and
  dependency names.  A `ClaimLedger` is a registry of named claims.

  Design choices:
  - `EpistemicTier` encodes the six proof-strength grades from CLAIMS.md.
  - `ClaimStatus` encodes the gating overlays `HOLD` / `NOGO`
    (these are not proof-strength tiers; they block publication).
  - `Confidence` is a real number in the closed unit interval [0,1].
  - `ClaimRecord P` carries a proof of `P` plus the metadata above.
  - `ClaimLedger` stores a list of named `ClaimRecord`s and can check
    whether every dependency name resolves to an entry in the ledger.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace PfLean

open Real

-- ---------------------------------------------------------------------------
-- 1. Epistemic tiers and confidence
-- ---------------------------------------------------------------------------

/-- The six epistemic proof-strength tiers from `CLAIMS.md`. -/
inductive EpistemicTier
  | DERIVED      -- follows from Axioms 1-3 by logic/math alone
  | CONDITIONAL  -- formally proved, but rests on a named extra premise
  | ARGUED       -- plausible reasoning, mechanism identified, proof pending
  | EMPIRICAL    -- matches experimental data, first-principles proof pending
  | INTUITION    -- insight-driven pattern, currently being tested
  | OPEN         -- unresolved gap
  deriving DecidableEq, BEq, Repr

namespace EpistemicTier

/-- Lower bound of the confidence range for each tier. -/
def minConfidence : EpistemicTier → ℝ
  | DERIVED     => 0.90
  | CONDITIONAL => 0.75
  | ARGUED      => 0.70
  | EMPIRICAL   => 0.60
  | INTUITION   => 0.30
  | OPEN        => 0.00

/-- Upper bound of the confidence range for each tier. -/
def maxConfidence : EpistemicTier → ℝ
  | DERIVED     => 1.00
  | CONDITIONAL => 0.89
  | ARGUED      => 0.89
  | EMPIRICAL   => 0.95
  | INTUITION   => 0.59
  | OPEN        => 0.29

end EpistemicTier

/-- Gating overlays. These are not proof-strength tiers; they block or
    mark a claim as a closed negative result. -/
inductive ClaimStatus
  | OK    -- no gate; the tier/confidence speak
  | HOLD  -- publication blocked, usually pending audit or dependency
  | NOGO  -- closed negative: the route/claim was shown not to hold
  deriving DecidableEq, BEq, Repr

/-- A confidence value in the closed unit interval [0,1]. -/
structure Confidence where
  value : ℝ
  valid : 0 ≤ value ∧ value ≤ 1

namespace Confidence

/-- Build a `Confidence` from a real and a proof it lies in [0,1]. -/
def mk' (c : ℝ) (h0 : 0 ≤ c) (h1 : c ≤ 1) : Confidence :=
  ⟨c, ⟨h0, h1⟩⟩

/-- A confidence of 1.0, the natural choice for `DERIVED` claims. -/
def one : Confidence :=
  ⟨1, by constructor <;> norm_num⟩

/-- A confidence of 0.0, the natural choice for `OPEN` claims. -/
def zero : Confidence :=
  ⟨0, by constructor <;> norm_num⟩

instance : Coe Confidence ℝ := ⟨fun c => c.value⟩

end Confidence

-- ---------------------------------------------------------------------------
-- 2. Claim records and ledgers
-- ---------------------------------------------------------------------------

/-- A claim record bundles a proof with epistemic metadata.

    The `tier_bound` field is a kernel-enforced guard: it is impossible to
    construct a `ClaimRecord` whose confidence falls outside the range
    prescribed by its tier. -/
structure ClaimRecord (P : Prop) where
  proof : P
  tier : EpistemicTier
  status : ClaimStatus := .OK
  confidence : Confidence
  evidence : String
  falsifier : String
  dependencies : List String
  tier_bound : EpistemicTier.minConfidence tier ≤ confidence.value ∧
               confidence.value ≤ EpistemicTier.maxConfidence tier

namespace ClaimRecord

/-- The claim meets the publication tier gate when it is not gated and its
    tier is `DERIVED` or `EMPIRICAL` with confidence at least 0.90.

    This is a **local metadata predicate**, not a release authorization.
    It checks only the tier and status fields stored in the record.  It does
    NOT verify data provenance, scientific validation, claim-scope review,
    independent replication, Legal review, or Greg approval.  Meeting this
    gate is necessary but not sufficient for any external release. -/
def meetsPublicationTierGate (c : ClaimRecord P) : Prop :=
  c.status = .OK ∧
  (c.tier = .DERIVED ∨
   c.tier = .EMPIRICAL ∧ c.confidence.value ≥ 0.90)

/-- The proof-grade minimum confidence is satisfied. -/
theorem minConfidence_le (c : ClaimRecord P) :
    EpistemicTier.minConfidence c.tier ≤ c.confidence.value :=
  c.tier_bound.1

/-- The proof-grade maximum confidence is satisfied. -/
theorem maxConfidence_le (c : ClaimRecord P) :
    c.confidence.value ≤ EpistemicTier.maxConfidence c.tier :=
  c.tier_bound.2

/-- Mark an existing claim as `HOLD` without discarding its proof. -/
def hold (c : ClaimRecord P) : ClaimRecord P :=
  { c with status := .HOLD }

/-- Mark an existing claim as `NOGO` without discarding its proof.
    (Useful when `P` itself is a negative statement, e.g. `¬Q`.) -/
def noGo (c : ClaimRecord P) : ClaimRecord P :=
  { c with status := .NOGO }

-- ---------------------------------------------------------------------------
-- 3. Convenience constructors for each tier
-- ---------------------------------------------------------------------------

/-- Construct a `DERIVED` claim with default confidence 0.95. -/
def derived (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .DERIVED
    status := .OK
    confidence := ⟨0.95, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

/-- Construct a `CONDITIONAL` claim with default confidence 0.85. -/
def conditional (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .CONDITIONAL
    status := .OK
    confidence := ⟨0.85, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

/-- Construct an `ARGUED` claim with default confidence 0.80. -/
def argued (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .ARGUED
    status := .OK
    confidence := ⟨0.80, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

/-- Construct an `EMPIRICAL` claim with default confidence 0.90. -/
def empirical (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .EMPIRICAL
    status := .OK
    confidence := ⟨0.90, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

/-- Construct an `INTUITION` claim with default confidence 0.50. -/
def intuition (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .INTUITION
    status := .OK
    confidence := ⟨0.50, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

/-- Construct an `OPEN` claim with default confidence 0.15. -/
def openClaim (proof : P) (evidence falsifier : String)
    (dependencies : List String := []) : ClaimRecord P :=
  { proof := proof
    tier := .OPEN
    status := .OK
    confidence := ⟨0.15, by constructor <;> norm_num⟩
    evidence := evidence
    falsifier := falsifier
    dependencies := dependencies
    tier_bound := by simp [EpistemicTier.minConfidence, EpistemicTier.maxConfidence]; norm_num }

end ClaimRecord

-- ---------------------------------------------------------------------------
-- 4. Named claim entries and ledgers
-- ---------------------------------------------------------------------------

/-- A named claim entry.  The `Prop` is exposed so the ledger can recover
    the theorem and its `ClaimRecord`. -/
structure ClaimEntry where
  name : String
  P : Prop
  record : ClaimRecord P

namespace ClaimEntry

def tier (e : ClaimEntry) : EpistemicTier := e.record.tier
def status (e : ClaimEntry) : ClaimStatus := e.record.status
def confidence (e : ClaimEntry) : Confidence := e.record.confidence
def evidence (e : ClaimEntry) : String := e.record.evidence
def falsifier (e : ClaimEntry) : String := e.record.falsifier
def dependencies (e : ClaimEntry) : List String := e.record.dependencies

end ClaimEntry

/-- A ledger is a list of named claim records. -/
structure ClaimLedger where
  entries : List ClaimEntry

namespace ClaimLedger

/-- The empty ledger. -/
def empty : ClaimLedger := ⟨[]⟩

/-- Add a named claim to the ledger. -/
def add (ledger : ClaimLedger) (name : String) {P : Prop}
    (record : ClaimRecord P) : ClaimLedger :=
  ⟨ClaimEntry.mk name P record :: ledger.entries⟩

/-- Lookup a claim by name. -/
def lookup (ledger : ClaimLedger) (name : String) : Option ClaimEntry :=
  ledger.entries.find? (fun e => e.name == name)

/-- All dependency names appearing in the ledger, with duplicates. -/
def allDependencies (ledger : ClaimLedger) : List String :=
  ledger.entries.foldr (fun e acc => e.dependencies ++ acc) []

/-- Every dependency name of every claim names an existing claim in the
    ledger.  This is the local well-formedness predicate. -/
def dependenciesResolved (ledger : ClaimLedger) : Prop :=
  ∀ e ∈ ledger.entries, ∀ d ∈ e.dependencies,
    ∃ e' ∈ ledger.entries, e'.name = d

/-- The ledger has unique entry names (value-level): no two entries share
    the same `name`.  This is the **weaker** invariant — it checks value
    equality and is satisfied by `[entry, entry]` (same value at two
    positions), which is insufficient for one-to-one contract-to-entry
    binding.  See `uniqueEntryNames` for the occurrence-level repair.

    Codex re-audit (2026-07-30, `clg_1b946d7211000490825d6aa6`) identified
    this predicate as too weak for the capstone's one-to-one binding claim.
    Retained for backward compatibility; new theorems should use
    `uniqueEntryNames`. -/
def uniqueNames (ledger : ClaimLedger) : Prop :=
  ∀ e₁ ∈ ledger.entries, ∀ e₂ ∈ ledger.entries,
    e₁.name = e₂.name → e₁ = e₂

/-- The ledger has occurrence-unique entry names: no two **positions** in
    `entries` have the same `name`.  This is the occurrence-level invariant
    required for one-to-one contract-to-entry binding in `MeasurementLedger`.

    This is **strictly stronger** than `uniqueNames`: `uniqueNames` checks
    value equality and is satisfied by `[entry, entry]` (same value at two
    positions), while `uniqueEntryNames` rejects that case because the name
    appears at two positions in the mapped list.

    Codex re-audit (2026-07-30, `clg_1b946d7211000490825d6aa6`) identified
    that `uniqueNames` is too weak for the capstone's one-to-one binding
    claim.  This predicate is the repair. -/
def uniqueEntryNames (ledger : ClaimLedger) : Prop :=
  (ledger.entries.map ClaimEntry.name).Nodup

/-- `uniqueEntryNames` implies `uniqueNames`: if no two positions share a
    name, then any two entries (as values) with the same name must be the
    same value (at the same position).  The new predicate is strictly
    stronger.  Proved by induction on the entry list. -/
theorem uniqueEntryNames_implies_uniqueNames
    (ledger : ClaimLedger) (h : ledger.uniqueEntryNames) :
    ledger.uniqueNames := by
  -- Specialized helper (avoids universe polymorphism leak)
  have helper : ∀ (l : List ClaimEntry) (f : ClaimEntry → String),
      (l.map f).Nodup → ∀ {a b : ClaimEntry}, a ∈ l → b ∈ l → f a = f b → a = b := by
    intro l f hnodup
    induction l with
    | nil => intro a b ha hb; simp at ha
    | cons x xs ih =>
      intro a b ha hb hfab
      simp only [List.mem_cons] at ha hb
      rw [List.map_cons, List.nodup_cons] at hnodup
      obtain ⟨hfx_notin, hxs_nodup⟩ := hnodup
      rcases ha with rfl | ha
      · rcases hb with rfl | hb
        · rfl
        · have hfb_mem : f b ∈ xs.map f := by
            rw [List.mem_map]; exact ⟨b, hb, rfl⟩
          rw [hfab] at hfx_notin
          exact absurd hfb_mem hfx_notin
      · rcases hb with rfl | hb
        · have hfa_mem : f a ∈ xs.map f := by
            rw [List.mem_map]; exact ⟨a, ha, rfl⟩
          rw [← hfab] at hfx_notin
          exact absurd hfa_mem hfx_notin
        · exact ih hxs_nodup ha hb hfab
  -- Unfold uniqueEntryNames to the Nodup form
  have hnodup : (ledger.entries.map ClaimEntry.name).Nodup := h
  intro e₁ h₁ e₂ h₂ hname
  exact @helper ledger.entries ClaimEntry.name hnodup e₁ e₂ h₁ h₂ hname

/-- The empty ledger vacuously satisfies `dependenciesResolved`. -/
theorem empty_dependencies_resolved :
    dependenciesResolved empty := by
  simp [empty, dependenciesResolved]

/-- The empty ledger vacuously satisfies `uniqueNames`. -/
theorem empty_unique_names :
    uniqueNames empty := by
  simp [empty, uniqueNames]

/-- The empty ledger vacuously satisfies `uniqueEntryNames`. -/
theorem empty_unique_entry_names :
    uniqueEntryNames empty := by
  simp [empty, uniqueEntryNames]

end ClaimLedger

-- ---------------------------------------------------------------------------
-- 5. Example ledger (demonstration only)
-- ---------------------------------------------------------------------------

theorem one_plus_one_eq_two : (1 : ℝ) + 1 = 2 := by norm_num

theorem zero_le_one : (0 : ℝ) ≤ 1 := by norm_num

def onePlusOneEntry : ClaimEntry :=
  let P : Prop := (1 : ℝ) + 1 = 2
  let h : P := one_plus_one_eq_two
  ClaimEntry.mk "one_plus_one" P
    (ClaimRecord.derived h
      "numerical equality verified by norm_num"
      "1 + 1 ≠ 2")

def zeroLeOneEntry : ClaimEntry :=
  let P : Prop := (0 : ℝ) ≤ 1
  let h : P := zero_le_one
  ClaimEntry.mk "zero_le_one" P
    (ClaimRecord.derived h
      "ordering verified by norm_num"
      "0 > 1"
      ["one_plus_one"])

def exampleLedger : ClaimLedger :=
  ⟨[zeroLeOneEntry, onePlusOneEntry]⟩

theorem exampleLedger_wellFormed :
    exampleLedger.dependenciesResolved := by
  simp [exampleLedger, zeroLeOneEntry, onePlusOneEntry, ClaimLedger.dependenciesResolved,
        ClaimEntry.dependencies]
  decide

-- ---------------------------------------------------------------------------
-- 6. Negative fixture: weak vs strong unique-name predicate
-- ---------------------------------------------------------------------------

/-- **Negative fixture**: a ledger `[entry, entry]` (same value at two
    positions) satisfies the weak `uniqueNames` but does NOT satisfy the
    occurrence-level `uniqueEntryNames`.  This is the defect Codex
    identified: `uniqueNames` checks value equality, not occurrence
    uniqueness. -/
theorem duplicate_entry_satisfies_weak_but_not_strong :
    ({ entries := [onePlusOneEntry, onePlusOneEntry] } : ClaimLedger).uniqueNames ∧
    ¬ ({ entries := [onePlusOneEntry, onePlusOneEntry] } : ClaimLedger).uniqueEntryNames := by
  refine ⟨?_, ?_⟩
  · -- uniqueNames: both entries are the same value, so e₁ = e₂ trivially
    intro e₁ h₁ e₂ h₂ hname
    simp at h₁ h₂
    exact h₁.trans h₂.symm
  · -- ¬uniqueEntryNames: [name, name] is not Nodup
    intro h
    simp only [ClaimLedger.uniqueEntryNames, onePlusOneEntry,
               List.map_cons, List.map_nil] at h
    -- Nodup ["one_plus_one", "one_plus_one"] is false
    exact absurd h (by decide)

end PfLean
