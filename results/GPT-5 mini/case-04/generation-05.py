import pytest
from decimal import Decimal
from cases.case04 import CreditService

# BR01 – Credit may only be approved if Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21
def test_br01_credit_approved_when_all_criteria_met():
    service = CreditService()
    # All criteria meet exact thresholds: expect explicit approval
    result = service.evaluate(700, Decimal("5000"), 21)
    assert result == "APPROVED"

# BR02 – If any of the criteria fail, the credit must be denied
def test_br02_credit_denied_when_one_criterion_fails_score_below_threshold():
    service = CreditService()
    # Score fails (699) while other inputs are valid: expect explicit denial
    result = service.evaluate(699, Decimal("5000"), 21)
    assert result == "DENIED"

# BR03 – Values as NaN or Infinity are not allowed and must result in an exception
def test_br03_exception_raised_for_income_nan():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("NaN"), 21)

# BR04 – Score: positive integer value (validate type/constraint)
def test_br04_exception_raised_for_non_integer_score():
    service = CreditService()
    # Score provided as non-integer (float) must be validation failure -> exception
    with pytest.raises(Exception):
        service.evaluate(700.0, Decimal("5000"), 21)

# BR04 – Income: positive decimal value (validate type/constraint)
def test_br04_exception_raised_for_non_decimal_income():
    service = CreditService()
    # Income provided as string (not Decimal) must be validation failure -> exception
    with pytest.raises(Exception):
        service.evaluate(700, "5000", 21)

# BR04 – Age: positive integer value (validate type/constraint)
def test_br04_exception_raised_for_non_integer_age():
    service = CreditService()
    # Age provided as negative integer violates "positive" constraint -> exception
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"), -1)

# BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 ≠ 5000)
def test_br05_income_not_normalized_and_results_in_denied():
    service = CreditService()
    # Income is 4999.9999; must NOT be normalized to 5000 and should therefore be denied
    result = service.evaluate(700, Decimal("4999.9999"), 21)
    assert result == "DENIED"

# BR06 – Any validation failure must result in an exception
def test_br06_exception_raised_for_negative_income_validation_failure():
    service = CreditService()
    # Negative income is a validation failure and must raise an exception
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("-1000"), 30)

# BR07 – The system must not infer, guess, or assume values that were not provided
def test_br07_exception_raised_when_age_missing_no_inference():
    service = CreditService()
    # Omitting age (missing value) must result in an exception (no inference)
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"))  # age omitted

# BR08 – There are no intermediate approval levels
def test_br08_evaluate_returns_only_final_status_string_not_intermediate_value():
    service = CreditService()
    # For a valid input set, evaluate must return a single final status (not an intermediate object)
    result = service.evaluate(800, Decimal("6000"), 40)
    # Validate the result is exactly one of the final statuses (single final decision)
    assert result == "APPROVED" or result == "DENIED"

# BR09 – Credit analysis is an indivisible operation (must not return partial results)
def test_br09_evaluate_returns_single_primitive_result_no_partial_structure():
    service = CreditService()
    result = service.evaluate(700, Decimal("5000"), 21)
    # The operation must return a single primitive result (string), not a tuple/list/dict
    assert isinstance(result, str)

# FR01 – Evaluate using exclusively provided score, income, and age values (no inference/normalization)
def test_fr01_evaluation_based_strictly_on_provided_values_approved_case():
    service = CreditService()
    # Using exact provided values that meet all thresholds must produce approval
    result = service.evaluate(750, Decimal("8000"), 35)
    assert result == "APPROVED"

# FR02 – Mandatory validation of all criteria before returning any result
def test_fr02_validation_of_all_criteria_raises_exception_on_invalid_type_before_result():
    service = CreditService()
    # Invalid score type should cause validation to raise before any business result is returned
    with pytest.raises(Exception):
        service.evaluate("700", Decimal("5000"), 21)

# FR03 – Return exclusively "APPROVED" or "DENIED" when all validations are successful
def test_fr03_return_denied_when_validations_pass_but_criteria_fail():
    service = CreditService()
    # All inputs are valid types, but a business criterion fails -> must return "DENIED"
    result = service.evaluate(700, Decimal("4999.9999"), 21)
    assert result == "DENIED"

# FR04 – Record exactly one analysis result only when a valid decision is produced (observable as single return)
def test_fr04_single_result_returned_when_decision_made():
    service = CreditService()
    result = service.evaluate(720, Decimal("5200"), 25)
    # The observable behavior is a single returned analysis result (single string)
    assert isinstance(result, str)

# FR05 – Raise an exception whenever any validation failure occurs
def test_fr05_exception_on_validation_failure_invalid_age_type():
    service = CreditService()
    # Age as float must be a validation failure and raise an exception
    with pytest.raises(Exception):
        service.evaluate(700, Decimal("5000"), 21.0)

# FR06 – Do not return any business result when an exception is raised
def test_fr06_no_business_result_returned_when_exception_is_raised():
    service = CreditService()
    with pytest.raises(Exception):
        service.evaluate(700.5, Decimal("5000"), 21)  # non-integer score triggers exception

# FR07 – Do not expose intermediate states, partial results, or progress messages
def test_fr07_no_intermediate_states_exposed_result_is_final_string_only():
    service = CreditService()
    result = service.evaluate(700, Decimal("5000"), 21)
    # Final API output must be a final decision string only
    assert isinstance(result, str)

# FR08 – Do not perform any kind of normalization, rounding, or automatic adjustment on input values
def test_fr08_no_normalization_on_income_boundary_value_results_in_denied():
    service = CreditService()
    # Income slightly below 5000 must not be rounded up; decision must reflect provided value
    result = service.evaluate(700, Decimal("4999.9999"), 21)
    assert result == "DENIED"