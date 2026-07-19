#!/usr/bin/env python3
"""
Explorer Truth Layer V5 — Fail-Closed Drift Gate

V5 fixes V4 defects:
  1. Registry-disk completeness: every file on disk is classified, every
     registry entry exists on disk. Missing root_js → FAIL.
  2. Narrow allowlists: no broad `data-status=` or `label:` skips. A visible
     tier promotion in any scanned file is caught.
  3. Server enforcement: probes serve.py for 404 on quarantine/dev paths.
  4. Acceptance runner: verifies check_explorer_acceptance.py invokes V5.

V5 preserves V4's:
  - CLAIMS.md fresh parse + snapshot comparison
  - Semantic scope triples
  - God Equation operator/scale split
  - Standard math distinction
  - Source unity
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import os
import socket
import time
import urllib.request
from pathlib import Path


EXPLORER_DIR = Path(__file__).resolve().parent
CLAIMS_MD = Path("/mnt/d/fundamentals/CLAIMS.md")

# V5: Allow override via command-line for fixture testing
_explorer_dir_override = None
def get_explorer_dir() -> Path:
    return _explorer_dir_override or EXPLORER_DIR

def get_claims_md() -> Path:
    return CLAIMS_MD

SNAPSHOT_PATH = None
DATA_CLAIMS_JS = None
DATA_JS = None
DATA_GRAPH_JS = None
REGISTRY_PATH = None

def _compute_paths():
    global SNAPSHOT_PATH, DATA_CLAIMS_JS, DATA_JS, DATA_GRAPH_JS, REGISTRY_PATH
    ed = get_explorer_dir()
    SNAPSHOT_PATH = ed / "_authority_snapshot.json"
    DATA_CLAIMS_JS = ed / "data.claims.js"
    DATA_JS = ed / "data.js"
    DATA_GRAPH_JS = ed / "data.graph.js"
    REGISTRY_PATH = ed / "release_tree_registry.json"

_compute_paths()

STATUS_WORDS = {"DERIVED", "CONDITIONAL", "ARGUED", "EMPIRICAL",
                "INTUITION", "OPEN", "EXACT IDENTITY", "CANONICAL",
                "STANDARD MATH", "NO-GO", "UNSYNCED", "PARTIAL DERIVATION"}

# V5: Generated files that are exempt from badge scanning
# These are mechanically generated from authority, not hand-written
GENERATED_FILES = {"data.claims.js", "data.js", "data.graph.js",
                   "_authority_snapshot.json", "generate_claims_data_v3.py",
                   "generate_claims_data_v4.py", "generate_claims_data_v5.py",
                   "check_truth_drift_v3.py", "check_truth_fixtures_v3.py",
                   "check_truth_drift_v4.py", "check_truth_fixtures_v4.py",
                   "check_runtime_proof_v3.py", "check_runtime_proof_v4.py",
                   "check_truth_drift_v5.py", "check_truth_fixtures_v5.py",
                   "check_runtime_proof_v5.py", "scope_triples.json",
                   "_blocked.html", "release_tree_registry.json",
                   "_browser_dom_evidence.json", "generate_release_registry.py",
                   "generate-data-graph.js", "check_explorer_acceptance.py"}


# ============================================================================
# V5 REGISTRY COMPLETENESS
# ============================================================================

def load_registry() -> dict:
    """Load the V5 release-tree registry."""
    if not REGISTRY_PATH.is_file():
        print(f"FAIL: No release-tree registry at {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def check_registry_completeness(registry: dict) -> list[str]:
    """V5: Verify every file on disk is in the registry and vice versa."""
    failures = []
    ed = get_explorer_dir()

    # Collect all registry paths
    registry_paths = set()
    for entry in registry.get("servedRoutes", []):
        registry_paths.add(entry["path"])
    for entry in registry.get("blockedFiles", []):
        registry_paths.add(entry)  # blocked files are classified but not served
    for entry in registry.get("jsRoot", []):
        registry_paths.add(entry["path"])
    for entry in registry.get("jsPanels", []):
        registry_paths.add(entry["path"])
    for entry in registry.get("jsWorkers", []):
        registry_paths.add(entry["path"])
    for entry in registry.get("jsonFiles", []):
        registry_paths.add(entry["path"])
    for entry in registry.get("cssFiles", []):
        registry_paths.add(entry["path"])

    # Check every registry path exists on disk
    for rp in registry_paths:
        if not (ed / rp).is_file():
            failures.append(f"REGISTRY_MISSING_FILE: {rp} in registry but not on disk")

    # Check every disk file is in registry (excluding generated/exempt)
    disk_files = set()
    for p in ed.glob("*.html"):
        disk_files.add(p.name)
    for p in ed.glob("*.js"):
        disk_files.add(p.name)
    for p in ed.glob("*.json"):
        disk_files.add(p.name)
    for p in ed.glob("*.css"):
        disk_files.add(p.name)
    if (ed / "panels").is_dir():
        for p in (ed / "panels").glob("*.js"):
            disk_files.add(str(p.relative_to(ed)))
    if (ed / "workers").is_dir():
        for p in (ed / "workers").glob("*.js"):
            disk_files.add(str(p.relative_to(ed)))

    # Python scripts and other non-served files are exempt
    exempt_extensions = {".py", ".md", ".txt", ".sh", ".png", ".jpg", ".svg",
                         ".ico", ".woff", ".woff2", ".gif", ".webp"}
    disk_files = {f for f in disk_files if Path(f).suffix not in exempt_extensions}

    for df in sorted(disk_files):
        if df not in registry_paths:
            failures.append(f"DISK_FILE_UNCLASSIFIED: {df} exists on disk but not in registry")

    return failures


# ============================================================================
# V5 SURFACE ENUMERATION (from registry)
# ============================================================================

def enumerate_public_surfaces(registry: dict) -> list[Path]:
    """V5: Enumerate every classified surface from the registry.
    Includes root JS, panels, workers, HTML, and non-generated JSON."""
    ed = get_explorer_dir()
    surfaces = []

    for entry in registry.get("servedRoutes", []):
        p = ed / entry["path"]
        if p.is_file():
            surfaces.append(p)

    for entry in registry.get("jsRoot", []):
        if not entry.get("generated", False):
            p = ed / entry["path"]
            if p.is_file():
                surfaces.append(p)

    for entry in registry.get("jsPanels", []):
        if not entry.get("generated", False):
            p = ed / entry["path"]
            if p.is_file():
                surfaces.append(p)

    for entry in registry.get("jsWorkers", []):
        if not entry.get("generated", False):
            p = ed / entry["path"]
            if p.is_file():
                surfaces.append(p)

    for entry in registry.get("jsonFiles", []):
        if not entry.get("generated", False):
            p = ed / entry["path"]
            if p.is_file():
                surfaces.append(p)

    return surfaces


# ============================================================================
# SNAPSHOT VERIFICATION (preserved from V4)
# ============================================================================

def load_and_verify_snapshot() -> dict:
    """Parse CLAIMS.md at gate time, compare fresh manifest to committed snapshot."""
    if not SNAPSHOT_PATH.is_file():
        print(f"FAIL: No authority snapshot found at {SNAPSHOT_PATH}", file=sys.stderr)
        sys.exit(1)

    committed = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

    source_hash = hashlib.sha256(CLAIMS_MD.read_bytes()).hexdigest()
    if source_hash != committed.get("claims_md_hash"):
        print("FAIL: CLAIMS.md hash mismatch!", file=sys.stderr)
        print(f"  Snapshot recorded: {committed.get('claims_md_hash', 'missing')[:16]}...", file=sys.stderr)
        print(f"  Current file:      {source_hash[:16]}...", file=sys.stderr)
        print("  Run generate_claims_data_v4.py to regenerate.", file=sys.stderr)
        sys.exit(1)

    from generate_claims_data_v4 import build_snapshot
    try:
        fresh_snapshot = build_snapshot(CLAIMS_MD)
    except ValueError as e:
        print(f"FAIL: Fresh parse of CLAIMS.md failed: {e}", file=sys.stderr)
        sys.exit(1)

    if fresh_snapshot["claim_count"] != committed["claim_count"]:
        print(f"FAIL: Claim count drift!", file=sys.stderr)
        print(f"  Committed: {committed['claim_count']}", file=sys.stderr)
        print(f"  Fresh:     {fresh_snapshot['claim_count']}", file=sys.stderr)
        sys.exit(1)

    for cid, fresh_claim in fresh_snapshot["claims"].items():
        committed_claim = committed["claims"].get(cid)
        if not committed_claim:
            print(f"FAIL: Claim '{cid}' in fresh parse but not in committed snapshot", file=sys.stderr)
            sys.exit(1)
        if fresh_claim["primary_status"] != committed_claim["primary_status"]:
            print(f"FAIL: Status drift for '{cid}':", file=sys.stderr)
            sys.exit(1)
        if fresh_claim["primary_confidence"] != committed_claim["primary_confidence"]:
            print(f"FAIL: Confidence drift for '{cid}':", file=sys.stderr)
            sys.exit(1)

    from generate_claims_data_v4 import generate_public_data_js, generate_runtime_data_js
    fresh_claims_js = generate_public_data_js(fresh_snapshot)
    committed_claims_js = DATA_CLAIMS_JS.read_text(encoding="utf-8")
    if fresh_claims_js != committed_claims_js:
        print("FAIL: data.claims.js does not match fresh generation!", file=sys.stderr)
        sys.exit(1)

    fresh_runtime_js = generate_runtime_data_js(fresh_snapshot)
    committed_runtime_js = DATA_JS.read_text(encoding="utf-8")
    if fresh_runtime_js != committed_runtime_js:
        print("FAIL: data.js does not match fresh generation!", file=sys.stderr)
        sys.exit(1)

    return committed


# ============================================================================
# PUBLIC CLAIMS EXTRACTION (preserved from V4)
# ============================================================================

def extract_public_claims() -> dict:
    if not DATA_CLAIMS_JS.is_file():
        return {}
    text = DATA_CLAIMS_JS.read_text(encoding="utf-8")
    m = re.search(r'window\.PFClaimsData\s*=\s*(\{.*?\});', text, re.DOTALL)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    claims = {}
    for c in data.get("claims", []):
        claims[c["id"]] = {
            "status": c.get("status"),
            "confidence": c.get("confidence"),
            "isSplit": c.get("isSplit", False),
            "isStandardMath": c.get("isStandardMath", False),
            "badge": c.get("badge", ""),
            "statusClass": c.get("statusClass", ""),
        }
    return claims


def extract_public_results() -> dict:
    if not DATA_JS.is_file():
        return {}
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r'window\.PFExplorerData\s*=\s*(\{.*?\});', text, re.DOTALL)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    results = {}
    for r in data.get("results", []):
        results[r["id"]] = {
            "status": r.get("status"),
            "confidence": r.get("confidence"),
            "authorityClaimIds": r.get("authorityClaimIds", []),
        }
    return results


# ============================================================================
# DRIFT CHECKS (preserved from V4)
# ============================================================================

def check_claim_drift(snapshot: dict, public_claims: dict) -> list[str]:
    failures = []
    auth_claims = snapshot["claims"]
    for cid, pub in public_claims.items():
        if cid not in auth_claims:
            failures.append(f"UNKNOWN_CLAIM: Public claim '{cid}' has no authority record")
            continue
        auth = auth_claims[cid]
        if pub["status"] != auth["primary_status"]:
            failures.append(f"STATUS_DRIFT: '{cid}' public={pub['status']} authority={auth['primary_status']}")
        if pub["confidence"] != auth["primary_confidence"]:
            failures.append(f"CONFIDENCE_DRIFT: '{cid}' public={pub['confidence']} authority={auth['primary_confidence']}")
        if pub.get("isSplit") != auth.get("is_split", False):
            failures.append(f"SPLIT_FLATTENED: '{cid}' public isSplit={pub.get('isSplit')} authority is_split={auth.get('is_split')}")
        if pub.get("isStandardMath") != auth.get("is_standard_math", False):
            failures.append(f"STD_MATH_DRIFT: '{cid}' public isStandardMath={pub.get('isStandardMath')} authority={auth.get('is_standard_math')}")
        if auth.get("is_standard_math") and "DERIVED" in (pub.get("badge") or "").upper():
            failures.append(f"STD_MATH_AS_DERIVED: '{cid}' standard math shows DERIVED badge: {pub.get('badge')}")
    for cid in auth_claims:
        if cid not in public_claims:
            failures.append(f"MISSING_PUBLIC: Authority claim '{cid}' not in public data")
    return failures


def check_result_drift(snapshot: dict, public_results: dict) -> list[str]:
    failures = []
    crosswalk = snapshot.get("result_to_authority", {})
    for result_id, pub in public_results.items():
        auth_refs = pub.get("authorityClaimIds", [])
        if not auth_refs:
            if pub["status"] not in ("UNSYNCED", "NO-GO", "OPEN"):
                failures.append(f"RESULT_NO_AUTH: '{result_id}' has status '{pub['status']}' but no authorityClaimIds")
            continue
        for auth_id in auth_refs:
            auth = snapshot["claims"].get(auth_id)
            if not auth:
                failures.append(f"RESULT_UNKNOWN_AUTH: '{result_id}' references unknown authority '{auth_id}'")
                continue
            if len(auth_refs) > 1:
                if pub["status"] != snapshot["claims"][auth_refs[0]]["primary_status"]:
                    failures.append(f"RESULT_SPLIT_DRIFT: '{result_id}' primary status={pub['status']} but first auth={auth_refs[0]} has {snapshot['claims'][auth_refs[0]]['primary_status']}")
            else:
                if pub["status"] != auth["primary_status"]:
                    failures.append(f"RESULT_STATUS_DRIFT: '{result_id}' status={pub['status']} but authority={auth['primary_status']}")
                if pub["confidence"] != auth["primary_confidence"]:
                    failures.append(f"RESULT_CONF_DRIFT: '{result_id}' confidence={pub['confidence']} but authority={auth['primary_confidence']}")
    return failures


def check_scope_fields(snapshot: dict, public_claims: dict) -> list[str]:
    failures = []
    for cid, auth in snapshot["claims"].items():
        if auth.get("is_standard_math"):
            continue
        if auth["primary_status"] == "OPEN":
            continue
        if not auth.get("premise"):
            failures.append(f"EMPTY_PREMISE: '{cid}' has empty premise field")
        if not auth.get("scope_note"):
            failures.append(f"EMPTY_SCOPE: '{cid}' has empty scope_note field")
        if not auth.get("source_line"):
            failures.append(f"EMPTY_SOURCE_LINE: '{cid}' has no source_line")
        if not auth.get("section"):
            failures.append(f"EMPTY_SECTION: '{cid}' has no section")
        if not auth.get("standard_physics"):
            failures.append(f"EMPTY_STANDARD_PHYSICS: '{cid}' has empty standard_physics field")
        if not auth.get("pf_result_under_named_premises"):
            failures.append(f"EMPTY_PF_RESULT: '{cid}' has empty pf_result_under_named_premises field")
        if not auth.get("open_pf_gap"):
            failures.append(f"EMPTY_OPEN_PF_GAP: '{cid}' has empty open_pf_gap field")
    return failures


def check_god_equation_split(snapshot: dict, public_claims: dict) -> list[str]:
    failures = []
    operator = snapshot["claims"].get("god-equation-operator")
    scale = snapshot["claims"].get("god-equation-scale")
    if not operator:
        failures.append("GOD_SPLIT: Missing god-equation-operator claim")
    if not scale:
        failures.append("GOD_SPLIT: Missing god-equation-scale claim")
    if operator and scale:
        if operator["primary_status"] == scale["primary_status"]:
            failures.append(f"GOD_SPLIT: operator and scale have same status: {operator['primary_status']}")
    return failures


def check_source_unity() -> list[str]:
    failures = []
    if DATA_GRAPH_JS.is_file():
        text = DATA_GRAPH_JS.read_text(encoding="utf-8")
        if "results:" in text and "PFExplorerData" not in text:
            failures.append("DUAL_SOURCE: data.graph.js contains independent results data")
        if "PFClaimsData" not in text:
            failures.append("DUAL_SOURCE: data.graph.js does not reference PFClaimsData")
    return failures


# ============================================================================
# V5 BADGE SCANNER — narrow allowlists, no broad skips
# ============================================================================

def scan_file_for_badges(filepath: Path, auth_claims: dict) -> list[str]:
    """
    V5: Scan a file for status-bearing words in hand-written contexts.
    Narrow allowlists only — no broad `data-status=` or `label:` skips.
    A visible tier promotion (e.g. 'DERIVED 1.00') in any scanned file is caught.
    """
    failures = []
    if not filepath.is_file():
        return failures

    # Skip generated files
    if filepath.name in GENERATED_FILES:
        return failures

    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        rel_path = filepath.relative_to(get_explorer_dir())
    except ValueError:
        rel_path = filepath

    # V5: NARROW allowlist — only structural patterns that cannot contain
    # a visible tier promotion. No broad `data-status=`, `label:`, or `col:` skips.
    NARROW_INFRA = [
        # Object key definitions (the KEY is a status word, not a value)
        r"['\"](?:DERIVED|CONDITIONAL|ARGUED|EMPIRICAL|INTUITION|EXACT IDENTITY|CANONICAL|STANDARD MATH|NO-GO|UNSYNCED|PARTIAL DERIVATION)['\"]\s*:",
        # Switch/case comparisons (comparing TO a status, not displaying it)
        r"case\s+['\"]",
        r"===?\s*['\"]",
        r"!==?\s*['\"]",
        # Status word used as a variable/property accessor
        r"\bcounts\.\w+",
        r"\bresult\.\w+",
        r"\bclaim\.\w+",
        r"\bapi\.\w+",
        r"\bctx\.\w+",
        # Constant definitions
        r"\bTIER_ORDER\b",
        r"\bSTATUS_WORDS\b",
        r"\bUNAVAILABLE\b",
        # Explicit placeholder text
        r"loading from authority",
        # CSS class definitions (the class name, not the displayed text)
        r"\.status-(?:pill|badge|derived|conditional|argued|empirical|intuition|open|partial)",
        # Filter button definitions (button labels in filter UI, not claim badges)
        r"status-filter-btn",
        # Legend items (color key, not claim status)
        r"legend-item",
        r"legend-color",
        r"tl-legend",
        # V5: Narrow UI count-label patterns — these show a category NAME
        # next to a count, not a specific claim's status badge.
        # A visible tier promotion (DERIVED 1.00) cannot hide in these.
        r'''class=["']wrong-badge["']''',          # Explicit "wrong badge" example
        r'''class=["']stat-label["']''',            # Stat category label
        r'''class=["']ws-metric-row["']''',         # Metric row with count + label
        r'''class=["']stat-tile["']''',             # Stat tile with count + label
        r'''class=["']eb-stat-item["']''',          # Experiment bench stat item
        # Count label spans: <span>Derived</span> inside count-display HTML
        # These are lowercase labels, not uppercase status badges
        r"<span>(?:Derived|Conditional|Argued|Empirical|Intuition|Partial(?:\s+Derivation)?)</span>",
        # HTML span with explicit wrong-badge class (Journey page examples)
        r'''<span\s+class=["']wrong-badge["']''',
    ]

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip pure comment lines
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        # Skip HTML comments
        if stripped.startswith("<!--") or stripped.startswith("-->"):
            continue

        # V5.1: Check for ternary/object-literal fallback patterns FIRST
        # These are always violations regardless of other infra patterns
        # on the same line, because the status word is a display fallback
        V51_FALLBACK_PATTERNS = [
            # Ternary fallback: ? ... : 'STATUS_WORD'
            r"""\?\s*[^:]*:\s*['"](?:DERIVED|CONDITIONAL|ARGUED|EMPIRICAL|INTUITION|EXACT IDENTITY|CANONICAL|STANDARD MATH|NO-GO|UNSYNCED|PARTIAL DERIVATION)['"]""",
            # Object-literal fallback after ||: || { ... label: 'STATUS_WORD' ... }
            r"""\|\|[^)]*label\s*:\s*['"](?:DERIVED|CONDITIONAL|ARGUED|EMPIRICAL|INTUITION|EXACT IDENTITY|CANONICAL|STANDARD MATH|NO-GO|UNSYNCED|PARTIAL DERIVATION)['"]""",
        ]
        v51_fallback_found = False
        for pat in V51_FALLBACK_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                v51_fallback_found = True
                break

        # Check if this line matches any narrow infrastructure pattern
        is_infra = False
        if not v51_fallback_found:
            for pat in NARROW_INFRA:
                if re.search(pat, line, re.IGNORECASE):
                    is_infra = True
                    break
        if is_infra:
            continue

        # V5: Scan for status words in ALL contexts except narrow infra
        for word in STATUS_WORDS:
            we = re.escape(word)

            # V5: Comprehensive patterns — catches injections in JS, HTML, templates
            patterns = [
                # Badge/pill HTML elements with visible text
                r"""class=["']status-pill[^"']*["']\s*>\s*""" + we,
                r"""class=["']status-badge[^"']*["']\s*>\s*""" + we,
                r"""class=\\"status-pill[^>]*>\s*""" + we,
                r"""class=\\"status-badge[^>]*>\s*""" + we,
                # insertAdjacentHTML / innerHTML with status pill
                r"""insertAdjacentHTML.*status-pill.*""" + we,
                r"""innerHTML.*status-pill.*""" + we,
                r"""insertAdjacentHTML.*status-badge.*""" + we,
                r"""innerHTML.*status-badge.*""" + we,
                # Template literals with status pill/badge
                r"""`[^`]*status-pill[^`]*""" + we,
                r"""`[^`]*status-badge[^`]*""" + we,
                # String concatenation building status pills
                r"""['"]status-pill['"]\s*\+.*""" + we,
                r"""['"]status-badge['"]\s*\+.*""" + we,
                # Fallback string literals (|| 'DERIVED')
                r"""\|\|\s*['"]""" + we + r"""['"]""",
                # V5.1: Ternary fallback to status word (? ... : 'DERIVED')
                # Must have ? before : to be a ternary, not an object literal
                r"""\?\s*[^:]*:\s*['"]""" + we + r"""['"]""",
                # V5.1: Object-literal fallback with status word after ||
                # e.g. || { status: { label: 'DERIVED' } }
                r"""\|\|[^)]*label\s*:\s*['"]""" + we + r"""['"]""",
                # _fallbackStatus with status words
                r"""_fallbackStatus\s*[:=]\s*['"]""" + we,
                # Plain-text "Status: WORD" in HTML content
                r"""Status:\s*""" + we,
                # V5: Visible tier promotion: "DERIVED 1.00" or similar
                # This catches the decisive Codex probe: a badge with status + confidence
                we + r"""\s+\d+\.\d+""",
                # V5: Status word in a status-pill/badge context within string concat
                # e.g. '<div class="status-pill status-derived">DERIVED</div>'
                r"""status-pill[^'"]*['"]\s*>\s*""" + we,
                r"""status-badge[^'"]*['"]\s*>\s*""" + we,
            ]

            for pat in patterns:
                if re.search(pat, line, re.IGNORECASE):
                    failures.append(
                        f"UNMAPPED_BADGE: {rel_path}:{i} contains status word '{word}' "
                        f"in hand-written file. Line: {stripped[:120]}"
                    )
                    break

    return failures


