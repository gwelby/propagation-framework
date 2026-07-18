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
