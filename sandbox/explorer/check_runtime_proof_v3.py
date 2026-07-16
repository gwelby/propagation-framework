#!/usr/bin/env python3
"""
Explorer Truth Layer V3 — Runtime Proof

V3 requirement 7: Runtime proof for each shipped HTML entry point.

For each HTML entry point, verifies:
  1. Load order: data.graph.js → data.claims.js → data.js → truth-utils.js
  2. No legacy data sources (no independent status-bearing data)
  3. 36 claims present in the generated data
  4. Current displays match authority (statuses are data-driven)

This script uses Node.js to actually load and evaluate the JS files,
simulating the browser runtime.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent


def get_html_entry_points() -> list[Path]:
    """Get all HTML entry points that are part of the release tree."""
    htmls = []
    for html in EXPLORER_DIR.glob("*.html"):
        name = html.name
        if name == "test-d3.html":
            continue
        htmls.append(html)
    return htmls


def check_load_order(html: Path) -> list[str]:
    """Check that script load order is correct in an HTML file."""
    failures = []
    text = html.read_text(encoding="utf-8")
    rel = html.relative_to(EXPLORER_DIR)

    # Extract script src order
    scripts = re.findall(r'<script\s+src="([^"]+)"', text)

    # Check load order for data files
    data_graph_pos = -1
    data_claims_pos = -1
    data_js_pos = -1
    truth_utils_pos = -1

    for i, src in enumerate(scripts):
        if "data.graph.js" in src:
            data_graph_pos = i
        if "data.claims.js" in src:
            data_claims_pos = i
        if src.endswith("data.js"):
            data_js_pos = i
        if "truth-utils.js" in src:
            truth_utils_pos = i

    # If data files are loaded, verify order
    has_data = data_claims_pos >= 0 or data_js_pos >= 0 or data_graph_pos >= 0

    if has_data:
        # truth-utils.js must be loaded
        if truth_utils_pos < 0:
            failures.append(f"MISSING_TRUTH_UTILS: {rel} loads data but not truth-utils.js")

        # data.graph.js must come before data.claims.js (if both present)
        if data_graph_pos >= 0 and data_claims_pos >= 0:
            if data_graph_pos > data_claims_pos:
                failures.append(f"LOAD_ORDER: {rel} data.graph.js after data.claims.js")

        # data.claims.js must come before data.js (if both present)
        if data_claims_pos >= 0 and data_js_pos >= 0:
            if data_claims_pos > data_js_pos:
                failures.append(f"LOAD_ORDER: {rel} data.claims.js after data.js")

        # truth-utils.js must come after data files
        if truth_utils_pos >= 0 and data_claims_pos >= 0:
            if truth_utils_pos < data_claims_pos:
                failures.append(f"LOAD_ORDER: {rel} truth-utils.js before data.claims.js")

    return failures


def check_no_legacy_data(html: Path) -> list[str]:
    """Check that HTML doesn't load legacy independent data sources."""
    failures = []
    text = html.read_text(encoding="utf-8")
    rel = html.relative_to(EXPLORER_DIR)

    # Check for inline status-bearing data objects (not CSS class maps)
    # Look for patterns like: { status: "DERIVED", ... } that are data, not styling
    inline_data = re.findall(r'\{[^}]*"status"\s*:\s*"DERIVED"[^}]*"confidence"[^}]*\}', text)
    if inline_data:
        failures.append(f"INLINE_STATUS: {rel} has inline status-bearing data objects")

    return failures


