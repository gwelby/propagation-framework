# PFExplorer Release Checklist

This checklist gates every push to `gh-pages` and every update to the
production site at `https://gwelby.github.io/PFExplorer/`. Do not skip steps.
Do not reorder them.

Requirement 10 of the `explorer-panel-render-health` spec is explicit:

> "deploy first, verify later" is forbidden.

A deployment that has not been visually verified against the acceptance
criteria below is not a release. It is a regression waiting to be noticed by
the user.

## Pre-push checklist

1. [ ] Run the panel health audit:
   ```
   python sandbox/explorer/check_panel_health.py
   ```
   Must exit 0. If any panel reports FAIL, fix that panel first. Do not push
   with known FAILs.

2. [ ] Run the audit tool's self-test:
   ```
   python sandbox/explorer/check_panel_health.py --self-test
   ```
   Must exit 0. This confirms the audit tool itself is healthy and that a
   green run on step 1 actually means something.

3. [ ] Start the local server in one shell:
   ```
   python sandbox/explorer/serve.py
   ```

4. [ ] In another shell, run the visual pass:
   ```
   python sandbox/explorer/visual_pass.py
   ```
   Must exit 0. All 17 panels must PASS. If any panel silently falls back to
   the observatory view (the tool detects this), fix the registration or
   loading code before proceeding. A silent fallback is a FAIL, not a PASS.

5. [ ] Optional but recommended — capture screenshots for the PR:
   ```
   python sandbox/explorer/visual_pass.py --screenshots <dir>
   ```

6. [ ] Open `http://localhost:8080/` manually in a real Chrome or Edge window
   at 1920×1080. Click every sidebar panel and every Observatory card grid
   entry. Confirm on each one:
   - Visible content actually paints (no blank canvas).
   - Aspect ratio is correct (no stretched or squashed rendering).
   - DevTools console is clean (no uncaught errors).

7. [ ] Append one row per panel to `sandbox/explorer/VISUAL_PASS_RESULTS.md`
   with commit hash, date (ISO-8601), panel name, PASS/FAIL, and a short
   note. This file is append-only — never edit prior rows.

8. [ ] Only after steps 1–7 all pass: commit and push to `gh-pages`. Include
   a reference to the `explorer-panel-render-health` spec in the commit
   message.

9. [ ] After the push, open `https://gwelby.github.io/PFExplorer/` in a fresh
   incognito window and confirm that at least three panels (`god-equation`,
   `bohr`, `hub`) actually paint on the live URL. CDN cache can delay the
   deploy by roughly a minute — wait and reload, do not declare success on
   the first stale load.

## Why this checklist exists

Requirement 10 of the spec codifies "no silent deployments." Previous
release cycles declared fixes done the moment a git push succeeded, without
ever loading the result in a browser. That failure mode shipped broken
panels to the live URL multiple times.

The user's correction is the rule this checklist enforces:

> NEVER declare a fix done based on build pipeline success or git push
> alone — visual evidence required.

## Footer rules

- A green `check_panel_health.py` is necessary but not sufficient.
- A successful `git push` is not evidence the user's bug is fixed.
- The only thing that counts is a painted panel in a real browser window on
  the live URL.
