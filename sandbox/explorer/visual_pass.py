"""
visual_pass.py -- PFExplorer visual render-health check.

Companion to `check_panel_health.py`. The static audit catches structural
bugs (unsized renderer, missing `this.resize`, unclamped `Math.exp`...).
This tool complements it by actually loading the live `index.html` in a
headless Chromium via Playwright and verifying that every registered
panel paints a non-background pixel on first mount.

Spec reference:
    `.kiro/specs/explorer-panel-render-health/` — Req 8 (live render
    verification before release) and Req 1.4 (non-background pixel in
    the canvas rectangle on first mount).

What it does
------------
For every panel id in `PANEL_IDS`:
  1. Navigate to the explorer via `PFExplorer.navigate('<id>')`
     (the router is hash-aware but only on first load, so we call the
     API directly inside `page.evaluate` for subsequent panels).
  2. Wait 500 ms for the first animation frame to paint.
  3. Measure the `#panelStage` bounding box and screenshot a 200x200
     block centered on the stage (or the stage itself if smaller).
  4. Load the PNG into a pixel array (Pillow) and compare every pixel
     to the page's body background colour. A panel PASSES if at least
     one sampled pixel is >5 away in max-channel distance. Otherwise
     FAIL ("blank canvas").

Output
------
One line per panel:
    OK   <panel_id>       rendered, N non-background pixels
    FAIL <panel_id>       blank — all sampled pixels within 5 of background
Exits 0 when every panel passes, 1 otherwise.
Exit 2 when Playwright is not installed, exit 3 when the server is
unreachable.

How to run
----------
Terminal 1:
    python sandbox/explorer/serve.py

Terminal 2:
    python sandbox/explorer/visual_pass.py
    # or, to also save screenshots per panel:
    python sandbox/explorer/visual_pass.py --screenshots out_screens
    # or to audit a subset:
    python sandbox/explorer/visual_pass.py --panels bohr,hub

Dependencies
------------
    pip install playwright pillow
    playwright install chromium

Assumptions
-----------
  * PFExplorer exposes `window.PFExplorer.navigate(id)` (it does as of
    `core.js` today).
  * The page body has a solid computed `background-color`. We read it
    via `window.getComputedStyle(document.body).backgroundColor` once
    at startup. If the body is transparent, we fall back to the
    `#panelStage` computed background and then finally to `#0a0a1a`
    (the theme colour declared in `index.html`).
  * Panels paint to a sibling DOM element inside `#panelStage` (div,
    canvas, svg). We do not reach into Three.js internals; we
    screenshot the composed frame as the user would see it.
"""
from __future__ import annotations

import argparse
import sys
import time
from io import BytesIO
from pathlib import Path
from typing import Sequence
from urllib.error import URLError
from urllib.request import urlopen


# The 17 panel ids currently registered in `sandbox/explorer/panels/*.js`.
# This list mirrors the sidebar (index.html) plus the overview routes
# ("observatory", "hub", "dashboard") that PFExplorer.registerPanel
# installs programmatically.
PANEL_IDS: tuple[str, ...] = (
    "observatory",
    "hub",
    "foundations",
    "god-equation",
    "koide",
    "weinberg",
    "refraction",
    "bohr",
    "generations",
    "consciousness",
    "koide-weinberg-bridge",
    "dashboard",
    "proof-atlas",
    "experiment-bench",
    "no-go-museum",
    "definition-lattice",
    "scale-ladder-panel",
)

# Used when the body background resolves to 'rgba(0,0,0,0)' / transparent.
THEME_FALLBACK_RGB = (0x0A, 0x0A, 0x1A)

# Pixel tolerance per requirement: "within 5 of the page's background colour".
BG_TOLERANCE = 5

# Centre sample block size (px, CSS).
SAMPLE_SIDE = 200

# Wait between navigate() and screenshot (ms) — matches the spec wording.
POST_NAV_WAIT_MS = 500


def parse_viewport(spec: str) -> tuple[int, int]:
    """`"1920x1080"` -> (1920, 1080). Raises on malformed input."""
    try:
        w_str, h_str = spec.lower().split("x", 1)
        w, h = int(w_str), int(h_str)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError(
            f"viewport must be WIDTHxHEIGHT (got {spec!r})"
        ) from exc
    if w < 320 or h < 240:
        raise argparse.ArgumentTypeError("viewport too small (minimum 320x240)")
    return w, h