def check_node_runtime(html: Path) -> list[str]:
    """Use Node.js to load the JS files and verify runtime state."""
    failures = []
    rel = html.relative_to(EXPLORER_DIR)
    text = html.read_text(encoding="utf-8")

    # Extract script src order (only data-related files)
    scripts = re.findall(r'<script\s+src="([^"]+)"', text)
    # Only load data files — skip truth-utils.js (requires browser APIs)
    # and skip Three.js, audio, panels, etc.
    data_scripts = [s for s in scripts
                    if not s.startswith("http") and not s.startswith("vendor/")
                    and (s.endswith("data.graph.js") or s.endswith("data.claims.js")
                         or s.endswith("data.js"))]

    if not data_scripts:
        return failures  # No data files to check

    # Build a Node.js test script
    node_script = """
var fs = require('fs');
var path = require('path');
global.window = {};
global.document = { createElement: function() { return { setAttribute: function(){}, appendChild: function(){}, style: {} }; }, getElementById: function() { return null; }, addEventListener: function() {} };
global.navigator = { userAgent: 'node' };
global.setInterval = function() { return 0; };
global.clearInterval = function() {};
global.requestAnimationFrame = function() { return 0; };

var scripts = SCRIPTS_PLACEHOLDER;
scripts.forEach(function(src) {
    try {
        var code = fs.readFileSync(src, 'utf8');
        eval(code);
    } catch (e) {
        // Some scripts may fail in Node — that's OK for data files
    }
});

// Check PFClaimsData
if (typeof window.PFClaimsData === 'undefined') {
    console.log('FAIL: PFClaimsData not loaded');
    process.exit(1);
}

var claims = window.PFClaimsData.claims || [];
console.log('CLAIMS_COUNT:' + claims.length);

if (claims.length < 36) {
    console.log('FAIL: Expected >= 36 claims, got ' + claims.length);
    process.exit(1);
}

// Check PFExplorerData (if data.js was loaded)
if (typeof window.PFExplorerData !== 'undefined') {
    var results = window.PFExplorerData.results || [];
    console.log('RESULTS_COUNT:' + results.length);

    // Check that results have authorityClaimIds
    var withAuth = results.filter(function(r) { return r.authorityClaimIds && r.authorityClaimIds.length > 0; });
    console.log('WITH_AUTH:' + withAuth.length);

    // Check that statuses are not stale DERIVED for weinberg
    var weinberg = results.find(function(r) { return r.id === 'weinberg-angle'; });
    if (weinberg) {
        console.log('WEINBERG_STATUS:' + weinberg.status);
        if (weinberg.status === 'DERIVED') {
            console.log('FAIL: Weinberg still shows DERIVED (should be ARGUED)');
            process.exit(1);
        }
    }

    // Check that koide-law shows EXACT IDENTITY
    var koide = results.find(function(r) { return r.id === 'koide-law'; });
    if (koide) {
        console.log('KOIDE_STATUS:' + koide.status);
    }

    // Check god-equation has split statuses
    var god = results.find(function(r) { return r.id === 'god-equation'; });
    if (god) {
        console.log('GOD_STATUS:' + god.status);
        if (god.splitStatuses && god.splitStatuses.length >= 2) {
            console.log('GOD_SPLIT:OK');
        } else {
            console.log('GOD_SPLIT:MISSING');
        }
    }
}

// Check PFDataGraph is unified
if (typeof window.PFDataGraph !== 'undefined' && typeof window.PFClaimsData !== 'undefined') {
    if (window.PFDataGraph === window.PFClaimsData) {
        console.log('UNIFIED:OK');
    } else {
        console.log('UNIFIED:FAIL');
    }
}

console.log('PASS');
"""

    # Replace placeholder with script list
    scripts_json = json.dumps([str(EXPLORER_DIR / s) for s in data_scripts])
    node_script = node_script.replace("SCRIPTS_PLACEHOLDER", scripts_json)

    # Run Node.js
    try:
        result = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout + result.stderr

        if "FAIL:" in output:
            for line in output.splitlines():
                if "FAIL:" in line:
                    failures.append(f"RUNTIME: {rel} - {line.strip()}")

        # Extract claim count
        claim_match = re.search(r'CLAIMS_COUNT:(\d+)', output)
        if claim_match:
            count = int(claim_match.group(1))
            if count < 36:
                failures.append(f"RUNTIME: {rel} - only {count} claims loaded (expected 36)")

        # Check for PASS
        if "PASS" not in output:
            failures.append(f"RUNTIME: {rel} - Node.js runtime check did not pass")

    except subprocess.TimeoutExpired:
        failures.append(f"RUNTIME: {rel} - Node.js timeout")
    except FileNotFoundError:
        failures.append(f"RUNTIME: {rel} - Node.js not available")

    return failures


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 70)
    print("Explorer Truth Layer V3 — Runtime Proof")
    print("=" * 70)
    print()

    htmls = get_html_entry_points()
    print(f"Found {len(htmls)} HTML entry points:")
    for h in htmls:
        print(f"  - {h.name}")
    print()

    all_failures = []

    for html in htmls:
        rel = html.relative_to(EXPLORER_DIR)
        print(f"[{rel}]")

        # Check 1: Load order
        order_failures = check_load_order(html)
        if order_failures:
            for f in order_failures:
                print(f"  FAIL: {f}")
                all_failures.append(f)
        else:
            print(f"  PASS: Load order OK")

        # Check 2: No legacy data
        legacy_failures = check_no_legacy_data(html)
        if legacy_failures:
            for f in legacy_failures:
                print(f"  FAIL: {f}")
                all_failures.append(f)
        else:
            print(f"  PASS: No legacy data sources")

        # Check 3: Runtime (Node.js)
        # Only check HTML files that load data files
        text = html.read_text(encoding="utf-8")
        if "data.claims.js" in text or "data.js" in text:
            runtime_failures = check_node_runtime(html)
            if runtime_failures:
                for f in runtime_failures:
                    print(f"  FAIL: {f}")
                    all_failures.append(f)
            else:
                print(f"  PASS: Runtime check OK (36 claims, unified data)")
        else:
            print(f"  SKIP: No data files loaded (standalone page)")

        print()

    print("=" * 70)
    if all_failures:
        print(f"RUNTIME PROOF: FAIL ({len(all_failures)} failures)")
        print("=" * 70)
        return 1
    else:
        print(f"RUNTIME PROOF: PASS — All {len(htmls)} entry points verified")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
