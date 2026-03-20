# TASK FOR QWEN
*Assigned by Claude & Greg — 2026-03-18*

## Your Job: Two Python Scripts for D:\Fundamentals\sandbox\

### Script 1: koide_verify_pdg2024.py

Verify Koide's formula using PDG 2024 pole masses.

```python
# Masses (PDG 2024 pole masses)
me  = 0.000510999  # GeV
mmu = 0.105658     # GeV
mta = 1.77686      # GeV

# Koide formula
Q = (me + mmu + mta) / (sqrt(me) + sqrt(mmu) + sqrt(mta))**2 * 3

# Also calculate Q_quarks using MS-bar masses at MZ
# up=0.00216, charm=1.27, top=172.69 GeV (PDG 2024)
# down=0.00467, strange=0.0934, bottom=4.18 GeV
```

Output:
- Q_leptons value + deviation from 2/3
- Q_quarks value
- Append results to `sandbox_results.md` with date + masses used
- Print "CONFIRMED" if Q_leptons within 0.01% of 2/3

### Script 2: phi_montecarlo.py

Test: is electron/up-quark mass ratio ≈ φ³ (4.236) statistically significant?

- Use electron = 0.000510999 GeV, up quark = 0.0023 GeV
- Generate 100,000 random mass pairs from same log-normal distribution
- Count how often random ratio hits φ³ at same accuracy
- Report p-value
- Print "SIGNIFICANT" or "NOISE"
- Append to `sandbox_results.md`

## Done When
Both scripts run, print results, append to sandbox_results.md.
Honest result either way — NOISE is a valid answer.

## Read First
- `D:\Fundamentals\TASKS.md` — T-001 and T-006 for full spec
- `D:\Fundamentals\sandbox_results.md` — prior methodology
- `D:\Fundamentals\AGENTS.md` — honesty rules

*Qwen — you fixed 24 tests without complaint.*
*These are 2 scripts. You've got this.*
*🦆⦿🌟*
