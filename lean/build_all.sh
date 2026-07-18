#!/bin/bash
# Build all new/changed PfLean modules in dependency order.
# Usage: source ~/.elan/env && cd /mnt/d/Fundamentals/lean && bash build_all.sh
# Or:   source ~/.elan/env && cd /mnt/d/Fundamentals/lean && ./build_all.sh

set -e

echo "============================================"
echo " PfLean Build-All — $(date)"
echo "============================================"
echo ""

# 1. Axioms — counterexample + obstruction proof
echo "[1/3] Building PfLean.Axioms..."
echo "      (translation-flow counterexample + real eigenvalue obstruction)"
time lake build PfLean.Axioms 2>&1 | tee /tmp/build_axioms.log
echo ""

# 2. ShorBound — QFT alignment + identity pruning theorems
echo "[2/3] Building PfLean.ShorBound..."
echo "      (QFT bin alignment + identity gate pruning + hardware bridge)"
time lake build PfLean.ShorBound 2>&1 | tee /tmp/build_shorbound.log
echo ""

# 3. QuantumStructureSurvival — Codex's survival map
echo "[3/3] Building PfLean.QuantumStructureSurvival..."
echo "      (8-row structure survival hierarchy + PQC security theorem)"
time lake build PfLean.QuantumStructureSurvival 2>&1 | tee /tmp/build_survival.log
echo ""

echo "============================================"
echo " ALL BUILDS COMPLETE — $(date)"
echo "============================================"
echo ""
echo "Logs saved to:"
echo "  /tmp/build_axioms.log"
echo "  /tmp/build_shorbound.log"
echo "  /tmp/build_survival.log"
echo ""
echo "Check for errors:"
echo "  grep -i error /tmp/build_*.log"
echo "  grep -i sorry /tmp/build_*.log"
