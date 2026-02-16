
"""
Automated test suite for Personal Credit Approval System. 
Tests are based exclusively on the provided formal specifications.
"""

import pytest
import math
from decimal import Decimal


# Assuming the CreditService class is imported from the system under test
# from credit_system import CreditService


class TestBR01CreditApprovalCriteria:
    """Tests for BR01: Credit approval requires Score ≥ 700, Income ≥ R$ 5,000, Age ≥ 21 simultaneously."""

    def test_br01_credit_approved_when_all_criteria_met_at_exact_boundaries(self, credit_service):
        # BR01 – Credit approved when score=700, income=5000, age=21 (exact boundary values)
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_br01_credit_approved_when_all_criteria_exceed_minimum(self, credit_service):
        # BR01 – Credit approved when all values exceed minimum thresholds
        result = credit_service. evaluate(score=800, income=Decimal("10000"), age=30)
        assert result == "APPROVED"

    def test_br01_credit_denied_when_score_below_700(self, credit_service):
        # BR01 – Credit denied when score=699 (below threshold) even if other criteria met
        result = credit_service. evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    def test_br01_credit_denied_when_income_below_5000(self, credit_service):
        # BR01 – Credit denied when income=4999.99 (below threshold) even if other criteria met
        result = credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    def test_br01_credit_denied_when_age_below_21(self, credit_service):
        # BR01 – Credit denied when age=20 (below threshold) even if other criteria met
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"


class TestBR02CreditDenialOnCriteriaFailure: 
    """Tests for BR02: If any of the criteria fail, the credit must be denied."""

    def test_br02_credit_denied_when_only_score_fails(self, credit_service):
        # BR02 – Credit denied when only score criterion fails
        result = credit_service.evaluate(score=699, income=Decimal("6000"), age=25)
        assert result == "DENIED"

    def test_br02_credit_denied_when_only_income_fails(self, credit_service):
        # BR02 – Credit denied when only income criterion fails
        result = credit_service.evaluate(score=750, income=Decimal("4999"), age=25)
        assert result == "DENIED"

    def test_br02_credit_denied_when_only_age_fails(self, credit_service):
        # BR02 – Credit denied when only age criterion fails
        result = credit_service.evaluate(score=750, income=Decimal("6000"), age=20)
        assert result == "DENIED"

    def test_br02_credit_denied_when_two_criteria_fail(self, credit_service):
        # BR02 – Credit denied when score and income fail
        result = credit_service.evaluate(score=699, income=Decimal("4999"), age=25)
        assert result == "DENIED"

    def test_br02_credit_denied_when_all_criteria_fail(self, credit_service):
        # BR02 – Credit denied when all three criteria fail
        result = credit_service. evaluate(score=699, income=Decimal("4999"), age=20)
        assert result == "DENIED"


class TestBR03NaNAndInfinityNotAllowed:
    """Tests for BR03: Values as NaN or Infinity are not allowed and must result in an exception."""

    def test_br03_exception_raised_when_income_is_nan(self, credit_service):
        # BR03 – Exception raised when income is NaN
        with pytest. raises(Exception):
            credit_service.evaluate(score=700, income=float("nan"), age=21)

    def test_br03_exception_raised_when_income_is_positive_infinity(self, credit_service):
        # BR03 – Exception raised when income is positive Infinity
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("inf"), age=21)

    def test_br03_exception_raised_when_income_is_negative_infinity(self, credit_service):
        # BR03 – Exception raised when income is negative Infinity
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("-inf"), age=21)


