
import pytest


# NOTE:
# These tests assume the SUT provides a CreditService class with:
#   evaluate(score: int, income: decimal, age: int) -> "APPROVED" | "DENIED"
# The tests do not implement the system; they validate the formal specification only.


@pytest.fixture
def credit_service():
    # FR01 – Evaluate using exclusively provided values (fixture only provides the service)
    from cases.case04 import CreditService  # type: ignore

    return CreditService()


def _valid_inputs():
    # Helper to keep each test focused on exactly one behavior; values are exact.
    return {"score": 700, "income": 5000.0, "age": 21}


# -------------------------
# Business Rules (BR)
# -------------------------

def test_br01_approves_when_score_income_and_age_meet_minimums(credit_service):
    # BR01 – Credit may only be approved if score ≥ 700, income ≥ 5000, age ≥ 21 (simultaneously)
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result == "APPROVED"


def test_br02_denies_when_score_below_700(credit_service):
    # BR02 – If any criteria fail, credit must be denied
    result = credit_service.evaluate(score=699, income=5000.0, age=21)
    assert result == "DENIED"


def test_br02_denies_when_income_below_5000(credit_service):
    # BR02 – If any criteria fail, credit must be denied
    result = credit_service.evaluate(score=700, income=4999.0, age=21)
    assert result == "DENIED"


def test_br02_denies_when_age_below_21(credit_service):
    # BR02 – If any criteria fail, credit must be denied
    result = credit_service.evaluate(score=700, income=5000.0, age=20)
    assert result == "DENIED"


def test_br03_raises_exception_when_score_is_nan(credit_service):
    # BR03 – Values as NaN are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=float("nan"), income=5000.0, age=21)


def test_br03_raises_exception_when_income_is_nan(credit_service):
    # BR03 – Values as NaN are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=float("nan"), age=21)


def test_br03_raises_exception_when_age_is_nan(credit_service):
    # BR03 – Values as NaN are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=float("nan"))


def test_br03_raises_exception_when_score_is_positive_infinity(credit_service):
    # BR03 – Values as Infinity are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=float("inf"), income=5000.0, age=21)


def test_br03_raises_exception_when_income_is_positive_infinity(credit_service):
    # BR03 – Values as Infinity are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=float("inf"), age=21)


def test_br03_raises_exception_when_age_is_positive_infinity(credit_service):
    # BR03 – Values as Infinity are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=float("inf"))


def test_br04_raises_exception_when_score_is_not_integer_type(credit_service):
    # BR04 – Score: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score="700", income=5000.0, age=21)


def test_br04_raises_exception_when_income_is_not_decimal_type(credit_service):
    # BR04 – Income: positive decimal value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income="5000.0", age=21)


def test_br04_raises_exception_when_age_is_not_integer_type(credit_service):
    # BR04 – Age: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age="21")


def test_br04_raises_exception_when_score_is_not_positive(credit_service):
    # BR04 – Score: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=0, income=5000.0, age=21)


def test_br04_raises_exception_when_income_is_not_positive(credit_service):
    # BR04 – Income: positive decimal value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=0.0, age=21)


def test_br04_raises_exception_when_age_is_not_positive(credit_service):
    # BR04 – Age: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=0)


def test_br05_does_not_approve_if_income_is_4999_9999(credit_service):
    # BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 ≠ 5000)
    result = credit_service.evaluate(score=700, income=4999.9999, age=21)
    assert result == "DENIED"


def test_br06_raises_exception_on_validation_failure_invalid_score_type(credit_service):
    # BR06 – Any validation failure must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=None, income=5000.0, age=21)


def test_br07_raises_exception_when_score_is_missing(credit_service):
    # BR07 – The system must not infer, guess, or assume values that were not provided
    with pytest.raises(Exception):
        credit_service.evaluate(income=5000.0, age=21)  # type: ignore


def test_br07_raises_exception_when_income_is_missing(credit_service):
    # BR07 – The system must not infer, guess, or assume values that were not provided
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, age=21)  # type: ignore


