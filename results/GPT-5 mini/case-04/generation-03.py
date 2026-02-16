import pytest

from cases.case04 import CreditService

# BR01 – Credit may only be approved if Score ≥ 700, Income ≥ 5000, Age ≥ 21
def test_br01_credit_approved_at_exact_thresholds():
    service = CreditService()
    result = service.evaluate(700, 5000.0, 21)
    assert result == "APPROVED"

# BR02 – If any of the criteria fail, the credit must be denied
def test_br02_credit_denied_when_score_below_threshold():
    service = CreditService()
    result = service.evaluate(699, 5000.0, 21)
    assert result == "DENIED"

# BR03 – Values as NaN or Infinity are not allowed and must result in an exception
def test_br03_exception_on_income_nan():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, float("nan"), 21)

# BR04 – Score must be a positive integer (type/constraint validation)
def test_br04_exception_on_score_non_integer_type():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700.0, 5000.0, 21)

# BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 != 5000)
def test_br05_income_not_normalized_4999_9999_results_in_denied():
    service = CreditService()
    result = service.evaluate(700, 4999.9999, 21)
    assert result == "DENIED"

# BR06 – Any validation failure must result in an exception
def test_br06_exception_on_missing_age_none():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, 5000.0, None)

# BR07 – The system must not infer, guess, or assume values that were not provided
def test_br07_exception_on_missing_income_none_no_inference():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, None, 21)

# BR08 – There are no intermediate approval levels (do not return partial structures)
def test_br08_no_intermediate_levels_returns_string_type_for_denied_case():
    service = CreditService()
    result = service.evaluate(699, 5000.0, 21)
    assert isinstance(result, str)

# BR09 – Credit analysis is an indivisible operation (must not return partial results)
def test_br09_indivisible_operation_returns_single_string_for_valid_input():
    service = CreditService()
    result = service.evaluate(700, 5000.0, 21)
    assert isinstance(result, str)

# FR01 – Evaluate using exclusively the provided values (no inference or normalization)
def test_fr01_no_inference_score_float_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700.0, 5000.0, 21)

# FR02 – Mandatory validation of all criteria before returning any result
def test_fr02_mandatory_validation_missing_score_none_raises():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(None, 5000.0, 21)

# FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful
def test_fr03_returns_exclusively_approved_for_all_criteria_met():
    service = CreditService()
    result = service.evaluate(700, 5000.0, 21)
    assert result == "APPROVED"

# FR04 – Record exactly one analysis result only when a valid decision is produced
def test_fr04_single_analysis_result_return_is_string_for_denied_decision():
    service = CreditService()
    result = service.evaluate(699, 5000.0, 21)
    assert isinstance(result, str)

# FR05 – Raise an exception whenever any validation failure occurs (including NaN)
def test_fr05_raise_exception_on_score_nan():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(float("nan"), 5000.0, 21)

# FR06 – Do not return any business result when an exception is raised
def test_fr06_no_business_result_returned_when_exception_on_age_string():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, 5000.0, "21")

# FR07 – Do not expose intermediate states, partial results, or progress messages
def test_fr07_no_intermediate_states_returned_for_valid_input():
    service = CreditService()
    result = service.evaluate(699, 5000.0, 21)
    assert isinstance(result, str)

# FR08 – Do not perform any normalization, rounding, or automatic adjustment on input values
def test_fr08_no_rounding_income_4999_9999_denied():
    service = CreditService()
    result = service.evaluate(700, 4999.9999, 21)
    assert result == "DENIED"