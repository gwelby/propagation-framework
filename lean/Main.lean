import PfLean

def main : IO Unit := do
  IO.println "Propagation Framework -- Lean 4 Formalization"
  IO.println "============================================"
  IO.println ""
  IO.println "Authors: Devin (Cognition Being), Greg Welby, PF Research Team"
  IO.println "Date: 2026-05-21"
  IO.println ""
  IO.println "Modules verified:"
  IO.println "  * PfLean.KoideGeometry    -- Koide R/Q conventions + bridge theorem"
  IO.println "  * PfLean.WeinbergAngle    -- Casimir derivation of sin²θ_W (0.13σ match)"
  IO.println "  * PfLean.GravityOptics    -- Weak-field refractive index from static metric"
  IO.println ""
  IO.println "Build: lake build"
  IO.println "See PfLean/ directory for theorem statements and proofs."
