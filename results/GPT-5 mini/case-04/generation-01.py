import pytest
from decimal import Decimal
from cases.case04 import CreditService

# BR01 – Credit may only be approved if Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21
def test_br01_approve_when_all_criteria_met():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('5000'), age=21)
    assert result == "APPROVED"

# BR02 – If any of the criteria fail, the credit must be denied (score fails)
def test_br02_deny_when_any_criterion_fails_score_below_threshold():
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal('5000'), age=21)
    assert result == "DENIED"

# BR03 – Values as NaN must result in an exception (income NaN)
def test_br03_income_nan_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('NaN'), age=21)

# BR03 – Values as Infinity must result in an exception (income Infinity)
def test_br03_income_infinity_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('Infinity'), age=21)

# BR04 – Score must be a positive integer: non-integer score (float) raises exception
def test_br04_score_must_be_positive_integer_type_float_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700.0, income=Decimal('5000'), age=21)

# BR04 – Income must be a positive decimal value: string income raises exception
def test_br04_income_must_be_decimal_type_string_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income="5000", age=21)

# BR04 – Age must be a positive integer value: non-integer age raises exception
def test_br04_age_must_be_positive_integer_type_float_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('5000'), age=21.5)

# BR05 – Values must not be normalized or implicitly adjusted (income just below threshold remains below)
def test_br05_income_not_normalized_decimal_4999_9999_results_in_denied():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('4999.9999'), age=21)
    assert result == "DENIED"

# BR06 – Any validation failure must result in an exception (negative age is a validation failure)
def test_br06_negative_age_validation_failure_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('5000'), age=-1)

# BR07 – The system must not infer values that were not provided (explicit None for score raises exception)
def test_br07_missing_score_none_raises_exception_no_inference():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=None, income=Decimal('5000'), age=21)

# BR08 – There are no intermediate approval levels (result must be either APPROVED or DENIED)
def test_br08_no_intermediate_levels_result_is_either_approved_or_denied():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('5000'), age=22)
    assert result in ("APPROVED", "DENIED")

# BR09 – Credit analysis is indivisible: evaluate must not return partial results (not a tuple/list/dict)
def test_br09_indivisible_operation_returns_single_value_not_structures():
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal('5000'), age=21)
    assert not isinstance(result, (tuple, list, dict))

# FR01 – Evaluate using exclusively provided values (no inference): approving input yields APPROVED
def test_fr01_evaluate_uses_only_provided_values_and_returns_approved_for_exact_inputs():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('5000'), age=21)
    assert result == "APPROVED"

# FR02 – Mandatory validation of all criteria before returning any result: NaN income causes exception (no result)
def test_fr02_mandatory_validation_before_return_income_nan_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('NaN'), age=21)

# FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful (denial case)
def test_fr03_return_denied_for_valid_inputs_failing_business_rules():
    service = CreditService()
    result = service.evaluate(score=650, income=Decimal('4000'), age=20)
    assert result == "DENIED"

# FR04 – Record exactly one analysis result only when a valid decision is produced: result is a single string
def test_fr04_record_exactly_one_analysis_result_result_is_single_string():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('5000'), age=21)
    assert isinstance(result, str)

# FR05 – Raise an exception whenever any validation failure occurs: invalid score type (string) raises
def test_fr05_invalid_score_type_string_raises_exception():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score="700", income=Decimal('5000'), age=21)

# FR06 – Do not return any business result when an exception is raised (None age raises, no result)
def test_fr06_no_business_result_returned_when_exception_for_none_age():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal('5000'), age=None)

# FR07 – Do not expose intermediate states, partial results, or progress messages (result is not a dict)
def test_fr07_no_intermediate_states_exposed_result_is_not_dict():
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal('5000'), age=21)
    assert not isinstance(result, dict)

# FR08 – Do not perform any normalization, rounding, or automatic adjustment on input values (income below threshold stays below)
def test_fr08_no_normalization_income_decimal_4999_9999_denied():
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal('4999.9999'), age=21)
    assert result == "DENIED"