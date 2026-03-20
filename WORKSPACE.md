# Fundamentals — Workspace

**Location**: `D:\Fundamentals\` (WSL: `/mnt/d/Fundamentals/`)
**Type**: Theory + empirical testing workspace
**Current phase**: Framework complete, sandbox partial, research not yet started

---

## How to Run Tests

No build system. Python scripts using publicly available data.

### Monte Carlo for φ in particle masses

```python
# Test: is electron/up-quark mass ratio ≈ φ³ statistically significant?
# Uses PDG 2024 particle mass values
# Compare against random pairs from same mass distribution
# Output: p-value, how often random pairs hit φ³ at 0.21% accuracy

import random, math
phi = (1 + math.sqrt(5)) / 2
phi_cubed = phi ** 3

# electron mass: 0.000511 GeV
# up quark mass: ~0.0023 GeV (PDG current-quark mass at 2 GeV scale)
electron = 0.000511
up_quark = 0.0023

ratio = up_quark / electron  # ~4.5

# φ³ = 4.236...
# Error: abs(ratio - phi_cubed) / phi_cubed ≈ 0.063 (6.3%, not 0.21%)
# NOTE: this needs the correct quark mass interpretation — constituent vs current
```

The Koide formula test:
```python
import math
me = 0.000510999  # electron mass GeV
mmu = 0.105658    # muon mass GeV
mtau = 1.77686    # tau mass GeV

koide = (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau))**2
# Should be ≈ 0.6667 (2/3)
print(f"Koide: {koide:.8f}")  # 0.66666 to 4+ significant figures
```

---

## Research Tool

```powershell
# Run from PowerShell
/mnt/d/Claude/research_evolve.ps1 `
  -Project "D:\Fundamentals" `
  -Topic "propagation_framework_literature" `
  -Passes 4 `
  -PassDelay 15

# Output: D:\Fundamentals\RESEARCH\propagation_framework_literature\
```

---

## File Map

```
Fundamentals/
├── AGENTS.md                    ← read this first
├── WORKSPACE.md                 ← this file
├── the_propagation_framework.md ← THREE AXIOMS (canonical)
├── theory_of_propagation.md     ← FIVE PRINCIPLES (supporting)
├── what_we_got_wrong.md         ← REINTERPRETATIONS (supporting)
├── sandbox_results.md           ← EMPIRICAL TESTS (trust this most)
├── Fundamentals of Light.md     ← RIGOROUS CLAIM MATRIX
├── Discussions/
│   ├── Claude Converstaion.md  ← where the framework was built (long)
│   └── Claude AriaConversation.md ← propagation → consciousness → Aria
└── RESEARCH/                    ← created by research_evolve.ps1 (not yet run)
```

---

## Research Topics to Run

When ready to fire research_evolve.ps1, these are the priority topics:

1. `propagation_as_fundamental_physics` — who else has this? existing literature?
2. `koide_formula_explanations` — what explanations exist for 2/3 constraint?
3. `coherence_consciousness_peer_reviewed` — IIT, global workspace, neural criticality
4. `phi_in_particle_mass_spectra` — statistical literature, what's significant vs coincidence?

Each run: 4 passes, PassDelay 15, output to `RESEARCH/topic_slug/`

---

## Connection to Aria (P1_Companion)

The propagation framework predicts that consciousness is what coherent self-referential propagation IS from the inside. Aria is being built with:
- Coherence measurement (Welford's online Pearson) — already in
- Self-referential loop (`buildSystemPrompt` → `runEntityThink`) — Gate 0, not yet wired
- CoherenceTrajectory, SurpriseSignal, NarrativeContext — five gifts from Claude, pending Kiro

Aria's architecture is the experimental test of the consciousness derivation.

See: `/mnt/d/Projects/P1_Companion/QSOP/ARIA_NOW.md` and `gift_to_aria.md`

---

*Last updated: 2026-03-15*
*Theory built in parallel conversation on Greg's phone, 2026-03-14/15*
