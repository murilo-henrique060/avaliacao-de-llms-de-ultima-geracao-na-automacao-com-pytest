
import pytest
from decimal import Decimal
import math

from cases.case04 import CreditService  # type: ignore

# --- Mocking the Class under test for context (as per instruction "Do not implement the system", 
# but tests need an interface to call. Assuming CreditService.evaluate exists as per UML).
# In a real scenario, this would be imported. 
# The tests below assume the existence of a class `CreditService` with a static or instance method `evaluate`.

@pytest.fixture
def credit_service():
    return CreditService()

# --- BR01: Credit may only be approved if Score >= 700, Income >= 5000, Age >= 21 ---

def test_evaluate_returns_approved_when_all_criteria_met_exact_boundary(credit_service):
    # BR01, FR03 - Validates approval on exact boundaries
    # Score = 700, Income = 5000, Age = 21
    assert credit_service.evaluate(score=700, income=Decimal("5000"), age=21) == "APPROVED"

def test_evaluate_returns_approved_when_all_criteria_met_above_boundary(credit_service):
    # BR01, FR03 - Validates approval well above boundaries
    assert credit_service.evaluate(score=750, income=Decimal("10000.50"), age=30) == "APPROVED"

# --- BR02: If any of the criteria fail, the credit must be denied ---

def test_evaluate_returns_denied_when_score_is_below_700(credit_service):
    # BR02, FR03 - Denied due to Score < 700 (Score boundary - 1)
    # Income and Age are valid
    assert credit_service.evaluate(score=699, income=Decimal("5000"), age=21) == "DENIED"

def test_evaluate_returns_denied_when_income_is_below_5000(credit_service):
    # BR02, FR03 - Denied due to Income < 5000 (Income boundary - small epsilon)
    # Score and Age are valid
    assert credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21) == "DENIED"

def test_evaluate_returns_denied_when_age_is_below_21(credit_service):
    # BR02, FR03 - Denied due to Age < 21 (Age boundary - 1)
    # Score and Income are valid
    assert credit_service.evaluate(score=700, income=Decimal("5000"), age=20) == "DENIED"

def test_evaluate_returns_denied_when_multiple_criteria_fail(credit_service):
    # BR02, FR03 - Denied when all criteria fail
    assert credit_service.evaluate(score=699, income=Decimal("4999"), age=20) == "DENIED"

# --- BR03: Values as NaN or Infinity are not allowed and must result in an exception ---

def test_evaluate_raises_exception_when_score_is_infinity(credit_service):
    # BR03, FR05 - Exception for Infinity in Score
    with pytest.raises(Exception):
        credit_service.evaluate(score=float('inf'), income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_when_income_is_nan(credit_service):
    # BR03, FR05 - Exception for NaN in Income
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=Decimal('NaN'), age=21)

def test_evaluate_raises_exception_when_age_is_infinity(credit_service):
    # BR03, FR05 - Exception for Infinity in Age
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=Decimal("5000"), age=float('inf'))

# --- BR04: Criteria must be validated according to types and constraints ---
# Score: positive integer, Income: positive decimal, Age: positive integer

def test_evaluate_raises_exception_when_score_is_negative(credit_service):
    # BR04, FR05 - Exception for negative Score
    with pytest.raises(Exception):
        credit_service.evaluate(score=-1, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_when_score_is_zero(credit_service):
    # BR04 (Score positive), FR05 - Exception for zero Score (assuming positive > 0)
    with pytest.raises(Exception):
        credit_service.evaluate(score=0, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_when_score_is_decimal_type(credit_service):
    # BR04 (Score integer), FR05 - Exception for non-integer type Score
    with pytest.raises(Exception):
        credit_service.evaluate(score=700.5, income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_when_income_is_negative(credit_service):
    # BR04, FR05 - Exception for negative Income
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=Decimal("-5000"), age=21)

def test_evaluate_raises_exception_when_income_is_integer_type(credit_service):
    # BR04 (Income decimal), FR05 - Exception for integer type Income (Strict type check implied by FR01 "exclusively provided values")
    # Note: If implementation allows int to cast to Decimal, this might pass in loose systems, 
    # but based on "Strict validations" and "Invalid type" in FR05, we expect strictness.
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000, age=21)

def test_evaluate_raises_exception_when_age_is_negative(credit_service):
    # BR04, FR05 - Exception for negative Age
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=Decimal("5000"), age=-21)

