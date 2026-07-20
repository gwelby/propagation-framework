#!/usr/bin/env python3
"""D-Series Shared Status Validator

Per Codex 2026-07-15 formula-readiness gate repair contract:

1. One documented/executable status enum and deterministic reducer.
2. Shared validator with fixtures for READY, EXPLORATORY, BLOCKED, and
   unknown/undeclared failure paths.
3. Wire D1 through this validator; change EXPLORATORY output from prediction
   to neutral fitted-model/reconstruction wording.
4. Q3 distinguishes computational diagnostics from physical sigma,
   compatibility, or falsification decisions.
5. Inventory D-series quantitative tasks and prove each invokes the validator
   or is explicitly blocked/non-quantitative.

Usage:
    from d_series_validator import validate_preflight, Status, QStatus

    result = validate_preflight(
        task_id="D1",
        q1_status=QStatus.CLOSED,
        q2_status=QStatus.DECLARED,
        q3_status=QStatus.DECLARED,
        q3_decision_type="computational_diagnostic",
    )
    print(result.overall_status)  # Status.EXPLORATORY
"""

import enum
import json
from typing import Optional, Dict, Any


class Status(enum.Enum):
    """Overall task status enum — the single documented taxonomy."""
    READY = "READY"
    EXPLORATORY = "EXPLORATORY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return self.value


class QStatus(enum.Enum):
    """Per-question status enum."""
    CLOSED = "CLOSED"
    DECLARED = "DECLARED"
    OPEN = "OPEN"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return self.value


class Q3DecisionType(enum.Enum):
    """Q3 decision type — distinguishes computational diagnostics from
    physical sigma, compatibility, or falsification decisions."""
    COMPUTATIONAL_DIAGNOSTIC = "computational_diagnostic"
    PHYSICAL_SIGMA = "physical_sigma"
    COMPATIBILITY_TEST = "compatibility_test"
    FALSIFICATION_TEST = "falsification_test"
    NONE = "none"

    def __str__(self):
        return self.value


class ValidationResult:
    """Result of validating a D-series task preflight."""

    def __init__(
        self,
        task_id: str,
        overall_status: Status,
        q1_status: QStatus,
        q2_status: QStatus,
        q3_status: QStatus,
        q3_decision_type: Q3DecisionType,
        reducer_reason: str,
        allowed_language: str,
        disallowed_language: list,
    ):
        self.task_id = task_id
        self.overall_status = overall_status
        self.q1_status = q1_status
        self.q2_status = q2_status
        self.q3_status = q3_status
        self.q3_decision_type = q3_decision_type
        self.reducer_reason = reducer_reason
        self.allowed_language = allowed_language
        self.disallowed_language = disallowed_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "overall_status": str(self.overall_status),
            "q1_status": str(self.q1_status),
            "q2_status": str(self.q2_status),
            "q3_status": str(self.q3_status),
            "q3_decision_type": str(self.q3_decision_type),
            "reducer_reason": self.reducer_reason,
            "allowed_language": self.allowed_language,
            "disallowed_language": self.disallowed_language,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def _coerce_q(value) -> QStatus:
    """Coerce string or QStatus to QStatus."""
    if isinstance(value, QStatus):
        return value
    if isinstance(value, str):
        try:
            return QStatus(value.upper())
        except ValueError:
            return QStatus.UNKNOWN
    return QStatus.UNKNOWN


def _coerce_q3_decision(value) -> Q3DecisionType:
    """Coerce string or Q3DecisionType to Q3DecisionType."""
    if isinstance(value, Q3DecisionType):
        return value
    if isinstance(value, str):
        try:
            return Q3DecisionType(value.lower())
        except ValueError:
            return Q3DecisionType.NONE
    return Q3DecisionType.NONE


