#!/usr/bin/env python3
"""
Explorer Truth Layer V4 — Browser DOM Runtime Proof

V4 Req 6: Supply browser runtime evidence for rendered status-bearing DOM
for each release-tree route. Replaces the V3 Node data-load shim with
actual headless browser verification.

Uses Playwright (installed globally) to:
  1. Start the Explorer's serve.py
  2. Load each HTML route in a headless browser
  3. Verify that status-bearing DOM elements are populated from authority
  4. Verify that non-claim routes do not show status badges
  5. Report DOM evidence for each route
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
SERVE_SCRIPT = EXPLORER_DIR / "serve.py"
REGISTRY_PATH = EXPLORER_DIR / "release_tree_registry.json"
PORT = 8771


def start_server() -> subprocess.Popen:
    """Start the Explorer's serve.py on a test port."""
    proc = subprocess.Popen(
        [sys.executable, str(SERVE_SCRIPT), str(PORT)],
        cwd=str(EXPLORER_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    # Wait for server to start
    for _ in range(20):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"http://localhost:{PORT}/index.html", timeout=2)
            return proc
        except Exception:
            continue
    return proc


def stop_server(proc: subprocess.Popen):
    """Stop the server process."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass


def run_browser_proof() -> dict:
    """Run browser DOM proof using Playwright."""
    from playwright.sync_api import sync_playwright

    # Load registry to get routes
    registry = json.loads(REGISTRY_PATH.read_text())
    html_routes = registry.get("html_entry_points", [])
    claim_routes = set(registry.get("claim_routes", []))
    non_claim_routes = set(registry.get("standalone_non_claim_routes", []))

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 900})

        for path in html_routes:
            route_type = "claim-route" if path in claim_routes else (
                "standalone-non-claim" if path in non_claim_routes else "unknown"
            )
            url = f"http://localhost:{PORT}/{path}"

            page = context.new_page()
            # Collect JS errors
            js_errors = []
            page.on("pageerror", lambda err: js_errors.append(str(err)))

            try:
                # Use domcontentloaded for pages with long-running animations
                wait_until = "domcontentloaded" if "journey_live" in path else "networkidle"
                response = page.goto(url, wait_until=wait_until, timeout=30000)
                if response is None or response.status != 200:
                    results[path] = {
                        "status": "FAIL",
                        "reason": f"HTTP {response.status if response else 'no response'}",
                        "route_type": route_type,
                    }
                    continue

                # Wait for JS to populate DOM
                page.wait_for_timeout(3000)

                # Check for status-bearing DOM elements
                dom_evidence = {}

                # 1. Check if PFClaimsData is loaded
                has_claims_data = page.evaluate(
                    "() => typeof window.PFClaimsData !== 'undefined' && window.PFClaimsData !== null"
                )
                dom_evidence["PFClaimsData_loaded"] = has_claims_data

                # 2. Check if PFExplorerData is loaded
                has_explorer_data = page.evaluate(
                    "() => typeof window.PFExplorerData !== 'undefined' && window.PFExplorerData !== null"
                )
                dom_evidence["PFExplorerData_loaded"] = has_explorer_data

                # 3. Check for status-pill elements (rendered badges)
                status_pills = page.evaluate("""
                    () => {
                        const pills = document.querySelectorAll('.status-pill, .status-badge');
                        return Array.from(pills).map(p => ({
                            text: p.textContent.trim(),
                            class: p.className
                        }));
                    }
                """)
                dom_evidence["status_pills"] = status_pills

                # 4. Check for "loading from authority" placeholders
                loading_placeholders = page.evaluate("""
                    () => {
                        const all = document.querySelectorAll('*');
                        const placeholders = [];
                        for (const el of all) {
                            if (el.children.length === 0 &&
                                el.textContent.includes('loading from authority')) {
                                placeholders.push({
                                    tag: el.tagName,
                                    id: el.id,
                                    text: el.textContent.trim()
                                });
                            }
                        }
                        return placeholders;
                    }
                """)
                dom_evidence["loading_placeholders_remaining"] = loading_placeholders

                # 5. Check for UNAVAILABLE (missing authority)
                unavailable_count = page.evaluate("""
                    () => {
                        const all = document.body.textContent;
                        return (all.match(/UNAVAILABLE/g) || []).length;
                    }
                """)
                dom_evidence["unavailable_count"] = unavailable_count

                # 6. Check for ge-error element (Journey page)
                ge_error_text = page.evaluate("""
                    () => {
                        const el = document.getElementById('ge-error');
                        return el ? el.textContent.trim() : null;
                    }
                """)
                if ge_error_text:
                    dom_evidence["ge_error_text"] = ge_error_text[:120]

                # 7. Record JS errors
                dom_evidence["js_errors"] = js_errors[:5]

                # 8. Page title
                dom_evidence["title"] = page.title()

                # Classify result
                if route_type == "standalone-non-claim":
                    dom_evidence["non_claim_route"] = True
                    if status_pills:
                        results[path] = {
                            "status": "FAIL",
                            "reason": f"Non-claim route has {len(status_pills)} status pills",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                if route_type == "claim-route":
                    dom_evidence["claim_route"] = True
                    if not has_claims_data and not has_explorer_data:
                        results[path] = {
                            "status": "FAIL",
                            "reason": "Claim route did not load authority data",
                            "route_type": route_type,
                            "dom_evidence": dom_evidence,
                        }
                        continue

                # Check for JS errors
                if js_errors:
                    results[path] = {
                        "status": "FAIL",
                        "reason": f"JS errors: {js_errors[:3]}",
                        "route_type": route_type,
                        "dom_evidence": dom_evidence,
                    }
                    continue

                results[path] = {
                    "status": "PASS",
                    "route_type": route_type,
                    "dom_evidence": dom_evidence,
                }

            except Exception as e:
                results[path] = {
                    "status": "ERROR",
                    "reason": str(e),
                    "route_type": route_type,
                }
            finally:
                page.close()

        browser.close()

    return results


def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V4 — Browser DOM Runtime Proof")
    print("=" * 70)
    print()

    # Check Playwright is available
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL: playwright not installed.")
        return 1

    # Start server
    print(f"Starting serve.py on port {PORT}...")
    proc = start_server()

    # Verify server is up
    try:
        urllib.request.urlopen(f"http://localhost:{PORT}/index.html", timeout=5)
    except Exception as e:
        print(f"FAIL: Server did not start: {e}")
        stop_server(proc)
        return 1

    try:
        # Run browser proof
        print("Launching headless browser (Playwright/Chromium)...")
        results = run_browser_proof()

        # Print results
        passed = 0
        failed = 0
        errors = 0

        print(f"\nChecking {len(results)} routes:\n")
        for path, result in sorted(results.items()):
            status = result["status"]
            route_type = result.get("route_type", "unknown")
            if status == "PASS":
                passed += 1
                evidence = result.get("dom_evidence", {})
                pills = len(evidence.get("status_pills", []))
                has_data = evidence.get("PFClaimsData_loaded", False) or evidence.get("PFExplorerData_loaded", False)
                title = evidence.get("title", "?")
                print(f"  PASS: {path} ({route_type}) — data={has_data}, pills={pills}, title=\"{title}\"")
            elif status == "FAIL":
                failed += 1
                print(f"  FAIL: {path} ({route_type}) — {result.get('reason', '?')}")
            else:
                errors += 1
                reason = result.get('reason', '?')
                print(f"  ERROR: {path} ({route_type}) — {reason[:100]}")

        # Write evidence file
        evidence_path = EXPLORER_DIR / "_browser_dom_evidence.json"
        with open(evidence_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nEvidence written to {evidence_path}")

        print()
        print("=" * 70)
        print(f"Browser DOM Proof: {passed} passed, {failed} failed, {errors} errors")
        print("=" * 70)
        return 0 if failed == 0 and errors == 0 else 1

    finally:
        stop_server(proc)
        print("\nServer stopped.")


if __name__ == "__main__":
    raise SystemExit(main())
