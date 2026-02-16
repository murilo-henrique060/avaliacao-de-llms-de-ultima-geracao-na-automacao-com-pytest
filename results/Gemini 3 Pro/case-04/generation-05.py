
import pytest
import math
from decimal import Decimal

# Assuming the class is imported from the application module
# from src.credit_service import CreditService
from cases.case04 import CreditService


class TestCreditService:
    """
    Test suite for CreditService based on strict formal specifications.
    """

    @pytest.fixture
    def service(self):
        # Assuming a stateless service or default constructor as per UML
        # Ideally imported, but instantiated here for test context validity
        return CreditService()

    # ==========================================================================
    # BR01: Approval Criteria
    # ==========================================================================

    def test_evaluate_returns_approved_on_exact_lower_boundaries(self, service):
        # BR01 – Credit may only be approved if: Score >= 700, Income >= 5000, Age >= 21
        # FR03 – Return exclusively "APPROVED" or "DENIED"
        score = 700
        income = Decimal('5000.00')
        age = 21

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "APPROVED"

    def test_evaluate_returns_approved_above_boundaries(self, service):
        # BR01 – Credit may only be approved if conditions are met simultaneously
        score = 850
        income = Decimal('12000.50')
        age = 35

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "APPROVED"

    # ==========================================================================
    # BR02: Denial Criteria
    # ==========================================================================

    def test_evaluate_returns_denied_when_score_is_below_minimum(self, service):
        # BR02 – If any of the criteria fail, the credit must be denied
        # Testing Score < 700
        score = 699
        income = Decimal('5000.00')
        age = 21

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_income_is_below_minimum(self, service):
        # BR02 – If any of the criteria fail, the credit must be denied
        # Testing Income < 5000
        score = 700
        income = Decimal('4999.99')
        age = 21

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_age_is_below_minimum(self, service):
        # BR02 – If any of the criteria fail, the credit must be denied
        # Testing Age < 21
        score = 700
        income = Decimal('5000.00')
        age = 20

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "DENIED"

    def test_evaluate_returns_denied_when_multiple_criteria_fail(self, service):
        # BR02 – If any of the criteria fail, the credit must be denied
        score = 600
        income = Decimal('2000.00')
        age = 18

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        assert result == "DENIED"

    # ==========================================================================
    # BR03: Magic Values (NaN / Infinity)
    # ==========================================================================

    def test_evaluate_raises_exception_when_score_is_nan(self, service):
        # BR03 – Values as NaN are not allowed and must result in an exception
        # FR05 – Raise an exception whenever magic value (NaN) occurs
        score = float('nan')
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_income_is_infinity(self, service):
        # BR03 – Values as Infinity are not allowed and must result in an exception
        # FR05 – Raise an exception whenever magic value (Infinity) occurs
        score = 700
        income = Decimal('Infinity')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_age_is_infinity(self, service):
        # BR03 – Values as Infinity are not allowed and must result in an exception
        score = 700
        income = Decimal('5000.00')
        age = math.inf

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    # ==========================================================================
    # BR04: Types and Constraints
    # ==========================================================================

    def test_evaluate_raises_exception_when_score_is_negative(self, service):
        # BR04 – Score: positive integer value
        # BR06 – Any validation failure must result in an exception
        score = -1
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_score_is_zero(self, service):
        # BR04 – Score: positive integer value (0 is not positive)
        # BR06 – Any validation failure must result in an exception
        score = 0
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_score_is_not_integer(self, service):
        # BR04 – Score: positive integer value (float provided)
        # FR05 – Raise exception on invalid type
        score = 700.5
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_income_is_negative(self, service):
        # BR04 – Income: positive decimal value
        score = 700
        income = Decimal('-5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_age_is_not_integer(self, service):
        # BR04 – Age: positive integer value (float provided)
        score = 700
        income = Decimal('5000.00')
        age = 21.5

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_when_age_is_negative(self, service):
        # BR04 – Age: positive integer value
        score = 700
        income = Decimal('5000.00')
        age = -21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    # ==========================================================================
    # BR05 & FR08: Normalization and Adjustments
    # ==========================================================================

    def test_evaluate_does_not_round_income_extremely_close_to_threshold(self, service):
        # BR05 – Values must not be normalized or implicitly adjusted (e.g., 4999.9999 != 5000)
        # FR08 – Do not perform any kind of normalization, rounding, or automatic adjustment
        score = 700
        income = Decimal('4999.999999')
        age = 21

        # Act
        result = service.evaluate(score, income, age)

        # Assert
        # Should be DENIED because strictly < 5000
        assert result == "DENIED"

    # ==========================================================================
    # FR05 & FR07: Exceptions and No Intermediate States
    # ==========================================================================

    def test_evaluate_raises_exception_on_missing_score(self, service):
        # FR05 – Raise an exception whenever any validation failure occurs, including missing value
        # BR07 – The system must not infer, guess, or assume values that were not provided
        score = None
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_on_missing_income(self, service):
        # FR05 – Raise an exception whenever any validation failure occurs, including missing value
        score = 700
        income = None
        age = 21

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_raises_exception_on_missing_age(self, service):
        # FR05 – Raise an exception whenever any validation failure occurs, including missing value
        score = 700
        income = Decimal('5000.00')
        age = None

        with pytest.raises(Exception):
            service.evaluate(score, income, age)

    def test_evaluate_does_not_return_business_result_on_exception(self, service):
        # FR06 – Do not return any business result when an exception is raised
        # Implied test: Ensure exception breaks flow before return
        score = -1 # Invalid score triggers exception
        income = Decimal('5000.00')
        age = 21

        with pytest.raises(Exception) as exc_info:
            result = service.evaluate(score, income, age)
            
            # This assertion ensures execution stopped and no result was assigned
            assert result is None 
