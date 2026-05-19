# Contributing to the Verification Harness

This guide covers the developer-facing extension surface of the
`verification/` harness. For the user-facing surface (what the
dashboard means, how to run the pipeline, what outcomes mean), see
`verification/README.md`.

The harness is read-only against every board document. It parses
`CLAIMS.md`, runs tier-appropriate local checks, wires the five
falsification tests, enforces guardrails, and emits a markdown
dashboard. The rules below exist to keep it that way.

## 1. Golden rules

Non-negotiable. Violations are caught by tests and by the guardrail
enforcer; don't try to route around them.

- Never modify `CLAIMS.md`, `ACTIVE_ISSUES.md`, or `WHATS_NEXT.md`
  from pipeline code. These are board documents.
- Never change confidence scores anywhere in the harness code paths.
  Scores are echoed verbatim from `CLAIMS.md`.
- Never treat a broken sandbox script as a falsification. A
  subprocess traceback, a missing dependency, or a timeout is always
  `SCRIPT_BROKEN`.
- Tier runners must emit exactly one of the six `VerificationOutcome`
  values: `REPRODUCED`, `REGRESSION_OK`, `HYPOTHESIS_OPEN`,
  `SCRIPT_BROKEN`, `EXTERNAL_ONLY`, `UNDER_PRESSURE`.
- Falsification tests must emit exactly one of the four
  `FalsificationReadout` values: `PARTIAL_LOCAL`, `UNDER_PRESSURE`,
  `EXTERNAL_ONLY`, `SCRIPT_BROKEN`.
- External-only falsification tests never emit `PASS`. A
  non-discovery so far is not a confirmation.

## 2. Adding a new claim (the common case)

1. Add a row to `CLAIMS.md` in the appropriate section (1. Fundamental
   Physics or 2. Biological & Cognitive Systems) following the
   existing 5-column format.
2. No changes needed in the harness. The parser picks it up on the
   next run.
3. If the new claim has explicit upstream dependencies, add an edge
   to `verification/dependency_overlay.yaml` (see §3). The overlay
   uses short ids that the resolver token-matches against the full
   slugified ids.
4. If the new claim has audit-qualified derivation support, add an
   entry to `verification/support_manifest.yaml` (see §4). Every
   referenced path must exist on disk.

## 3. Adding a dependency edge (overlay extension)

Edit `verification/dependency_overlay.yaml`. Each edge needs
`upstream`, `downstream`, `reason`, and `source`.

- Never add `status:` or `confidence:` keys. They are rejected at
  load. The overlay is metadata, not a second scoreboard.
- Never add a claim id that doesn't exist in `CLAIMS.md`. The loader
  BLOCKs on unresolvable ids and lists candidate ids in the error.
- Self-loops are rejected.
- Smoke-test the load: `python -m verification.dependency_overlay`.

## 4. Adding a support manifest entry

Edit `verification/support_manifest.yaml`.

- Every `path:` must point to an existing file on disk.
- `audit_status:` should be one of `DERIVED`, `AUDIT_PASSED`, or
  `AUDIT_PENDING`. Only the first two count as positive support in
  `DerivedRunner`.
- Smoke-test: `python -m verification.support_manifest`.

## 5. Adding a no-go entry

Preferred: document the failed approach in `AGENTS.md` under a
`## No-Go` or `## Failed Approaches` section. The loader picks it up.

Filename convention: a derivation file named `*_no_go*.md` in
`derivations/` is also auto-detected.

Fallback: add to `HARDCODED_NO_GO_FALLBACK` in
`verification/guardrails.py` as a last resort. That constant is a
cache for offline runs, not a truth source.

## 6. Adding a new tier runner (rare)

The eight `ClaimStatus` tiers are all covered. In practice, every new
claim fits an existing tier. Resist adding a tier unless the existing
ones are genuinely insufficient.

If you must:

1. Add the status value to `ClaimStatus` in `verification/models.py`.
2. Create `verification/runners/<tier>.py` subclassing `TierRunner`.
3. Register in `verification/runners/base.py` `get_runner_for_tier()`.
4. Add a confidence-range entry in `verification/claim_parser.py`
   `CONFIDENCE_RANGES`.
5. Add a color-code entry in `verification/report.py`
   `_OUTCOME_MARKERS` if a new outcome is involved.
6. Write unit tests in `tests/unit/test_runners.py`.

