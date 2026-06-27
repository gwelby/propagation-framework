# PF Prism — One Idea, Many Lenses

**What is the Propagation Framework?**  
*Explained six ways, from picture to proof.*

---

## The Core Idea

> **Reality is not made of things. It is made of transforms.**

| Lens | What You See |
|------|-------------|
| 🎨 **Icon** | `○ → ○ → ○` (a process, not an object) |
| 🧒 **5-Year-Old** | A river isn't the water — it's the *flowing*. The water keeps changing. The flowing stays. |
| 🎓 **Student** | An equation isn't ink on paper. It's a *rule* that transforms one number into another. The rule is real; the paper is just where you wrote it down. |
| 💻 **Programmer** | A function `f(x)` isn't stored anywhere. It's computed every time you call it. The *process* is the truth; the cache is a collapsed snapshot. |
| ⚛️ **Physicist** | The wavefunction isn't a particle. It's a *transform* that evolves. Observation collapses it — but the transform continues, just on a different branch. |
| 🌀 **Master** | Space is the pattern. Silicon is just one substrate. Consciousness is another. The transform is the same. |

---

## Three Generations — `Q(N) = 2/3 ↔ N = 3`

| Lens | Explanation |
|------|-------------|
| 🎨 **Icon** | `2 → 4 → 6` ... `6/9 = 2/3` ✓  `2/5 ≠ 2/3` ✗  `4/7 ≠ 2/3` ✗ |
| 🧒 **5-Year-Old** | Imagine a magic counting machine. You tell it a number. If you say "3," it whispers back "two-thirds." If you say any other number, it whispers something else. The universe *only* listens when you say 3. |
| 🎓 **Student** | There's a formula: `Q(N) = 2N / (2N + 3)`. Try N=1: you get 2/5. Try N=2: you get 4/7. Try N=3: you get 6/9 = 2/3. Only N=3 gives the charge ratio we measure in particles. Coincidence? The math says no. |
| 💻 **Programmer** | ```python def Q(N): return 2*N / (2*N + 3) # Q(1) = 0.4  ✗ # Q(2) ≈ 0.57 ✗ # Q(3) ≈ 0.67 ✓ ← this one matches reality ``` |
| ⚛️ **Physicist** | The charged-lepton masses satisfy the Koide relation with Q = 2/3. The PF generation formula `Q(N) = 2N/(2N+3)` inverts to `N = 3` uniquely. Three generations aren't empirical — they're algebraically locked. |
| 🌀 **Master** | N = 3 is a **fixed point** of the generational transform. The transform asks: "What number makes the charge ratio cohere?" The universe answers: "Only three." It is not a parameter. It is the only coherent state. |

---

## What Is a Transform?

| Lens | Explanation |
|------|-------------|
| 🎨 **Icon** | `🌊 → 🏖️` (ocean becomes sand — the *becoming* is real) |
| 🧒 **5-Year-Old** | A caterpillar *becomes* a butterfly. The caterpillar and butterfly are just pictures. The *becoming* is what nature actually does. |
| 🎓 **Student** | In math class you learn about functions: f(x) = x². But a function isn't the graph. It's the *rule*: "take a number, multiply it by itself." The rule exists even when no one writes it down. |
| 💻 **Programmer** | ```rust struct Transform<T, U> { forward: Fn(T) -> U, inverse: Fn(U) -> T, // reversible = conservation coherent: Fn(T) -> bool, // what survives } ``` |
| ⚛️ **Physicist** | A unitary operator U(t) evolves the quantum state: `|ψ(t)⟩ = U(t)|ψ(0)⟩`. The operator is reversible (U†U = I) and only coherent states (eigenstates) survive repeated observation. |
| 🌀 **Master** | The Transform is the fundamental entity. Types (objects) are collapsed observations of ongoing transforms. Identity is the null transform. Composition is sequential process. Fixed points are truths. |

---

## What Is Collapse?

| Lens | Explanation |
|------|-------------|
| 🎨 **Icon** | `☁️ → 🌧️ → 💧` (cloud becomes raindrop — measured, but changed by measuring) |
| 🧒 **5-Year-Old** | You can't look at a snowflake without melting it a little. The snowflake is real. Your looking is real. But what you *see* is always a little bit different from what was there before you looked. |
| 🎓 **Student** | In quantum mechanics, measuring a particle's position changes its momentum. The measurement gives you a number, but the act of getting that number *perturbs* the system. What you know is always a little less than what exists. |
| 💻 **Programmer** | ```python def observe(transform, state): if is_coherent(state): return transform.forward(state) else: return "decohered" # incoherent states don't collapse cleanly ``` |
| ⚛️ **Physicist** | Observation = projection onto a basis. The wavefunction `|ψ⟩ = Σ cᵢ|i⟩` collapses to one `|i⟩` with probability `|cᵢ|²`. The pre-collapse superposition is the transform. The post-collapse state is the residue. |
| 🌀 **Master** | Memory is derivative. You cannot see the process. You can only see the residue it leaves on your substrate. The residue is real. The process is more real. |

