
import pytest
from datetime import date, timedelta
from decimal import Decimal

from cases.case03 import Subscription, Payment  # type: ignore

# ASSUMPTION: The following classes are imported from the system implementation.
# Since the implementation is not provided, we assume the interface matches the UML and Rules.
# from system import Subscription, Payment, Status

# Mocks/Stubs for context if this file were to be executed in isolation 
# (Included only to ensure the test code structure is valid Python, strictly adhering to the prompt's SUT description)
# In a real scenario, these would be imports.


class TestSubscriptionBusinessRules:
    
    # BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
    def test_br01_subscription_initial_state_validity(self):
        """
        Validates that a new subscription starts in a valid state (ACTIVE) 
        and matches one of the defined allowed states.
        """
        # Arrange
        subscription = Subscription()
        
        # Act
        current_status = subscription.status
        
        # Assert
        allowed_states = {SubscriptionStatus.ACTIVE, SubscriptionStatus.SUSPENDED, SubscriptionStatus.CANCELED}
        assert current_status in allowed_states
        assert current_status == SubscriptionStatus.ACTIVE

    # BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    def test_br02_canceled_subscription_cannot_transition_to_active(self):
        """
        Validates that a CANCELED subscription does not change status to ACTIVE
        even after a successful payment.
        """
        # Arrange
        subscription = Subscription()
        subscription.status = SubscriptionStatus.CANCELED
        payment = Payment(success=True)
        
        # Act
        # FR05 implies exception on failure, attempting to modify a CANCELED state is a logic failure.
        # However, if the method simply rejects the change silently (idempotent), strictly checking state is required.
        # Based on FR04 (prevent invalid transitions), this should likely raise or silently fail. 
        # Checking state persistence is the core of BR02.
        try:
            subscription.record_payment(payment)
        except Exception:
            pass # Exception is acceptable, state change is forbidden
            
        # Assert
        assert subscription.status == SubscriptionStatus.CANCELED

    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    def test_br03_suspension_after_exactly_three_consecutive_failures(self):
        """
        Validates that the subscription transitions to SUSPENDED status
        immediately upon the 3rd consecutive payment failure.
        """
        # Arrange
        subscription = Subscription()
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.payment_failures = 0
        payment_fail = Payment(success=False)

        # Act & Assert - 1st Failure
        subscription.record_payment(payment_fail)
        assert subscription.payment_failures == 1
        assert subscription.status == SubscriptionStatus.ACTIVE

        # Act & Assert - 2nd Failure
        subscription.record_payment(payment_fail)
        assert subscription.payment_failures == 2
        assert subscription.status == SubscriptionStatus.ACTIVE

        # Act & Assert - 3rd Failure (Trigger)
        subscription.record_payment(payment_fail)
        assert subscription.payment_failures == 3
        assert subscription.status == SubscriptionStatus.SUSPENDED

    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    def test_br04_successful_payment_resets_failure_counter(self):
        """
        Validates that a successful payment resets the failure counter 
        from a non-zero value (e.g., 2) back to zero.
        """
        # Arrange
        subscription = Subscription()
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.payment_failures = 2
        payment_success = Payment(success=True)

        # Act
        subscription.record_payment(payment_success)

        # Assert
        assert subscription.payment_failures == 0

    # BR05 – Billing dates must not be retroactive
    def test_br05_payment_with_retroactive_billing_date_raises_exception(self):
        """
        Validates that attempting to record a payment with a retroactive billing date
        raises an exception.
        Assumption: Payment class accepts a 'date' parameter or similar mechanism exists 
        to satisfy BR05 within the 'record_payment' context.
        """
        # Arrange
        subscription = Subscription()
        # Using a deterministic past date relative to current system context (2026-01-12)
        retroactive_date = date(2025, 1, 1) 
        
        # Assuming Payment constructor can take a date as per BR necessity
        payment = Payment(success=True, date=retroactive_date)

        # Act & Assert
        # FR05: System must raise exception in case of failure (validation failure)
        with pytest.raises(Exception):
            subscription.record_payment(payment)


class TestFunctionalRequirements:

    # FR01 – The system must record payments
    def test_fr01_record_payment_execution(self):
        """
        Validates that the record_payment method accepts a payment object
        and processes it without interface errors.
        """
        # Arrange
        subscription = Subscription()
        payment = Payment(success=True)

        # Act
        result = subscription.record_payment(payment)

        # Assert
        # Assuming return type is Decimal as per UML
        assert isinstance(result, Decimal)

    # FR02 – The system must update the subscription status based on payment success or failure
    def test_fr02_status_update_on_failure_sequence(self):
        """
        Validates that status changes dynamically based on the sequence of payments.
        """
        # Arrange
        subscription = Subscription()
        subscription.status = SubscriptionStatus.ACTIVE
        payment_fail = Payment(success=False)
        
        # Act: Push to suspended
        subscription.record_payment(payment_fail) # 1
        subscription.record_payment(payment_fail) # 2
        subscription.record_payment(payment_fail) # 3
        
        # Assert
        assert subscription.status == SubscriptionStatus.SUSPENDED

    # FR03 – The system must control the number of consecutive payment failures
    def test_fr03_consecutive_failure_counter_increment(self):
        """
        Validates strict incrementing of the failure counter.
        """
        # Arrange
        subscription = Subscription()
        subscription.payment_failures = 0
        payment = Payment(success=False)

        # Act
        subscription.record_payment(payment)

        # Assert
        assert subscription.payment_failures == 1

    # FR04 – The system must prevent invalid state transitions
    def test_fr04_prevent_invalid_transition_suspended_to_active_without_payment(self):
        """
        Validates that status cannot arbitrarily change from SUSPENDED to ACTIVE 
        without a successful payment (implicit in logic, ensuring stability).
        """
        # Arrange
        subscription = Subscription()
        subscription.status = SubscriptionStatus.SUSPENDED
        payment_fail = Payment(success=False)

        # Act
        subscription.record_payment(payment_fail)

        # Assert
        # Failure on suspended account should not reactivate it
        assert subscription.status == SubscriptionStatus.SUSPENDED

    # FR05 – The system must raise an exception in case of a failure
    def test_fr05_raise_exception_on_general_processing_failure(self):
        """
        Validates that the system raises an exception when encountering 
        an invalid operation or data state (e.g., None input).
        """
        # Arrange
        subscription = Subscription()

        # Act & Assert
        with pytest.raises(Exception):
            subscription.record_payment(None)
