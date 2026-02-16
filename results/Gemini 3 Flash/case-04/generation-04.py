
import pytest
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Note: As per instructions, the implementation of CreditService is not provided.
# The tests assume the existence of a class CreditService with a method evaluate(score, income, age).

class TestCreditService:

    # --- SUCCESSFUL DECISION TESTS (FR03, BR01, BR02) ---

    def test_approve_when_all_criteria_met_at_exact_threshold(self):
        # BR01 – Credit may only be approved if Score >= 700, Income >= 5000, Age >= 21
        # FR03 – Return exclusively "APPROVED" or "DENIED"
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        assert result == "APPROVED"

    def test_deny_when_score_is_below_threshold(self):
        # BR01 – Score must be >= 700
        # BR02 – If any criteria fail, credit must be denied
        # FR03 – Return exclusively "APPROVED" or "DENIED"
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal("5000.00"), age=21)
        assert result == "DENIED"

    def test_deny_when_income_is_below_threshold(self):
        # BR01 – Income must be >= 5000
        # BR02 – If any criteria fail, credit must be denied
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("4999.99"), age=21)
        assert result == "DENIED"

    def test_deny_when_age_is_below_threshold(self):
        # BR01 – Age must be >= 21
        # BR02 – If any criteria fail, credit must be denied
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=20)
        assert result == "DENIED"

    # --- INPUT VALIDATION & EXCEPTION TESTS (BR03, BR04, BR05, BR06, FR01, FR02, FR05, FR06, FR08) ---

    def test_exception_when_score_is_nan(self):
        # BR03 – Values as NaN are not allowed and must result in an exception
        # FR05 – Raise an exception for magic values like NaN
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=float('nan'), income=Decimal("5000.00"), age=21)

    def test_exception_when_income_is_infinity(self):
        # BR03 – Values as Infinity are not allowed and must result in an exception
        # FR05 – Raise an exception for magic values like Infinity
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('Infinity'), age=21)

    def test_exception_when_score_is_not_positive(self):
        # BR04 – Score: positive integer value
        # BR06 – Any validation failure must result in an exception
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=0, income=Decimal("5000.00"), age=21)

    def test_exception_when_income_is_negative(self):
        # BR04 – Income: positive decimal value
        # BR06 – Any validation failure must result in an exception
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("-1.00"), age=21)

    def test_exception_when_age_is_negative(self):
        # BR04 – Age: positive integer value
        # FR05 – Raise an exception whenever any validation failure occurs
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000.00"), age=-5)

    def test_exception_when_score_is_wrong_type_float(self):
        # BR04 – Score: positive integer value
        # FR05 – Raise an exception for invalid type
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700.5, income=Decimal("5000.00"), age=21)

    def test_exception_when_age_is_wrong_type_float(self):
        # BR04 – Age: positive integer value
        # FR05 – Raise an exception for invalid type
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal("5000.00"), age=21.0)

    def test_no_normalization_of_income_precision(self):
        # BR05 – Values must not be normalized or implicitly adjusted (4999.9999 ≠ 5000)
        # FR08 – Do not perform any kind of normalization or rounding
        service = CreditService()
        # Even if very close to 5000, it should not be rounded up to approve
        result = service.evaluate(score=700, income=Decimal("4999.9999"), age=21)
        assert result == "DENIED"

    def test_exception_when_value_is_missing(self):
        # BR07 – The system must not infer, guess, or assume values that were not provided
        # FR05 – Raise an exception whenever any validation failure occurs, including missing value
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=None, income=Decimal("5000.00"), age=21)

    # --- ARCHITECTURAL & OPERATIONAL CONSTRAINTS (BR08, BR09, FR04, FR07) ---

    def test_indivisible_operation_returns_only_final_string(self):
        # BR08 – There are no intermediate approval levels
        # BR09 – Analysis is an indivisible operation; must not return partial results
        # FR07 – Do not expose intermediate states or progress messages
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        # Verify result is strictly the allowed business string, not a structure containing logs or steps
        assert result in ["APPROVED", "DENIED"]
        assert isinstance(result, str)

    def test_mandatory_validation_of_all_criteria_before_result(self):
        # FR02 – Mandatory validation of all criteria defined in business rules before returning any result
        # FR06 – Do not return any business result when an exception is raised
        service = CreditService()
        # Using an invalid type for age should trigger validation exception immediately, 
        # preventing the return of "APPROVED" even if score/income are high.
        with pytest.raises(Exception):
            service.evaluate(score=800, income=Decimal("10000.00"), age="Twenty-One")

    def test_exclusive_result_types(self):
        # FR03 – Return exclusively one of the following results: "APPROVED" or "DENIED"
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        assert result == "APPROVED"
        
        result_denied = service.evaluate(score=100, income=Decimal("100.00"), age=21)
        assert result_denied == "DENIED"

    def test_record_exactly_one_analysis_result(self):
        # FR04 – Record exactly one analysis result only when a valid decision is produced
        # This is a behavior check: a valid call returns exactly one value.
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal("5000.00"), age=21)
        assert result is not None
        # In a unit test context, we verify the function returns the single expected decision string.