def status_reducer(
    task_id: str,
    q1_status,
    q2_status,
    q3_status,
    q3_decision_type=Q3DecisionType.NONE,
) -> ValidationResult:
    """
    Deterministic reducer: Q1/Q2/Q3 statuses → overall Status.

    Rules:
    - READY: all three Q statuses are CLOSED.
    - EXPLORATORY: all three Q statuses are at least DECLARED (CLOSED or
      DECLARED), but not all CLOSED.
    - BLOCKED: any Q status is OPEN or BLOCKED.
    - UNKNOWN: any Q status is UNKNOWN or unparseable.

    Q3 decision type further constrains allowed language:
    - COMPUTATIONAL_DIAGNOSTIC: may report chi^2, p-values as numerical
      outputs of the declared model. May NOT claim physical sigma,
      compatibility, or falsification.
    - PHYSICAL_SIGMA: may report sigma-based results (requires READY).
    - COMPATIBILITY_TEST: may claim compatibility/incompatibility (requires
      READY).
    - FALSIFICATION_TEST: may claim falsification (requires READY).
    - NONE: no decision-type language allowed.
    """
    q1 = _coerce_q(q1_status)
    q2 = _coerce_q(q2_status)
    q3 = _coerce_q(q3_status)
    dt = _coerce_q3_decision(q3_decision_type)

    statuses = [q1, q2, q3]

    # Check for UNKNOWN first
    if any(s == QStatus.UNKNOWN for s in statuses):
        overall = Status.UNKNOWN
        reason = "One or more Q statuses is UNKNOWN or unparseable."
    elif any(s in (QStatus.OPEN, QStatus.BLOCKED) for s in statuses):
        overall = Status.BLOCKED
        blocked = [f"Q{i+1}" for i, s in enumerate(statuses)
                   if s in (QStatus.OPEN, QStatus.BLOCKED)]
        reason = f"Blocked by: {', '.join(blocked)}"
    elif all(s == QStatus.CLOSED for s in statuses):
        overall = Status.READY
        reason = "All three checks are CLOSED."
    else:
        # All at least DECLARED, not all CLOSED
        overall = Status.EXPLORATORY
        reason = "All checks at least DECLARED, but not all CLOSED."

    # Determine allowed/disallowed language based on status + decision type
    if overall == Status.READY:
        if dt == Q3DecisionType.PHYSICAL_SIGMA:
            allowed = "May report sigma-based results, fitted-model values, and reconstruction outputs."
            disallowed = ["falsification claim", "compatibility verdict"]
        elif dt == Q3DecisionType.COMPATIBILITY_TEST:
            allowed = "May report compatibility/incompatibility verdicts and fitted-model values."
            disallowed = ["falsification claim", "physical sigma claim"]
        elif dt == Q3DecisionType.FALSIFICATION_TEST:
            allowed = "May report falsification verdicts and fitted-model values."
            disallowed = []
        else:
            allowed = "May report fitted-model values and reconstruction outputs."
            disallowed = ["prediction", "physical sigma", "compatibility verdict", "falsification claim"]
    elif overall == Status.EXPLORATORY:
        if dt == Q3DecisionType.COMPUTATIONAL_DIAGNOSTIC:
            allowed = ("May report chi^2, p-values, and numerical outputs as "
                       "computational diagnostics of the declared model. "
                       "May use 'fitted-model value' and 'reconstruction output' wording.")
            disallowed = [
                "prediction",
                "physical sigma",
                "compatibility verdict",
                "falsification claim",
                "statistical test",
            ]
        else:
            allowed = ("May report fitted-model values and reconstruction "
                       "outputs only. Numerical diagnostics must be labeled "
                       "as computational, not physical.")
            disallowed = [
                "prediction",
                "physical sigma",
                "compatibility verdict",
                "falsification claim",
                "statistical test",
            ]
    elif overall == Status.BLOCKED:
        allowed = "No quantitative output is valid until the blocking check is resolved."
        disallowed = [
            "prediction",
            "physical sigma",
            "compatibility verdict",
            "falsification claim",
            "statistical test",
            "fitted-model value",
        ]
    else:  # UNKNOWN
        allowed = "Status is unknown. No quantitative output is valid."
        disallowed = [
            "prediction",
            "physical sigma",
            "compatibility verdict",
            "falsification claim",
            "statistical test",
            "fitted-model value",
        ]

    return ValidationResult(
        task_id=task_id,
        overall_status=overall,
        q1_status=q1,
        q2_status=q2,
        q3_status=q3,
        q3_decision_type=dt,
        reducer_reason=reason,
        allowed_language=allowed,
        disallowed_language=disallowed,
    )


