
import pytest
from decimal import Decimal
import math

from cases.case04 import CreditService  # type: ignore

# Note: The implementation of CreditService is not provided, but the tests strictly follow the interface defined:
# CreditService.evaluate(score: int, income: decimal, age: int) -> "APPROVED" | "DENIED"
# We assume the class CreditService exists for the purpose of these tests.

# Initialize service for testing
@pytest.fixture
def service():
    return CreditService()

# --- BR01: Credit may only be approved if score >= 700, income >= 5000, age >= 21 ---
# --- FR03: Return exclusively "APPROVED" or "DENIED" ---

def test_evaluate_returns_approved_when_all_criteria_met_exact_boundary(service):
    # BR01, FR03 - Exact boundary values for approval
    # Score = 700, Income = 5000, Age = 21
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"

def test_evaluate_returns_approved_when_all_criteria_exceed_boundary(service):
    # BR01, FR03 - Values exceeding minimums
    result = service.evaluate(score=701, income=Decimal("5000.01"), age=22)
    assert result == "APPROVED"

# --- BR02: If any of the criteria fail, the credit must be denied ---

def test_evaluate_returns_denied_when_score_is_below_700(service):
    # BR02 - Score violation (699 < 700)
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"

def test_evaluate_returns_denied_when_income_is_below_5000(service):
    # BR02 - Income violation (4999.99 < 5000)
    result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
    assert result == "DENIED"

def test_evaluate_returns_denied_when_age_is_below_21(service):
    # BR02 - Age violation (20 < 21)
    result = service.evaluate(score=700, income=Decimal("5000"), age=20)
    assert result == "DENIED"

def test_evaluate_returns_denied_when_multiple_criteria_fail(service):
    # BR02 - Multiple violations (Score < 700, Age < 21)
    result = service.evaluate(score=600, income=Decimal("5000"), age=18)
    assert result == "DENIED"

# --- BR03: Values as NaN or Infinity are not allowed and must result in an exception ---
# --- FR05: Raise an exception whenever any validation failure occurs, including magic values ---

def test_evaluate_raises_exception_on_nan_income(service):
    # BR03, FR05 - Income is NaN
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)

def test_evaluate_raises_exception_on_infinity_income(service):
    # BR03, FR05 - Income is Infinity
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)

def test_evaluate_raises_exception_on_float_nan_income(service):
    # BR03, FR05 - Income is float NaN (if passed despite type hint, system must validate)
    with pytest.raises(Exception):
        service.evaluate(score=700, income=math.nan, age=21)

# --- BR04: Criteria must be validated according to types and constraints ---
# Score: positive integer, Income: positive decimal, Age: positive integer
# --- FR05: Raise exception on invalid type or validation failure ---

def test_evaluate_raises_exception_on_negative_score(service):
    # BR04, FR05 - Score must be positive integer
    with pytest.raises(Exception):
        service.evaluate(score=-1, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_on_zero_score(service):
    # BR04, FR05 - Score must be positive integer (> 0 implied by positive, or non-negative? 
    # Strict 'positive' usually means > 0. Assuming > 0 based on "positive")
    with pytest.raises(Exception):
        service.evaluate(score=0, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_on_negative_income(service):
    # BR04, FR05 - Income must be positive decimal
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("-5000"), age=21)

def test_evaluate_raises_exception_on_negative_age(service):
    # BR04, FR05 - Age must be positive integer
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=-5)

def test_evaluate_raises_exception_on_invalid_score_type_float(service):
    # BR04, FR05 - Score must be integer
    with pytest.raises(Exception):
        service.evaluate(score=700.5, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_on_invalid_age_type_float(service):
    # BR04, FR05 - Age must be integer
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=21.5)

# --- BR05: Values must not be normalized or implicitly adjusted ---
# --- FR08: Do not perform any kind of normalization ---

def test_evaluate_raises_exception_or_denies_without_rounding_income(service):
    # BR05, FR08 - 4999.9999 is NOT 5000. It is < 5000.
    # Should be DENIED, not APPROVED.
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"

def test_evaluate_does_not_normalize_age_float_to_int(service):
    # BR05, FR08, BR04 - 20.9 must not be rounded to 21. 
    # Additionally, 20.9 is not an integer (BR04 violation). 
    # Must raise Exception (Validation Failure on Type) OR if handled as value check, fail strict rules.
    # Given BR04 requires "Age: positive integer value", passing a float violates the type rule.
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=20.9)

