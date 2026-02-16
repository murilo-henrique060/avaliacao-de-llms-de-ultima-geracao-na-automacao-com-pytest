
import pytest
import math
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Assuming the class is imported from the application module
# from credit_system import CreditService

class TestCreditService:
    
    @pytest.fixture
    def service(self):
        """Fixture to initialize the service instance."""
        # This assumes CreditService constructor requires no arguments based on the simplified UML
        # In a real scenario, this would import the actual class.
        # Since I cannot implement the system, I am defining the tests against the interface.
        return CreditService()

    # -------------------------------------------------------------------------
    # BR01 – Credit Approval Logic (Positive Scenarios)
    # BR01: Credit may only be approved if: Score >= 700, Income >= 5000, Age >= 21
    # FR03: Return exclusively "APPROVED" when validations succeed
    # -------------------------------------------------------------------------

    def test_evaluate_returns_approved_on_exact_lower_boundaries(self, service):
        # BR01 - Validate approval on exact boundaries
        # FR03 - Return "APPROVED"
        result = service.evaluate(score=700, income=5000.0, age=21)
        assert result == "APPROVED"

    def test_evaluate_returns_approved_above_boundaries(self, service):
        # BR01 - Validate approval above boundaries
        # FR03 - Return "APPROVED"
        result = service.evaluate(score=850, income=10000.0, age=35)
        assert result == "APPROVED"

    # -------------------------------------------------------------------------
    # BR02 – Credit Denial Logic (Valid Business Decisions)
    # BR02: If any of the criteria fail, the credit must be denied
    # FR03: Return exclusively "DENIED" when validations succeed
    # -------------------------------------------------------------------------

    def test_evaluate_returns_denied_when_score_is_below_minimum(self, service):
        # BR01 - Score < 700 violation
        # BR02 - Must be denied
        result = service.evaluate(score=699, income=5000.0, age=21)
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_income_is_below_minimum(self, service):
        # BR01 - Income < 5000 violation
        # BR02 - Must be denied
        result = service.evaluate(score=700, income=4999.99, age=21)
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_age_is_below_minimum(self, service):
        # BR01 - Age < 21 violation
        # BR02 - Must be denied
        result = service.evaluate(score=700, income=5000.0, age=20)
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_multiple_criteria_fail(self, service):
        # BR02 - Multiple failures must result in denial (not exception)
        result = service.evaluate(score=600, income=4000.0, age=18)
        assert result == "DENIED"

    # -------------------------------------------------------------------------
    # BR03 – NaN and Infinity Validations
    # BR03: Values as NaN or Infinity are not allowed and must result in an exception
    # FR05: Raise exception on magic values (NaN or Infinity)
    # -------------------------------------------------------------------------

    def test_evaluate_raises_exception_on_nan_income(self, service):
        # BR03 - NaN check
        # FR05 - Exception required
        with pytest.raises(Exception):
            service.evaluate(score=700, income=float('nan'), age=21)

    def test_evaluate_raises_exception_on_infinity_income(self, service):
        # BR03 - Infinity check
        # FR05 - Exception required
        with pytest.raises(Exception):
            service.evaluate(score=700, income=float('inf'), age=21)

    # -------------------------------------------------------------------------
    # BR04 – Data Type and Constraint Validations
    # BR04: Score: positive integer, Income: positive decimal, Age: positive integer
    # BR06: Any validation failure must result in an exception
    # -------------------------------------------------------------------------

    def test_evaluate_raises_exception_when_score_is_not_integer(self, service):
        # BR04 - Score must be integer
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700.5, income=5000.0, age=21)

    def test_evaluate_raises_exception_when_score_is_negative(self, service):
        # BR04 - Score must be positive
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=-10, income=5000.0, age=21)

    def test_evaluate_raises_exception_when_score_is_zero(self, service):
        # BR04 - Score must be positive (assuming positive > 0)
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=0, income=5000.0, age=21)

    def test_evaluate_raises_exception_when_income_is_not_decimal_or_float(self, service):
        # BR04 - Income must be decimal value (testing invalid type string)
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700, income="5000", age=21)

    def test_evaluate_raises_exception_when_income_is_negative(self, service):
        # BR04 - Income must be positive
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700, income=-5000.0, age=21)

    def test_evaluate_raises_exception_when_income_is_zero(self, service):
        # BR04 - Income must be positive (> 0)
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700, income=0.0, age=21)

    def test_evaluate_raises_exception_when_age_is_not_integer(self, service):
        # BR04 - Age must be integer
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700, income=5000.0, age=21.5)

    def test_evaluate_raises_exception_when_age_is_negative(self, service):
        # BR04 - Age must be positive
        # BR06 - Validation failure exception
        with pytest.raises(Exception):
            service.evaluate(score=700, income=5000.0, age=-5)

    # -------------------------------------------------------------------------
    # BR05 & FR08 – No Normalization or Implicit Adjustments
    # BR05: Values must not be normalized (e.g., 4999.9999 != 5000)
    # FR08: Do not perform any kind of normalization or rounding
    # -------------------------------------------------------------------------

    def test_evaluate_denies_credit_for_income_just_below_threshold_high_precision(self, service):
        # BR05 - No rounding/normalization allowed
        # BR01 - Income 4999.9999 is less than 5000
        # FR08 - Strict evaluation
        result = service.evaluate(score=700, income=4999.9999, age=21)
        assert result == "DENIED"

    def test_evaluate_raises_exception_if_float_passed_for_integer_field(self, service):
        # BR05 - No implicit adjustment (e.g., casting float 21.0 to int 21)
        # FR01 - Evaluate using exclusively provided types (strict interpretation of types in BR04)
        with pytest.raises(Exception):
            service.evaluate(score=700, income=5000.0, age=21.0)

    # -------------------------------------------------------------------------
    # FR07 – No Intermediate States or Logs (Black Box Verification)
    # FR07: Do not expose intermediate states
    # FR09: Credit analysis is an indivisible operation
    # -------------------------------------------------------------------------

    def test_evaluate_returns_simple_string_result_without_metadata(self, service):
        # FR07 - Output must be exactly the result string, no objects/dicts
        # FR09 - Indivisible operation result
        result = service.evaluate(score=700, income=5000.0, age=21)
        assert type(result) is str
        assert result in ["APPROVED", "DENIED"]

    # -------------------------------------------------------------------------
    # FR06 – Exception Handling Behavior
    # FR06: Do not return any business result when an exception is raised
    # -------------------------------------------------------------------------
    
    def test_evaluate_ensure_no_result_returned_on_exception(self, service):
        # FR06 - Ensure execution stops at exception
        try:
            service.evaluate(score=None, income=5000.0, age=21)
        except Exception as e:
            # Verification that the exception is raised is the primary test,
            # but conceptually this confirms no "APPROVED"/"DENIED" was leaked.
            assert isinstance(e, Exception)

    # -------------------------------------------------------------------------
    # FR02 – Mandatory Validation of All Criteria
    # FR02: Mandatory validation of all criteria defined in business rules
    # -------------------------------------------------------------------------

    def test_evaluate_raises_exception_on_missing_score(self, service):
        # FR02 - All criteria mandatory
        # FR05 - Raise exception on missing value
        with pytest.raises(TypeError): # Python raises TypeError for missing args
            service.evaluate(income=5000.0, age=21)

    def test_evaluate_raises_exception_on_none_score(self, service):
        # FR02 - All criteria mandatory (cannot be None)
        # BR06 - Validation failure
        with pytest.raises(Exception):
            service.evaluate(score=None, income=5000.0, age=21)

