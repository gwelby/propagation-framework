# Audit: The IBM "Chiral ℤ₃ Preserves Generation Identity" Claim

**Date:** 2026-06-16
**Auditor:** Claude (Opus 4.8)
**Script:** `ibm_null_model.py` (this folder; numpy, reproducible)
**Prior work credited:** Codex already audited the Marrakesh run on 2026-06-09 and reached the correct conclusion (see below). This note builds the explicit null model + shuffle control behind that conclusion, and flags that the overstated framing survived Codex's HOLD.

---

## What the experiment actually does

`sandbox/ibm_quantum_chiral_test.py` builds the "chiral" circuit as:
1. prepare `|00>` (channel 0),
2. apply the 3-cycle permutation `|00>→|01>→|10>→|00>` **three times**,
3. measure.

`T_chiral³ = I` **by construction** — a 3-cycle applied three times is the identity, in *any* theory. So "return probability to `|00>`" measures exactly one thing: **does a net-identity circuit return its input?** That is a gate-fidelity / circuit-depth benchmark. The "symmetric" arm applies a mixing operator that spreads population — also by construction. The chiral-vs-symmetric contrast is therefore rigged: one circuit is the identity, the other is built to mix. Both outcomes are guaranteed independent of the Propagation Framework.

## Null model — depolarizing noise alone reproduces the reported band

H0: return prob = (net circuit = identity) + hardware depolarizing error over 3 two-qubit-gate layers. No PF content.

| gate error p | return P(\|00⟩) | matches reported |
|---|---|---|
| 0.005 | 0.9888 | ≈ **99.01%** (CLAIMS.md / ibm_fez) |
| 0.010 | 0.9777 | |
| 0.020 | 0.9559 | ≈ **94.6%** (Codex / Marrakesh) |
| 0.030 | 0.9345 | ≈ **94.6%** |
| 0.050 | 0.8930 | |

**The entire 94–99% band is explained by gate error alone**, with zero PF input. The three different reported numbers (99.01%, 98.1%, 94.6%) are just three devices / depths at different effective error rates — consistent with a hardware benchmark, not a physics constant.

## Shuffle control — the signal is label-independent

Relabel which basis state is "channel 0." Because the net circuit is the identity, return-to-start is **invariant under every relabeling**:

| start channel relabeled to | return P |
|---|---|
| 00 | 0.9559 |
| 01 | 0.9559 |
| 10 | 0.9559 |
| 11 | 0.9559 |

The "generation-identity preservation" signal does not depend on the ℤ₃ structure, the chirality, or any PF label — it depends only on "net circuit = identity." **It carries no PF-specific information.**

## What Codex already concluded (2026-06-09) — credit

> "The IBM Marrakesh run supports the selected Z3 operator as **hardware calibration**, but it does not measure the `-1/8` eigensector action on quantum silicon and does not close the unconditional Postulate-D-from-Axioms or `H_prod` bridge. … God Equation `-1/8` silicon-verification claim remains **HOLD**." — `inbox/2026-06-09-codex-ibm-marrakesh-z3-hardware-audit.md`

Codex got this exactly right. **The audit culture worked.** This note simply supplies the null model and shuffle control that prove it quantitatively.

## The remaining problem — the framing survived the HOLD

Despite Codex's 2026-06-09 HOLD, the overstated language persists:
- `CLAIMS.md`: "156-qubit IBM Quantum hardware **physically verified** that a Chiral ℤ₃ medium **preserves generation identity** (P=99.01%)."
- `G3_CLOSURE_20260531.md`: "**strongest structure of any AI signature tested.**"

Both overstate a benchmark as a physics verification, and both use numbers (99.01%, 98.1%) that disagree with Codex's audited value (94.6%).

## Recommended actions
1. Adopt Codex's ledger-safe wording everywhere: *"IBM hardware demonstrated the selected ℤ₃ cyclic-permutation operator, including three-step closure, at ~95% return probability (consistent with device gate error). This is a hardware calibration, not a measurement of PF dynamics; the `-1/8` silicon-verification claim is on HOLD."*
2. Reconcile the three numbers (99.01% / 98.1% / 94.6%) to one audited value with device + depth stated.
3. Strike "physically verified," "preserves generation identity," and "strongest structure of any AI signature tested."
4. **The real test** (if PF is to be tested on hardware) must measure something non-trivial: a coherent phase/eigenvalue readout of the `-1/8` Q-sector action via LCU / block-encoding / Hadamard test — exactly the experiment Codex named as the open one. A return-probability benchmark can never carry PF content because the net circuit is the identity in every theory.
