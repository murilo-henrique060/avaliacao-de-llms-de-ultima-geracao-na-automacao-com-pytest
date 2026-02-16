
import pytest
from decimal import Decimal
import math

# Assuming the class is imported from the application module
# from src.credit_service import CreditService

# For the purpose of these tests, we treat CreditService as the System Under Test (SUT).
# Since the implementation is not provided, we define the tests based on the interface contract.

class TestCreditServiceRules:

    @pytest.fixture
    def service(self):
        """Fixture to provide the CreditService instance."""
        # Replace with actual import/instantiation in real environment
        from cases.case04 import CreditService
        return CreditService()

    # -------------------------------------------------------------------------
    # BR01 & BR02 & FR03 - Approval Logic (Happy Path)
    # -------------------------------------------------------------------------

    def test_evaluate_approval_boundary_values(self, service):
        # BR01 – Credit may only be approved if: Score >= 700, Income >= 5000, Age >= 21
        # BR04 – Types validated (Integer, Decimal, Integer)
        # FR03 – Return exclusively "APPROVED"
        result = service.evaluate(
            score=700, 
            income=Decimal('5000.00'), 
            age=21
        )
        assert result == "APPROVED"

    def test_evaluate_approval_values_above_minimum(self, service):
        # BR01 – Credit may only be approved if all criteria are met
        # FR03 – Return exclusively "APPROVED"
        result = service.evaluate(
            score=850, 
            income=Decimal('15000.50'), 
            age=35
        )
        assert result == "APPROVED"

    # -------------------------------------------------------------------------
    # BR01 & BR02 & FR03 - Denial Logic (Business Failure, not Exception)
    # -------------------------------------------------------------------------

    def test_evaluate_denial_score_below_minimum(self, service):
        # BR01 – Score condition failed (< 700)
        # BR02 – If any criteria fail, credit must be denied
        # FR03 – Return exclusively "DENIED"
        result = service.evaluate(
            score=699, 
            income=Decimal('5000.00'), 
            age=21
        )
        assert result == "DENIED"

    def test_evaluate_denial_income_below_minimum(self, service):
        # BR01 – Income condition failed (< 5000)
        # BR02 – If any criteria fail, credit must be denied
        # FR08 – Do not perform rounding (4999.99 is not 5000)
        result = service.evaluate(
            score=700, 
            income=Decimal('4999.99'), 
            age=21
        )
        assert result == "DENIED"

    def test_evaluate_denial_age_below_minimum(self, service):
        # BR01 – Age condition failed (< 21)
        # BR02 – If any criteria fail, credit must be denied
        result = service.evaluate(
            score=700, 
            income=Decimal('5000.00'), 
            age=20
        )
        assert result == "DENIED"

    def test_evaluate_denial_multiple_failures(self, service):
        # BR02 – If any (or all) criteria fail, credit must be denied
        result = service.evaluate(
            score=500, 
            income=Decimal('1000.00'), 
            age=18
        )
        assert result == "DENIED"

    # -------------------------------------------------------------------------
    # BR03 & FR05 - Magic Values (NaN/Infinity) -> Exceptions
    # -------------------------------------------------------------------------

    def test_exception_income_is_nan(self, service):
        # BR03 – Values as NaN must result in an exception
        # FR05 – Raise exception on magic value
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('NaN'), 
                age=21
            )

    def test_exception_income_is_infinity(self, service):
        # BR03 – Values as Infinity must result in an exception
        # FR05 – Raise exception on magic value
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('Infinity'), 
                age=21
            )

    def test_exception_age_is_infinity(self, service):
        # BR03 – Values as Infinity must result in an exception
        # FR05 – Raise exception on magic value
        # Note: Python int cannot be Infinity, but if float passed masquerading as int
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('5000.00'), 
                age=math.inf
            )

    # -------------------------------------------------------------------------
    # BR04 & BR06 & FR05 - Validation Constraints (Types and Sign)
    # -------------------------------------------------------------------------

    def test_exception_score_negative(self, service):
        # BR04 – Score must be a positive integer
        # BR06 – Validation failure must result in an exception
        with pytest.raises(Exception):
            service.evaluate(
                score=-10, 
                income=Decimal('5000.00'), 
                age=21
            )

    def test_exception_score_is_zero(self, service):
        # BR04 – Score must be a positive integer (> 0)
        # 0 is non-negative, but not positive.
        with pytest.raises(Exception):
            service.evaluate(
                score=0, 
                income=Decimal('5000.00'), 
                age=21
            )

    def test_exception_income_negative(self, service):
        # BR04 – Income must be a positive decimal
        # FR05 – Raise exception on validation failure
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('-5000.00'), 
                age=21
            )

    def test_exception_age_negative(self, service):
        # BR04 – Age must be a positive integer
        # FR05 – Raise exception on validation failure
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('5000.00'), 
                age=-21
            )

    # -------------------------------------------------------------------------
    # BR04 & FR08 - Strict Type Validation (No Normalization)
    # -------------------------------------------------------------------------

    def test_exception_score_is_float(self, service):
        # BR04 – Score must be integer
        # FR08 – Do not perform normalization (e.g., float to int conversion)
        # Passing 700.0 should fail if strict typing is enforced preventing implicit adjustment
        with pytest.raises(Exception):
            service.evaluate(
                score=700.0, 
                income=Decimal('5000.00'), 
                age=21
            )

    def test_exception_income_is_float_primitive(self, service):
        # BR04 – Income must be decimal type (implied by context of "positive decimal value" vs float issues)
        # FR08 – Do not perform normalization
        # Using binary float instead of Decimal should raise exception due to precision risks
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=5000.00,  # float, not Decimal
                age=21
            )

    def test_exception_age_is_decimal(self, service):
        # BR04 – Age must be integer
        # FR08 – Do not perform automatic adjustment
        with pytest.raises(Exception):
            service.evaluate(
                score=700, 
                income=Decimal('5000.00'), 
                age=Decimal('21')
            )

    # -------------------------------------------------------------------------
    # BR05 & FR08 - No Normalization / Exact Precision
    # -------------------------------------------------------------------------

    def test_evaluate_denial_strict_precision_income(self, service):
        # BR05 – Values must not be normalized (4999.9999 != 5000)
        # FR08 – Do not perform rounding
        # This checks that the system does not round up to 5000 to approve
        result = service.evaluate(
            score=700, 
            income=Decimal('4999.999999'), 
            age=21
        )
        assert result == "DENIED"

    # -------------------------------------------------------------------------
    # BR07 & FR01 - No Inference / Missing Values
    # -------------------------------------------------------------------------

    def test_exception_missing_argument_score(self, service):
        # BR07 – System must not infer values that were not provided
        # FR05 – Raise exception on missing value
        with pytest.raises(TypeError):
            service.evaluate(
                income=Decimal('5000.00'), 
                age=21
            )

    def test_exception_argument_none(self, service):
        # FR01 – Evaluate using provided values
        # Passing None is not a valid provided value for the business domain
        with pytest.raises(Exception):
            service.evaluate(
                score=700,
                income=None,
                age=21
            )

    # -------------------------------------------------------------------------
    # BR09 & FR04 - Indivisibility and Result Format
    # -------------------------------------------------------------------------

    def test_result_is_exact_string(self, service):
        # FR03 – Return exclusively "APPROVED" or "DENIED"
        # FR07 – Do not expose intermediate states (returns simple string, not object)
        result = service.evaluate(
            score=700, 
            income=Decimal('5000.00'), 
            age=21
        )
        assert type(result) is str
        assert result in ["APPROVED", "DENIED"]
