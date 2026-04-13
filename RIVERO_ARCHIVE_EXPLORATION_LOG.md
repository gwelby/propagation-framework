# Rivero Archive Exploration Log

*Date: April 12, 2026*  
*Status: SERVER INACCESSIBLE — Alternative approaches identified*

---

## What We Tried to Access

**Target**: `http://lxbifi11.bifi.unizar.es:8080/3/`

- Rivero's invitation to Greg (Mar 21, 2026): "start in <http://lxbifi11.bifi.unizar.es:8080/3/> with the e-collaborators, not a task for the human"
- Referenced in our `ISSUES/issue_05_koide_phase.md` as source for Koide phases data

---

## Access Attempts

1. **Direct HTTP access** - Failed: Connection timeout (2973ms)
2. **curl check** - Failed: Could not connect to server
3. **Domain check** - Server appears to be down or moved

---

## Alternative Sources Found

### 1. ArXiv Papers (Accessible)

- **hep-ph/0505220**: "The strange formula of Dr. Koide" (Rivero & Gsponer, 2005)
  - Historical review of Koide formula
  - Speculations on extensions to quarks and neutrinos

- **hep-ph/0606171**: "Mass terms to break susy-like degeneration" (Rivero, 2006)
  - Mentions Weinberg angle at 0.13σ (similar to our derivation)
  - PDF not readable in chunks but abstract accessible

- **1301.4143**: "Koide's Z3-symmetric parametrization, quark masses and..." (2013)
  - Discusses Z3 symmetry in Koide parametrization
  - PDF not readable in chunks

### 2. Personal Website (Partially Accessible)

- **https://a.rivero.nom.es/research/** - Basic structure accessible
  - Contains references to his work but not detailed papers
  - Links to reference pages but Koide materials not directly found

### 3. What We Already Have

- Rivero's mechanism documented in `ISSUES/issue_05_koide_phase.md`:
  - Three-instanton superpotential: W₃ = c₃ (det M)³ / Λ¹⁸
  - Effective potential: V_eff(δ) ∝ [f(δ)]⁶ × (harmonic sum)
  - Fourier expansion showing cos(9δ) at 34% amplitude of cos(3δ)
  - Z₉ symmetry from 3 instantons × 3 generations

---

## Research Leads Identified

1. **Foot Reference**: <hep-ph/9402242> (cone presentation of Koide)
   - Already confirmed as prior art for R/A = √2 geometry
   - Need to check for any phase-related content

2. **Newcastle Cubic Invariants**: Anonymous Wikipedia contributor
   - Theory connecting Koide to symmetric polynomials
   - e₂/e₁² = 1/6 in Vieta basis
   - May provide bridge to U(3) decomposition

3. **Recent Z3 Work**: 2013 paper on Z3-symmetric parametrization
   - Might have evolved beyond the 2006 instanton mechanism
   - Worth checking when PDF access is available

## Update: Foot Paper Downloaded

Successfully downloaded Foot's 1994 paper (`foot_1994.pdf`, 37KB) but unable to extract text due to PDF format limitations. The abstract confirms:

- "We point out that this relation has a geometric interpretation"
- This is the cone presentation Rivero mentioned
- No indication of phase-related content in abstract

---

## Next Steps

1. **Extract Foot paper content** - Need PDF text extraction tool to check for phase discussion
2. **Monitor Rivero's server** - It may be temporarily down
3. **Email Rivero?** - Could politely ask if the materials are available elsewhere
4. **Focus on what we have** - The mechanism is already documented; the gap is harmonic suppression

---

## Honest Assessment

The inaccessible archive is a setback but not a blocker. We have:

- The core mechanism (three-instanton superpotential)
- The numerical Fourier expansion
- The open problem (why cos(9δ) dominates over lower harmonics)

What we might be missing:

- Detailed calculations of V_cross cancellation
- Any updates since 2006
- Connections to other approaches Rivero may have explored

The fundamental question remains: **What suppresses cos(3δ) and cos(6δ) to make cos(9δ) dominant?** This is a physics calculation problem, not an access problem.