## 7. Adding a new falsification test

1. Add `verification/falsification/testN_<name>.py` exposing
   `run_testN()` returning a `FalsificationTest`.
2. Register it in `FalsificationPipeline.run_local_tests()` or
   `check_external_watch()` in
   `verification/falsification/pipeline.py`.
3. Local tests must wrap an existing `sandbox/*.py` script via
   `run_sandbox_script()`. Do not reimplement the science inside the
   harness.
4. External-only tests return `FalsificationReadout.EXTERNAL_ONLY`
   unconditionally.
5. Write tests in `tests/unit/test_falsification.py`.

## 8. Extending hypothesis / gap extraction

The parser's named-hypothesis heuristics live in
`verification/claim_parser.py` as `_HYP_TOKEN_RE` and
`_HYP_PHRASE_PATTERNS`. Add a regex when a new hypothesis-naming
convention enters `CLAIMS.md`. Same pattern for
`_GAP_SENTENCE_PATTERNS` on ARGUED-tier gaps.

Always add a unit test in `tests/unit/test_claim_parser.py` with a
fixture that exercises the new pattern.

## 9. Writing a sandbox script the harness can consume

- Place it under `sandbox/<descriptive_name>.py` as a standalone
  Python script.
- For numerical results, emit a JSON blob to stdout. The runner's
  extractor picks up the first well-formed JSON object it finds:
  - `{"predicted": X, "measured": Y}` for empirical match
  - `{"error_margin": X}` for explicit relative error
  - `{"no_go_confirmed": true}` for `NO_GO`-tier scripts confirming
    the no-go
- The runner wraps your script in a subprocess with
  `PF_READONLY_BOARDS=1`, a temp cwd, and (optionally) `PF_SEED=N` /
  `PYTHONHASHSEED=N` for deterministic runs.
- Your script must not write to `CLAIMS.md`, `ACTIVE_ISSUES.md`,
  `WHATS_NEXT.md`, or `derivations/`. Use the temp cwd or `sandbox/`
  for outputs.
- Reference your script from a `CLAIMS.md` row's evidence cell; the
  parser picks up `sandbox/*.py` tokens automatically.

## 10. Testing your changes

```
python -m pytest tests/unit/ -v         # fast, mocked subprocesses (~2s)
python -m pytest tests/integration/ -v  # real CLAIMS.md, monkey-patched sandbox (~4s)
python -m pytest tests/ -v              # full suite (~10s)
python -m verification.pipeline --quick # end-to-end smoke against the real workspace
```

## 11. Common pitfalls

- The overlay and manifest use short human-friendly claim ids; the
  parser slugifies `CLAIMS.md` row labels into long snake_case ids.
  `resolve_claim_id` bridges both via exact → suffix → token-superset
  matching. If your overlay id doesn't resolve, the error lists
  candidate ids.
- `PARTIAL DERIVATION` in `CLAIMS.md` (two words) maps to
  `PARTIAL_DERIVATION` (one enum name). The parser normalizes.
- The pipe-cell splitter handles pipes inside backticked code and
  math-norm notation (`||X||`). Don't add new cell-splitting logic
  without re-running the parser tests.
- `CONDITIONAL` rows with zero named hypotheses are WARN, not BLOCK.
  The parser may have failed to match a non-standard hypothesis name.
  Add a pattern (see §8) rather than editing the row.
- The cache is SHA-256 content-keyed. Editing a sandbox script
  invalidates its cache automatically. Deleting `verification/.cache/`
  wipes everything.

## 12. Style guide

- Python 3.10+ type hints (`list[str]`, `dict[str, int]`, etc.).
- `from __future__ import annotations` at the top of every module.
- Module docstrings cite the relevant requirement numbers from
  `.kiro/specs/propagation-framework-verification/requirements.md`.
- Docstrings on all public functions; concise inline comments where
  behavior is non-obvious.
- Keep runners pure: no side effects beyond subprocess execution.
- Never raise from a sandbox-runner helper. Return a
  `SandboxRunResult` with `success=False` instead.

## Questions / Out of scope

Architectural changes to the six `VerificationOutcome` values, the
four `FalsificationReadout` values, or the truth-order hierarchy are
out of scope for contributions. Those changes require spec-level
agreement in
`.kiro/specs/propagation-framework-verification/design.md` before any
code change lands.
