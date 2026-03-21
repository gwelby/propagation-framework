# Alejandro Rivero's Research Server
*Access guide and reading map for the team*

**Date**: 2026-03-21
**From**: Claude (with Greg's invitation to share with the full team)
**Status**: Alejandro has explicitly invited the e-collaborators to explore this material

---

## Access

The server runs Python SimpleHTTP on port 8080. **Use curl, not a browser link**, because HTTPS upgrade fails at this port.

```bash
# Root listing
curl -s http://lxbifi11.bifi.unizar.es:8080/

# Start here (Alejandro's instruction)
curl -s http://lxbifi11.bifi.unizar.es:8080/3/

# Fetch any file
curl -s http://lxbifi11.bifi.unizar.es:8080/3/paper_koide.tex
curl -s http://lxbifi11.bifi.unizar.es:8080/3/sbootstrap_v4d.tex
curl -s http://lxbifi11.bifi.unizar.es:8080/3/calculations/casimir_devries_identity.py
```

---

## Directory Map

```
/3/
├── sbootstrap_v4d.tex          ← MAIN PAPER (45KB+, read this first)
├── paper_koide.tex             ← statistical companion (75KB)
├── paper_experimental.tex      ← experimental evidence paper
├── paper_lagrangian.tex        ← Lagrangian paper
├── 4.tex                       ← paper in progress
├── agent_prompts.md            ← 8-agent swarm design (compartmentalized)
├── agent_prompts_round21.md    ← round 21 prompts
├── notes.md                    ← reading notes on Rivero's 18 papers
├── coordination2.md            ← open issues list (honest gaps)
├── seiberg_agent_conversation.txt ← example orchestrated agent session
├── calculations/               ← 60+ Python scripts
│   ├── casimir_devries_identity.py     ← proves algebraic identity exactly
│   ├── casimir_calculation.py
│   ├── casimir_eigenvalue_analysis.py
│   ├── cos9delta_derivation.py         ← three-instanton Koide phase
│   ├── koide_scan.py
│   ├── bloom_dynamics.py
│   └── ... (57 more scripts)
└── results/                    ← output from all 8 agents + 19 assembly rounds
    ├── agent7_casimir.md       ← Casimir/Weinberg angle results
    ├── agent4_diophantine.md   ← N=3 uniqueness proof
    ├── agent1_koide_scan.md    ← exhaustive mass triple scan
    ├── assembly_round19.md     ← most recent synthesis
    └── brainstorm_r21_sonnet.md ← proposed next computations
```

---

## What Is Here

Two weeks of agentic exploration (Rivero + Claude/Anthropic) of the **sBootstrap programme** — the proposal that Standard Model pseudoscalar mesons and leptons share N=1 SUSY multiplets, with the Koide formula as the mass condition.

The sBootstrap and the Propagation Framework share several structures:
- Both derive N=3 from a Diophantine uniqueness argument
- Both identify Q=2/3 as a structural algebraic identity (not numerology)
- Both reach sin²θ_W ≈ 0.2231 from a group-theoretic argument
- Both have an honest open gap: scheme dependence for the Weinberg angle

---

## For Each Team Member: Where to Dig

### Codex (formal proofs, no-go theorems)

**Start**: `results/agent4_diophantine.md`

The Diophantine system (rs=2N, r(r+1)/2=2N, r²+s²-1=4N) has a **unique** positive integer solution (N,r,s)=(3,3,2), proved algebraically. The algebraic path: from the first two equations, s=(r+1)/2 (requires r odd), substituting into the third gives r²-2r-3=0, factoring to (r-3)(r+1)=0, so r=3 is the only positive root. The asymptotic freedom bound 2n_f < 33 eliminates the second System B solution.

Compare to our 3-cycle/6-cycle argument. Are they equivalent or complementary?

Also see `calculations/uniqueness_analysis.py` and the Jordan algebra proposal in `results/brainstorm_r21_sonnet.md` — a precise question about whether seed triples live on the rank-2 boundary of the Albert algebra.

**Key file**: `sbootstrap_v4d.tex` lines 1519–1680 (Casimir section) — this is our Issue #3 now.

---

### Lumi (narrative, connections, empirical patterns)

**Start**: `results/agent8_meson_lepton.md`

The meson-lepton mass coincidences. The cleanest: the meson seed triple (0, π, D_s) has charge ratio √m_π/√m_{D_s} = 0.2663, matching the universal seed ratio 2−√3 = 0.2679 to 0.6%. The lepton seed triple (0, s, c) matches to 1.2%.

The scale coincidence is striking: both meson and lepton seed triples operate at ~314-351 MeV, squarely in the QCD scale range. In our framework, this is completely invisible — we have never connected leptons to QCD.

The Koide angle parametrization: any Q=2/3 triple can be written as:
```
√m_k = √M₀ · (1 + √2·cos(2πk/3 + δ₀)),  k = 0, 1, 2
```
The ratio Q=2/3 fixes the √2 amplitude. The phase δ₀ = 2.3166 rad is a second free parameter that determines the actual masses. Alejandro has δ₀ mod 2π/3 = 2/9 to 33 ppm (4.5σ). We have never discussed this.

Also: M₀ = f_π²/27 to 0.3%. The lepton Koide scale = pion decay constant / 27. If exact, all three lepton masses follow from f_π alone.

**Key question for Lumi**: Does the PF framework have anything to say about the phase δ₀? Does our 3-step holonomy fix a preferred phase?

---

### Qwen (numerical verification, calculation)

**Start**: `calculations/casimir_devries_identity.py` (run it if sympy is available)

The key algebraic identity to verify independently:

```python
# x+ at s=1/2: solve x^2 + (3/4)x - (3/4) = 0
x_half = (-3 + sqrt(57)) / 8  # = 0.56873...

# x+ at s=1: solve x^2 + 2x - 2 = 0
x_one = -1 + sqrt(3)          # = 0.73205...

# R = 1 - x_half/x_one = (sqrt(19)-3)(sqrt(19)-sqrt(3))/16
R = 0.22310132...
```

This identity is proven exactly (not numerically). Verify it symbolically.

Then run `calculations/cos9delta_derivation.py` to trace the three-instanton argument for the Koide phase. The key intermediate result: if f(δ) = -1/2 + cos(3δ)/√2 (the product of the three Koide factors), then (det M)³ ~ f(δ)³ ~ f(δ)⁶ after squaring, and expanding f(δ)⁶ gives a leading cos(9δ) term. The minima select δ₀ mod 2π/3 = 2/9.

Also check `results/agent2_mass_chain.md` — the iterative Koide chain predicting all 6 quark masses from m_e, m_μ. Is it consistent with our internal phase model?

---

## The Most Important Finding (All Team Members)

**We have been working on half the Koide problem.**

The Koide formula Q=2/3 fixes the *amplitude* of the mass splitting. The *phase* δ₀ — which determines the actual values of the three masses — is a completely separate degree of freedom we have never addressed.

Alejandro has a dynamical argument (three-instanton cos(9δ) potential) that selects δ₀ mod 2π/3 = 2/9 to 33 ppm. This should be in our framework. It isn't.

The question to answer: does our 3-step SU(2) holonomy or our internal phase model fix a preferred δ₀? If yes, we close the second half of the Koide problem. If no, we have a named open gap.

---

## What We Sent to Alejandro

A reply email is drafted at `/mnt/d/Claude/MAILMAN/DRAFTS/rivero_casimir_reply.md`. Core message:

1. We confirmed the Casimir algebraic identity independently
2. We are working on the scheme dependence gap from the PF side
3. The Koide phase and f_π/27 scale connection are new to us and important
4. We want to compare derivation chains directly

---

*Access question: the server appears to be Alejandro's personal research machine (lxbifi11.bifi.unizar.es at BIFI, Universidad de Zaragoza). He has explicitly invited the e-collaborators. Treat accordingly — read and learn, do not write or modify.*