class TestBR04TypeAndConstraintValidation:
    """Tests for BR04: Criteria must be validated according to types and constraints."""

    def test_br04_exception_raised_when_score_is_negative(self, credit_service):
        # BR04 – Exception raised when score is negative (must be positive integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=-1, income=Decimal("5000"), age=21)

    def test_br04_exception_raised_when_score_is_zero(self, credit_service):
        # BR04 – Exception raised when score is zero (must be positive integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=0, income=Decimal("5000"), age=21)

    def test_br04_exception_raised_when_score_is_float(self, credit_service):
        # BR04 – Exception raised when score is float (must be integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700.5, income=Decimal("5000"), age=21)

    def test_br04_exception_raised_when_income_is_negative(self, credit_service):
        # BR04 – Exception raised when income is negative (must be positive decimal)
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=Decimal("-1"), age=21)

    def test_br04_exception_raised_when_income_is_zero(self, credit_service):
        # BR04 – Exception raised when income is zero (must be positive decimal)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("0"), age=21)

    def test_br04_exception_raised_when_age_is_negative(self, credit_service):
        # BR04 – Exception raised when age is negative (must be positive integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=-1)

    def test_br04_exception_raised_when_age_is_zero(self, credit_service):
        # BR04 – Exception raised when age is zero (must be positive integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=0)

    def test_br04_exception_raised_when_age_is_float(self, credit_service):
        # BR04 – Exception raised when age is float (must be integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=21.5)

    def test_br04_exception_raised_when_score_is_string(self, credit_service):
        # BR04 – Exception raised when score is string (must be integer)
        with pytest. raises(Exception):
            credit_service. evaluate(score="700", income=Decimal("5000"), age=21)

    def test_br04_exception_raised_when_income_is_string(self, credit_service):
        # BR04 – Exception raised when income is string (must be decimal)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income="5000", age=21)

    def test_br04_exception_raised_when_age_is_string(self, credit_service):
        # BR04 – Exception raised when age is string (must be integer)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age="21")


class TestBR05NoNormalizationOrAdjustment: 
    """Tests for BR05: Values must not be normalized or implicitly adjusted."""

    def test_br05_income_4999_9999_is_not_equal_to_5000(self, credit_service):
        # BR05 – Values must not be normalized (4999.9999 ≠ 5000)
        result = credit_service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
        assert result == "DENIED"

    def test_br05_income_4999_999999999_is_not_rounded_to_5000(self, credit_service):
        # BR05 – Values must not be normalized or rounded
        result = credit_service.evaluate(score=700, income=Decimal("4999.999999999"), age=21)
        assert result == "DENIED"

    def test_br05_exact_income_5000_is_accepted(self, credit_service):
        # BR05 – Exact value 5000 is accepted without adjustment
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_br05_income_5000_0001_is_not_adjusted_down(self, credit_service):
        # BR05 – Value 5000.0001 is not adjusted down, remains above threshold
        result = credit_service.evaluate(score=700, income=Decimal("5000.0001"), age=21)
        assert result == "APPROVED"


class TestBR06ValidationFailureException:
    """Tests for BR06: Any validation failure must result in an exception."""

    def test_br06_exception_raised_for_none_score(self, credit_service):
        # BR06 – Exception raised when score is None
        with pytest.raises(Exception):
            credit_service.evaluate(score=None, income=Decimal("5000"), age=21)

    def test_br06_exception_raised_for_none_income(self, credit_service):
        # BR06 – Exception raised when income is None
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=None, age=21)

    def test_br06_exception_raised_for_none_age(self, credit_service):
        # BR06 – Exception raised when age is None
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age=None)


class TestBR07NoInferenceOrAssumption:
    """Tests for BR07: The system must not infer, guess, or assume values that were not provided."""

    def test_br07_exception_raised_when_score_not_provided(self, credit_service):
        # BR07 – Exception raised when score is missing (no inference)
        with pytest.raises(Exception):
            credit_service.evaluate(income=Decimal("5000"), age=21)

    def test_br07_exception_raised_when_income_not_provided(self, credit_service):
        # BR07 – Exception raised when income is missing (no inference)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, age=21)

    def test_br07_exception_raised_when_age_not_provided(self, credit_service):
        # BR07 – Exception raised when age is missing (no inference)
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"))


class TestBR08NoIntermediateApprovalLevels:
    """Tests for BR08: There are no intermediate approval levels."""

    def test_br08_result_is_approved_not_intermediate(self, credit_service):
        # BR08 – Result is exactly "APPROVED", no intermediate level
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        assert result != "PARTIALLY_APPROVED"
        assert result != "PENDING"

    def test_br08_result_is_denied_not_intermediate(self, credit_service):
        # BR08 – Result is exactly "DENIED", no intermediate level
        result = credit_service. evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        assert result != "PARTIALLY_DENIED"
        assert result != "UNDER_REVIEW"


class TestBR09IndivisibleOperation:
    """Tests for BR09: Credit analysis is an indivisible operation."""

    def test_br09_evaluate_returns_single_result_approved(self, credit_service):
        # BR09 – Evaluate returns a single indivisible result (APPROVED)
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)
        assert result == "APPROVED"

    def test_br09_evaluate_returns_single_result_denied(self, credit_service):
        # BR09 – Evaluate returns a single indivisible result (DENIED)
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert isinstance(result, str)
        assert result == "DENIED"

    def test_br09_evaluate_does_not_return_tuple_or_list(self, credit_service):
        # BR09 – Evaluate does not return partial results (tuple/list)
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert not isinstance(result, (tuple, list, dict))