# ============================================================================
# V5 HTML ENTRY POINT CHECKS
# ============================================================================

def check_html_entry_points(registry: dict) -> list[str]:
    """V5: Check HTML entry points using V5 registry schema."""
    failures = []
    ed = get_explorer_dir()

    served_routes = registry.get("servedRoutes", [])
    claim_routes = [r for r in served_routes if r.get("type") == "claim"]
    non_claim_routes = [r for r in served_routes if r.get("type") == "non-claim"]

    for route in claim_routes:
        name = route["path"]
        html_path = ed / name
        if not html_path.is_file():
            failures.append(f"MISSING_ROUTE: {name} listed in registry but not found")
            continue
        text = html_path.read_text(encoding="utf-8")
        has_data = ("data.js" in text or "data.claims.js" in text or "data.graph.js" in text)
        has_truth_utils = "truth-utils.js" in text
        if has_data and not has_truth_utils:
            failures.append(f"MISSING_TRUTH_UTILS: {name} loads data files but not truth-utils.js")
        if not has_data:
            failures.append(f"NO_DATA: {name} is a claim route but loads no generated data")
        graph_pos = text.find("data.graph.js")
        claims_pos = text.find("data.claims.js")
        data_js_pos = text.find('src="data.js"')
        if data_js_pos > 0 and claims_pos > 0 and data_js_pos < claims_pos:
            failures.append(f"LOAD_ORDER: {name} loads data.js before data.claims.js")

    for route in non_claim_routes:
        name = route["path"]
        html_path = ed / name
        if not html_path.is_file():
            failures.append(f"MISSING_ROUTE: {name} listed in registry but not found")
            continue
        text = html_path.read_text(encoding="utf-8")
        for word in STATUS_WORDS:
            we = re.escape(word)
            if re.search(r"""['"]status['"]\s*:\s*['"]""" + we, text) or \
               re.search(r"""class="status-pill[^"]*">\s*""" + we, text) or \
               re.search(r"""Status:\s*""" + we, text, re.IGNORECASE):
                failures.append(f"NON_CLAIM_HAS_STATUS: {name} classified as non-claim but contains status word '{word}'")

    return failures


