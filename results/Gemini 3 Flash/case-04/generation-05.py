
import pytest
from decimal import Decimal

from cases.case04 import CreditService  # type: ignore

# Note: As per instructions, the implementation of CreditService is not provided.
# The tests assume CreditService follows the provided Simplified UML Class Diagram.

class TestCreditApproval:

    # BR01, FR01, FR02, FR03 – Valid approval at exact lower boundaries
    def test_approved_at_exact_boundaries(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal('5000.00'), age=21)
        assert result == "APPROVED"

    # BR01, FR03 – Valid approval with values above boundaries
    def test_approved_above_boundaries(self):
        service = CreditService()
        result = service.evaluate(score=800, income=Decimal('10000.00'), age=30)
        assert result == "APPROVED"

    # BR02, FR03 – Credit denied when score is below minimum requirement
    def test_denied_score_below_boundary(self):
        service = CreditService()
        result = service.evaluate(score=699, income=Decimal('5000.00'), age=21)
        assert result == "DENIED"

    # BR02, FR03 – Credit denied when income is below minimum requirement
    def test_denied_income_below_boundary(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal('4999.99'), age=21)
        assert result == "DENIED"

    # BR02, FR03 – Credit denied when age is below minimum requirement
    def test_denied_age_below_boundary(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal('5000.00'), age=20)
        assert result == "DENIED"

    # BR03, FR05 – Exception raised for NaN value in income
    def test_exception_on_nan_income(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('NaN'), age=21)

    # BR03, FR05 – Exception raised for Infinity value in income
    def test_exception_on_infinity_income(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('Infinity'), age=21)

    # BR04, FR05 – Exception raised for invalid score type (float instead of int)
    def test_exception_score_invalid_type(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700.5, income=Decimal('5000.00'), age=21)

    # BR04, FR05 – Exception raised for non-positive score
    def test_exception_score_not_positive(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=0, income=Decimal('5000.00'), age=21)

    # BR04, FR05 – Exception raised for non-positive income
    def test_exception_income_not_positive(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('-1.00'), age=21)

    # BR04, FR05 – Exception raised for non-positive age
    def test_exception_age_not_positive(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('5000.00'), age=-5)

    # BR05, FR08 – Values must not be normalized or implicitly adjusted
    def test_no_normalization_income_precision(self):
        service = CreditService()
        # 4999.9999 must not be treated as 5000
        result = service.evaluate(score=700, income=Decimal('4999.9999'), age=21)
        assert result == "DENIED"

    # BR06, FR05, FR06 – Validation failure results in exception and no business result
    def test_exception_on_invalid_input_type_string(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score="700", income=Decimal('5000.00'), age=21)

    # BR07, FR05 – Exception raised when mandatory value (score) is missing
    def test_exception_missing_score(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=None, income=Decimal('5000.00'), age=21)

    # BR07, FR05 – Exception raised when mandatory value (income) is missing
    def test_exception_missing_income(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=None, age=21)

    # BR07, FR05 – Exception raised when mandatory value (age) is missing
    def test_exception_missing_age(self):
        service = CreditService()
        with pytest.raises(Exception):
            service.evaluate(score=700, income=Decimal('5000.00'), age=None)

    # BR08, BR09, FR07 – Operation must not return partial results or intermediate states
    def test_indivisible_operation_return_type(self):
        service = CreditService()
        result = service.evaluate(score=700, income=Decimal('5000.00'), age=21)
        # Result must be exactly one of the allowed strings, not an object with metadata
        assert result in ["APPROVED", "DENIED"]
        assert isinstance(result, str)
