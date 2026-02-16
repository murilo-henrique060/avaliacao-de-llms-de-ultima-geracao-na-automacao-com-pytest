
import pytest
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Assuming CreditService follows the UML: evaluate(score: int, income: decimal, age: int)
# Since the implementation is not provided, we refer to the class and method name.

def test_br01_fr03_credit_approved_at_minimum_boundary():
    """Validates credit is APPROVED when all criteria meet the exact minimum threshold."""
    # BR01 – Score ≥ 700, Income ≥ 5,000, Age ≥ 21
    # FR03 – Return exclusively "APPROVED" or "DENIED"
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
    assert result == "APPROVED"

def test_br01_br02_denied_score_below_limit():
    """Validates credit is DENIED when score is exactly one unit below the limit."""
    # BR01 – Score must be ≥ 700
    # BR02 – If any criteria fail, credit must be denied
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal("5000.00"), age=21)
    assert result == "DENIED"

def test_br01_br02_denied_income_below_limit():
    """Validates credit is DENIED when income is exactly 0.01 below the limit."""
    # BR01 – Income must be ≥ 5,000
    # BR02 – If any criteria fail, credit must be denied
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
    assert result == "DENIED"

def test_br01_br02_denied_age_below_limit():
    """Validates credit is DENIED when age is exactly one unit below the limit."""
    # BR01 – Age must be ≥ 21
    # BR02 – If any criteria fail, credit must be denied
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=20)
    assert result == "DENIED"

def test_br03_fr05_income_nan_raises_exception():
    """Validates that NaN income results in an exception."""
    # BR03 – NaN values are not allowed and must result in an exception
    # FR05 – Raise exception on magic values (NaN)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)

def test_br03_fr05_income_infinity_raises_exception():
    """Validates that Infinity income results in an exception."""
    # BR03 – Infinity values are not allowed and must result in an exception
    # FR05 – Raise exception on magic values (Infinity)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)

def test_br04_br06_fr05_score_invalid_type_float():
    """Validates that a non-integer score results in an exception."""
    # BR04 – Score must be a positive integer
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on invalid type
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700.5, income=Decimal("5000.00"), age=21)

def test_br04_br06_fr05_income_invalid_type_string():
    """Validates that a non-decimal income results in an exception."""
    # BR04 – Income must be a positive decimal
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on invalid type
    service = CreditService()
    with pytest.raises(Exception):
        # Passing string instead of decimal object
        service.evaluate(score=700, income="5000.00", age=21)

def test_br04_br06_fr05_age_invalid_type_float():
    """Validates that a non-integer age results in an exception."""
    # BR04 – Age must be a positive integer
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on invalid type
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000.00"), age=21.0)

def test_br04_br06_fr05_score_negative_value():
    """Validates that a negative score results in an exception."""
    # BR04 – Score must be positive
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on business rule violation
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=-1, income=Decimal("5000.00"), age=21)

def test_br04_br06_fr05_income_negative_value():
    """Validates that a negative income results in an exception."""
    # BR04 – Income must be positive
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on business rule violation
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("-0.01"), age=21)

def test_br04_br06_fr05_age_negative_value():
    """Validates that a negative age results in an exception."""
    # BR04 – Age must be positive
    # BR06 – Any validation failure must result in an exception
    # FR05 – Raise exception on business rule violation
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000.00"), age=-21)

def test_br05_fr08_income_no_normalization_denied():
    """Validates that income is not normalized or rounded up to meet the requirement."""
    # BR05 – Values must not be normalized or implicitly adjusted (4999.9999 ≠ 5000)
    # FR08 – Do not perform rounding or automatic adjustment
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"

def test_br07_fr05_missing_value_raises_exception():
    """Validates that not providing a mandatory value results in an exception."""
    # BR07 – The system must not infer or assume values not provided
    # FR05 – Raise exception whenever missing value occurs
    service = CreditService()
    with pytest.raises(Exception):
        # Simulating missing value by passing None (assuming explicit provision is required)
        service.evaluate(score=None, income=Decimal("5000.00"), age=21)

def test_br09_fr07_indivisible_operation_no_partial_results():
    """Validates the operation returns a final decision and does not expose intermediate states."""
    # BR09 – Credit analysis is an indivisible operation, no partial results
    # FR07 – Do not expose intermediate states or progress messages
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
    # The requirement mandates exclusively "APPROVED" or "DENIED" as results
    assert result in ["APPROVED", "DENIED"]
    assert result != "IN_PROGRESS"
    assert result != "PARTIAL_VALIDATION_SUCCESS"

def test_fr01_fr02_strict_evaluation_of_provided_data():
    """Validates evaluation uses exclusively provided data without enrichment."""
    # FR01 – Evaluate using exclusively provided score, income, and age
    # FR02 – Mandatory validation of all criteria before returning result
    service = CreditService()
    # If the system were to enrich data (e.g. looking up a real age for a provided ID), 
    # it would violate FR01. We ensure the provided parameters are the sole drivers.
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
    assert result == "APPROVED"

def test_fr04_fr06_no_result_on_exception():
    """Validates that no business result is returned when an exception is raised."""
    # FR04 – Record result ONLY when a valid decision is produced
    # FR06 – Do not return any business result when an exception is raised
    service = CreditService()
    
    # We ensure the function raises an exception instead of returning "DENIED" or "ERROR" 
    # when an input is invalid (e.g. invalid type).
    with pytest.raises(Exception):
        service.evaluate(score="invalid", income=Decimal("5000.00"), age=21)
