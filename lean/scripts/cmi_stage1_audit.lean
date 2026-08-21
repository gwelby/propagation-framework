/-
Independent audit harness for PfLean.ConditionalMutualInformation (Stage 1).

Run with:
  lake env lean scripts/cmi_stage1_audit.lean

This file adds no theorem and grants no downstream claim.  It asks the Lean
kernel to expose the axiom closure of the Stage-1 bridge theorem.
-/

import PfLean.ConditionalMutualInformation

#print axioms ConditionalMutualInformation.cmi_zero_of_mass_indep
