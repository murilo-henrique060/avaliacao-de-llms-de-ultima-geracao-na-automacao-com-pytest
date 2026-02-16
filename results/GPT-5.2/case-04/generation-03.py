
import pytest
from decimal import Decimal

# NOTE:
# These tests assume the existence of CreditService with:
#   CreditService().evaluate(score: int, income: decimal, age: int) -> "APPROVED" | "DENIED"
# The system implementation is NOT provided here (tests only), per requirements.
from cases.case04 import CreditService


@pytest.fixture()
def service():
    return CreditService()


# -----------------------------
# BR01: Approval requires all three criteria simultaneously
# -----------------------------

def test_br01_approves_when_score_income_age_meet_minimums(service):
    # BR01 – Credit may only be approved if score≥700, income≥5000, age≥21 simultaneously
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"


def test_br01_denies_when_score_below_700_even_if_income_and_age_meet(service):
    # BR01 – Score criterion must be met for approval
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"


def test_br01_denies_when_income_below_5000_even_if_score_and_age_meet(service):
    # BR01 – Income criterion must be met for approval
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"


def test_br01_denies_when_age_below_21_even_if_score_and_income_meet(service):
    # BR01 – Age criterion must be met for approval
    result = service.evaluate(score=700, income=Decimal("5000"), age=20)
    assert result == "DENIED"


# -----------------------------
# BR02: If any criterion fails, credit must be denied
# -----------------------------

def test_br02_denies_when_multiple_criteria_fail(service):
    # BR02 – If any criteria fail, the credit must be denied
    result = service.evaluate(score=699, income=Decimal("4999.99"), age=20)
    assert result == "DENIED"


# -----------------------------
# BR03: NaN or Infinity not allowed -> exception
# -----------------------------

def test_br03_raises_exception_for_score_nan(service):
    # BR03 – NaN not allowed
    with pytest.raises(Exception):
        service.evaluate(score=float("nan"), income=Decimal("5000"), age=21)


def test_br03_raises_exception_for_income_nan(service):
    # BR03 – NaN not allowed
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("NaN"), age=21)


def test_br03_raises_exception_for_age_nan(service):
    # BR03 – NaN not allowed
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=float("nan"))


def test_br03_raises_exception_for_score_infinity(service):
    # BR03 – Infinity not allowed
    with pytest.raises(Exception):
        service.evaluate(score=float("inf"), income=Decimal("5000"), age=21)


def test_br03_raises_exception_for_income_infinity(service):
    # BR03 – Infinity not allowed
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("Infinity"), age=21)


def test_br03_raises_exception_for_age_infinity(service):
    # BR03 – Infinity not allowed
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=float("inf"))


# -----------------------------
# BR04: Type and constraints
#   Score: positive integer
#   Income: positive decimal
#   Age: positive integer
# -----------------------------

def test_br04_raises_exception_when_score_is_not_integer_type(service):
    # BR04 – Score must be a positive integer value
    with pytest.raises(Exception):
        service.evaluate(score="700", income=Decimal("5000"), age=21)


def test_br04_raises_exception_when_score_is_not_positive(service):
    # BR04 – Score must be a positive integer value
    with pytest.raises(Exception):
        service.evaluate(score=0, income=Decimal("5000"), age=21)


def test_br04_raises_exception_when_income_is_not_decimal_type(service):
    # BR04 – Income must be a positive decimal value
    with pytest.raises(Exception):
        service.evaluate(score=700, income="5000", age=21)


def test_br04_raises_exception_when_income_is_not_positive(service):
    # BR04 – Income must be a positive decimal value
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("0"), age=21)


def test_br04_raises_exception_when_age_is_not_integer_type(service):
    # BR04 – Age must be a positive integer value
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age="21")


def test_br04_raises_exception_when_age_is_not_positive(service):
    # BR04 – Age must be a positive integer value
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=0)


# -----------------------------
# BR05: No normalization/implicit adjustments
# -----------------------------

def test_br05_denies_when_income_is_4999_9999_not_equal_to_5000(service):
    # BR05 – Values must not be normalized or implicitly adjusted (4999.9999 ≠ 5000)
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"


# -----------------------------
# BR06: Any validation failure must result in an exception
# -----------------------------

def test_br06_raises_exception_when_score_is_negative(service):
    # BR06 – Any validation failure must result in an exception
    with pytest.raises(Exception):
        service.evaluate(score=-1, income=Decimal("5000"), age=21)