def parse_rgb(css_colour: str) -> tuple[int, int, int]:
    """Parse a CSS `rgb(...)` or `rgba(...)` string into an (R,G,B) tuple.

    Alpha is ignored — we compare the rendered-on-page RGB.
    Returns the theme fallback if parsing fails or alpha is 0.
    """
    if not css_colour:
        return THEME_FALLBACK_RGB
    s = css_colour.strip().lower()
    if not (s.startswith("rgb(") or s.startswith("rgba(")):
        return THEME_FALLBACK_RGB
    inside = s[s.index("(") + 1 : s.rindex(")")]
    parts = [p.strip() for p in inside.split(",")]
    try:
        r = int(float(parts[0]))
        g = int(float(parts[1]))
        b = int(float(parts[2]))
        if len(parts) >= 4 and float(parts[3]) == 0.0:
            # Transparent → caller will fall back to the next layer.
            return THEME_FALLBACK_RGB
        return (r, g, b)
    except (ValueError, IndexError):
        return THEME_FALLBACK_RGB


def max_channel_distance(pixel: Sequence[int], bg: Sequence[int]) -> int:
    """L∞ distance between two RGB triples."""
    return max(
        abs(int(pixel[0]) - int(bg[0])),
        abs(int(pixel[1]) - int(bg[1])),
        abs(int(pixel[2]) - int(bg[2])),
    )


def probe_server(url: str, timeout: float = 3.0) -> None:
    """Raise on a non-reachable server. Used for the 'exit 3' path."""
    try:
        with urlopen(url, timeout=timeout) as resp:  # noqa: S310  (localhost)
            resp.read(64)
    except URLError as exc:
        raise ConnectionError(f"cannot reach {url}: {exc.reason}") from exc
    except OSError as exc:
        raise ConnectionError(f"cannot reach {url}: {exc}") from exc


def resolve_body_background(page) -> tuple[int, int, int]:
    """Best-effort page background: body → panelStage → theme fallback."""
    body_colour = page.evaluate(
        "() => window.getComputedStyle(document.body).backgroundColor"
    )
    rgb = parse_rgb(body_colour)
    if rgb != THEME_FALLBACK_RGB:
        return rgb
    # Body was transparent / default. Try the stage.
    stage_colour = page.evaluate(
        "() => {"
        "  const el = document.getElementById('panelStage');"
        "  return el ? window.getComputedStyle(el).backgroundColor : '';"
        "}"
    )
    return parse_rgb(stage_colour)


def screenshot_panel_centre(page, side: int) -> bytes:
    """Screenshot a `side`x`side` CSS-pixel block at the stage centre.

    Returns PNG bytes. If the stage is smaller than `side`, clip to the
    whole stage rectangle.
    """
    box = page.evaluate(
        "() => {"
        "  const el = document.getElementById('panelStage');"
        "  if (!el) return null;"
        "  const r = el.getBoundingClientRect();"
        "  return {x: r.left, y: r.top, w: r.width, h: r.height};"
        "}"
    )
    if not box or box["w"] < 2 or box["h"] < 2:
        raise RuntimeError("#panelStage missing or has zero size")

    w = min(side, int(box["w"]))
    h = min(side, int(box["h"]))
    cx = box["x"] + box["w"] / 2.0
    cy = box["y"] + box["h"] / 2.0
    clip = {
        "x": max(0.0, cx - w / 2.0),
        "y": max(0.0, cy - h / 2.0),
        "width": float(w),
        "height": float(h),
    }
    return page.screenshot(clip=clip, type="png")


def count_non_background(png_bytes: bytes, bg: tuple[int, int, int]) -> int:
    """Count pixels whose max-channel distance from `bg` exceeds the tolerance."""
    from PIL import Image  # Deferred so the --panels parse path doesn't need PIL.

    img = Image.open(BytesIO(png_bytes)).convert("RGB")
    hits = 0
    for pixel in img.getdata():
        if max_channel_distance(pixel, bg) > BG_TOLERANCE:
            hits += 1
    return hits


def navigate_to(page, panel_id: str) -> None:
    """Drive PFExplorer.navigate() for a panel. Waits for the renderer to mount.

    Raises RuntimeError if PFExplorer silently falls back to another route
    (core.js does this when a panel id is not registered: it logs a warning
    and boots the observatory instead). Without this check the visual pass
    reports a false PASS — the observatory frame is painted, but the
    requested panel never mounted.

    Also forwards any uncaught exception thrown inside `panel.mount()` so
    it becomes a FAIL for that panel rather than a silent misreport.
    """
    result = page.evaluate(
        """(id) => {
            if (!window.PFExplorer || typeof window.PFExplorer.navigate !== 'function') {
                return { ok: false, err: 'window.PFExplorer.navigate is not available' };
            }
            try {
                window.PFExplorer.navigate(id);
            } catch (e) {
                return { ok: false, err: 'mount() threw: ' + (e && e.message ? e.message : String(e)) };
            }
            const actual = (window.PFExplorer.getContext && window.PFExplorer.getContext().state)
                ? window.PFExplorer.getContext().state.currentRoute
                : null;
            if (actual !== id) {
                return {
                    ok: false,
                    err: "PFExplorer.navigate('" + id + "') silently fell back to '" + actual + "' (route not registered or init failed)",
                };
            }
            return { ok: true, route: actual };
        }""",
        panel_id,
    )
    if not result.get("ok"):
        raise RuntimeError(result.get("err") or "unknown navigate failure")
    page.wait_for_timeout(POST_NAV_WAIT_MS)