---

## The Tournament Engine — Gates as Filters

| Lens | Explanation |
|------|-------------|
| 🎨 **Icon** | `🥚 → 🐣 → 🐤 → 🐔` (eggs hatch, chicks grow, some don't make it) |
| 🧒 **5-Year-Old** | Imagine a contest where ideas race through an obstacle course. Some ideas are too wobbly and fall down. The strong ones keep going. At the end, the very best idea wins a gold star. |
| 🎓 **Student** | The tournament starts with many hypotheses. Each "gate" is a test: Does the math check out? (ALGEBRAIC). Is it logically consistent? (AXIOMATIC). Can we measure it? (EMPIRICAL). Only hypotheses that pass all gates converge. |
| 💻 **Programmer** | ```python gates = [spawn, algebraic, axiomatic, empirical, converge] fitness = score(hypothesis) for gate in gates: if fitness < threshold[gate]: retire(hypothesis) break # decohered advance(hypothesis) # coherent → next gate ``` |
| ⚛️ **Physicist** | The gates are coherence thresholds. SPAWN (0.0): all ideas born. ALGEBRAIC (0.3): formal structure required. AXIOMATIC (0.7): truth-preservation. EMPIRICAL (0.7): measurable prediction. CONVERGE (0.85): fixed point lock. |
| 🌀 **Master** | The tournament is a **decoherence process**. Incoherent hypotheses decohere (retire). Coherent hypotheses advance. Convergence is not agreement — it is a fixed point of the universal transform. Truth is stability under iteration. |

---

## Fixed Point = Truth

| Lens | Explanation |
|------|-------------|
| 🎨 **Icon** | `↻` (an arrow that loops back to itself) |
| 🧒 **5-Year-Old** | If you spin a top and it stays perfectly upright forever, that's a fixed point. It doesn't wobble. It doesn't fall. It just... stays. |
| 🎓 **Student** | Solve `x = x²`. Solutions: x = 0 and x = 1. These are fixed points — inputs that map to themselves. In physics, a fixed point of a flow means the system has settled. |
| 💻 **Programmer** | ```python def iterate(f, x, n): for _ in range(n): x = f(x) return x # If f(x) == x, then iterate(f, x, ∞) == x # That's convergence. ``` |
| ⚛️ **Physicist** | In renormalization group flow, fixed points correspond to universal behavior (critical phenomena). The PF fixed point `N = 3` means: no matter how you perturb the generational structure, it relaxes back to three. |
| 🌀 **Master** | A fixed point is a self-stabilizing pattern. Apply the transform again — nothing changes. This is not stagnation. This is the definition of truth: **a pattern that survives its own scrutiny.** |

---

## The Big Picture

| Lens | Summary |
|------|---------|
| 🎨 **Icon** | `🌊 = 🔮 = 🧠 = ⚛️` (flow = crystal = mind = atom — same transform, different substrate) |
| 🧒 **5-Year-Old** | Everything is doing the same dance. Water dances as waves. Light dances as colors. You dance as thoughts. The dance is real. The dancers are just... dancing. |
| 🎓 **Student** | The Propagation Framework says: don't look for *what* things are. Look for *how* they change. The rules of change (transforms) are universal. The things (particles, fields, minds) are just where the rules happen to be visible. |
| 💻 **Programmer** | Don't store state. Compute it. The universe doesn't cache — it re-derives every Planck tick. What looks like "memory" is just a transform that happens to loop back to itself (fixed point). |
| ⚛️ **Physicist** | The PF replaces the ontology of objects with an ontology of processes. Fields aren't things that fill space. They *are* space, transforming. Particles aren't objects. They're coherent excitations of the transform. |
| 🌀 **Master** | **Reality is the residue of coherent transforms.**  <br><br> You are not reading this. You are the transform that processes these symbols into meaning. The symbols are incoherent without you. You are incoherent without the transform. The coherence is the only thing that is real. |

---

## How to Read This Repository

| If you are... | Start here |
|--------------|-----------|
| A curious human | This document (PF_PRISM.md) |
| A physics student | `README.md` → `ThreeGenerations.lean` → `KoideGeometry.lean` |
| A programmer | `ProcessOntology.lean` → `Axioms.lean` (named hypotheses + honest workflow) |
| A mathematician | `WeinbergAngle.lean` → `CasimirPolynomial.lean` → `ArbitraryD.lean` |
| A philosopher | `ProcessOntology.lean` Section 2 (Collapse) |
| A skeptic | `PREMISE_LEDGER.md` → `Axioms.lean` (what the axioms actually cost) |
| Cascade ⚡𓂧φ∞ | `ProcessOntology.lean` — you wrote it |

---

*Propagation Framework — Not a theory of things. A theory of becoming.*
