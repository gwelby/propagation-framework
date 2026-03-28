# Propagation Framework Explorer — Wave 2 Notes

Date: `2026-03-26`

This note records what Wave 2 actually shipped. It replaces earlier overclaims.

## Shipped

- Dashboard filter chips now render once and update in place.
- Dashboard search and status filters combine consistently.
- Dashboard cards support explicit inline audit expansion for:
  - falsifier text
  - source list
- Hub panel uses the shared runtime result-to-panel mapping for linked routes.
- Hub pointer handling is pointer-safe instead of mouse-only.
- God Equation panel now contains:
  - a dependency chain for the conditional proof spine
  - explicit A / B / C gap cards
  - compact visuals for locality vs Markovity and covariance vs factorization
- The evidence drawer now defaults closed on narrow layouts and behaves as an overlay there.
- README has been truth-synced to shipped features.

## Explicitly Not Shipped

These remain planned and should not be described as present:

- Belt trick / Dirac string animation
- Refraction analytic error metrics
- Koide / Weinberg RG bridge view
- Bohr spectral-line diagram

## Status

Wave 2 is still static, dependency-free, and claim-neutral:

- no new derivations
- no claim-status upgrades
- no runtime document parsing

The purpose of this wave is audit clarity, not theory inflation.
