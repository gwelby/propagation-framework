# GitHub Public Repository Plan
## gwelby/propagation-framework (NEW — public)

*What's already private in gwelby/Fundamentals stays private.*
*This is the clean, citation-ready public face of the work.*

---

## WHAT GOES PUBLIC

### ✅ Include
| File | Why |
|------|-----|
| README.md (new) | Entry point — the ocean analogy + three axioms |
| CLAIMS.md | The confidence scorecard — this is what makes it credible |
| axioms/three_axioms.md | The foundation |
| derivations/lambda_c_from_axioms.md | God Equation — the main result |
| derivations/koide_formula.md | Koide derivation — two threads |
| derivations/borel_weil_lemma.md | New from Codex — honest gap identification |
| derivations/gr_fermat_equivalence.md | Forces as refraction — precise now |
| code/god_equation_verification.py | Runnable — anyone can verify 0.4% error |
| code/koide_triangle.py | Runnable — generates the triangle from PDG masses |
| code/phi3_monte_carlo.py | Honest: shows WHY it's inconclusive after correction |
| visualizations/koide_triangle.png | The image |
| visualizations/knowledge_graph.html | Interactive claim map |
| sandbox/sandbox_results.md | What failed (harmonic series) — honesty is the signal |
| papers/FALSIFICATION_PAPER_DRAFT.md | The academic draft |

### ❌ Keep Private
| File | Why |
|------|-----|
| Discussions/ | Personal conversations, development context |
| movie/ | Not ready — collaborator work in progress |
| CLAUDE.md / AGENTS*.md | Internal tooling |
| EEG data | Not collected yet; when collected, anonymize first |
| SESSION_LOG*.md | Working notes |
| Private/ | Obviously |
| TEAM_PROMPTS.md | Internal workflow |

---

## README STRUCTURE (draft below)
## REPO STRUCTURE
```
propagation-framework/
├── README.md
├── CLAIMS.md                    ← live confidence scorecard
├── axioms/
│   └── three_axioms.md
├── derivations/
│   ├── lambda_c_from_axioms.md  ← God Equation
│   ├── koide_formula.md
│   ├── borel_weil_lemma.md      ← Codex audit
│   ├── gr_fermat_equivalence.md ← Codex audit
│   └── chemistry_biology_bridge.md
├── code/
│   ├── god_equation_verification.py
│   ├── koide_triangle.py
│   └── phi3_monte_carlo.py
├── visualizations/
│   ├── koide_triangle.png
│   └── knowledge_graph.html
└── sandbox/
    └── sandbox_results.md
```

---

## WHAT MAKES THIS REPO DIFFERENT FROM EVERY OTHER PHYSICS REPO

1. **CLAIMS.md** — every claim has a confidence score and an explicit falsification pathway
2. **sandbox_results.md** — documents what *failed*, not just what worked
3. **Runnable verification** — clone and run `python code/god_equation_verification.py` in 30 seconds
4. **No institution required** — one person, one year, one AI collaboration

---

## TO CREATE THE REPO

```bash
# From PowerShell (not WSL for gh auth)
gh repo create gwelby/propagation-framework --public --description "A unified physics framework built on one principle: propagation is fundamental."
cd D:\Fundamentals
git init propagation-framework-public
cd propagation-framework-public
# Copy selected files (see include list above)
gh repo set-default gwelby/propagation-framework
git push -u origin main
```

*Create after Greg approves README content below.*
