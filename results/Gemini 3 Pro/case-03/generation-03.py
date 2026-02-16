
import pytest
from decimal import Decimal
from datetime import date, timedelta

from cases.case03 import Subscription, Payment  # type: ignore

# Note: The following tests assume the existence of a 'subscription_system' module 
# or similar context containing the 'Subscription' and 'Payment' classes.
# Since the implementation is not provided, we test against the specified public interface.

class TestSubscriptionBusinessRules:
    
    @pytest.fixture
    def subscription(self):
        """
        Fixture to provide a fresh Subscription instance in the initial valid state.
        Assumed initial state is ACTIVE with 0 failures based on standard lifecycle implies.
        """
        sub = Subscription()
        sub.status = "ACTIVE"
        sub.payment_failures = 0
        return sub

    @pytest.fixture
    def successful_payment(self):
        """Fixture for a successful payment object."""
        payment = Payment()
        payment.success = True
        payment.date = date.today()  # Satisfying BR05 requirement for valid date
        return payment

    @pytest.fixture
    def failed_payment(self):
        """Fixture for a failed payment object."""
        payment = Payment()
        payment.success = False
        payment.date = date.today()
        return payment

    # -------------------------------------------------------------------------
    # BR01: A subscription may be in only one of the following states: 
    # ACTIVE, SUSPENDED, or CANCELED
    # -------------------------------------------------------------------------
    
    def test_subscription_initial_state_validity(self, subscription):
        # BR01 – Validation of allowed states
        # FR02 – System updates status (checking baseline)
        assert subscription.status in ["ACTIVE", "SUSPENDED", "CANCELED"]

    # -------------------------------------------------------------------------
    # BR02: Subscriptions with status CANCELED must not be reactivated 
    # under any circumstances
    # -------------------------------------------------------------------------

    def test_canceled_subscription_cannot_be_reactivated_by_success(self, subscription, successful_payment):
        # BR02 – No reactivation from CANCELED
        # FR04 – Prevent invalid state transitions
        # FR05 – Raise exception in case of failure (invalid transition attempt)
        
        subscription.status = "CANCELED"
        
        with pytest.raises(Exception):
            subscription.record_payment(successful_payment)
            
        assert subscription.status == "CANCELED"

    def test_canceled_subscription_cannot_be_changed_by_failure(self, subscription, failed_payment):
        # BR02 – No state change from CANCELED even on failure
        # FR04 – Prevent invalid state transitions
        
        subscription.status = "CANCELED"
        
        with pytest.raises(Exception):
            subscription.record_payment(failed_payment)
            
        assert subscription.status == "CANCELED"

    # -------------------------------------------------------------------------
    # BR03: The subscription must be automatically suspended after exactly 
    # 3 consecutive payment failures
    # -------------------------------------------------------------------------

    def test_status_remains_active_after_one_failure(self, subscription, failed_payment):
        # BR03 – Not suspended before 3 failures
        # FR01 – Record payment
        # FR03 – Control consecutive failures
        
        subscription.record_payment(failed_payment)
        
        assert subscription.payment_failures == 1
        assert subscription.status == "ACTIVE"

    def test_status_remains_active_after_two_consecutive_failures(self, subscription, failed_payment):
        # BR03 – Not suspended before 3 failures
        # FR03 – Control consecutive failures
        
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        
        assert subscription.payment_failures == 2
        assert subscription.status == "ACTIVE"

    def test_status_changes_to_suspended_after_exactly_three_failures(self, subscription, failed_payment):
        # BR03 – Suspension after 3 consecutive payment failures
        # FR02 – Update status based on payment failure
        # FR03 – Control consecutive failures
        
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        
        assert subscription.payment_failures == 3
        assert subscription.status == "SUSPENDED"

    # -------------------------------------------------------------------------
    # BR04: A successful payment must reset the consecutive payment failure 
    # counter to zero
    # -------------------------------------------------------------------------

    def test_successful_payment_resets_failure_counter(self, subscription, failed_payment, successful_payment):
        # BR04 – Reset failure counter on success
        # FR01 – Record payment
        # FR03 – Control consecutive failures
        
        # Setup: 2 failures recorded
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        assert subscription.payment_failures == 2
        
        # Action: Successful payment
        subscription.record_payment(successful_payment)
        
        # Verification
        assert subscription.payment_failures == 0

    def test_successful_payment_keeps_counter_zero(self, subscription, successful_payment):
        # BR04 – Reset (or keep) failure counter zero on success
        
        subscription.payment_failures = 0
        subscription.record_payment(successful_payment)
        
        assert subscription.payment_failures == 0

    # -------------------------------------------------------------------------
    # BR05: Billing dates must not be retroactive
    # -------------------------------------------------------------------------

    def test_payment_with_retroactive_date_raises_exception(self, subscription):
        # BR05 – Billing dates must not be retroactive
        # FR05 – Raise exception in case of failure (validation error)
        
        retroactive_payment = Payment()
        retroactive_payment.success = True
        # Explicit precise value: Yesterday
        retroactive_payment.date = date.today() - timedelta(days=1)
        
        with pytest.raises(Exception):
            subscription.record_payment(retroactive_payment)

    def test_payment_with_current_date_is_accepted(self, subscription):
        # BR05 – Current date is valid (not retroactive)
        # FR01 – Record payment
        
        current_payment = Payment()
        current_payment.success = True
        current_payment.date = date.today()
        
        try:
            subscription.record_payment(current_payment)
        except Exception:
            pytest.fail("Payment with current date should not raise Exception")

    # -------------------------------------------------------------------------
    # Additional Functional Requirement Validations
    # -------------------------------------------------------------------------

    def test_record_payment_raises_exception_on_general_failure(self, subscription):
        # FR05 – The system must raise an exception in case of a failure
        # Testing a generic invalid input scenario implied by the requirement for robustness
        
        invalid_payment = None 
        
        with pytest.raises(Exception):
            subscription.record_payment(invalid_payment)

# Mock definitions for context (to satisfy the requirement of "Generates tests" 
# that are syntactically valid against a hypothetical SUT)

class Payment:
    def __init__(self):
        self.success = False
        self.date = date.today()

class Subscription:
    def __init__(self):
        self.status = "ACTIVE"
        self.payment_failures = 0
        
    def record_payment(self, payment: Payment) -> Decimal:
        # This method is stubbed to allow linter validation of the tests above.
        # The actual logic is NOT implemented per instructions.
        pass
