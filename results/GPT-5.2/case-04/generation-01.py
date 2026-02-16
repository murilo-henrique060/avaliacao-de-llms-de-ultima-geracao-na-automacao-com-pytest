
import math
import pytest

# NOTE:
# These tests assume a class CreditService exists and is importable in the SUT.
# Adjust the import path below to match the real project structure.
from cases.case04 import CreditService  # noqa: F401


# ---------- BR01: approval only if ALL criteria simultaneously satisfied ----------
def test_br01_approves_when_score_income_and_age_meet_minimums():
    # BR01 – Credit may only be approved if Score ≥ 700, Income ≥ 5000, Age ≥ 21
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21)
    assert result == "APPROVED"


# ---------- BR02: if ANY criterion fails => DENIED (business outcome, not exception) ----------
def test_br02_denies_when_score_below_700_with_other_criteria_passing():
    # BR02 – If any criteria fail, credit must be denied
    service = CreditService()
    result = service.evaluate(score=699, income=5000.0, age=21)
    assert result == "DENIED"


# ---------- BR03: NaN/Infinity not allowed => exception ----------
def test_br03_raises_exception_when_score_is_nan():
    # BR03 – Values as NaN are not allowed and must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=float("nan"), income=5000.0, age=21)


def test_br03_raises_exception_when_income_is_positive_infinity():
    # BR03 – Values as Infinity are not allowed and must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=float("inf"), age=21)


# ---------- BR04: type/constraint validation (positive integer / positive decimal / positive integer) ----------
def test_br04_raises_exception_when_score_is_not_integer_type():
    # BR04 – Score: positive integer value (invalid type must raise exception)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score="700", income=5000.0, age=21)


def test_br04_raises_exception_when_income_is_not_decimal_type():
    # BR04 – Income: positive decimal value (invalid type must raise exception)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income="5000.0", age=21)


def test_br04_raises_exception_when_age_is_not_integer_type():
    # BR04 – Age: positive integer value (invalid type must raise exception)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=5000.0, age="21")


def test_br04_raises_exception_when_score_is_not_positive_integer_zero():
    # BR04 – Score: positive integer value (0 is not positive)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=0, income=5000.0, age=21)


def test_br04_raises_exception_when_income_is_not_positive_decimal_zero():
    # BR04 – Income: positive decimal value (0 is not positive)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=0.0, age=21)


def test_br04_raises_exception_when_age_is_not_positive_integer_zero():
    # BR04 – Age: positive integer value (0 is not positive)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=5000.0, age=0)


# ---------- BR05: no normalization/implicit adjustment ----------
def test_br05_denies_when_income_is_4999_9999_not_equal_5000():
    # BR05 – Values must not be normalized or implicitly adjusted (4999.9999 ≠ 5000)
    service = CreditService()
    result = service.evaluate(score=700, income=4999.9999, age=21)
    assert result == "DENIED"


# ---------- BR06: any validation failure => exception ----------
def test_br06_raises_exception_when_score_is_negative_integer():
    # BR06 – Any validation failure must result in an exception
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=-1, income=5000.0, age=21)


# ---------- BR07: no inference/guessing/assuming values not provided ----------
def test_br07_raises_exception_when_score_is_missing_none():
    # BR07 – The system must not infer, guess, or assume values that were not provided
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=None, income=5000.0, age=21)


# ---------- BR08: no intermediate approval levels (only APPROVED or DENIED) ----------
def test_br08_returns_only_approved_or_denied_when_valid_inputs_produce_decision():
    # BR08 – There are no intermediate approval levels
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


# ---------- BR09: indivisible operation, no partial results/logs exposed to API consumer ----------
def test_br09_evaluate_returns_plain_result_string_not_tuple_or_dict():
    # BR09 – Credit analysis is indivisible; must not return partial results
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21)
    assert isinstance(result, str)


# ---------- FR01: use exclusively provided values, no enrichment/normalization/inference ----------
def test_fr01_denies_when_age_20_even_if_other_values_meet_thresholds():
    # FR01 – Evaluate using exclusively provided values (no enrichment/inference)
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=20)
    assert result == "DENIED"


# ---------- FR02: mandatory validation of ALL criteria before returning any result ----------
def test_fr02_raises_exception_for_invalid_income_type_even_if_score_and_age_valid():
    # FR02 – Mandatory validation of all criteria defined in business rules before returning any result
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=object(), age=21)


# ---------- FR03: when validations successful, return exclusively "APPROVED" or "DENIED" ----------
def test_fr03_returns_exclusively_denied_for_valid_inputs_that_fail_business_thresholds():
    # FR03 – Return exclusively "APPROVED" or "DENIED" when validations are successful
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21 - 1)
    assert result == "DENIED"


# ---------- FR04: record exactly one analysis result when a valid decision is produced ----------
def test_fr04_evaluate_produces_single_scalar_result_not_multiple_results():
    # FR04 – Record exactly one analysis result only when a valid decision is produced
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")
    assert not isinstance(result, (list, tuple, dict, set))


# ---------- FR05: raise exception on validation failure incl invalid type, missing, NaN/Inf, or business rule violation ----------
def test_fr05_raises_exception_when_age_is_nan():
    # FR05 – Raise exception whenever any validation failure occurs, including magic value (NaN)
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=5000.0, age=float("nan"))


def test_fr05_raises_exception_when_income_is_missing_none():
    # FR05 – Raise exception whenever any validation failure occurs, including missing value
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(score=700, income=None, age=21)


# ---------- FR06: do not return business result when exception is raised ----------
def test_fr06_no_result_returned_when_exception_raised_for_infinite_age():
    # FR06 – Do not return any business result when an exception is raised
    service = CreditService()
    with pytest.raises(Exception):
        _ = service.evaluate(score=700, income=5000.0, age=float("inf"))


# ---------- FR07: do not expose intermediate states/partial results/progress messages ----------
def test_fr07_return_value_contains_no_progress_or_intermediate_message_on_success():
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    service = CreditService()
    result = service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


# ---------- FR08: no normalization/rounding/automatic adjustment ----------
def test_fr08_denies_when_score_699_not_rounded_up_to_700():
    # FR08 – Do not perform any normalization, rounding, or automatic adjustment on input values
    service = CreditService()
    result = service.evaluate(score=699, income=5000.0, age=21)
    assert result == "DENIED"
