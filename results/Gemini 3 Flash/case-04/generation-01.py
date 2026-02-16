
import pytest
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Assuming the service is available for import as per instructions
# from system import CreditService

def test_credit_approval_at_exact_minimum_thresholds():
    """
    BR01 – Credit may only be approved if Score >= 700, Income >= 5000, Age >= 21.
    FR01 – Evaluate using exclusively provided values.
    FR03 – Return 'APPROVED'.
    """
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
    assert result == "APPROVED"

def test_credit_denial_for_score_below_threshold():
    """
    BR02 – If any criteria fail, credit must be denied.
    FR03 – Return 'DENIED'.
    """
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal("5000.00"), age=21)
    assert result == "DENIED"

def test_credit_denial_for_income_below_threshold():
    """
    BR02 – If any criteria fail, credit must be denied.
    FR03 – Return 'DENIED'.
    """
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
    assert result == "DENIED"

def test_credit_denial_for_age_below_threshold():
    """
    BR02 – If any criteria fail, credit must be denied.
    FR03 – Return 'DENIED'.
    """
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=20)
    assert result == "DENIED"

def test_exception_for_nan_income():
    """
    BR03 – Values as NaN are not allowed and must result in an exception.
    FR05 – Raise exception for magic value NaN.
    """
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)

def test_exception_for_infinity_income():
    """
    BR03 – Values as Infinity are not allowed and must result in an exception.
    FR05 – Raise exception for magic value Infinity.
    """
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)

def test_exception_for_invalid_score_type_float():
    """
    BR04 – Score must be an integer value.
    FR05 – Raise exception for invalid type.
    """
    service = CreditService()
    with pytest.raises(Exception):
        # Passing float instead of int
        service.evaluate(score=700.0, income=Decimal("5000.00"), age=21)

def test_exception_for_invalid_age_type_string():
    """
    BR04 – Age must be an integer value.
    FR05 – Raise exception for invalid type.
    """
    service = CreditService()
    with pytest.raises(Exception):
        # Passing string instead of int
        service.evaluate(score=700, income=Decimal("5000.00"), age="21")

def test_exception_for_invalid_income_type_string():
    """
    BR04 – Income must be a decimal value.
    FR05 – Raise exception for invalid type.
    """
    service = CreditService()
    with pytest.raises(Exception):
        # Passing string instead of Decimal
        service.evaluate(score=700, income="5000.00", age=21)

def test_exception_for_non_positive_score_zero():
    """
    BR04 – Score must be a positive integer value.
    BR06 – Any validation failure must result in an exception.
    """
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=0, income=Decimal("5000.00"), age=21)

def test_exception_for_non_positive_income_negative():
    """
    BR04 – Income must be a positive decimal value.
    BR06 – Any validation failure must result in an exception.
    """
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("-1.00"), age=21)

def test_exception_for_non_positive_age_zero():
    """
    BR04 – Age must be a positive integer value.
    BR06 – Any validation failure must result in an exception.
    """
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000.00"), age=0)

def test_strict_income_value_no_normalization():
    """
    BR05 – Values must not be normalized or implicitly adjusted (4999.9999 != 5000).
    FR08 – Do not perform any kind of normalization, rounding, or automatic adjustment.
    """
    service = CreditService()
    # 4999.9999 is technically closer to 5000 but must be treated as < 5000
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"

def test_exception_on_missing_provided_values():
    """
    BR07 – The system must not infer, guess, or assume values that were not provided.
    FR05 – Raise exception for missing value.
    """
    service = CreditService()
    with pytest.raises(Exception):
        # Simulating missing values via None
        service.evaluate(score=None, income=Decimal("5000.00"), age=21)

def test_indivisible_operation_atomic_result():
    """
    BR09 – Credit analysis is an indivisible operation; must not return partial results.
    FR07 – Do not expose intermediate states.
    """
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
    # The return must be exactly the final string result, not a dict or object with states
    assert result in ["APPROVED", "DENIED"]
    assert isinstance(result, str)

def test_no_business_result_on_exception_trigger():
    """
    FR06 – Do not return any business result when an exception is raised.
    """
    service = CreditService()
    try:
        service.evaluate(score=-10, income=Decimal("5000.00"), age=21)
        pytest.fail("Should have raised an exception")
    except Exception:
        # Success if exception is caught and no value was returned
        pass

def test_mandatory_validation_of_all_criteria():
    """
    FR02 – Mandatory validation of all criteria defined in business rules.
    """
    service = CreditService()
    # Even if score and income are high, age must be validated
    result = service.evaluate(score=900, income=Decimal("10000.00"), age=18)
    assert result == "DENIED"

def test_no_intermediate_approval_levels():
    """
    BR08 – There are no intermediate approval levels.
    FR03 – Return exclusively 'APPROVED' or 'DENIED'.
    """
    service = CreditService()
    result = service.evaluate(score=750, income=Decimal("6000.00"), age=25)
    # Result must not be "PARTIAL_APPROVAL" or "PENDING"
    assert result != "PARTIAL_APPROVAL"
    assert result != "PENDING"
    assert result in ["APPROVED", "DENIED"]
