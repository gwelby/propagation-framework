#!/usr/bin/env python3
"""Writer-level copied-candidate fixtures for D1 and D3.

Per Codex 2026-07-20 formula-readiness scanner repair contract:
- Copy the candidate writer to a temporary file.
- Inject a contrast sentence into an emitted user-facing field.
- Assert the writer exits nonzero before publication.
- Assert the original output artifact remains unchanged.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

def _hash_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _run_writer_fixture(name: str, script_src: Path, output_json: Path,
                        trap_field: str, trap_text: str) -> None:
    """Run one writer-level copied-candidate fixture."""
    original_hash = _hash_file(output_json) if output_json.is_file() else None

    tmpdir = Path(tempfile.mkdtemp(prefix=f"{name}_writer_trap_"))
    try:
        # Copy candidate to temp dir
        tmp_script = tmpdir / script_src.name
        shutil.copy2(script_src, tmp_script)

        # Read the copied source and inject the trap sentence
        source = tmp_script.read_text(encoding="utf-8")
        # Find the scan_artifact call and inject the trap just before it
        # We inject into the output dict by inserting a line before _scan_artifact call.
        scan_call = "art_violations = _scan_artifact("
        assert scan_call in source, f"Could not find _scan_artifact call in {script_src.name}"
        injection = (
            f"    # LANGUAGE TRAP INJECTION for copied-candidate fixture\n"
            f"    {trap_field} += {trap_text!r}\n"
        )
        new_source = source.replace(scan_call, injection + scan_call, 1)
        tmp_script.write_text(new_source, encoding="utf-8")

        # Run the copied candidate
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, str(tmp_script)],
            cwd=str(tmpdir),
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print(f"FAIL {name}: copied candidate should have exited nonzero")
            print(result.stdout[-500:])
            print(result.stderr[-500:])
            raise SystemExit(1)

        # Verify the original artifact is unchanged
        if original_hash is not None:
            after_hash = _hash_file(output_json)
            if after_hash != original_hash:
                print(f"FAIL {name}: original artifact changed: {output_json}")
                raise SystemExit(1)

        print(f"PASS {name}: writer exited {result.returncode}, original {output_json.name} unchanged")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main() -> int:
    print("=== D-Series Writer-Level Copied-Candidate Fixtures ===")
    print()

    _run_writer_fixture(
        "D1",
        ROOT / "quark_masses" / "d1_fit_v4.py",
        ROOT / "quark_masses" / "d1_v4_4_results.json",
        'output["claim_boundary"]',
        " This is not a statistical test, but it makes a falsification claim.",
    )

    _run_writer_fixture(
        "D3",
        ROOT / "ckm_mixing" / "d3_ckm_scan_v3_1.py",
        ROOT / "ckm_mixing" / "d3_v3_1_results.json",
        'output["claim_boundary"]',
        " No statistical test is claimed, but this is a compatibility verdict.",
    )

    print()
    print("All writer-level copied-candidate fixtures passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