def test_br07_raises_exception_when_age_is_missing(credit_service):
    # BR07 – The system must not infer, guess, or assume values that were not provided
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0)  # type: ignore


def test_br08_returns_only_approved_or_denied_when_valid(credit_service):
    # BR08 – There are no intermediate approval levels
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


def test_br09_evaluate_returns_indivisible_single_result_value(credit_service):
    # BR09 – Credit analysis is an indivisible operation: must not return partial results
    # Validate that the return is a single scalar business result, not a structure with partials/logs.
    result = credit_service.evaluate(**_valid_inputs())
    assert isinstance(result, str)


# -------------------------
# Functional Requirements (FR)
# -------------------------

def test_fr01_uses_exclusively_provided_values_no_inference_allows_denial_when_score_fails(credit_service):
    # FR01 – Evaluate using exclusively provided score/income/age (no inference/enrichment)
    # Provide income/age passing, score failing => must be denied (no inferred adjustment).
    result = credit_service.evaluate(score=1, income=5000.0, age=21)
    assert result == "DENIED"


def test_fr02_validates_all_criteria_before_returning_result_nan_in_income_raises(credit_service):
    # FR02 – Mandatory validation of all criteria before returning any result
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=float("nan"), age=21)


def test_fr03_returns_exclusively_approved_or_denied_when_valid_inputs(credit_service):
    # FR03 – Return exclusively "APPROVED" or "DENIED" when validations are successful
    result = credit_service.evaluate(**_valid_inputs())
    assert result in ("APPROVED", "DENIED")


def test_fr04_records_exactly_one_analysis_result_only_when_valid_decision_is_produced(credit_service, monkeypatch):
    # FR04 – Record exactly one analysis result only when a valid decision is produced
    # We assume the service exposes a dependency/callback for recording; if not present, test will fail,
    # indicating nonconformance to the specified requirement in the public API design.
    calls = []

    def recorder(value):
        calls.append(value)

    # Attempt to attach a recorder if the SUT supports it via an attribute commonly used for DI.
    # This does not implement behavior; it only observes whether recording is invoked.
    if hasattr(credit_service, "set_result_recorder"):
        credit_service.set_result_recorder(recorder)
    elif hasattr(credit_service, "result_recorder"):
        setattr(credit_service, "result_recorder", recorder)
    else:
        pytest.fail("CreditService provides no observable mechanism to validate FR04 recording behavior.")

    result = credit_service.evaluate(**_valid_inputs())
    assert result == "APPROVED"
    assert calls == ["APPROVED"]


def test_fr05_raises_exception_on_invalid_type_for_age(credit_service):
    # FR05 – Raise an exception whenever any validation failure occurs, including invalid type
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=21.0)


def test_fr05_raises_exception_on_magic_value_infinity_for_income(credit_service):
    # FR05 – Raise an exception whenever any validation failure occurs, including magic value Infinity
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=float("inf"), age=21)


def test_fr05_raises_exception_on_missing_value_for_score(credit_service):
    # FR05 – Raise an exception whenever any validation failure occurs, including missing value
    with pytest.raises(Exception):
        credit_service.evaluate(income=5000.0, age=21)  # type: ignore


def test_fr05_raises_exception_on_business_rule_violation_non_positive_income(credit_service):
    # FR05 – Raise an exception whenever any validation failure occurs, including business rule violation
    # (Income must be positive decimal value per BR04; violation is a validation failure)
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=-1.0, age=21)


def test_fr06_does_not_return_business_result_when_exception_is_raised(credit_service):
    # FR06 – Do not return any business result when an exception is raised
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=0.0, age=21)


def test_fr07_does_not_expose_intermediate_states_or_progress_messages_in_return(credit_service):
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    result = credit_service.evaluate(**_valid_inputs())
    assert result in ("APPROVED", "DENIED")


def test_fr08_does_not_round_or_adjust_income_4999_9999_is_denied(credit_service):
    # FR08 – Do not perform normalization, rounding, or automatic adjustment on input values
    result = credit_service.evaluate(score=700, income=4999.9999, age=21)
    assert result == "DENIED"