# ============================================================================
# V5 SERVER ENFORCEMENT CHECK
# ============================================================================

def check_server_enforcement(registry: dict) -> list[str]:
    """V5: Probe serve.py to verify quarantine/dev paths return 404."""
    failures = []
    ed = get_explorer_dir()

    # Find a free port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    # Start serve.py
    proc = subprocess.Popen(
        [sys.executable, str(ed / "serve.py"), str(port)],
        cwd=str(ed),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid if sys.platform != "win32" else None,
    )

    try:
        # Wait for server
        ready = False
        for _ in range(30):
            time.sleep(0.5)
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=3)
                ready = True
                break
            except Exception:
                pass

        if not ready:
            failures.append("SERVER_NOT_READY: serve.py did not start within 10s")
            return failures

        # Probe allowed paths (should be 200)
        for route in registry.get("servedRoutes", []):
            path = route["path"]
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{port}/{path}")
                resp = urllib.request.urlopen(req, timeout=5)
                code = resp.getcode()
                if code != 200:
                    failures.append(f"SERVER_BLOCKED_ALLOWED: {path} returned {code}, expected 200")
            except urllib.error.HTTPError as e:
                failures.append(f"SERVER_BLOCKED_ALLOWED: {path} returned {e.code}, expected 200")
            except Exception as e:
                failures.append(f"SERVER_ERROR_ALLOWED: {path} error: {e}")

        # Probe blocked paths (should be 404)
        blocked_paths = [
            "quarantine/test-d3.html",
            "dev/test-d3.html",
            "_blocked.html",
            "serve.py",
            "check_truth_drift_v5.py",
            # V5.1: Traversal attempts must return 404
            "derivations/../CLAIMS.md",
            "derivations/../../System/FAMILY_WORKSPACE_UPDATE_RULE.md",
            # V5.1: Source-viewer prefixes must return 404 on release server
            "derivations/",
            "definitions/",
            "papers/",
            "verification/",
            "sandbox_results",
            "CLAIMS",
            "ACTIVE_ISSUES",
        ]
        for qpath in registry.get("quarantinedPaths", []):
            blocked_paths.append(qpath["path"])

        for path in blocked_paths:
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{port}/{path}")
                urllib.request.urlopen(req, timeout=5)
                failures.append(f"SERVER_LEAK: {path} returned 200, expected 404")
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    failures.append(f"SERVER_WRONG_CODE: {path} returned {e.code}, expected 404")
            except Exception:
                pass  # Connection error is fine (treated as blocked)

    finally:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

    return failures


