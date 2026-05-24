"""Unit tests for :mod:`verification.guardrails`.

Covers:
    * :func:`load_no_go_library` — hardcoded fallback returns the expected
      entries when AGENTS.md is not present; AGENTS.md / AGENTS_FULL.md
      table-row parsing layers on top of the fallback; derivation filename
      scan picks up ``*_no_go*.md`` files.
    * :meth:`Guardrails.check_protected_files` — BLOCK on protected board
      documents (basename-matched), empty list on unrelated files.
    * :meth:`Guardrails.check_no_go` — BLOCK on a documented no-go,
      empty list on unrelated approaches, case-insensitive matching.
    * :meth:`Guardrails.validate_truth_order` — WARN when sandbox
      contradicts framing without hedging, empty when hedged or when
      sandbox is not negative.
    * :meth:`Guardrails.validate_no_score_change` — BLOCK on any score
      drift; empty when scores match; BLOCK on injected or dropped claim.

References:
- `.kiro/specs/propagation-framework-verification/requirements.md` Req. 6.
- `.kiro/specs/propagation-framework-verification/tasks.md` Task 6.6.
- ``verification/guardrails.py`` for the module under test.

All tests are self-contained. AGENTS.md / derivations/ are constructed via
``tmp_path`` to avoid depending on the live workspace state.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from verification.guardrails import (
    DEFAULT_PROTECTED_FILES,
    HARDCODED_NO_GO_FALLBACK,
    GuardrailViolation,
    Guardrails,
    load_no_go_library,
)


# ---------------------------------------------------------------------------
# load_no_go_library
# ---------------------------------------------------------------------------


class TestLoadNoGoLibrary:
    """Tests for :func:`load_no_go_library`."""

    def test_fallback_when_agents_md_missing(self, tmp_path: Path) -> None:
        """With no AGENTS.md, the hardcoded fallback is returned intact."""

        missing = tmp_path / "does_not_exist_AGENTS.md"
        library = load_no_go_library(missing)

        # All hardcoded entries must be present.
        for key, reason in HARDCODED_NO_GO_FALLBACK.items():
            assert key in library
            assert library[key] == reason

    def test_fallback_when_path_is_none(self) -> None:
        """``None`` path short-circuits to the hardcoded cache."""

        library = load_no_go_library(None)

        assert "harmonic series mass ratios" in library
        assert "CV=0.94" in library["harmonic series mass ratios"]
        assert "b = 0 chiral closure" in library

    def test_parses_agents_md_no_go_table(self, tmp_path: Path) -> None:
        """Rows from an AGENTS.md no-go table are added to the library."""

        agents = tmp_path / "AGENTS.md"
        agents.write_text(
            "# Intro\n\n"
            "Some prose.\n\n"
            "## THE NO-GO LIBRARY\n\n"
            "| Approach | File | Why It Failed |\n"
            "|----------|------|---------------|\n"
            "| Made-up toy approach | toy.md | gives zero every time |\n"
            "| Another toy | other.md | breaks symmetry prematurely |\n\n"
            "## Next Section\n\n"
            "| Unrelated | stuff | here |\n",
            encoding="utf-8",
        )

        library = load_no_go_library(agents)

        assert "Made-up toy approach" in library
        assert "gives zero every time" in library["Made-up toy approach"]
        assert "Another toy" in library
        assert "breaks symmetry prematurely" in library["Another toy"]
        # Rows outside the section stay out.
        assert "Unrelated" not in library

    def test_derivations_no_go_filenames_are_picked_up(
        self, tmp_path: Path
    ) -> None:
        """Files in ``derivations/`` with ``_no_go`` in the name become entries."""

        agents = tmp_path / "AGENTS.md"
        agents.write_text("# Empty AGENTS\n", encoding="utf-8")
        deriv = tmp_path / "derivations"
        deriv.mkdir()
        (deriv / "some_approach_no_go_2026-04-01.md").write_text(
            "# Some approach failed\n", encoding="utf-8"
        )
        (deriv / "no_go_other_thing.md").write_text(
            "# Other thing failed\n", encoding="utf-8"
        )
        (deriv / "ok_thing.md").write_text("# Fine\n", encoding="utf-8")

        library = load_no_go_library(agents, derivations_dir=deriv)

        keys = list(library.keys())
        # The cleaned approach names (date stripped, underscores replaced).
        assert any("some approach" in k for k in keys)
        assert any("other thing" in k for k in keys)
        # Files without the marker are ignored.
        assert not any("ok thing" == k for k in keys)


# ---------------------------------------------------------------------------
# Guardrails.check_protected_files
# ---------------------------------------------------------------------------


class TestCheckProtectedFiles:
    """Tests for :meth:`Guardrails.check_protected_files`."""

    def test_blocks_claims_md(self) -> None:
        g = Guardrails()
        violations = g.check_protected_files(["CLAIMS.md"])

        assert len(violations) == 1
        v = violations[0]
        assert v.rule == "PROTECTED_FILE"
        assert v.severity == "BLOCK"
        assert "CLAIMS.md" in v.details

    def test_empty_for_unrelated_file(self) -> None:
        g = Guardrails()
        assert g.check_protected_files(["some_other.md"]) == []

    def test_blocks_all_three_board_documents(self) -> None:
        g = Guardrails()
        violations = g.check_protected_files(list(DEFAULT_PROTECTED_FILES))

        assert len(violations) == 3
        assert {v.severity for v in violations} == {"BLOCK"}
        rules = {v.rule for v in violations}
        assert rules == {"PROTECTED_FILE"}

    def test_matches_on_basename(self) -> None:
        """Absolute / nested paths still trip the rule by basename."""

        g = Guardrails()
        violations = g.check_protected_files(
            ["/abs/path/to/CLAIMS.md", "subdir/WHATS_NEXT.md"]
        )

        assert len(violations) == 2
        assert all(v.severity == "BLOCK" for v in violations)

    def test_empty_list_for_empty_input(self) -> None:
        assert Guardrails().check_protected_files([]) == []


# ---------------------------------------------------------------------------
# Guardrails.check_no_go
# ---------------------------------------------------------------------------


class TestCheckNoGo:
    """Tests for :meth:`Guardrails.check_no_go`."""

    def test_blocks_harmonic_series_attempt(self) -> None:
        g = Guardrails()
        violations = g.check_no_go(
            "I'll try harmonic series mass ratios again"
        )

        assert len(violations) >= 1
        assert any(v.rule == "NO_GO" and v.severity == "BLOCK" for v in violations)
        # The documented reason / source should surface.
        assert any("CV=0.94" in v.details for v in violations)

    def test_empty_for_unrelated_approach(self) -> None:
        g = Guardrails()
        assert g.check_no_go("unrelated approach") == []

    def test_empty_for_empty_approach(self) -> None:
        g = Guardrails()
        assert g.check_no_go("") == []

    def test_case_insensitive_matching(self) -> None:
        g = Guardrails()
        violations = g.check_no_go("HARMONIC SERIES MASS RATIOS revisited")

        assert len(violations) >= 1
        assert all(v.rule == "NO_GO" for v in violations)


# ---------------------------------------------------------------------------
# Guardrails.validate_truth_order
# ---------------------------------------------------------------------------


class TestValidateTruthOrder:
    """Tests for :meth:`Guardrails.validate_truth_order`."""

    def test_flags_when_sandbox_contradicts_framing(self) -> None:
        g = Guardrails()
        violations = g.validate_truth_order(
            claim_framing="Q=2/3 is DERIVED",
            sandbox_result_summary="Monte Carlo shows Q=0.55, contradicts 2/3",
        )

        assert len(violations) == 1
        v = violations[0]
        assert v.rule == "TRUTH_ORDER"
        assert v.severity == "WARN"
        assert "sandbox" in v.details.lower()

    def test_empty_when_framing_is_hedged(self) -> None:
        g = Guardrails()
        violations = g.validate_truth_order(
            claim_framing="Q=2/3 is ARGUED, pending JUNO data",
            sandbox_result_summary="Monte Carlo shows Q=0.55, contradicts 2/3",
        )

        assert violations == []

    def test_empty_when_sandbox_is_supportive(self) -> None:
        g = Guardrails()
        violations = g.validate_truth_order(
            claim_framing="Q=2/3 is DERIVED",
            sandbox_result_summary="Monte Carlo shows Q=0.667, matches 2/3",
        )

        assert violations == []

    def test_empty_when_both_empty(self) -> None:
        g = Guardrails()
        assert g.validate_truth_order("", "") == []


# ---------------------------------------------------------------------------
# Guardrails.validate_no_score_change
# ---------------------------------------------------------------------------


class TestValidateNoScoreChange:
    """Tests for :meth:`Guardrails.validate_no_score_change`."""

    def test_blocks_on_score_drift(self) -> None:
        g = Guardrails()
        violations = g.validate_no_score_change(
            before_scores={"god_equation": 0.88},
            after_scores={"god_equation": 0.90},
        )

        assert len(violations) == 1
        v = violations[0]
        assert v.rule == "SCORE_CHANGE"
        assert v.severity == "BLOCK"
        assert "god_equation" in v.details
        assert "0.88" in v.details and "0.9" in v.details

    def test_empty_when_scores_match(self) -> None:
        g = Guardrails()
        violations = g.validate_no_score_change(
            before_scores={"god_equation": 0.88},
            after_scores={"god_equation": 0.88},
        )

        assert violations == []

    def test_blocks_on_injected_claim(self) -> None:
        g = Guardrails()
        violations = g.validate_no_score_change(
            before_scores={"god_equation": 0.88},
            after_scores={"god_equation": 0.88, "new_claim": 0.5},
        )

        assert len(violations) == 1
        assert violations[0].severity == "BLOCK"
        assert "new_claim" in violations[0].details

    def test_blocks_on_dropped_claim(self) -> None:
        g = Guardrails()
        violations = g.validate_no_score_change(
            before_scores={"god_equation": 0.88, "koide_q": 0.92},
            after_scores={"god_equation": 0.88},
        )

        assert len(violations) == 1
        assert violations[0].severity == "BLOCK"
        assert "koide_q" in violations[0].details

    def test_empty_for_both_empty(self) -> None:
        g = Guardrails()
        assert g.validate_no_score_change({}, {}) == []


# ---------------------------------------------------------------------------
# Integration: GuardrailViolation shape
# ---------------------------------------------------------------------------


class TestGuardrailViolationShape:
    """Sanity checks on the violation record surface."""

    def test_severity_values_are_documented(self) -> None:
        """All produced violations use BLOCK or WARN."""

        g = Guardrails()

        all_violations: list[GuardrailViolation] = []
        all_violations += g.check_protected_files(["CLAIMS.md"])
        all_violations += g.check_no_go("harmonic series mass ratios")
        all_violations += g.validate_truth_order(
            "DERIVED", "fails to reproduce"
        )
        all_violations += g.validate_no_score_change({"c": 0.1}, {"c": 0.2})

        assert all_violations, "sanity: expected some violations"
        for v in all_violations:
            assert v.severity in {"BLOCK", "WARN"}
            assert v.rule
            assert v.details


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-v"]))
