import pytest
from decimal import Decimal

# Assumes the system under test provides CreditService with the specified interface.
# Do not implement CreditService here; tests call it as specified.
from cases.case04 import CreditService


# BR01 – Credit may only be approved if Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21
def test_br01_approval_when_all_criteria_met_exact_thresholds():
    service = CreditService()
    # Exact threshold values (no normalization): score=700, income=5000, age=21
    result = service.evaluate(700, Decimal("5000"), 21)
    assert result == "APPROVED"


# BR02 – If any of the criteria fail, the credit must be denied
def test_br02_deny_when_score_below_required():
    service = CreditService()
    # Score fails (699) while other criteria meet thresholds
    result = service.evaluate(699, Decimal("5000"), 21)
    assert result == "DENIED"


# BR03 – Values as NaN are not allowed and must result in an exception
def test_br03_raise_on_score_nan():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(Decimal("NaN"), Decimal("5000"), 21)


# BR03 – Values as Infinity are not allowed and must result in an exception
def test_br03_raise_on_income_infinity():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("Infinity"), 21)


# BR04 – Score must be a positive integer value: non-integer type must raise an exception
def test_br04_raise_on_score_non_integer_type():
    service = CreditService()
    # Passing a string for score must raise an exception (type validation)
    with pytest.raises(Exception):
        service.evaluate("700", Decimal("5000"), 21)


# BR04 – Income must be a positive decimal value: non-decimal type must raise an exception
def test_br04_raise_on_income_non_decimal_type():
    service = CreditService()
    # Passing a plain int for income must raise an exception (type validation)
    with pytest.raises(Exception):
        service.evaluate(700, 5000, 21)


# BR04 – Age must be a positive integer value: non-positive (zero) must raise an exception
def test_br04_raise_on_age_non_positive_zero():
    service = CreditService()
    # Age = 0 is not positive; must raise an exception
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"), 0)


# BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 != 5000)
def test_br05_income_not_normalized_fractional():
    service = CreditService()
    # Income slightly below threshold must not be rounded up or normalized
    result = service.evaluate(700, Decimal("4999.9999"), 21)
    assert result == "DENIED"


# BR06 – Any validation failure must result in an exception (missing value triggers exception)
def test_br06_raise_exception_on_missing_income_argument():
    service = CreditService()
    # Omitting the income argument should raise an exception (missing value validation)
    with pytest.raises(Exception):
        # Call with positional args but omit income intentionally
        service.evaluate(700, 21)  # type: ignore[arg-type]


# BR07 – The system must not infer, guess, or assume values that were not provided
def test_br07_no_inference_when_score_is_none():
    service = CreditService()
    # Passing None for score must not be inferred; must raise an exception
    with pytest.raises(Exception):
        service.evaluate(None, Decimal("5000"), 21)


# BR08 – There are no intermediate approval levels (only "APPROVED" or "DENIED")
def test_br08_no_intermediate_approval_levels_returns_only_approved_or_denied_string():
    service = CreditService()
    # Use valid types that produce a decision; assert it is one of the two allowed outcomes
    result = service.evaluate(650, Decimal("4000"), 30)
    assert isinstance(result, str)
    assert result in ("APPROVED", "DENIED")
    # Explicitly assert it is not any other intermediate label
    assert result not in ("PENDING", "PARTIAL", "REVIEW")


# BR09 – Credit analysis is an indivisible operation: must not return partial results or expose decision criteria
def test_br09_analysis_indivisible_returns_single_result_type_str():
    service = CreditService()
    # For valid inputs, the return must be a single string result (no tuple/dict/list)
    result = service.evaluate(700, Decimal("5000"), 21)
    assert isinstance(result, str)


# FR01 – Evaluate using exclusively the provided score, income, and age values (no enrichment): unexpected extra parameter not accepted
def test_fr01_reject_extra_unexpected_input_parameters_ensures_no_enrichment():
    service = CreditService()
    # Passing an extra unexpected keyword argument must not be silently accepted or used
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"), 21, extra="unexpected")  # type: ignore[arg-type]


# FR02 – Mandatory validation of all criteria before returning any result
def test_fr02_mandatory_validation_before_return_raises_on_invalid_type():
    service = CreditService()
    # Invalid type for age should raise before any decision is returned
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"), "21")


# FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful
def test_fr03_return_only_approved_or_denied_for_valid_input():
    service = CreditService()
    # Use valid types that fail business thresholds so a valid decision ("DENIED") is expected
    result = service.evaluate(600, Decimal("4000"), 30)
    assert result in ("APPROVED", "DENIED")
    assert result == "DENIED"


# FR04 – Record exactly one analysis result only when a valid decision ("APPROVED" or "DENIED") is produced
def test_fr04_record_exactly_one_analysis_result_returns_single_string():
    service = CreditService()
    # For a valid decision, ensure a single string result is returned (not a collection)
    result = service.evaluate(700, Decimal("5000"), 21)
    assert isinstance(result, str)


# FR05 – Raise an exception whenever any validation failure occurs (including magic values like NaN)
def test_fr05_raise_on_magic_value_nan_in_income():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("NaN"), 21)


# FR06 – Do not return any business result when an exception is raised
def test_fr06_no_business_result_returned_when_exception_is_raised():
    service = CreditService()
    with pytest.raises(Exception):
        _ = service.evaluate("invalid_score", Decimal("5000"), 21)


# FR07 – Do not expose intermediate states, partial results, or progress messages during or after the analysis
def test_fr07_no_exposure_of_intermediate_states_returns_no_partial_results_type():
    service = CreditService()
    # Ensure return is a single primitive string type for a valid decision (no partial structure)
    result = service.evaluate(699, Decimal("4999.99"), 20)
    assert isinstance(result, str)


# FR08 – Do not perform any kind of normalization, rounding, or automatic adjustment on input values
def test_fr08_no_normalization_income_decimal_strict():
    service = CreditService()
    # Income below threshold with high precision must not be rounded up to reach threshold
    result = service.evaluate(700, Decimal("4999.999999"), 21)
    assert result == "DENIED"