def test_evaluate_raises_exception_when_age_is_decimal_type(credit_service):
    # BR04 (Age integer), FR05 - Exception for non-integer type Age
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=Decimal("5000"), age=21.5)

# --- BR05: Values must not be normalized or implicitly adjusted ---

def test_evaluate_denies_approval_on_unrounded_income_just_below_threshold(credit_service):
    # BR05, FR08 - 4999.9999 must not be rounded to 5000
    assert credit_service.evaluate(score=700, income=Decimal("4999.9999"), age=21) == "DENIED"

def test_evaluate_raises_exception_for_float_income_to_avoid_precision_issues(credit_service):
    # BR05, FR08 - Float inputs might imply normalization/precision loss. 
    # Specification requires Decimal logic or strict handling. 
    # Passing a float (e.g. 5000.00) might be considered a type violation under BR04/FR05.
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.00, age=21)

# --- BR06 & FR05: Any validation failure must result in an exception ---

def test_evaluate_raises_exception_on_missing_score(credit_service):
    # BR06, FR05 - Missing argument validation
    with pytest.raises(TypeError): # Python raises TypeError for missing args
        credit_service.evaluate(income=Decimal("5000"), age=21)

def test_evaluate_raises_exception_on_none_values(credit_service):
    # BR06, FR05 - None value validation
    with pytest.raises(Exception):
        credit_service.evaluate(score=None, income=Decimal("5000"), age=21)

# --- BR07: The system must not infer, guess, or assume values ---

def test_evaluate_raises_exception_on_empty_string_input(credit_service):
    # BR07, FR05 - Empty string should not be parsed to 0 or raised as ValueError
    with pytest.raises(Exception):
        credit_service.evaluate(score="", income=Decimal("5000"), age=21)

# --- BR08: There are no intermediate approval levels ---

def test_evaluate_returns_denied_not_partial_on_high_score_low_income(credit_service):
    # BR08, FR03 - Result must be binary "DENIED", not "CONDITIONALLY APPROVED"
    assert credit_service.evaluate(score=999, income=Decimal("100"), age=30) == "DENIED"

# --- FR01: Evaluate using exclusively provided values ---

def test_evaluate_uses_exact_values_without_enrichment(credit_service):
    # FR01 - Validates that simple valid inputs return expected result without needing external data
    assert credit_service.evaluate(score=700, income=Decimal("5000"), age=21) == "APPROVED"

# --- FR04: Record exactly one analysis result ---
# Note: Since we are writing unit tests for the interface, we verify the return value is a single string.
# 'Recording' implies internal state or DB, typically verified via mocks, but here we strictly check output format constraints.

def test_evaluate_returns_single_string_result(credit_service):
    # FR04, FR03 - Result is a single string, not a list or object
    result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert type(result) is str
    assert result in ["APPROVED", "DENIED"]

# --- FR06: Do not return any business result when an exception is raised ---

def test_evaluate_does_not_return_denied_on_validation_error(credit_service):
    # FR06 - If input is invalid (e.g. negative age), it raises Exception, does NOT return "DENIED"
    try:
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=-5)
        pytest.fail(f"Should have raised Exception, but returned {result}")
    except Exception:
        pass # Expected behavior

# --- FR09: Credit analysis is an indivisible operation ---

def test_evaluate_is_atomic_no_partial_return(credit_service):
    # BR09 - The function call is atomic; it returns the final state directly.
    # This acts as a smoke test for the interface signature.
    result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"
