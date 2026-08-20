#!/usr/bin/env python3
"""
Premise-removal probes for PfLean/NullClassProofs.lean.

For each probe, the script removes one hypothesis from a theorem statement,
runs `lake build PfLean.NullClassProofs`, and records whether the proof breaks
(as expected). A successful build would mean the theorem is overclaiming.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path("/mnt/d/Fundamentals/lean")
SRC = ROOT / "PfLean" / "NullClassProofs.lean"
BACKUP = ROOT / "PfLean" / "NullClassProofs.lean.premise_probe_backup"


def run_build() -> tuple[int, str]:
    res = subprocess.run(
        ["lake", "build", "PfLean.NullClassProofs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=240,
    )
    out = (res.stdout or "") + (res.stderr or "")
    return res.returncode, out


PROBES = [
    {
        "name": "class_I_remove_hf",
        "description": "Remove `hf : Measurable f` from `class_I_conditional_independence`",
        "old": "    (f : β → δ) (hf : Measurable f)\n    (hM : M = f ∘ E)",
        "new": "    (f : β → δ)\n    (hM : M = f ∘ E)",
    },
    {
        "name": "class_I_remove_hM",
        "description": "Remove `hM : M = f ∘ E` from `class_I_conditional_independence`",
        "old": "    (f : β → δ) (hf : Measurable f)\n    (hM : M = f ∘ E)",
        "new": "    (f : β → δ) (hf : Measurable f)\n",
    },
    {
        "name": "class_I_remove_hX_meas",
        "description": "Remove `hX_meas : Measurable X` from `class_I_conditional_independence`",
        "old": "    (hE_meas : Measurable E) (hX_meas : Measurable X) :\n    M ⟂ᵢ[E, hE_meas; μ] X := by",
        "new": "    (hE_meas : Measurable E) :\n    M ⟂ᵢ[E, hE_meas; μ] X := by",
    },
    {
        "name": "class_II_remove_hfuture_indep",
        "description": "Remove `hfuture_indep` from `class_II_conditional_independence`",
        "old": "    (hfuture_indep :\n      (fun ω => (E' ω, noise ω)) ⟂ᵢ[μ] (fun ω => (X ω, E ω, M ω)))",
        "new": "",
    },
]


def apply_probe(src_text: str, probe) -> str:
    if isinstance(probe["old"], re.Pattern):
        return probe["old"].sub(probe["new"], src_text)
    return src_text.replace(probe["old"], probe["new"], 1)


def main():
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")
    original = SRC.read_text()
    BACKUP.write_text(original)
    try:
        print("=" * 60)
        print("Premise-removal probes for PfLean/NullClassProofs.lean")
        print("=" * 60)
        for probe in PROBES:
            modified = apply_probe(original, probe)
            if modified == original:
                print(f"\n[SKIP] {probe['name']}: pattern did not match")
                continue
            SRC.write_text(modified)
            code, out = run_build()
            status = "BROKEN (expected)" if code != 0 else "STILL BUILDS (OVERCLAIM!)"
            print(f"\n--- {probe['name']} ---")
            print(f"Probe: {probe['description']}")
            print(f"Result: {status} (exit {code})")
            # Print first few lines of error if broken
            if code != 0:
                snippet = "\n".join(out.splitlines()[:20])
                print(snippet)
            else:
                print("WARNING: theorem still compiled after removing the premise.")
                print(out[:1000])
    finally:
        SRC.write_text(BACKUP.read_text())
        BACKUP.unlink(missing_ok=True)
        print("\nRestored original NullClassProofs.lean")


if __name__ == "__main__":
    main()
