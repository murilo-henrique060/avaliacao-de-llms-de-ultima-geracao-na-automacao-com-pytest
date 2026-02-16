
"""
Automated test cases for Personal Credit Approval System. 
Generated using pytest library based on formal specifications.
"""

import pytest
from decimal import Decimal
import math

# Import the system under test (assumed to be implemented elsewhere)
from cases.case04 import CreditService


class TestBR01CreditApprovalCriteria:
    """Tests for BR01: Credit approval requires Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21 simultaneously."""

    # BR01 – Credit approved when all criteria are met exactly at boundaries
    def test_credit_approved_when_score_exactly_700_income_exactly_5000_age_exactly_21(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # BR01 – Credit approved when all criteria exceed minimum thresholds
    def test_credit_approved_when_all_criteria_exceed_minimum_thresholds(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal("10000"), age=30)
        assert result == "APPROVED"

    # BR01 – Credit approved with score exactly at threshold and others above
    def test_credit_approved_with_score_exactly_700_and_other_criteria_above_minimum(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("6000"), age=25)
        assert result == "APPROVED"

    # BR01 – Credit approved with income exactly at threshold and others above
    def test_credit_approved_with_income_exactly_5000_and_other_criteria_above_minimum(self):
        service = CreditService()
        result = service. evaluate(score=750, income=Decimal("5000"), age=25)
        assert result == "APPROVED"

    # BR01 – Credit approved with age exactly at threshold and others above
    def test_credit_approved_with_age_exactly_21_and_other_criteria_above_minimum(self):
        service = CreditService()
        result = service. evaluate(score=750, income=Decimal("6000"), age=21)
        assert result == "APPROVED"


class TestBR02CreditDenialOnCriteriaFailure: 
    """Tests for BR02: Credit must be denied if any of the criteria fail."""

    # BR02 – Credit denied when score is below 700
    def test_credit_denied_when_score_is_699(self):
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # BR02 – Credit denied when income is below 5000
    def test_credit_denied_when_income_is_4999_99(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999. 99"), age=21)
        assert result == "DENIED"

    # BR02 – Credit denied when age is below 21
    def test_credit_denied_when_age_is_20(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    # BR02 – Credit denied when only score fails
    def test_credit_denied_when_only_score_fails_with_other_criteria_exceeding(self):
        service = CreditService()
        result = service.evaluate(score=600, income=Decimal("10000"), age=30)
        assert result == "DENIED"

    # BR02 – Credit denied when only income fails
    def test_credit_denied_when_only_income_fails_with_other_criteria_exceeding(self):
        service = CreditService()
        result = service. evaluate(score=800, income=Decimal("4000"), age=30)
        assert result == "DENIED"

    # BR02 – Credit denied when only age fails
    def test_credit_denied_when_only_age_fails_with_other_criteria_exceeding(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal("10000"), age=18)
        assert result == "DENIED"

    # BR02 – Credit denied when all criteria fail
    def test_credit_denied_when_all_criteria_fail(self):
        service = CreditService()
        result = service. evaluate(score=500, income=Decimal("3000"), age=18)
        assert result == "DENIED"

    # BR02 – Credit denied when two criteria fail (score and income)
    def test_credit_denied_when_score_and_income_fail(self):
        service = CreditService()
        result = service.evaluate(score=600, income=Decimal("4000"), age=25)
        assert result == "DENIED"

    # BR02 – Credit denied when two criteria fail (score and age)
    def test_credit_denied_when_score_and_age_fail(self):
        service = CreditService()
        result = service.evaluate(score=600, income=Decimal("6000"), age=18)
        assert result == "DENIED"

    # BR02 – Credit denied when two criteria fail (income and age)
    def test_credit_denied_when_income_and_age_fail(self):
        service = CreditService()
        result = service.evaluate(score=750, income=Decimal("4000"), age=18)
        assert result == "DENIED"


class TestBR03NaNAndInfinityValidation:
    """Tests for BR03: NaN or Infinity values must result in an exception."""

    # BR03 – Exception raised when score is NaN (using float representation)
    def test_exception_raised_when_score_is_nan(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=float("nan"), income=Decimal("5000"), age=21)

    # BR03 – Exception raised when income is NaN
    def test_exception_raised_when_income_is_nan(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("nan"), age=21)

    # BR03 – Exception raised when age is NaN (using float representation)
    def test_exception_raised_when_age_is_nan(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=float("nan"))

    # BR03 – Exception raised when score is positive Infinity
    def test_exception_raised_when_score_is_positive_infinity(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=float("inf"), income=Decimal("5000"), age=21)

    # BR03 – Exception raised when score is negative Infinity
    def test_exception_raised_when_score_is_negative_infinity(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=float("-inf"), income=Decimal("5000"), age=21)

    # BR03 – Exception raised when income is positive Infinity
    def test_exception_raised_when_income_is_positive_infinity(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=700, income=Decimal("Infinity"), age=21)

    # BR03 – Exception raised when income is negative Infinity
    def test_exception_raised_when_income_is_negative_infinity(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("-Infinity"), age=21)

    # BR03 – Exception raised when age is positive Infinity
    def test_exception_raised_when_age_is_positive_infinity(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=float("inf"))

    # BR03 – Exception raised when age is negative Infinity
    def test_exception_raised_when_age_is_negative_infinity(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=float("-inf"))


class TestBR04TypeAndConstraintValidation: 
    """Tests for BR04: Score must be positive integer, Income must be positive decimal, Age must be positive integer."""

    # BR04 – Exception raised when score is not an integer (float)
    def test_exception_raised_when_score_is_float(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700.5, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is not an integer (string)
    def test_exception_raised_when_score_is_string(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score="700", income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is zero
    def test_exception_raised_when_score_is_zero(self):
        service = CreditService()
        with pytest.raises(Exception):
            service. evaluate(score=0, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is negative
    def test_exception_raised_when_score_is_negative(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=-100, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when income is not a decimal (integer)
    def test_exception_raised_when_income_is_integer(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=5000, age=21)

    # BR04 – Exception raised when income is not a decimal (string)
    def test_exception_raised_when_income_is_string(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income="5000", age=21)

    # BR04 – Exception raised when income is zero
    def test_exception_raised_when_income_is_zero(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("0"), age=21)

    # BR04 – Exception raised when income is negative
    def test_exception_raised_when_income_is_negative(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("-1000"), age=21)

    # BR04 – Exception raised when age is not an integer (float)
    def test_exception_raised_when_age_is_float(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=21.5)

    # BR04 – Exception raised when age is not an integer (string)
    def test_exception_raised_when_age_is_string(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age="21")

    # BR04 – Exception raised when age is zero
    def test_exception_raised_when_age_is_zero(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=0)

    # BR04 – Exception raised when age is negative
    def test_exception_raised_when_age_is_negative(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=-5)

    # BR04 – Valid positive integer score is accepted
    def test_valid_positive_integer_score_is_accepted(self):
        service = CreditService()
        result = service.evaluate(score=1, income=Decimal("5000"), age=21)
        assert result == "DENIED"  # Score is valid but below threshold

    # BR04 – Valid positive decimal income is accepted
    def test_valid_positive_decimal_income_is_accepted(self):
        service = CreditService()
        result = service. evaluate(score=700, income=Decimal("0.01"), age=21)
        assert result == "DENIED"  # Income is valid but below threshold

    # BR04 – Valid positive integer age is accepted
    def test_valid_positive_integer_age_is_accepted(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=1)
        assert result == "DENIED"  # Age is valid but below threshold


class TestBR05NoNormalizationOrAdjustment: 
    """Tests for BR05: Values must not be normalized or implicitly adjusted."""

    # BR05 – Income 4999.9999 is not normalized to 5000
    def test_income_4999_9999_is_not_normalized_to_5000(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
        assert result == "DENIED"

    # BR05 – Income 4999.999999999999 is not normalized to 5000
    def test_income_4999_999999999999_is_not_normalized_to_5000(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.999999999999"), age=21)
        assert result == "DENIED"

    # BR05 – Score 699 is not rounded up to 700
    def test_score_699_is_not_rounded_up_to_700(self):
        service = CreditService()
        result = service. evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # BR05 – Age 20 is not adjusted to 21
    def test_age_20_is_not_adjusted_to_21(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    # BR05 – Income 5000.0000000001 is treated as exactly that value (above threshold)
    def test_income_5000_0000000001_is_above_threshold(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.0000000001"), age=21)
        assert result == "APPROVED"


class TestBR06ValidationFailureException:
    """Tests for BR06: Any validation failure must result in an exception."""

    # BR06 – Exception raised when score is None
    def test_exception_raised_when_score_is_none(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=None, income=Decimal("5000"), age=21)

    # BR06 – Exception raised when income is None
    def test_exception_raised_when_income_is_none(self):
        service = CreditService()
        with pytest.raises(Exception):
            service. evaluate(score=700, income=None, age=21)

    # BR06 – Exception raised when age is None
    def test_exception_raised_when_age_is_none(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=None)

    # BR06 – Exception raised when all parameters are None
    def test_exception_raised_when_all_parameters_are_none(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=None, income=None, age=None)


class TestBR07NoInferenceOrAssumption:
    """Tests for BR07: The system must not infer, guess, or assume values not provided."""

    # BR07 – Exception raised when score is missing (not provided)
    def test_exception_raised_when_score_is_not_provided(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(income=Decimal("5000"), age=21)

    # BR07 – Exception raised when income is missing (not provided)
    def test_exception_raised_when_income_is_not_provided(self):
        service = CreditService()
        with pytest.raises(Exception):
            service. evaluate(score=700, age=21)

    # BR07 – Exception raised when age is missing (not provided)
    def test_exception_raised_when_age_is_not_provided(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"))

    # BR07 – Exception raised when no parameters are provided
    def test_exception_raised_when_no_parameters_are_provided(self):
        service = CreditService()
        with pytest.raises(Exception):
            service. evaluate()


class TestBR08NoIntermediateApprovalLevels:
    """Tests for BR08: There are no intermediate approval levels."""

    # BR08 – Result is exactly APPROVED when all criteria are met
    def test_result_is_exactly_approved_when_all_criteria_met(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        assert result != "PARTIALLY_APPROVED"
        assert result != "CONDITIONALLY_APPROVED"

    # BR08 – Result is exactly DENIED when criteria are not met
    def test_result_is_exactly_denied_when_criteria_not_met(self):
        service = CreditService()
        result = service. evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        assert result != "PARTIALLY_DENIED"
        assert result != "PENDING"


class TestBR09IndivisibleOperation:
    """Tests for BR09: Credit analysis is an indivisible operation."""

    # BR09 – Evaluate returns only final result (APPROVED)
    def test_evaluate_returns_only_final_result_approved(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        assert isinstance(result, str)

    # BR09 – Evaluate returns only final result (DENIED)
    def test_evaluate_returns_only_final_result_denied(self):
        service = CreditService()
        result = service.evaluate(score=600, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        assert isinstance(result, str)

    # BR09 – CreditService does not expose internal state or steps
    def test_credit_service_does_not_expose_internal_state(self):
        service = CreditService()
        # Verify that there are no public methods for partial evaluation
        public_methods = [m for m in dir(service) if not m.startswith('_') and callable(getattr(service, m))]
        assert public_methods == ['evaluate']


class TestFR01EvaluationWithProvidedValuesOnly:
    """Tests for FR01: Evaluate using exclusively the provided score, income, and age values."""

    # FR01 – Evaluation uses exact score value provided
    def test_evaluation_uses_exact_score_value_provided(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # FR01 – Evaluation uses exact income value provided
    def test_evaluation_uses_exact_income_value_provided(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000. 00"), age=21)
        assert result == "APPROVED"

    # FR01 – Evaluation uses exact age value provided
    def test_evaluation_uses_exact_age_value_provided(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"


class TestFR02MandatoryValidationBeforeResult:
    """Tests for FR02: Mandatory validation of all criteria before returning any result."""

    # FR02 – All parameters must pass type validation before result
    def test_invalid_score_type_causes_exception_before_result(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score="invalid", income=Decimal("5000"), age=21)

    # FR02 – All parameters must pass value validation before result
    def test_invalid_income_value_causes_exception_before_result(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("-5000"), age=21)

    # FR02 – All parameters must be present before result
    def test_missing_age_causes_exception_before_result(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"))


class TestFR03ExclusiveResultValues:
    """Tests for FR03: Return exclusively APPROVED or DENIED when all validations are successful."""

    # FR03 – Valid evaluation returns APPROVED
    def test_valid_evaluation_returns_approved(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal("10000"), age=30)
        assert result == "APPROVED"

    # FR03 – Valid evaluation returns DENIED
    def test_valid_evaluation_returns_denied(self):
        service = CreditService()
        result = service.evaluate(score=500, income=Decimal("10000"), age=30)
        assert result == "DENIED"

    # FR03 – Result is string type
    def test_result_is_string_type(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)

    # FR03 – Result is one of exactly two possible values
    def test_result_is_one_of_two_possible_values(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result in ["APPROVED", "DENIED"]


class TestFR04SingleAnalysisResult:
    """Tests for FR04: Record exactly one analysis result only when a valid decision is produced."""

    # FR04 – Single APPROVED result returned for valid approval
    def test_single_approved_result_returned(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        # No additional results or side effects expected

    # FR04 – Single DENIED result returned for valid denial
    def test_single_denied_result_returned(self):
        service = CreditService()
        result = service.evaluate(score=600, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        # No additional results or side effects expected


class TestFR05ExceptionOnValidationFailure:
    """Tests for FR05: Raise exception on invalid type, missing value, magic value, or business rule violation."""

    # FR05 – Exception raised for invalid type (score as list)
    def test_exception_raised_for_score_as_list(self):
        service = CreditService()
        with pytest. raises(Exception):
            service.evaluate(score=[700], income=Decimal("5000"), age=21)

    # FR05 – Exception raised for invalid type (income as dict)
    def test_exception_raised_for_income_as_dict(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income={"value": 5000}, age=21)

    # FR05 – Exception raised for invalid type (age as boolean)
    def test_exception_raised_for_age_as_boolean(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000"), age=True)

    # FR05 – Exception raised for missing value (score is None)
    def test_exception_raised_for_missing_score_value(self):
        service = CreditService()
        with pytest.raises(Exception):
            service. evaluate(score=None, income=Decimal("5000"), age=21)

    # FR05 – Exception raised for magic value (income is NaN)
    def test_exception_raised_for_income_nan_magic_value(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("nan"), age=21)


class TestFR06NoBusinessResultOnException:
    """Tests for FR06: Do not return any business result when an exception is raised."""

    # FR06 – No result returned when exception is raised for invalid score
    def test_no_result_returned_when_exception_raised_for_invalid_score(self):
        service = CreditService()
        with pytest.raises(Exception) as exc_info: 
            service.evaluate(score="invalid", income=Decimal("5000"), age=21)
        # Verify exception was raised and no APPROVED/DENIED was returned
        assert exc_info.value is not None

    # FR06 – No result returned when exception is raised for invalid income
    def test_no_result_returned_when_exception_raised_for_invalid_income(self):
        service = CreditService()
        with pytest.raises(Exception) as exc_info:
            service.evaluate(score=700, income="invalid", age=21)
        assert exc_info.value is not None

    # FR06 – No result returned when exception is raised for invalid age
    def test_no_result_returned_when_exception_raised_for_invalid_age(self):
        service = CreditService()
        with pytest.raises(Exception) as exc_info:
            service.evaluate(score=700, income=Decimal("5000"), age="invalid")
        assert exc_info.value is not None


class TestFR07NoIntermediateStatesExposed:
    """Tests for FR07: Do not expose intermediate states, partial results, or progress messages."""

    # FR07 – Only evaluate method is publicly accessible
    def test_only_evaluate_method_is_publicly_accessible(self):
        service = CreditService()
        public_methods = [m for m in dir(service) if not m.startswith('_') and callable(getattr(service, m))]
        assert 'evaluate' in public_methods
        # Should not have methods like 'validate_score', 'check_income', 'get_partial_result', etc. 
        forbidden_methods = ['validate_score', 'check_income', 'check_age', 'get_partial_result', 'get_progress']
        for method in forbidden_methods:
            assert method not in public_methods

    # FR07 – Evaluate returns only final string result
    def test_evaluate_returns_only_final_string_result_not_dict(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)
        assert not isinstance(result, dict)
        assert not isinstance(result, list)
        assert not isinstance(result, tuple)


class TestFR08NoNormalizationRoundingOrAdjustment: 
    """Tests for FR08: Do not perform any normalization, rounding, or automatic adjustment on input values."""

    # FR08 – Income 4999.50 is not rounded to 5000
    def test_income_4999_50_is_not_rounded_to_5000(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.50"), age=21)
        assert result == "DENIED"

    # FR08 – Income with many decimal places is preserved exactly
    def test_income_with_many_decimal_places_preserved_exactly(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.123456789012345"), age=21)
        assert result == "APPROVED"

    # FR08 – Score is not adjusted from 699 to 700
    def test_score_is_not_adjusted_from_699_to_700(self):
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal("10000"), age=30)
        assert result == "DENIED"

    # FR08 – Age is not adjusted from 20 to 21
    def test_age_is_not_adjusted_from_20_to_21(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal("10000"), age=20)
        assert result == "DENIED"


class TestEdgeCasesExplicitlyRequiredByRules:
    """Edge case tests explicitly required by the business rules and functional requirements."""

    # Edge case – Exact boundary values all met simultaneously
    def test_exact_boundary_values_all_met_simultaneously(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # Edge case – One unit below score threshold
    def test_one_unit_below_score_threshold(self):
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # Edge case – One cent below income threshold
    def test_one_cent_below_income_threshold(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    # Edge case – One year below age threshold
    def test_one_year_below_age_threshold(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    # Edge case – Large valid values
    def test_large_valid_values(self):
        service = CreditService()
        result = service.evaluate(score=999, income=Decimal("999999999.99"), age=120)
        assert result == "APPROVED"

    # Edge case – Minimum positive integer for score
    def test_minimum_positive_integer_score(self):
        service = CreditService()
        result = service.evaluate(score=1, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # Edge case – Minimum positive decimal for income
    def test_minimum_positive_decimal_income(self):
        service = CreditService()
        result = service. evaluate(score=700, income=Decimal("0.01"), age=21)
        assert result == "DENIED"

    # Edge case – Minimum positive integer for age
    def test_minimum_positive_integer_age(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000"), age=1)
        assert result == "DENIED"

    # Edge case – Very precise decimal income just below threshold
    def test_very_precise_decimal_income_just_below_threshold(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.9999999999999999"), age=21)
        assert result == "DENIED"

    # Edge case – Very precise decimal income just above threshold
    def test_very_precise_decimal_income_just_above_threshold(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.0000000000000001"), age=21)
        assert result == "APPROVED"