def audit_panel(page, panel_id: str, bg: tuple[int, int, int],
                screenshots_dir: Path | None) -> tuple[bool, str]:
    """Return (ok, detail) for a single panel."""
    try:
        navigate_to(page, panel_id)
    except Exception as exc:  # noqa: BLE001  (surface any nav error)
        return False, f"navigate() threw: {exc}"

    try:
        png = screenshot_panel_centre(page, SAMPLE_SIDE)
    except Exception as exc:  # noqa: BLE001
        return False, f"screenshot failed: {exc}"

    if screenshots_dir is not None:
        try:
            out = screenshots_dir / f"{panel_id}.png"
            out.write_bytes(png)
        except OSError as exc:
            return False, f"couldn't write screenshot: {exc}"

    try:
        non_bg = count_non_background(png, bg)
    except Exception as exc:  # noqa: BLE001
        return False, f"pixel scan failed: {exc}"

    if non_bg == 0:
        return False, (
            f"blank — all sampled pixels within {BG_TOLERANCE} of background "
            f"rgb{bg}"
        )
    return True, f"rendered, {non_bg} non-background pixel(s)"


def run_audit(args: argparse.Namespace) -> int:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        print(
            "Playwright is not installed. Install it with:\n"
            "    pip install playwright\n"
            "    playwright install chromium",
            file=sys.stderr,
        )
        return 2
    # Pillow import is deferred into count_non_background; we still want a
    # clean error message if it's absent, so probe it now.
    try:
        import PIL  # noqa: F401, PLC0415
    except ImportError:
        print(
            "Pillow is not installed. Install it with:\n    pip install pillow",
            file=sys.stderr,
        )
        return 2

    try:
        probe_server(args.server)
    except ConnectionError as exc:
        print(f"Server not reachable: {exc}", file=sys.stderr)
        print(
            "Start it first with:\n    python sandbox/explorer/serve.py",
            file=sys.stderr,
        )
        return 3

    panels_to_audit = args.panels or list(PANEL_IDS)
    viewport_w, viewport_h = args.viewport

    screenshots_dir: Path | None = None
    if args.screenshots:
        screenshots_dir = Path(args.screenshots).resolve()
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        print(f"Screenshots -> {screenshots_dir}")

    print(
        f"Auditing {len(panels_to_audit)} panel(s) at {args.server} "
        f"({viewport_w}x{viewport_h})..."
    )
    t0 = time.monotonic()

    failures: list[tuple[str, str]] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": viewport_w, "height": viewport_h},
                device_scale_factor=1,
            )
            page = context.new_page()
            # Route the first load through the initial hash so PFExplorer
            # boots into a known panel before we start driving navigate().
            page.goto(args.server + "#observatory", wait_until="load")
            # Give core.js a beat to register panels and run initial mount.
            page.wait_for_function(
                "() => !!(window.PFExplorer && typeof window.PFExplorer.navigate === 'function')",
                timeout=10_000,
            )
            page.wait_for_timeout(POST_NAV_WAIT_MS)

            bg = resolve_body_background(page)
            print(f"Background colour (RGB) = {bg}")

            for panel_id in panels_to_audit:
                ok, detail = audit_panel(page, panel_id, bg, screenshots_dir)
                marker = "OK  " if ok else "FAIL"
                print(f"  {marker} {panel_id:<24} {detail}")
                if not ok:
                    failures.append((panel_id, detail))
        finally:
            browser.close()

    elapsed = time.monotonic() - t0
    print(f"\nDone in {elapsed:.1f}s. {len(panels_to_audit) - len(failures)}"
          f"/{len(panels_to_audit)} panel(s) clean.")
    if failures:
        print("Failing panels:")
        for pid, detail in failures:
            print(f"  - {pid}: {detail}")
        return 1
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Visual render-health pass for PFExplorer panels.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--server",
        default="http://localhost:8080/index.html",
        help="Explorer URL (default: %(default)s)",
    )
    p.add_argument(
        "--screenshots",
        metavar="DIR",
        default=None,
        help="Optional: save one PNG per panel into DIR",
    )
    p.add_argument(
        "--viewport",
        type=parse_viewport,
        default=(1920, 1080),
        metavar="WxH",
        help="Viewport in CSS pixels (default: 1920x1080)",
    )
    p.add_argument(
        "--panels",
        type=lambda s: [p.strip() for p in s.split(",") if p.strip()],
        default=None,
        metavar="ID,ID,...",
        help=(
            "Comma-separated list of panel ids to audit. "
            "Default: all 17 registered panels."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    return run_audit(args)


if __name__ == "__main__":
    sys.exit(main())