def validate_preflight(
    task_id: str,
    q1_status,
    q2_status,
    q3_status,
    q3_decision_type=Q3DecisionType.NONE,
) -> ValidationResult:
    """Validate a D-series task preflight. Alias for status_reducer."""
    return status_reducer(task_id, q1_status, q2_status, q3_status, q3_decision_type)


def check_language(result: ValidationResult, text: str) -> list:
    """
    Check text for disallowed language given the validation result.
    Returns a list of violations found.
    """
    violations = []
    text_lower = text.lower()
    for term in result.disallowed_language:
        if term.lower() in text_lower:
            violations.append(term)
    return violations


# Paths in a D-series JSON artifact that are policy metadata, not user-facing
# output. These are excluded from the structured artifact scan.
_POLICY_PATHS = {
    "preflight.disallowed_language",
    "preflight.allowed_language",
    "preflight.reducer_reason",
}


def scan_artifact(result: ValidationResult, artifact: dict) -> list:
    """
    Structured scan of a D-series JSON artifact for disallowed language.

    Walks all keys and string values in the artifact, excluding policy metadata
    paths (preflight.disallowed_language, etc.). Returns a list of violations,
    each as a (path, term, value_snippet) tuple.

    Negation context: terms appearing in explicit negation phrases such as
    "No falsification claim" or "not a statistical test" are NOT violations.
    A term is in negation context if it is preceded by "no ", "not a ", "not ",
    "cannot ", or "is not " within the same string value.
    """
    import re

    violations = []

    # Words that break a negation phrase; a negation before one of these
    # cannot govern a term on the far side.
    _NEGATION_BLOCKERS = {
        "but", "however", "yet", "though", "although", "nevertheless",
        "nonetheless", "only", "just", "also", "merely", "then", "therefore",
        "so", "thus", "hence", "if", "because", "since", "while", "whereas",
    }

    # Clause/sentence splitters. A negation in one clause cannot exempt a term
    # in another clause separated by one of these.
    _CLAUSE_SPLIT_RE = re.compile(
        r"(?:"
        r"\.\s+|"              # sentence end
        r";\s+|"               # semicolon
        r",?\s*\bbut\b\s+|"   # but (optionally after comma)
        r"\bhowever\b\s+|"    # however
        r"\byet\b\s+|"        # yet
        r"\bthough\b\s+|"      # though
        r"\balthough\b\s+"     # although
        r")",
        re.IGNORECASE,
    )

    # Allowed negation phrases that can govern a following term, with up to
    # three modifier words between the negation and the term. The modifiers
    # must not be blockers above (e.g. "only", "but").
    _NEGATION_PHRASE_RE = re.compile(
        r"(?:^|.*\s)"  # any prefix, last whitespace before negation
        r"(?:"
        r"no|"
        r"not\s+a|"
        r"not|"
        r"cannot(?:\s+be(?:\s+a)?)?|"
        r"is\s+not(?:\s+a)?|"
        r"are\s+not(?:\s+a)?|"
        r"no\s+sigma-based"
        r")"
        r"\s+"
        r"(?:(?!" + r"|".join(re.escape(w) for w in _NEGATION_BLOCKERS) + r")\b[\w-]+\b\s+){0,3}"
        r"$",
        re.IGNORECASE | re.VERBOSE,
    )

    def _is_negated(text_lower, term_lower, pos):
        """Check if term at position pos is governed by a negation phrase.

        A term is only in negation context when the negation phrase directly
        precedes it in the same clause, with no intervening clause breaker or
        blocker word. Earlier sentence negation does not blanket-exempt later
        affirmative uses (e.g. "not a statistical test, but it makes a
        falsification claim" flags the second clause).
        """
        # Find clause start: last clause splitter before term
        clause_start = 0
        for m in _CLAUSE_SPLIT_RE.finditer(text_lower[:pos]):
            clause_start = m.end()
        clause = text_lower[clause_start:]
        term_pos_in_clause = pos - clause_start
        prefix = clause[:term_pos_in_clause]
        if not prefix.strip():
            return False
        return bool(_NEGATION_PHRASE_RE.search(prefix))

    def _walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                child_path = f"{path}.{k}" if path else k
                if child_path in _POLICY_PATHS:
                    continue
                # Check the key name itself against disallowed terms
                # Key names are never in negation context
                for term in result.disallowed_language:
                    tl = term.lower()
                    if tl in k.lower():
                        violations.append((child_path, term, f"KEY:{k}"))
                _walk(v, child_path)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _walk(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            # Check the string value with negation awareness
            obj_lower = obj.lower()
            for term in result.disallowed_language:
                tl = term.lower()
                search_pos = 0
                while True:
                    pos = obj_lower.find(tl, search_pos)
                    if pos == -1:
                        break
                    if not _is_negated(obj_lower, tl, pos):
                        violations.append((path, term, obj[:80]))
                        break  # one violation per term per string
                    search_pos = pos + len(tl)

    _walk(artifact)
    return violations


# ============================================================================
# Self-test fixtures
# ============================================================================

def _run_fixtures():
    """Run all fixture cases and return results."""
    fixtures = []

    # Fixture 1: READY (all CLOSED, physical sigma)
    r = validate_preflight("FIXTURE_READY", "CLOSED", "CLOSED", "CLOSED",
                           Q3DecisionType.PHYSICAL_SIGMA)
    fixtures.append(("READY", r))
    assert r.overall_status == Status.READY, f"Expected READY, got {r.overall_status}"

    # Fixture 2: EXPLORATORY (all DECLARED, computational diagnostic)
    r = validate_preflight("FIXTURE_EXPLORATORY", "CLOSED", "DECLARED", "DECLARED",
                           Q3DecisionType.COMPUTATIONAL_DIAGNOSTIC)
    fixtures.append(("EXPLORATORY", r))
    assert r.overall_status == Status.EXPLORATORY, f"Expected EXPLORATORY, got {r.overall_status}"

    # Fixture 3: BLOCKED (one OPEN)
    r = validate_preflight("FIXTURE_BLOCKED", "CLOSED", "OPEN", "DECLARED")
    fixtures.append(("BLOCKED", r))
    assert r.overall_status == Status.BLOCKED, f"Expected BLOCKED, got {r.overall_status}"

    # Fixture 4: UNKNOWN (unparseable status)
    r = validate_preflight("FIXTURE_UNKNOWN", "CLOSED", "GARBLED", "DECLARED")
    fixtures.append(("UNKNOWN", r))
    assert r.overall_status == Status.UNKNOWN, f"Expected UNKNOWN, got {r.overall_status}"

    # Fixture 5: EXPLORATORY with NONE decision type
    r = validate_preflight("FIXTURE_EXPLORATORY_NONE", "CLOSED", "DECLARED", "DECLARED",
                           Q3DecisionType.NONE)
    fixtures.append(("EXPLORATORY_NONE", r))
    assert r.overall_status == Status.EXPLORATORY

    # Fixture 6: READY with falsification
    r = validate_preflight("FIXTURE_READY_FALSIFICATION", "CLOSED", "CLOSED", "CLOSED",
                           Q3DecisionType.FALSIFICATION_TEST)
    fixtures.append(("READY_FALSIFICATION", r))
    assert r.overall_status == Status.READY

    # Negative test: EXPLORATORY should reject "prediction"
    r_exp = validate_preflight("FIXTURE_LANG_CHECK", "CLOSED", "DECLARED", "DECLARED",
                               Q3DecisionType.COMPUTATIONAL_DIAGNOSTIC)
    violations = check_language(r_exp, "This is a prediction of the model.")
    assert "prediction" in violations, "EXPLORATORY should flag 'prediction'"

    # Negative test: BLOCKED should reject "fitted-model value"
    r_blk = validate_preflight("FIXTURE_BLK_LANG", "CLOSED", "OPEN", "DECLARED")
    violations = check_language(r_blk, "The fitted-model value is 4.3.")
    assert "fitted-model value" in violations, "BLOCKED should flag 'fitted-model value'"

    # Fixture 7: Structured artifact scan — clean D1 artifact passes
    r_art = validate_preflight("D1", "CLOSED", "DECLARED", "DECLARED",
                               Q3DecisionType.COMPUTATIONAL_DIAGNOSTIC)
    clean_artifact = {
        "task": "D1",
        "status": "EXPLORATORY",
        "preflight": {
            "overall_status": "EXPLORATORY",
            "disallowed_language": ["prediction", "physical sigma"],
            "allowed_language": "May report chi^2.",
        },
        "free_fit": {
            "up": {"fitted_model_values": [2.16, 1273.0, 172570.0]},
        },
    }
    art_violations = scan_artifact(r_art, clean_artifact)
    assert not art_violations, f"Clean artifact should have no violations: {art_violations}"
    fixtures.append(("ARTIFACT_CLEAN", r_art))

    # Fixture 8: Structured artifact scan — injected "prediction" key fails
    dirty_artifact = {
        "task": "D1",
        "status": "EXPLORATORY",
        "preflight": {
            "overall_status": "EXPLORATORY",
            "disallowed_language": ["prediction", "physical sigma"],
        },
        "free_fit": {
            "up": {"predictions": [2.16, 1273.0, 172570.0]},
        },
    }
    art_violations = scan_artifact(r_art, dirty_artifact)
    assert art_violations, "Dirty artifact with 'predictions' key should fail"
    assert any("prediction" in v[1] for v in art_violations), \
        f"Should flag 'prediction' in key: {art_violations}"
    fixtures.append(("ARTIFACT_DIRTY", r_art))

    # Fixture 9: Contrast sentences — earlier negation does not blanket-exempt
    # a later affirmative forbidden term
    contrast_artifact = {
        "task": "D1",
        "status": "EXPLORATORY",
        "preflight": {
            "overall_status": "EXPLORATORY",
            "disallowed_language": ["prediction", "physical sigma",
                                    "compatibility verdict", "falsification claim",
                                    "statistical test"],
        },
        "claim_boundary": (
            "This is not a statistical test, but it makes a falsification claim. "
            "No statistical test is claimed, but this is a compatibility verdict. "
            "This is not a statistical test but the prediction is confirmed."
        ),
    }
    art_violations = scan_artifact(r_art, contrast_artifact)
    assert art_violations, "Contrast artifact must fail on the affirmative clauses"
    flagged = {v[1] for v in art_violations}
    assert "falsification claim" in flagged, f"Should flag falsification claim: {art_violations}"
    assert "compatibility verdict" in flagged, f"Should flag compatibility verdict: {art_violations}"
    assert "prediction" in flagged, f"Should flag prediction: {art_violations}"
    # The negated 'statistical test' phrases must NOT be flagged
    assert "statistical test" not in flagged, f"Should not flag negated statistical test: {art_violations}"
    fixtures.append(("ARTIFACT_CONTRAST", r_art))

    # Fixture 10: Direct negation boundaries still permitted
    neg_boundary_artifact = {
        "task": "D1",
        "status": "EXPLORATORY",
        "preflight": {
            "overall_status": "EXPLORATORY",
            "disallowed_language": ["falsification claim", "statistical test"],
        },
        "claim_boundary": (
            "No falsification claim. not a closed statistical test."
        ),
    }
    art_violations = scan_artifact(r_art, neg_boundary_artifact)
    assert not art_violations, f"Direct negation boundaries should pass: {art_violations}"
    fixtures.append(("ARTIFACT_NEG_BOUNDARY", r_art))

    return fixtures


if __name__ == "__main__":
    print("=== D-Series Validator Self-Test ===")
    print()
    fixtures = _run_fixtures()
    for name, r in fixtures:
        print(f"[PASS] {name}: {r.overall_status}")
    print()
    print(f"All {len(fixtures)} fixtures passed.")
    print()

    # Print D1 expected status
    print("=== D1 Expected Status ===")
    d1 = validate_preflight("D1", "CLOSED", "DECLARED", "DECLARED",
                            Q3DecisionType.COMPUTATIONAL_DIAGNOSTIC)
    print(d1.to_json())
    print()
    print("All tests passed.")
