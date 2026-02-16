
import pytest


@pytest.fixture
def credit_service():
    # Assumes SUT is available at runtime.
    # Tests only; SUT implementation/import is intentionally not provided.
    from cases.case04 import CreditService  # type: ignore

    return CreditService()


def test_br01_approves_when_score_income_age_all_meet_minimums(credit_service):
    # BR01 – Credit may only be approved if: Score ≥ 700, Income ≥ 5000, Age ≥ 21
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result == "APPROVED"


def test_br02_denies_when_score_fails_even_if_income_and_age_pass(credit_service):
    # BR02 – If any criteria fail, credit must be denied
    result = credit_service.evaluate(score=699, income=5000.0, age=21)
    assert result == "DENIED"


def test_br03_raises_when_score_is_nan(credit_service):
    # BR03 – Values as NaN are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=float("nan"), income=5000.0, age=21)


def test_br03_raises_when_income_is_positive_infinity(credit_service):
    # BR03 – Values as Infinity are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=float("inf"), age=21)


def test_br03_raises_when_age_is_negative_infinity(credit_service):
    # BR03 – Values as Infinity are not allowed and must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=float("-inf"))


def test_br04_raises_when_score_is_not_integer_type(credit_service):
    # BR04 – Score: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700.0, income=5000.0, age=21)


def test_br04_raises_when_score_is_zero(credit_service):
    # BR04 – Score: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=0, income=5000.0, age=21)


def test_br04_raises_when_score_is_negative(credit_service):
    # BR04 – Score: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=-1, income=5000.0, age=21)


def test_br04_raises_when_income_is_not_decimal_number_type(credit_service):
    # BR04 – Income: positive decimal value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income="5000.0", age=21)


def test_br04_raises_when_income_is_zero(credit_service):
    # BR04 – Income: positive decimal value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=0.0, age=21)


def test_br04_raises_when_income_is_negative(credit_service):
    # BR04 – Income: positive decimal value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=-0.01, age=21)


def test_br04_raises_when_age_is_not_integer_type(credit_service):
    # BR04 – Age: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=21.0)


def test_br04_raises_when_age_is_zero(credit_service):
    # BR04 – Age: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=0)


def test_br04_raises_when_age_is_negative(credit_service):
    # BR04 – Age: positive integer value
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=5000.0, age=-1)


def test_br05_denies_when_income_is_4999_9999_without_normalization(credit_service):
    # BR05 – Values must not be normalized or implicitly adjusted (4999.9999 ≠ 5000)
    result = credit_service.evaluate(score=700, income=4999.9999, age=21)
    assert result == "DENIED"


def test_br06_raises_on_validation_failure_invalid_score_type(credit_service):
    # BR06 – Any validation failure must result in an exception
    with pytest.raises(Exception):
        credit_service.evaluate(score="700", income=5000.0, age=21)


def test_br07_raises_when_score_is_missing_none(credit_service):
    # BR07 – The system must not infer, guess, or assume values that were not provided
    with pytest.raises(Exception):
        credit_service.evaluate(score=None, income=5000.0, age=21)


def test_br08_returns_no_intermediate_levels_only_approved_or_denied_for_valid_inputs(credit_service):
    # BR08 – There are no intermediate approval levels
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


def test_br09_return_value_is_atomic_string_no_partial_result_structure(credit_service):
    # BR09 – Credit analysis is an indivisible operation: must not return partial results
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert isinstance(result, str)


def test_fr01_approves_using_only_provided_values_without_enrichment(credit_service):
    # FR01 – Evaluate using exclusively provided score, income, and age values
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result == "APPROVED"


def test_fr02_raises_when_income_invalid_even_if_score_and_age_valid(credit_service):
    # FR02 – Mandatory validation of all criteria before returning any result
    with pytest.raises(Exception):
        credit_service.evaluate(score=700, income=-0.01, age=21)


def test_fr03_returns_exclusively_approved_or_denied_for_valid_inputs(credit_service):
    # FR03 – Return exclusively "APPROVED" or "DENIED" when validations are successful
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


def test_fr04_record_exactly_one_analysis_result_on_valid_decision_via_hook(monkeypatch, credit_service):
    # FR04 – Record exactly one analysis result only when a valid decision is produced
    # This test expects the SUT to call an internal method responsible for recording exactly once.
    if not hasattr(credit_service, "_record_result"):
        pytest.fail("SUT does not expose _record_result hook required to test FR04 without adding new behavior.")

    calls = []

    def _spy_record_result(result):
        calls.append(result)

    monkeypatch.setattr(credit_service, "_record_result", _spy_record_result)

    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert calls == [result]


def test_fr05_raises_on_business_rule_violation_score_below_threshold(credit_service):
    # FR05 – Raise an exception whenever any validation failure occurs, including business rule violation
    with pytest.raises(Exception):
        credit_service.evaluate(score=699, income=5000.0, age=21)


def test_fr06_does_not_return_business_result_when_exception_is_raised(credit_service):
    # FR06 – Do not return any business result when an exception is raised
    with pytest.raises(Exception):
        credit_service.evaluate(score="700", income=5000.0, age=21)


def test_fr07_does_not_expose_intermediate_states_in_return_type(credit_service):
    # FR07 – Do not expose intermediate states, partial results, or progress messages
    result = credit_service.evaluate(score=700, income=5000.0, age=21)
    assert result in ("APPROVED", "DENIED")


def test_fr08_does_not_round_income_4999_999999_denied(credit_service):
    # FR08 – Do not perform normalization, rounding, or automatic adjustment on input values
    result = credit_service.evaluate(score=700, income=4999.999999, age=21)
    assert result == "DENIED"
