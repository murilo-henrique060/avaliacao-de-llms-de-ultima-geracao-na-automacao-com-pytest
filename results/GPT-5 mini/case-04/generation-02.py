import pytest
from decimal import Decimal
from cases.case04 import CreditService

# BR01 – Credit may only be approved if Score ≥ 700, Income ≥ 5000, Age ≥ 21
def test_br01_credit_approved_when_all_criteria_met():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"

# BR02 – If any of the criteria fail, the credit must be denied
def test_br02_credit_denied_when_score_below_threshold():
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"

# BR03 – Values as NaN or Infinity are not allowed and must result in an exception
def test_br03_nan_income_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)

# BR04 – Score: positive integer value (validate score type)
def test_br04_score_must_be_integer_type_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700.0, income=Decimal("5000"), age=21)

# BR04 – Income: positive decimal value (validate income type)
def test_br04_income_must_be_decimal_type_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=5000.0, age=21)

# BR04 – Age: positive integer value (validate age type)
def test_br04_age_must_be_integer_type_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=21.0)

# BR05 – Values must not be normalized or implicitly adjusted (4999.9999 != 5000)
def test_br05_income_not_normalized_just_below_threshold_denied():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"

# BR06 – Any validation failure must result in an exception (None treated as validation failure)
def test_br06_none_income_results_in_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=None, age=21)

# BR07 – The system must not infer, guess, or assume values that were not provided
def test_br07_missing_age_none_must_not_be_inferred_and_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=None)

# BR08 – There are no intermediate approval levels (result must be a final single decision)
def test_br08_no_intermediate_approval_levels_result_is_not_structured():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4000"), age=30)
    assert isinstance(result, str)
    assert result in ("APPROVED", "DENIED")

# BR09 – Credit analysis is an indivisible operation: must not return partial results
def test_br09_evaluation_returns_single_atomic_value_not_tuple_or_dict():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert not isinstance(result, (tuple, list, dict))
    assert isinstance(result, str)

# FR01 – Evaluate using exclusively the provided score, income, and age values
def test_fr01_evaluation_uses_only_provided_values_produces_deterministic_result():
    service = CreditService()
    # Deterministic call with explicit inputs must produce the expected decision
    result = service.evaluate(score=650, income=Decimal("6000"), age=30)
    assert result == "DENIED"

# FR02 – Mandatory validation of all criteria before returning any result
def test_fr02_mandatory_validation_raises_on_invalid_income_type_before_result():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income="5000", age=21)

# FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful
def test_fr03_returns_denied_when_a_single_business_criterion_fails():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4000"), age=25)
    assert result == "DENIED"

# FR04 – Record exactly one analysis result only when a valid decision is produced
def test_fr04_returns_single_result_value_of_allowed_type_when_valid():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert isinstance(result, str)

# FR05 – Raise an exception whenever any validation failure occurs (Infinity example)
def test_fr05_infinite_income_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)

# FR06 – Do not return any business result when an exception is raised
def test_fr06_no_business_result_is_returned_when_exception_occurs():
    service = CreditService()
    sentinel = object()
    result = sentinel
    with pytest.raises(Exception):
        result = service.evaluate(score="invalid", income=Decimal("5000"), age=21)
    assert result is sentinel

# FR07 – Do not expose intermediate states, partial results, or progress messages
def test_fr07_no_intermediate_states_exposed_result_is_single_string():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert isinstance(result, str)
    assert not hasattr(result, "__iter__") or isinstance(result, str)

# FR08 – Do not perform normalization, rounding, or automatic adjustment on input values
def test_fr08_no_normalization_income_close_value_not_adjusted_denied():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"