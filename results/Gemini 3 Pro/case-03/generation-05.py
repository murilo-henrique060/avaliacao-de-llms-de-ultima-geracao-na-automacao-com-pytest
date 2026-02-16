import pytest
from datetime import date, timedelta
from decimal import Decimal

from cases.case03 import Subscription, Payment  # type: ignore


# -------------------------------------------------------------------------
# ASSUMPTIONS & CONTEXT
# -------------------------------------------------------------------------
# The tests assume the following classes are imported from the system module:
# from system import Subscription, Payment
#
# To satisfy BR05 (dates) which is not explicitly in the simplified diagram
# but is a mandatory rule, we assume Payment accepts a 'payment_date'.
# -------------------------------------------------------------------------

class TestSubscriptionBusinessRules:

    # -------------------------------------------------------------------------
    # BR01 – A subscription may be in only one of the following states: 
    #        ACTIVE, SUSPENDED, or CANCELED
    # FR01 – The system must record payments
    # FR02 – The system must update the subscription status
    # -------------------------------------------------------------------------
    def test_br01_fr01_fr02_subscription_starts_active_and_records_payment(self):
        """
        Validates that a new subscription is ACTIVE and can record a successful payment.
        """
        # Arrange
        sub = Subscription()
        payment = Payment(success=True, payment_date=date(2024, 1, 1))

        # Act
        result = sub.record_payment(payment)

        # Assert
        assert sub.status == "ACTIVE"
        assert isinstance(result, Decimal)
        # Verifies the system recorded the interaction without error

    # -------------------------------------------------------------------------
    # BR02 – Subscriptions with status CANCELED must not be reactivated
    # FR04 – The system must prevent invalid state transitions
    # FR05 – The system must raise an exception in case of a failure
    # -------------------------------------------------------------------------
    def test_br02_fr04_fr05_prevent_payment_on_canceled_subscription(self):
        """
        Validates that processing a payment on a CANCELED subscription raises an exception
        and does not change the status to ACTIVE.
        """
        # Arrange
        sub = Subscription()
        sub.status = "CANCELED"  # Force state for test setup
        payment = Payment(success=True, payment_date=date(2024, 1, 1))

        # Act & Assert
        with pytest.raises(Exception):
            sub.record_payment(payment)
        
        # Verify state remains immutable
        assert sub.status == "CANCELED"

    # -------------------------------------------------------------------------
    # BR03 – The subscription must be automatically suspended after exactly 
    #        3 consecutive payment failures
    # FR03 – The system must control the number of consecutive payment failures
    # -------------------------------------------------------------------------
    def test_br03_fr03_suspend_after_exactly_three_failures(self):
        """
        Validates that status changes to SUSPENDED on the exactly 3rd failure.
        """
        # Arrange
        sub = Subscription()
        fail_1 = Payment(success=False, payment_date=date(2024, 1, 1))
        fail_2 = Payment(success=False, payment_date=date(2024, 1, 2))
        fail_3 = Payment(success=False, payment_date=date(2024, 1, 3))

        # Act
        sub.record_payment(fail_1)
        sub.record_payment(fail_2)
        sub.record_payment(fail_3)

        # Assert
        assert sub.payment_failures == 3
        assert sub.status == "SUSPENDED"

    def test_br03_fr03_no_suspension_before_three_failures(self):
        """
        Validates that the subscription remains ACTIVE with only 2 failures.
        """
        # Arrange
        sub = Subscription()
        fail_1 = Payment(success=False, payment_date=date(2024, 1, 1))
        fail_2 = Payment(success=False, payment_date=date(2024, 1, 2))

        # Act
        sub.record_payment(fail_1)
        sub.record_payment(fail_2)

        # Assert
        assert sub.payment_failures == 2
        assert sub.status == "ACTIVE"

    # -------------------------------------------------------------------------
    # BR04 – A successful payment must reset the consecutive payment failure 
    #        counter to zero
    # FR03 – The system must control the number of consecutive payment failures
    # -------------------------------------------------------------------------
    def test_br04_fr03_success_resets_failure_counter(self):
        """
        Validates that a successful payment resets the failure counter even if 
        previous failures existed.
        """
        # Arrange
        sub = Subscription()
        # Simulate 2 previous failures
        sub.record_payment(Payment(success=False, payment_date=date(2024, 1, 1)))
        sub.record_payment(Payment(success=False, payment_date=date(2024, 1, 2)))
        
        # Pre-check
        assert sub.payment_failures == 2

        # Act
        success_payment = Payment(success=True, payment_date=date(2024, 1, 3))
        sub.record_payment(success_payment)

        # Assert
        assert sub.payment_failures == 0
        assert sub.status == "ACTIVE"

    # -------------------------------------------------------------------------
    # BR05 – Billing dates must not be retroactive
    # FR05 – The system must raise an exception in case of a failure
    # -------------------------------------------------------------------------
    def test_br05_fr05_prevent_retroactive_billing_dates(self):
        """
        Validates that attempting to record a payment with a date earlier than 
        the last recorded interaction raises an exception.
        """
        # Arrange
        sub = Subscription()
        # Establish a baseline date
        initial_payment = Payment(success=True, payment_date=date(2024, 2, 1))
        sub.record_payment(initial_payment)

        # Create retroactive payment (past date)
        retroactive_payment = Payment(success=True, payment_date=date(2024, 1, 1))

        # Act & Assert
        with pytest.raises(Exception):
            sub.record_payment(retroactive_payment)