# --- BR06: Any validation failure must result in an exception ---
# --- FR05: Raise an exception whenever any validation failure occurs ---

def test_evaluate_raises_exception_on_missing_score(service):
    # BR06, FR05 - Missing argument (Python raises TypeError, fits general exception requirement)
    with pytest.raises(TypeError):
        service.evaluate(income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_on_missing_income(service):
    # BR06, FR05
    with pytest.raises(TypeError):
        service.evaluate(score=700, age=21)

def test_evaluate_raises_exception_on_missing_age(service):
    # BR06, FR05
    with pytest.raises(TypeError):
        service.evaluate(score=700, income=Decimal("5000"))

# --- BR07: The system must not infer, guess, or assume values ---

def test_evaluate_raises_exception_on_none_income(service):
    # BR07 - None is not a value, system cannot assume 0 or any defaults
    with pytest.raises(Exception):
        service.evaluate(score=700, income=None, age=21)

def test_evaluate_raises_exception_on_string_score_numeric(service):
    # BR07, BR04 - String "700" is not Integer 700. No casting/inference allowed.
    with pytest.raises(Exception):
        service.evaluate(score="700", income=Decimal("5000"), age=21)

# --- BR08: There are no intermediate approval levels ---
# --- FR03: Return exclusively "APPROVED" or "DENIED" ---

def test_evaluate_returns_exactly_approved_string(service):
    # BR08, FR03 - Result must be strictly "APPROVED"
    result = service.evaluate(score=800, income=Decimal("10000"), age=30)
    assert result == "APPROVED"
    assert result not in ["Approved", "approved", "PARTIALLY_APPROVED"]

def test_evaluate_returns_exactly_denied_string(service):
    # BR08, FR03 - Result must be strictly "DENIED"
    result = service.evaluate(score=600, income=Decimal("5000"), age=21)
    assert result == "DENIED"
    assert result not in ["Denied", "denied", "REJECTED"]

# --- BR09: Credit analysis is an indivisible operation ---
# --- FR09 (Implicit in indivisibility) / FR06: Do not return business result on exception ---
# --- FR07: Do not expose intermediate states ---

def test_evaluate_raises_exception_and_returns_no_result_on_invalid_input(service):
    # BR09, FR06 - If exception occurs, no return value exists (control flow interruption)
    # This validates that we don't get a tuple like (None, error) or similar "soft" errors.
    with pytest.raises(Exception):
        # Invalid score type triggers exception immediately
        result = service.evaluate(score="invalid", income=Decimal("5000"), age=21)
        # Verify execution never reaches assignment (implicit in pytest.raises)

# --- FR01: Evaluate using exclusively provided values (No inference) ---

def test_evaluate_does_not_use_external_defaults_for_low_income(service):
    # FR01, BR07 - Explicitly verifying that a value just below threshold is DENIED,
    # preventing any "default minimum wage" logic injection.
    result = service.evaluate(score=700, income=Decimal("4999"), age=21)
    assert result == "DENIED"

# --- FR02: Mandatory validation of all criteria ---

def test_evaluate_validates_all_criteria_simultaneously(service):
    # FR02 - Validates that if one is valid, it doesn't short-circuit return True without checking others.
    # Score OK, Income OK, Age BAD -> DENIED
    assert service.evaluate(score=700, income=Decimal("5000"), age=20) == "DENIED"
    # Score BAD, Income OK, Age OK -> DENIED
    assert service.evaluate(score=699, income=Decimal("5000"), age=21) == "DENIED"
    # Score OK, Income BAD, Age OK -> DENIED
    assert service.evaluate(score=700, income=Decimal("4999"), age=21) == "DENIED"

# --- FR04: Record exactly one analysis result ---
# Note: Since we are testing black-box behavior via return values, 'Recording' is implicitly tested 
# by the fact that we get a single deterministic return value. 
# However, purely functional tests cannot verify side-effects (database records) without mocks.
# We verify the return constraint.

def test_evaluate_returns_single_string_object(service):
    # FR04 - Ensuring return type is a single string, not a list or history
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert isinstance(result, str)