# -----------------------------
# BR07: No inferring/guessing/assuming missing values
# -----------------------------

def test_br07_raises_exception_when_score_is_missing(service):
    # BR07 – The system must not infer values that were not provided
    with pytest.raises(Exception):
        service.evaluate(score=None, income=Decimal("5000"), age=21)


def test_br07_raises_exception_when_income_is_missing(service):
    # BR07 – The system must not infer values that were not provided
    with pytest.raises(Exception):
        service.evaluate(score=700, income=None, age=21)


def test_br07_raises_exception_when_age_is_missing(service):
    # BR07 – The system must not infer values that were not provided
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=None)


# -----------------------------
# BR08: No intermediate approval levels
# -----------------------------

def test_br08_returns_only_approved_when_valid_and_all_criteria_met(service):
    # BR08 – There are no intermediate approval levels
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result == "APPROVED"


def test_br08_returns_only_denied_when_valid_but_any_criterion_fails(service):
    # BR08 – There are no intermediate approval levels
    result = service.evaluate(score=700, income=Decimal("5000"), age=20)
    assert result == "DENIED"


# -----------------------------
# BR09: Indivisible operation; no partial results/logs/criteria exposed
# -----------------------------

def test_br09_evaluate_returns_only_business_result_string(service):
    # BR09 – Credit analysis is indivisible; must not expose partial results or decision criteria
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert result in ("APPROVED", "DENIED")


# -----------------------------
# FR01: Use exclusively provided values; no inference/normalization/enrichment
# -----------------------------

def test_fr01_denies_when_income_is_not_exactly_5000_without_adjustment(service):
    # FR01 – Evaluate using exclusively the provided values (no normalization/data enrichment)
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"


# -----------------------------
# FR02: Mandatory validation of all criteria before returning any result
# -----------------------------

def test_fr02_raises_exception_for_invalid_type_even_if_other_values_would_approve(service):
    # FR02 – Mandatory validation of all criteria before returning any result
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("5000"), age=Decimal("21"))


# -----------------------------
# FR03: Return exclusively "APPROVED" or "DENIED" when validations succeed
# -----------------------------

def test_fr03_returns_only_approved_or_denied_on_valid_inputs(service):
    # FR03 – Return exclusively one of: "APPROVED" or "DENIED" when all validations are successful
    result = service.evaluate(score=701, income=Decimal("5000"), age=21)
    assert result in ("APPROVED", "DENIED")


# -----------------------------
# FR04: Record exactly one analysis result only when valid decision is produced
# -----------------------------
# The specification requires recording, but provides no observable API for retrieving records.
# Therefore, we assert the minimum externally observable requirement: a single decision value is returned.

def test_fr04_returns_single_decision_value_not_collection(service):
    # FR04 – Record exactly one analysis result only when a valid decision is produced
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert not isinstance(result, (list, tuple, dict, set))


# -----------------------------
# FR05: Raise exception on any validation failure, including business rule violation
# -----------------------------

def test_fr05_raises_exception_when_income_is_negative(service):
    # FR05 – Raise exception whenever any validation failure occurs (invalid constraint)
    with pytest.raises(Exception):
        service.evaluate(score=700, income=Decimal("-1"), age=21)


def test_fr05_returns_denied_when_business_threshold_not_met_but_types_valid(service):
    # FR05 – Business rule violation produces a valid business decision ("DENIED") when validations are successful
    result = service.evaluate(score=699, income=Decimal("5000"), age=21)
    assert result == "DENIED"


# -----------------------------
# FR06: Do not return any business result when an exception is raised
# -----------------------------

def test_fr06_no_business_result_returned_when_exception_raised(service):
    # FR06 – Do not return any business result when an exception is raised
    with pytest.raises(Exception):
        service.evaluate(score="700", income=Decimal("5000"), age=21)


# -----------------------------
# FR07: Do not expose intermediate states/partial results/progress messages
# -----------------------------

def test_fr07_evaluate_does_not_return_intermediate_structure(service):
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    result = service.evaluate(score=700, income=Decimal("5000"), age=21)
    assert isinstance(result, str)


# -----------------------------
# FR08: Do not normalize/round/auto-adjust input values
# -----------------------------

def test_fr08_denies_when_income_is_4999_9999_without_rounding(service):
    # FR08 – Do not perform normalization, rounding, or automatic adjustment on input values
    result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
    assert result == "DENIED"