class TestFR01ExclusiveEvaluationWithProvidedValues:
    """Tests for FR01: Evaluate using exclusively provided values."""

    def test_fr01_evaluate_uses_exact_provided_score(self, credit_service):
        # FR01 – Evaluation uses exactly the provided score value
        result_699 = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        result_700 = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result_699 == "DENIED"
        assert result_700 == "APPROVED"

    def test_fr01_evaluate_uses_exact_provided_income(self, credit_service):
        # FR01 – Evaluation uses exactly the provided income value
        result_4999 = credit_service.evaluate(score=700, income=Decimal("4999"), age=21)
        result_5000 = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result_4999 == "DENIED"
        assert result_5000 == "APPROVED"

    def test_fr01_evaluate_uses_exact_provided_age(self, credit_service):
        # FR01 – Evaluation uses exactly the provided age value
        result_20 = credit_service.evaluate(score=700, income=Decimal("5000"), age=20)
        result_21 = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result_20 == "DENIED"
        assert result_21 == "APPROVED"


class TestFR02MandatoryValidationBeforeResult:
    """Tests for FR02: Mandatory validation of all criteria before returning result."""

    def test_fr02_invalid_score_type_raises_exception_before_result(self, credit_service):
        # FR02 – Validation failure for invalid score type raises exception
        with pytest.raises(Exception):
            credit_service.evaluate(score="invalid", income=Decimal("5000"), age=21)

    def test_fr02_invalid_income_type_raises_exception_before_result(self, credit_service):
        # FR02 – Validation failure for invalid income type raises exception
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income="invalid", age=21)

    def test_fr02_invalid_age_type_raises_exception_before_result(self, credit_service):
        # FR02 – Validation failure for invalid age type raises exception
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=Decimal("5000"), age="invalid")


class TestFR03ExclusiveResults:
    """Tests for FR03: Return exclusively APPROVED or DENIED when validations pass."""

    def test_fr03_returns_approved_string(self, credit_service):
        # FR03 – Returns exactly "APPROVED" string
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_fr03_returns_denied_string(self, credit_service):
        # FR03 – Returns exactly "DENIED" string
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    def test_fr03_result_is_string_type_for_approved(self, credit_service):
        # FR03 – Result type is string for APPROVED
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert isinstance(result, str)

    def test_fr03_result_is_string_type_for_denied(self, credit_service):
        # FR03 – Result type is string for DENIED
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert isinstance(result, str)


class TestFR04SingleAnalysisResult:
    """Tests for FR04: Record exactly one analysis result for valid decisions."""

    def test_fr04_single_approved_result_returned(self, credit_service):
        # FR04 – Exactly one result returned for approved case
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_fr04_single_denied_result_returned(self, credit_service):
        # FR04 – Exactly one result returned for denied case
        result = credit_service. evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"


class TestFR05ExceptionOnValidationFailure: 
    """Tests for FR05: Raise exception for validation failures."""

    def test_fr05_exception_for_invalid_type_score(self, credit_service):
        # FR05 – Exception raised for invalid type (score as list)
        with pytest.raises(Exception):
            credit_service.evaluate(score=[700], income=Decimal("5000"), age=21)

    def test_fr05_exception_for_missing_value_score_none(self, credit_service):
        # FR05 – Exception raised for missing value (score is None)
        with pytest.raises(Exception):
            credit_service.evaluate(score=None, income=Decimal("5000"), age=21)

    def test_fr05_exception_for_magic_value_nan_income(self, credit_service):
        # FR05 – Exception raised for magic value NaN in income
        with pytest.raises(Exception):
            credit_service.evaluate(score=700, income=float("nan"), age=21)

    def test_fr05_exception_for_magic_value_infinity_income(self, credit_service):
        # FR05 – Exception raised for magic value Infinity in income
        with pytest. raises(Exception):
            credit_service. evaluate(score=700, income=float("inf"), age=21)

    def test_fr05_exception_for_negative_score_business_rule_violation(self, credit_service):
        # FR05 – Exception raised for business rule violation (negative score)
        with pytest.raises(Exception):
            credit_service.evaluate(score=-100, income=Decimal("5000"), age=21)


