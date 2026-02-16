
"""
Automated test cases for Personal Credit Approval System. 
Based exclusively on the formal specifications provided.
"""

import pytest
import math
from decimal import Decimal

# Assuming the CreditService class is imported from the system under test
from cases.case04 import CreditService


class TestBR01CreditApprovalCriteria:
    """Tests for BR01: Credit approval requires Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21 simultaneously."""

    # BR01 – Credit approved when all three criteria are met exactly at thresholds
    def test_credit_approved_when_score_equals_700_income_equals_5000_age_equals_21(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # BR01 – Credit approved when all criteria exceed minimum thresholds
    def test_credit_approved_when_score_above_700_income_above_5000_age_above_21(self, credit_service):
        result = credit_service. evaluate(score=800, income=Decimal("10000"), age=35)
        assert result == "APPROVED"

    # BR01 – Credit approved with score exactly 700
    def test_credit_approved_with_score_exactly_700(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("6000"), age=30)
        assert result == "APPROVED"

    # BR01 – Credit approved with income exactly 5000
    def test_credit_approved_with_income_exactly_5000(self, credit_service):
        result = credit_service.evaluate(score=750, income=Decimal("5000"), age=25)
        assert result == "APPROVED"

    # BR01 – Credit approved with age exactly 21
    def test_credit_approved_with_age_exactly_21(self, credit_service):
        result = credit_service.evaluate(score=750, income=Decimal("6000"), age=21)
        assert result == "APPROVED"


class TestBR02CreditDenialCriteria:
    """Tests for BR02: Credit must be denied if any criterion fails."""

    # BR02 – Credit denied when score is below 700
    def test_credit_denied_when_score_below_700(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # BR02 – Credit denied when income is below 5000
    def test_credit_denied_when_income_below_5000(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("4999"), age=21)
        assert result == "DENIED"

    # BR02 – Credit denied when age is below 21
    def test_credit_denied_when_age_below_21(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    # BR02 – Credit denied when only score fails
    def test_credit_denied_when_only_score_fails(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("10000"), age=40)
        assert result == "DENIED"

    # BR02 – Credit denied when only income fails
    def test_credit_denied_when_only_income_fails(self, credit_service):
        result = credit_service.evaluate(score=800, income=Decimal("4999.99"), age=40)
        assert result == "DENIED"

    # BR02 – Credit denied when only age fails
    def test_credit_denied_when_only_age_fails(self, credit_service):
        result = credit_service.evaluate(score=800, income=Decimal("10000"), age=20)
        assert result == "DENIED"

    # BR02 – Credit denied when two criteria fail
    def test_credit_denied_when_score_and_income_fail(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("4999"), age=21)
        assert result == "DENIED"

    # BR02 – Credit denied when all three criteria fail
    def test_credit_denied_when_all_criteria_fail(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("4999"), age=20)
        assert result == "DENIED"


class TestBR03NaNAndInfinityValues:
    """Tests for BR03: NaN or Infinity values must result in an exception."""

    # BR03 – Exception raised when income is NaN
    def test_exception_raised_when_income_is_nan(self, credit_service):
        with pytest. raises(Exception):
            credit_service.evaluate(score=700, income=float("nan"), age=21)

    # BR03 – Exception raised when income is positive infinity
    def test_exception_raised_when_income_is_positive_infinity(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("inf"), age=21)

    # BR03 – Exception raised when income is negative infinity
    def test_exception_raised_when_income_is_negative_infinity(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("-inf"), age=21)


class TestBR04TypeAndConstraintValidation: 
    """Tests for BR04: Score and Age must be positive integers, Income must be positive decimal."""

    # BR04 – Exception raised when score is negative
    def test_exception_raised_when_score_is_negative(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=-1, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is zero
    def test_exception_raised_when_score_is_zero(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score=0, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is float instead of integer
    def test_exception_raised_when_score_is_float(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700.5, income=Decimal("5000"), age=21)

    # BR04 – Exception raised when score is string
    def test_exception_raised_when_score_is_string(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score="700", income=Decimal("5000"), age=21)

    # BR04 – Exception raised when income is negative
    def test_exception_raised_when_income_is_negative(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("-1"), age=21)

    # BR04 – Exception raised when income is zero
    def test_exception_raised_when_income_is_zero(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=Decimal("0"), age=21)

    # BR04 – Exception raised when income is string
    def test_exception_raised_when_income_is_string(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income="5000", age=21)

    # BR04 – Exception raised when age is negative
    def test_exception_raised_when_age_is_negative(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=Decimal("5000"), age=-1)

    # BR04 – Exception raised when age is zero
    def test_exception_raised_when_age_is_zero(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=0)

    # BR04 – Exception raised when age is float instead of integer
    def test_exception_raised_when_age_is_float(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=21.5)

    # BR04 – Exception raised when age is string
    def test_exception_raised_when_age_is_string(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=Decimal("5000"), age="21")


class TestBR05NoNormalizationOrAdjustment: 
    """Tests for BR05: Values must not be normalized or implicitly adjusted."""

    # BR05 – Values must not be normalized:  4999.9999 is not equal to 5000
    def test_income_4999_9999_is_not_normalized_to_5000(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
        assert result == "DENIED"

    # BR05 – Values must not be normalized: 699.9 score should raise exception (not integer)
    def test_score_699_9_is_not_normalized_to_700(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=699.9, income=Decimal("5000"), age=21)

    # BR05 – Values must not be normalized: 20. 9 age should raise exception (not integer)
    def test_age_20_9_is_not_normalized_to_21(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=20.9)

    # BR05 – Income with many decimal places must be evaluated exactly
    def test_income_with_precise_decimal_value_below_threshold(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("4999.999999999999"), age=21)
        assert result == "DENIED"

    # BR05 – Income exactly at threshold with decimal representation
    def test_income_exactly_5000_as_decimal_with_zeros(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000.00"), age=21)
        assert result == "APPROVED"


class TestBR06ValidationFailureException:
    """Tests for BR06: Any validation failure must result in an exception."""

    # BR06 – Exception raised for None score
    def test_exception_raised_when_score_is_none(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=None, income=Decimal("5000"), age=21)

    # BR06 – Exception raised for None income
    def test_exception_raised_when_income_is_none(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=None, age=21)

    # BR06 – Exception raised for None age
    def test_exception_raised_when_age_is_none(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=Decimal("5000"), age=None)

    # BR06 – Exception raised for invalid type combination
    def test_exception_raised_when_all_values_are_none(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=None, income=None, age=None)


class TestBR07NoValueInference:
    """Tests for BR07: System must not infer, guess, or assume values not provided."""

    # BR07 – Exception raised when score is missing (not provided)
    def test_exception_raised_when_score_not_provided(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(income=Decimal("5000"), age=21)

    # BR07 – Exception raised when income is missing (not provided)
    def test_exception_raised_when_income_not_provided(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, age=21)

    # BR07 – Exception raised when age is missing (not provided)
    def test_exception_raised_when_age_not_provided(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"))

    # BR07 – Exception raised when no parameters provided
    def test_exception_raised_when_no_parameters_provided(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate()


class TestBR08NoIntermediateApprovalLevels:
    """Tests for BR08: There are no intermediate approval levels."""

    # BR08 – Result is exactly APPROVED when all criteria met
    def test_result_is_exactly_approved_string(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        assert result != "PARTIALLY_APPROVED"
        assert result != "PENDING"

    # BR08 – Result is exactly DENIED when criteria not met
    def test_result_is_exactly_denied_string(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        assert result != "PARTIALLY_DENIED"
        assert result != "PENDING"


class TestBR09IndivisibleOperation:
    """Tests for BR09: Credit analysis is an indivisible operation."""

    # BR09 – Operation returns single result without intermediate states
    def test_evaluate_returns_single_final_result_approved(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)
        assert result in ["APPROVED", "DENIED"]

    # BR09 – Operation returns single result without intermediate states for denial
    def test_evaluate_returns_single_final_result_denied(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert isinstance(result, str)
        assert result in ["APPROVED", "DENIED"]


class TestFR01EvaluateWithProvidedValuesOnly:
    """Tests for FR01: Evaluate using exclusively provided values, no inference or enrichment."""

    # FR01 – Evaluation uses exact score value provided
    def test_evaluation_uses_exact_score_value(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # FR01 – Evaluation uses exact income value provided
    def test_evaluation_uses_exact_income_value(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000.01"), age=21)
        assert result == "APPROVED"

    # FR01 – Evaluation uses exact age value provided
    def test_evaluation_uses_exact_age_value(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=22)
        assert result == "APPROVED"


class TestFR02MandatoryValidationBeforeResult:
    """Tests for FR02: Mandatory validation of all criteria before returning any result."""

    # FR02 – All criteria validated:  valid inputs produce result
    def test_all_criteria_validated_produces_approved_result(self, credit_service):
        result = credit_service.evaluate(score=750, income=Decimal("7500"), age=30)
        assert result == "APPROVED"

    # FR02 – All criteria validated: invalid score type raises exception before result
    def test_invalid_score_type_raises_exception_before_result(self, credit_service):
        with pytest. raises(Exception):
            credit_service. evaluate(score="invalid", income=Decimal("5000"), age=21)

    # FR02 – All criteria validated: invalid income type raises exception before result
    def test_invalid_income_type_raises_exception_before_result(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income="invalid", age=21)

    # FR02 – All criteria validated:  invalid age type raises exception before result
    def test_invalid_age_type_raises_exception_before_result(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age="invalid")


class TestFR03ReturnApprovedOrDeniedOnly:
    """Tests for FR03: Return exclusively APPROVED or DENIED when validations succeed."""

    # FR03 – Returns APPROVED for valid application meeting criteria
    def test_returns_approved_for_valid_application_meeting_criteria(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # FR03 – Returns DENIED for valid application not meeting criteria
    def test_returns_denied_for_valid_application_not_meeting_criteria(self, credit_service):
        result = credit_service.evaluate(score=600, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # FR03 – Return type is string
    def test_return_type_is_string_for_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)

    # FR03 – Return type is string for denied
    def test_return_type_is_string_for_denied(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert isinstance(result, str)


class TestFR04RecordExactlyOneResult:
    """Tests for FR04: Record exactly one analysis result for valid decisions."""

    # FR04 – Single APPROVED result is produced
    def test_single_approved_result_produced(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # FR04 – Single DENIED result is produced
    def test_single_denied_result_produced(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"


class TestFR05ExceptionForValidationFailure: 
    """Tests for FR05: Raise exception for validation failures including invalid type, missing value, NaN, Infinity."""

    # FR05 – Exception for invalid type:  score as list
    def test_exception_for_score_as_list(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=[700], income=Decimal("5000"), age=21)

    # FR05 – Exception for invalid type: income as dict
    def test_exception_for_income_as_dict(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income={"value": 5000}, age=21)

    # FR05 – Exception for invalid type: age as boolean
    def test_exception_for_age_as_boolean(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=True)

    # FR05 – Exception for NaN income value
    def test_exception_for_nan_income(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("nan"), age=21)

    # FR05 – Exception for Infinity income value
    def test_exception_for_infinity_income(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("inf"), age=21)

    # FR05 – Exception for missing score value
    def test_exception_for_missing_score_value(self, credit_service):
        with pytest.raises(Exception):
            credit_service.evaluate(score=None, income=Decimal("5000"), age=21)


class TestFR06NoBusinessResultOnException:
    """Tests for FR06: Do not return any business result when an exception is raised."""

    # FR06 – No business result returned when exception raised for invalid score
    def test_no_result_when_exception_for_invalid_score(self, credit_service):
        with pytest.raises(Exception):
            result = credit_service. evaluate(score="invalid", income=Decimal("5000"), age=21)
            # If we reach here, the test should fail as exception was not raised
            assert result not in ["APPROVED", "DENIED"]

    # FR06 – No business result returned when exception raised for NaN
    def test_no_result_when_exception_for_nan(self, credit_service):
        with pytest.raises(Exception):
            result = credit_service.evaluate(score=700, income=float("nan"), age=21)
            assert result not in ["APPROVED", "DENIED"]

    # FR06 – No business result returned when exception raised for missing parameter
    def test_no_result_when_exception_for_missing_parameter(self, credit_service):
        with pytest. raises(Exception):
            result = credit_service.evaluate(score=700, income=Decimal("5000"))
            assert result not in ["APPROVED", "DENIED"]


class TestFR07NoIntermediateStatesExposed:
    """Tests for FR07: Do not expose intermediate states, partial results, or progress messages."""

    # FR07 – Evaluate returns only final result, not a tuple or list
    def test_evaluate_returns_only_final_result_not_tuple(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert not isinstance(result, tuple)

    # FR07 – Evaluate returns only final result, not a list
    def test_evaluate_returns_only_final_result_not_list(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert not isinstance(result, list)

    # FR07 – Evaluate returns only final result, not a dict
    def test_evaluate_returns_only_final_result_not_dict(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert not isinstance(result, dict)


class TestFR08NoNormalizationRoundingOrAdjustment: 
    """Tests for FR08: No normalization, rounding, or automatic adjustment on input values."""

    # FR08 – Income 4999.99 is not rounded up to 5000
    def test_income_4999_99_not_rounded_up(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    # FR08 – Income 5000.01 is not rounded down to 5000
    def test_income_5000_01_not_rounded_down(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000.01"), age=21)
        assert result == "APPROVED"

    # FR08 – Score 699 is not adjusted to 700
    def test_score_699_not_adjusted_to_700(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # FR08 – Age 20 is not adjusted to 21
    def test_age_20_not_adjusted_to_21(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"


class TestEdgeCasesScoreThreshold:
    """Edge case tests for score threshold boundary."""

    # Edge case – Score exactly at boundary 700 (approved)
    def test_score_exactly_700_boundary_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # Edge case – Score one below boundary 699 (denied)
    def test_score_one_below_boundary_699_denied(self, credit_service):
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # Edge case – Score one above boundary 701 (approved)
    def test_score_one_above_boundary_701_approved(self, credit_service):
        result = credit_service. evaluate(score=701, income=Decimal("5000"), age=21)
        assert result == "APPROVED"


class TestEdgeCasesIncomeThreshold:
    """Edge case tests for income threshold boundary."""

    # Edge case – Income exactly at boundary 5000 (approved)
    def test_income_exactly_5000_boundary_approved(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # Edge case – Income one cent below boundary 4999. 99 (denied)
    def test_income_one_cent_below_boundary_4999_99_denied(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    # Edge case – Income one cent above boundary 5000.01 (approved)
    def test_income_one_cent_above_boundary_5000_01_approved(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("5000.01"), age=21)
        assert result == "APPROVED"


class TestEdgeCasesAgeThreshold:
    """Edge case tests for age threshold boundary."""

    # Edge case – Age exactly at boundary 21 (approved)
    def test_age_exactly_21_boundary_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # Edge case – Age one below boundary 20 (denied)
    def test_age_one_below_boundary_20_denied(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    # Edge case – Age one above boundary 22 (approved)
    def test_age_one_above_boundary_22_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=22)
        assert result == "APPROVED"


class TestEdgeCasesMinimumPositiveValues:
    """Edge case tests for minimum positive values as per BR04."""

    # Edge case – Minimum positive score (1) with other valid values
    def test_minimum_positive_score_1_denied(self, credit_service):
        result = credit_service. evaluate(score=1, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    # Edge case – Minimum positive income with other valid values
    def test_minimum_positive_income_denied(self, credit_service):
        result = credit_service. evaluate(score=700, income=Decimal("0.01"), age=21)
        assert result == "DENIED"

    # Edge case – Minimum positive age (1) with other valid values
    def test_minimum_positive_age_1_denied(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=1)
        assert result == "DENIED"


class TestEdgeCasesLargeValues:
    """Edge case tests for large values."""

    # Edge case – Very high score approved
    def test_very_high_score_approved(self, credit_service):
        result = credit_service.evaluate(score=999999999, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    # Edge case – Very high income approved
    def test_very_high_income_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("999999999. 99"), age=21)
        assert result == "APPROVED"

    # Edge case – Very high age approved
    def test_very_high_age_approved(self, credit_service):
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=150)
        assert result == "APPROVED"


# Fixture for CreditService instance
@pytest.fixture
def credit_service():
    """Fixture to provide CreditService instance for tests."""
    # This would be replaced with actual import in real implementation
    # from credit_system import CreditService
    # return CreditService()
    
    # Placeholder for test structure - actual implementation would import real class
    from credit_system import CreditService
    return CreditService()
