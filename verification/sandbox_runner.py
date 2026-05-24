"""Subprocess runner for sandbox scripts.

Sandbox scripts live under ``sandbox/`` and produce numerical outputs
that the verification runners use as local evidence. This module runs
one such script as a subprocess, captures stdout/stderr, parses the
structured numerical outputs (JSON blobs) when present, and always
returns a :class:`SandboxRunResult` — never raises for a broken script.

Safety posture
--------------

* The subprocess is started in a temporary working directory (created
  via :func:`tempfile.mkdtemp`) unless an explicit ``cwd`` is supplied.
  That insulates the host workspace from sandbox scripts that write
  artifacts next to their cwd.
* The environment variable ``PF_READONLY_BOARDS=1`` is set so that
  cooperating scripts can self-check and refuse to touch board
  documents.
* The ``PYTHONHASHSEED`` and ``PF_SEED`` environment variables are set
  from the caller's ``seed`` argument when one is given, so scripts
  that honor them produce deterministic output.

This module does **not** install OS-level filesystem ACLs or
chroot-style sandboxing — a sandbox script that insists on writing to
``derivations/`` or ``CLAIMS.md`` will succeed at the OS level. Catching
that kind of bug is the guardrail enforcer's job (see Req. 6 and the
Component 4 design); the runner's job is to run scripts and report what
happened. See the TODO below for future hardening.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md`
  Req. 8 (sandbox execution), Req. 3.4 (broken script → SCRIPT_BROKEN,
  never a falsification).
- `.kiro/specs/propagation-framework-verification/design.md`
  Algorithm 2 (derived-claim runner calls ``run_sandbox_script``).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# TODO(verification/hardening): wrap the subprocess in a real sandbox.
# Candidate approaches, in rough order of portability:
#   - Linux: firejail/bubblewrap with --tmpfs on Board_Documents paths.
#   - macOS: sandbox-exec with a deny-write profile on Board_Documents.
#   - Windows: AppContainer / Job Object with file-system capability
#     restrictions.
# The Python-only fallback below (temp cwd + env var) is intentionally
# coarse and relies on scripts cooperating.


@dataclass
class SandboxRunResult:
    """Structured result from :func:`run_sandbox_script`.

    Attributes:
        script_path: The script that was executed, as a string.
        success: True iff the subprocess exited cleanly with return
            code 0 *and* no pre-exec exception fired.
        stdout: Captured stdout (full text).
        stderr: Captured stderr (full text).
        return_code: Subprocess exit code. ``-1`` when the runner
            caught an exception before/around the subprocess (timeout,
            file-not-found, etc.).
        error: Exception class name when a runtime error was caught;
            empty string on clean runs.
        parsed_output: Parsed JSON object recovered from stdout when
            the script emits one. See :func:`_extract_json_blob`.
    """

    script_path: str
    success: bool
    stdout: str
    stderr: str
    return_code: int
    error: str = ""
    parsed_output: dict[str, Any] = field(default_factory=dict)


def run_sandbox_script(
    script_path: str | Path,
    seed: int | None = None,
    timeout: float = 300.0,
    cwd: str | Path | None = None,
) -> SandboxRunResult:
    """Execute a sandbox script as a subprocess and capture its output.

    Args:
        script_path: Path to the Python script to run. The script is
            invoked with the current Python interpreter
            (``sys.executable``).
        seed: Optional integer seed. When provided, it is written to
            ``PF_SEED`` and ``PYTHONHASHSEED`` in the subprocess
            environment so cooperating scripts can produce deterministic
            output.
        timeout: Wall-clock timeout in seconds. On timeout the
            subprocess is terminated and a :class:`SandboxRunResult`
            with ``success=False`` / ``error="TimeoutExpired"`` is
            returned.
        cwd: Working directory for the subprocess. If ``None``, a
            fresh :func:`tempfile.mkdtemp` directory is used and
            removed after the run.

    Returns:
        A :class:`SandboxRunResult`. Broken/missing scripts, runtime
        crashes, and timeouts all return ``success=False`` with the
        caught exception's class name in ``error`` — they never raise.
    """

    script = Path(script_path)
    own_tempdir: str | None = None
    env = os.environ.copy()
    env["PF_READONLY_BOARDS"] = "1"
    if seed is not None:
        env["PF_SEED"] = str(seed)
        env["PYTHONHASHSEED"] = str(seed)

    if cwd is None:
        own_tempdir = tempfile.mkdtemp(prefix="pf_sandbox_")
        run_cwd = own_tempdir
    else:
        run_cwd = str(cwd)

    try:
        if not script.is_file():
            return SandboxRunResult(
                script_path=str(script),
                success=False,
                stdout="",
                stderr=f"script not found: {script}",
                return_code=-1,
                error="FileNotFoundError",
            )

        try:
            completed = subprocess.run(
                [sys.executable, str(script.resolve())],
                cwd=run_cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return SandboxRunResult(
                script_path=str(script),
                success=False,
                stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + f"\n[timeout after {timeout}s]",
                return_code=-1,
                error="TimeoutExpired",
            )
        except Exception as exc:  # pragma: no cover - truly unexpected
            return SandboxRunResult(
                script_path=str(script),
                success=False,
                stdout="",
                stderr=f"{type(exc).__name__}: {exc}",
                return_code=-1,
                error=type(exc).__name__,
            )

        parsed = _extract_json_blob(completed.stdout)
        return SandboxRunResult(
            script_path=str(script),
            success=completed.returncode == 0,
            stdout=completed.stdout,
            stderr=completed.stderr,
            return_code=completed.returncode,
            error="" if completed.returncode == 0 else "NonZeroExit",
            parsed_output=parsed,
        )
    finally:
        if own_tempdir is not None:
            shutil.rmtree(own_tempdir, ignore_errors=True)


def _extract_json_blob(stdout: str) -> dict[str, Any]:
    """Best-effort JSON recovery from a script's stdout.

    Strategy:

        1. Try to parse the entire stdout as JSON.
        2. If that fails, scan for the last top-level ``{...}`` block
           (balanced braces, single-line or multi-line) and parse it.

    Returns an empty dict on failure. Non-dict JSON values (lists,
    scalars) are wrapped as ``{"value": <parsed>}`` for uniform access.
    """

    text = stdout.strip()
    if not text:
        return {}

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = _find_last_json_object(text)
        if value is None:
            return {}

    if isinstance(value, dict):
        return value
    return {"value": value}


def _find_last_json_object(text: str) -> Any | None:
    """Return the last top-level ``{...}`` JSON object parsed from ``text``.

    Walks the string tracking brace depth and string-literal state. When
    a ``{`` at depth 0 is seen we record the start index; the matching
    ``}`` at depth 0 closes the candidate. The last successfully parsed
    candidate wins. Returns ``None`` if no valid object is found.
    """

    depth = 0
    start: int | None = None
    in_string = False
    escape = False
    best: Any | None = None
    for idx, ch in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            if depth == 0:
                start = idx
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    candidate = text[start : idx + 1]
                    try:
                        best = json.loads(candidate)
                    except json.JSONDecodeError:
                        pass
                    start = None
    return best