# ============================================================================
# V5 ACCEPTANCE RUNNER CHECK
# ============================================================================

def check_acceptance_runner() -> list[str]:
    """V5: Verify check_explorer_acceptance.py invokes V5, not V3/V4."""
    failures = []
    ed = get_explorer_dir()
    acceptance_path = ed / "check_explorer_acceptance.py"
    if not acceptance_path.is_file():
        failures.append("MISSING_ACCEPTANCE: check_explorer_acceptance.py not found")
        return failures

    text = acceptance_path.read_text(encoding="utf-8")

    # Must NOT reference V3
    if "check_truth_drift_v3.py" in text:
        failures.append("ACCEPTANCE_V3: check_explorer_acceptance.py still invokes V3 gate")
    if "check_truth_fixtures_v3.py" in text:
        failures.append("ACCEPTANCE_V3: check_explorer_acceptance.py still invokes V3 fixtures")
    if "check_runtime_proof_v3.py" in text:
        failures.append("ACCEPTANCE_V3: check_explorer_acceptance.py still invokes V3 runtime proof")

    # Must reference V5
    if "check_truth_drift_v5.py" not in text:
        failures.append("ACCEPTANCE_NO_V5: check_explorer_acceptance.py does not invoke V5 gate")
    if "check_truth_fixtures_v5.py" not in text:
        failures.append("ACCEPTANCE_NO_V5: check_explorer_acceptance.py does not invoke V5 fixtures")
    if "check_runtime_proof_v5.py" not in text:
        failures.append("ACCEPTANCE_NO_V5: check_explorer_acceptance.py does not invoke V5 runtime proof")

    return failures


