
import pytest
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Assuming the existence of CreditService and its evaluate method as per the UML Class Diagram
# The tests will focus on the behavior defined in the Business Rules (BR) and Functional Requirements (FR).

class TestCreditApprovalSystem:

    # BR01 – Credit may only be approved if Score ≥ 700, Income ≥ 5,000, Age ≥ 21
    # FR01 – Evaluate using exclusively provided values
    # FR03 – Return exclusively "APPROVED" or "DENIED"
    def test_approval_at_exact_minimum_thresholds(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        assert result == "APPROVED"

    # BR02 – If any criteria fail, credit must be denied
    # BR01 – Condition Score ≥ 700
    def test_denial_when_score_is_below_minimum(self):
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal("5000.00"), age=21)
        assert result == "DENIED"

    # BR02 – If any criteria fail, credit must be denied
    # BR01 – Condition Income ≥ 5,000
    def test_denial_when_income_is_below_minimum(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    # BR02 – If any criteria fail, credit must be denied
    # BR01 – Condition Age ≥ 21
    def test_denial_when_age_is_below_minimum(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=20)
        assert result == "DENIED"

    # BR03 – Values as NaN are not allowed and must result in an exception
    # FR05 – Raise exception on magic value (NaN)
    def test_exception_when_income_is_nan(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("NaN"), age=21)

    # BR03 – Values as Infinity are not allowed and must result in an exception
    # FR05 – Raise exception on magic value (Infinity)
    def test_exception_when_income_is_infinity(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("Infinity"), age=21)

    # BR04 – Score: positive integer value
    # FR05 – Raise exception on invalid type
    def test_exception_when_score_is_not_integer(self):
        service = CreditService()
        with pytest.raises(Exception):
            # Providing float instead of int
            service.evaluate(score=700.0, income=Decimal("5000.00"), age=21)

    # BR04 – Score: positive integer value
    # FR05 – Raise exception on business rule violation (non-positive)
    def test_exception_when_score_is_negative(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=-1, income=Decimal("5000.00"), age=21)

    # BR04 – Income: positive decimal value
    # FR05 – Raise exception on invalid type
    def test_exception_when_income_is_not_decimal(self):
        service = CreditService()
        with pytest.raises(Exception):
            # Providing string instead of decimal
            service.evaluate(score=700, income="5000.00", age=21)

    # BR04 – Income: positive decimal value
    # FR05 – Raise exception on business rule violation (non-positive)
    def test_exception_when_income_is_negative(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("-0.01"), age=21)

    # BR04 – Age: positive integer value
    # FR05 – Raise exception on invalid type
    def test_exception_when_age_is_not_integer(self):
        service = CreditService()
        with pytest.raises(Exception):
            # Providing float instead of int
            service.evaluate(score=700, income=Decimal("5000.00"), age=21.0)

    # BR04 – Age: positive integer value
    # FR05 – Raise exception on business rule violation (non-positive)
    def test_exception_when_age_is_zero(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000.00"), age=0)

    # BR05 – Values must not be normalized or implicitly adjusted
    # FR08 – Do not perform normalization, rounding, or automatic adjustment
    def test_no_normalization_on_near_threshold_income(self):
        service = CreditService()
        # 4999.9999 should not be rounded to 5000.00
        result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
        assert result == "DENIED"

    # BR06 – Any validation failure must result in an exception
    # FR06 – Do not return any business result when an exception is raised
    def test_no_result_returned_on_validation_failure(self):
        service = CreditService()
        with pytest.raises(Exception):
            # Invalid type for score (string) should trigger exception, not return "DENIED"
            service.evaluate(score="700", income=Decimal("5000.00"), age=21)

    # BR07 – The system must not infer, guess, or assume values not provided
    # FR05 – Raise exception whenever any validation failure occurs, including missing value
    def test_exception_on_missing_score(self):
        service = CreditService()
        with pytest.raises(Exception):
            # score is mandatory
            service.evaluate(score=None, income=Decimal("5000.00"), age=21)

    # BR08 – There are no intermediate approval levels
    # FR03 – Return exclusively "APPROVED" or "DENIED"
    def test_strict_return_value_approved(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal("10000.00"), age=30)
        assert result == "APPROVED"
        assert result != "PARTIALLY_APPROVED"
        assert result != 1

    # BR09 – Credit analysis is an indivisible operation
    # FR07 – Do not expose intermediate states or progress messages
    def test_indivisible_operation_returns_final_result_only(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        # Verify that only the final string is returned, no dictionary or object with progress
        assert isinstance(result, str)
        assert result in ["APPROVED", "DENIED"]

    # FR02 – Mandatory validation of all criteria before returning any result
    def test_all_criteria_validated_before_result(self):
        service = CreditService()
        # Even if score and income are high, an invalid age type must trigger exception
        with pytest.raises(Exception):
            service.evaluate(score=900, income=Decimal("10000.00"), age=None)

    # FR04 – Record exactly one analysis result only when a valid decision is produced
    def test_valid_decision_produced_for_boundary_denial(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=20)
        assert result == "DENIED"
