"""
Panel health audit for PFExplorer.

Checks each file in `panels/` for the concrete failure modes that make
Three.js canvases render blank or at postage-stamp size:

    1. WebGLRenderer created but `setSize()` never called before the
       first animation frame (300x150 default = tiny unused buffer).
    2. Renderer created inside a helper but no `this.resize(ctx)` /
       equivalent call after the helper returns (so initial dimensions
       never sync to the DOM).
    3. EffectComposer created without `composer.setSize()` (same class
       of bug at the post-processing layer).
    4. PerspectiveCamera created with hard-coded aspect=1 and then
       never updated (stretched output).
    5. Math/geometry failure modes that clamp the visible region to a
       single point (exp blowup, divide-by-zero).

This audit is read-only. It prints one row per panel with verdicts.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


PANEL_DIR = Path(__file__).resolve().parent / "panels"
FIXTURE_DIR = Path(__file__).resolve().parent / "_audit_fixtures"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_renderer_sized(src: str) -> tuple[bool, str]:
    """True if every WebGLRenderer() construction has a reachable setSize.

    File-scope presence check: a panel is OK if both `new THREE.WebGLRenderer`
    and `renderer.setSize(` appear in the file. Three.js renderer wrappers
    routinely put the `setSize` call inside a sibling `resize()` method, so
    a narrow-window scan produced false positives on healthy panels
    (koide.js is the canonical example).

    If the renderer is constructed but no `setSize` appears anywhere, that is
    the real bug — the 300x150 default drawing buffer will ship.
    """
    if "new THREE.WebGLRenderer" not in src:
        return True, "no WebGL renderer (ok: 2D / no-Three panel)"
    has_set_size = bool(re.search(r"\brenderer\.setSize\(", src))
    if not has_set_size:
        # Find the line the renderer lives on for reporting.
        for i, line in enumerate(src.splitlines(), start=1):
            if "new THREE.WebGLRenderer" in line:
                return False, f"renderer at line {i} — no renderer.setSize() anywhere in the file"
        return False, "renderer constructed but no setSize anywhere"
    return True, "setSize present in file"


def check_resize_wired(src: str) -> tuple[bool, str]:
    """True if the mount/renderInfo path calls this.resize() after build.

    Panels that never trigger a resize after DOM layout stay stuck at
    whatever initial size the renderer had. We consider it wired if
    we find `this.resize(` or `self.resize(` anywhere in the file.
    """
    # No renderer = no need to resize.
    if "WebGLRenderer" not in src:
        return True, "no Three.js renderer"
    has_call = bool(re.search(r"\b(?:this|self)\.resize\(", src))
    has_resize_method = bool(re.search(r"resize:\s*function", src))
    if not has_resize_method:
        return False, "no resize() method defined"
    if not has_call:
        return False, "resize() defined but never invoked from mount path"
    return True, "resize method + post-mount call"


def check_composer_sized(src: str) -> tuple[bool, str]:
    """True if every EffectComposer gets a setSize call somewhere."""
    if "EffectComposer" not in src:
        return True, "no post-processing composer"
    # Any `composer.setSize(` anywhere in the file is enough; the resize
    # handler usually re-applies it on window resize.
    if re.search(r"\bcomposer\.setSize\(", src):
        return True, "composer.setSize present"
    return False, "composer created but setSize never called"


def check_camera_aspect(src: str) -> tuple[bool, str]:
    """Flag hard-coded PerspectiveCamera aspect=1 with no later update.

    The canonical bug: `new THREE.PerspectiveCamera(fov, 1, ...)` and
    then nothing touches `.aspect` again. Result: stretched / squashed.
    """
    cam_matches = re.findall(
        r"new THREE\.PerspectiveCamera\(([^)]+)\)", src
    )
    if not cam_matches:
        return True, "no perspective camera"
    has_update = bool(re.search(r"\.updateProjectionMatrix\(", src))
    hard_one = [m for m in cam_matches if re.search(r",\s*1\s*,", m)]
    if hard_one and not has_update:
        return False, f"{len(hard_one)} camera(s) with aspect=1 and no updateProjectionMatrix"
    return True, f"{len(cam_matches)} camera(s), aspect handled"


def check_exp_blowup(src: str) -> tuple[bool, str]:
    """Crude check for uncapped Math.exp in geometry loops.

    Rules for flagging:
        - `Math.exp(X)` where X is a user-derived expression that could grow.
        - Skip bounded negative-exponent forms: the argument begins with a
          literal `-` (i.e. `-Math.abs(`, `-(`, `-t`, etc.). These are
          bounded above by 1 and never blow up.
        - Skip calls whose argument contains a clamp idiom
          (`Math.min(`, `Math.max(`, `clamp`) within 3 lines of the call.

    Not definitive — legitimate uses still exist — so this remains a
    warning-severity check.
    """
    if "Math.exp(" not in src:
        return True, "no Math.exp"
    lines = src.splitlines()
    risky = []
    for i, line in enumerate(lines):
        for m in re.finditer(r"Math\.exp\(\s*(.*?)\)", line):
            arg = m.group(1).lstrip()
            # Bounded by construction: negative exponent.
            if arg.startswith("-"):
                continue
            # Clamped within an 8-line window (before or after). Wide enough
            # to catch `if (delta > N) return ...` guards a few lines above
            # a subsequent Math.exp call, narrow enough that a clamp in a
            # completely different function does not accidentally cover for
            # an unclamped call elsewhere.
            window = "\n".join(lines[max(0, i - 8) : i + 9])
            if re.search(r"Math\.(?:min|max)|clamp|if\s*\(.*?>\s*\d|if\s*\(.*?<\s*-?\d", window):
                continue
            risky.append(i + 1)
    if risky:
        return False, f"Math.exp at line(s) {', '.join(map(str, risky))} may overflow (no nearby clamp)"
    return True, "all Math.exp calls are bounded or clamped"


def check_points_size(src: str) -> tuple[bool, str]:
    """PointsMaterial with no `sizeAttenuation:false` and tiny `size`.

    Tiny screen-space points show up as single pixels that look like
    nothing. Not definitive; informational.
    """
    if "PointsMaterial" not in src:
        return True, "no Points material"
    if re.search(r"size:\s*0?\.0[0-5]", src):
        return False, "PointsMaterial size < 0.06 (may be invisible)"
    return True, "points sized ok"


CHECKS = [
    ("renderer_sized", check_renderer_sized),
    ("resize_wired", check_resize_wired),
    ("composer_sized", check_composer_sized),
    ("camera_aspect", check_camera_aspect),
    ("exp_blowup", check_exp_blowup),
    ("points_size", check_points_size),
]


def audit_panel(path: Path) -> dict:
    src = read(path)
    results = {}
    for name, fn in CHECKS:
        ok, detail = fn(src)
        results[name] = (ok, detail)
    return results


def main() -> int:
    # Simple arg handling: `--self-test` runs the fixture harness instead
    # of the panel audit. Everything else falls through to the audit.
    args = sys.argv[1:]
    if "--self-test" in args:
        return run_self_test()

    panels = sorted(p for p in PANEL_DIR.glob("*.js"))
    print(f"Auditing {len(panels)} panels...\n")

    any_fail = False
    for panel in panels:
        results = audit_panel(panel)
        fails = [(n, d) for n, (ok, d) in results.items() if not ok]
        status = "OK" if not fails else "FAIL"
        marker = "   " if not fails else ">> "
        print(f"{marker}{panel.name}: {status}")
        if fails:
            any_fail = True
            for name, detail in fails:
                print(f"      [{name}] {detail}")
    print()
    print("Summary:", "all panels clean" if not any_fail else "failures found above")
    return 1 if any_fail else 0


def run_self_test() -> int:
    """Run each check against hand-crafted pass/fail fixtures.

    For each registered check `<name>`, the harness expects two fixtures:

        _audit_fixtures/<name>_pass.js   -> check must return True
        _audit_fixtures/<name>_fail.js   -> check must return False

    Any missing fixture or any mismatch is a harness failure.
    Exits 0 on full pass, 1 otherwise. Normal panel-audit mode is untouched.
    """
    print(f"Self-test: fixtures in {FIXTURE_DIR}\n")
    if not FIXTURE_DIR.is_dir():
        print(f"FAIL: fixture directory does not exist: {FIXTURE_DIR}")
        return 1

    failures: list[str] = []
    total = 0
    for check_name, fn in CHECKS:
        for expected, suffix in ((True, "pass"), (False, "fail")):
            total += 1
            fixture = FIXTURE_DIR / f"{check_name}_{suffix}.js"
            if not fixture.is_file():
                msg = f"[{check_name}] missing fixture: {fixture.name}"
                print(f">> {msg}")
                failures.append(msg)
                continue
            src = read(fixture)
            ok, detail = fn(src)
            if ok is expected:
                print(f"   OK   [{check_name}_{suffix}] -> {ok} ({detail})")
            else:
                msg = (
                    f"[{check_name}_{suffix}] expected {expected}, got {ok} "
                    f"({detail})"
                )
                print(f">> FAIL {msg}")
                failures.append(msg)

    print()
    passed = total - len(failures)
    print(f"Self-test summary: {passed}/{total} assertions held")
    if failures:
        print("Failures:")
        for msg in failures:
            print(f"  - {msg}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
