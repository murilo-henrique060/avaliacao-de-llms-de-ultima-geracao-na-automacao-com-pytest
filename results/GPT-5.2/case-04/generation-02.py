
import pytest
from decimal import Decimal

# NOTE:
# Tests assume an import path where CreditService is available to the test environment.
# Do not implement the system here.
from cases.case04 import CreditService


# ---------------------------
# BR01: approval only if ALL thresholds are met simultaneously
# ---------------------------

def test_br01_approves_when_score_income_age_all_meet_thresholds():
    # BR01 – Credit may only be approved if score ≥ 700, income ≥ 5000, age ≥ 21
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"


def test_br01_denies_when_score_below_700_even_if_income_and_age_meet_thresholds():
    # BR01 – Credit may only be approved if score ≥ 700, income ≥ 5000, age ≥ 21
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"


# ---------------------------
# BR02: if any criteria fail, credit must be denied
# ---------------------------

def test_br02_denies_when_income_below_5000_even_if_score_and_age_meet_thresholds():
    # BR02 – If any of the criteria fail, the credit must be denied
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
    assert result == "DENIED"


# ---------------------------
# BR03: NaN/Infinity are not allowed -> exception
# ---------------------------

def test_br03_raises_exception_when_income_is_nan():
    # BR03 – Values as NaN are not allowed and must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)


def test_br03_raises_exception_when_income_is_infinity():
    # BR03 – Values as Infinity are not allowed and must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)


# ---------------------------
# BR04: type + constraints
#   Score: positive integer
#   Income: positive decimal
#   Age: positive integer
# ---------------------------

def test_br04_raises_exception_when_score_is_not_integer_type():
    # BR04 – Score must be a positive integer value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score="700", income=Decimal("5000"), age=21)


def test_br04_raises_exception_when_score_is_not_positive():
    # BR04 – Score must be a positive integer value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=0, income=Decimal("5000"), age=21)


def test_br04_raises_exception_when_income_is_not_decimal_type():
    # BR04 – Income must be a positive decimal value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income="5000", age=21)


def test_br04_raises_exception_when_income_is_not_positive():
    # BR04 – Income must be a positive decimal value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("0"), age=21)


def test_br04_raises_exception_when_age_is_not_integer_type():
    # BR04 – Age must be a positive integer value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age="21")


def test_br04_raises_exception_when_age_is_not_positive():
    # BR04 – Age must be a positive integer value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=0)


# ---------------------------
# BR05: no normalization/implicit adjustment (exact values)
# ---------------------------

def test_br05_denies_when_income_is_4999_9999_not_equal_5000():
    # BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 ≠ 5000)
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"


# ---------------------------
# BR06: any validation failure must result in an exception
# ---------------------------

def test_br06_raises_exception_when_income_is_negative():
    # BR06 – Any validation failure must result in an exception
    # BR04 – Income must be a positive decimal value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("-1"), age=21)


# ---------------------------
# BR07: must not infer/guess/assume values not provided
# ---------------------------

def test_br07_raises_exception_when_score_is_missing():
    # BR07 – The system must not infer, guess, or assume values that were not provided
    # FR02 – Mandatory validation of all criteria before returning any result
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=None, income=Decimal("5000"), age=21)


# ---------------------------
# BR08: no intermediate approval levels
# ---------------------------

def test_br08_returns_only_approved_or_denied_when_valid_inputs_produce_a_decision():
    # BR08 – There are no intermediate approval levels
    # FR03 – Return exclusively "APPROVED" or "DENIED" when validations are successful
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result in ("APPROVED", "DENIED")
    assert result == "APPROVED"


# ---------------------------
# BR09: indivisible operation; no partial results/logs exposed to API consumer
# ---------------------------

def test_br09_return_value_is_plain_decision_string_not_structured_partial_result():
    # BR09 – Credit analysis is an indivisible operation: must not return partial results
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert isinstance(result, str)
    assert result == "APPROVED"


# ---------------------------
# FR01: evaluate using exclusively provided values; no inference/normalization/enrichment
# ---------------------------

def test_fr01_denies_when_age_is_below_21_no_inference_to_increase_age():
    # FR01 – Evaluate using exclusively provided values, with no inference/normalization
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=20)
    assert result == "DENIED"


# ---------------------------
# FR02: mandatory validation of all criteria before returning any result
# ---------------------------

def test_fr02_raises_exception_when_age_invalid_type_no_business_result_returned():
    # FR02 – Mandatory validation of all criteria before returning any result
    # FR06 – Do not return any business result when an exception is raised
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=None)


# ---------------------------
# FR03: when validations succeed, return exclusively "APPROVED" or "DENIED"
# ---------------------------

def test_fr03_returns_denied_for_valid_inputs_that_fail_business_thresholds():
    # FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful
    # BR02 – If any criteria fail, credit must be denied
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=20)
    assert result == "DENIED"


# ---------------------------
# FR04: record exactly one analysis result only when a valid decision is produced
# ---------------------------

def test_fr04_decision_is_single_value_not_multiple_results():
    # FR04 – Record exactly one analysis result only when a valid decision is produced
    # (API-level assertion: only one decision is returned, not multiple entries)
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result in ("APPROVED", "DENIED")
    assert not isinstance(result, (list, tuple, dict))


# ---------------------------
# FR05: raise exception on any validation failure incl. invalid type, missing value, magic value, or business rule violation
# ---------------------------

def test_fr05_raises_exception_when_income_is_missing():
    # FR05 – Raise an exception whenever any validation failure occurs, including missing value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=None, age=21)


def test_fr05_raises_exception_when_score_is_infinity():
    # FR05 – Raise an exception whenever any validation failure occurs, including magic value (Infinity)
    # BR03 – Values as Infinity are not allowed and must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=float("inf"), income=Decimal("5000"), age=21)


def test_fr05_raises_exception_when_business_rule_type_constraint_violated_age_negative():
    # FR05 – Raise an exception whenever any validation failure occurs, including business rule violation
    # BR04 – Age must be a positive integer value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=-1)


# ---------------------------
# FR06: do not return any business result when an exception is raised
# ---------------------------

def test_fr06_exception_prevents_returning_approved_or_denied():
    # FR06 – Do not return any business result when an exception is raised
    # (Assertion: call raises; no returned value to assert)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)


# ---------------------------
# FR07: do not expose intermediate states/partial results/progress messages
# ---------------------------

def test_fr07_result_is_exactly_approved_or_denied_without_extra_message():
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    # FR03 – Return exclusively one of: "APPROVED" or "DENIED"
    service = CreditService()
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"


# ---------------------------
# FR08: no normalization/rounding/automatic adjustment on input values
# ---------------------------

def test_fr08_denies_when_score_is_699_no_rounding_up_to_700():
    # FR08 – Do not perform normalization, rounding, or automatic adjustment on input values
    service = CreditService()
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"