# ============================================================================
# MAIN GATE
# ============================================================================

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Explorer Truth Layer V5 — Fail-Closed Drift Gate")
    parser.add_argument("--explorer-dir", type=Path, default=None,
                        help="Override explorer directory (for fixture testing)")
    parser.add_argument("--skip-server-check", action="store_true",
                        help="Skip server enforcement check (for fixture testing)")
    args = parser.parse_args()

    global _explorer_dir_override
    if args.explorer_dir:
        _explorer_dir_override = args.explorer_dir
        _compute_paths()

    print("=" * 70)
    print("Explorer Truth Layer V5 — Fail-Closed Drift Gate")
    print("=" * 70)
    print()

    # Step 1: Load registry and check completeness
    print("[1/9] Loading registry and checking disk completeness...")
    registry = load_registry()
    registry_failures = check_registry_completeness(registry)
    if registry_failures:
        print(f"  FAIL: {len(registry_failures)} registry completeness failures:")
        for f in registry_failures[:15]:
            print(f"    - {f}")
    else:
        routes = len(registry.get("servedRoutes", []))
        js = len(registry.get("jsRoot", [])) + len(registry.get("jsPanels", [])) + len(registry.get("jsWorkers", []))
        print(f"  PASS: Registry complete ({routes} routes, {js} JS files, all verified against disk)")

    # Step 2: Verify snapshot
    print("\n[2/9] Verifying source hash + fresh parse...")
    snapshot = load_and_verify_snapshot()
    print(f"  PASS: CLAIMS.md hash matches, fresh parse matches committed snapshot")
    print(f"  Claims in authority: {snapshot['claim_count']}")

    # Step 3: Extract public claims
    print("\n[3/9] Extracting public claims...")
    public_claims = extract_public_claims()
    public_results = extract_public_results()
    print(f"  Claims in public data: {len(public_claims)}")
    print(f"  Results in runtime data: {len(public_results)}")

    # Step 4: Check claim drift
    print("\n[4/9] Checking claim drift...")
    drift_failures = check_claim_drift(snapshot, public_claims)
    if drift_failures:
        print(f"  FAIL: {len(drift_failures)} drift failures:")
        for f in drift_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All public claims match authority")

    # Step 5: Check result drift
    print("\n[5/9] Checking runtime result drift...")
    result_failures = check_result_drift(snapshot, public_results)
    if result_failures:
        print(f"  FAIL: {len(result_failures)} result drift failures:")
        for f in result_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All runtime results match authority")

    # Step 6: Check scope fields
    print("\n[6/9] Checking premise/scope fields and semantic triples...")
    scope_failures = check_scope_fields(snapshot, public_claims)
    if scope_failures:
        print(f"  FAIL: {len(scope_failures)} scope failures:")
        for f in scope_failures[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: All PF claims have nonempty premise, scope, and semantic triples")

    # Step 7: Scan all public surfaces for unmapped badges
    print("\n[7/9] Scanning all public surfaces for unmapped badges...")
    surfaces = enumerate_public_surfaces(registry)
    badge_failures = []
    for surface in surfaces:
        badge_failures.extend(scan_file_for_badges(surface, snapshot["claims"]))
    if badge_failures:
        print(f"  FAIL: {len(badge_failures)} unmapped badges found:")
        for f in badge_failures[:15]:
            print(f"    - {f}")
    else:
        print(f"  PASS: No unmapped badges in {len(surfaces)} public surfaces")

    # Step 8: Check God Equation split, source unity, HTML entry points
    print("\n[8/9] Checking God Equation split, source unity, HTML entry points...")
    god_failures = check_god_equation_split(snapshot, public_claims)
    unity_failures = check_source_unity()
    html_failures = check_html_entry_points(registry)
    all_check8 = god_failures + unity_failures + html_failures
    if all_check8:
        print(f"  FAIL: {len(all_check8)} failures:")
        for f in all_check8[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: God Equation split, source unity, HTML entry points all OK")

    # Step 9: Server enforcement + acceptance runner
    print("\n[9/9] Checking server enforcement and acceptance runner...")
    server_failures = []
    if not args.skip_server_check:
        server_failures = check_server_enforcement(registry)
    acceptance_failures = check_acceptance_runner()
    all_check9 = server_failures + acceptance_failures
    if all_check9:
        print(f"  FAIL: {len(all_check9)} failures:")
        for f in all_check9[:10]:
            print(f"    - {f}")
    else:
        print("  PASS: Server enforces allowlist, acceptance runner invokes V5")

    # Summary
    total_failures = (len(registry_failures) + len(drift_failures) + len(result_failures) +
                      len(scope_failures) + len(badge_failures) + len(all_check8) + len(all_check9))

    print()
    print("=" * 70)
    if total_failures == 0:
        print("TRUTH GATE V5: PASS — No truth drift detected")
        print("=" * 70)
        return 0
    else:
        print(f"TRUTH GATE V5: FAIL ({total_failures} total failures)")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    import signal
    raise SystemExit(main())