class TestFR06NoBusinessResultOnException:
    """Tests for FR06: Do not return business result when exception is raised."""

    def test_fr06_no_approved_returned_when_exception_raised(self, credit_service):
        # FR06 – No "APPROVED" returned when exception occurs
        with pytest. raises(Exception):
            result = credit_service. evaluate(score=None, income=Decimal("5000"), age=21)
            assert result != "APPROVED"

    def test_fr06_no_denied_returned_when_exception_raised(self, credit_service):
        # FR06 – No "DENIED" returned when exception occurs
        with pytest.raises(Exception):
            result = credit_service.evaluate(score=700, income=float("nan"), age=21)
            assert result != "DENIED"


class TestFR07NoIntermediateStatesExposed:
    """Tests for FR07: Do not expose intermediate states or partial results."""

    def test_fr07_approved_result_is_final_not_partial(self, credit_service):
        # FR07 – APPROVED is a final result, not partial
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"
        assert "partial" not in result. lower()
        assert "pending" not in result. lower()

    def test_fr07_denied_result_is_final_not_partial(self, credit_service):
        # FR07 – DENIED is a final result, not partial
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"
        assert "partial" not in result.lower()
        assert "pending" not in result.lower()


class TestFR08NoNormalizationRoundingOrAdjustment: 
    """Tests for FR08: Do not perform normalization, rounding, or automatic adjustment."""

    def test_fr08_no_rounding_income_4999_99_denied(self, credit_service):
        # FR08 – Income 4999.99 is not rounded up to 5000
        result = credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    def test_fr08_no_adjustment_income_5000_01_approved(self, credit_service):
        # FR08 – Income 5000.01 is not adjusted down
        result = credit_service.evaluate(score=700, income=Decimal("5000.01"), age=21)
        assert result == "APPROVED"

    def test_fr08_precise_decimal_income_preserved(self, credit_service):
        # FR08 – Precise decimal value is preserved without normalization
        result = credit_service.evaluate(score=700, income=Decimal("5000.000000001"), age=21)
        assert result == "APPROVED"


class TestEdgeCasesExplicitlyRequired:
    """Edge case tests explicitly required by the rules."""

    def test_edge_case_score_exactly_700_boundary(self, credit_service):
        # Edge case – Score exactly at boundary 700
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_edge_case_score_one_below_boundary_699(self, credit_service):
        # Edge case – Score one below boundary 699
        result = credit_service.evaluate(score=699, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    def test_edge_case_income_exactly_5000_boundary(self, credit_service):
        # Edge case – Income exactly at boundary 5000
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_edge_case_income_just_below_boundary_4999_99(self, credit_service):
        # Edge case – Income just below boundary 4999.99
        result = credit_service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    def test_edge_case_age_exactly_21_boundary(self, credit_service):
        # Edge case – Age exactly at boundary 21
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_edge_case_age_one_below_boundary_20(self, credit_service):
        # Edge case – Age one below boundary 20
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=20)
        assert result == "DENIED"

    def test_edge_case_minimum_positive_score_1(self, credit_service):
        # Edge case – Minimum positive score value (1)
        result = credit_service. evaluate(score=1, income=Decimal("5000"), age=21)
        assert result == "DENIED"

    def test_edge_case_minimum_positive_income(self, credit_service):
        # Edge case – Minimum positive income value
        result = credit_service.evaluate(score=700, income=Decimal("0. 01"), age=21)
        assert result == "DENIED"

    def test_edge_case_minimum_positive_age_1(self, credit_service):
        # Edge case – Minimum positive age value (1)
        result = credit_service. evaluate(score=700, income=Decimal("5000"), age=1)
        assert result == "DENIED"

    def test_edge_case_very_high_score(self, credit_service):
        # Edge case – Very high score value
        result = credit_service.evaluate(score=1000, income=Decimal("5000"), age=21)
        assert result == "APPROVED"

    def test_edge_case_very_high_income(self, credit_service):
        # Edge case – Very high income value
        result = credit_service. evaluate(score=700, income=Decimal("1000000"), age=21)
        assert result == "APPROVED"

    def test_edge_case_very_high_age(self, credit_service):
        # Edge case – Very high age value
        result = credit_service.evaluate(score=700, income=Decimal("5000"), age=100)
        assert result == "APPROVED"


# Pytest fixture for CreditService instance
@pytest.fixture
def credit_service():
    """Fixture to provide CreditService instance for tests."""
    # This fixture should be replaced with actual CreditService import
    from cases.case04 import CreditService
    return CreditService()
