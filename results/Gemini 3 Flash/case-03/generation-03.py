
import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from cases.case03 import Subscription, Payment  # type: ignore

# --- AUTOMATED TESTS ---

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_subscription_status_allowed_values():
    subscription = Subscription()
    # Initial state check
    assert subscription.status in ["ACTIVE", "SUSPENDED", "CANCELED"]
    
    # State transition check
    subscription.status = "SUSPENDED"
    assert subscription.status == "SUSPENDED"
    
    subscription.status = "CANCELED"
    assert subscription.status == "CANCELED"

# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
# FR04 – The system must prevent invalid state transitions
# FR05 – The system must raise an exception in case of a failure
def test_br02_fr04_fr05_prevent_reactivation_of_canceled_subscription():
    subscription = Subscription()
    subscription.status = "CANCELED"
    payment = Payment(success=True)
    
    with pytest.raises(Exception):
        # Attempting to record a payment that would typically reactivate or process an active sub
        subscription.record_payment(payment)

# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
# FR02 – The system must update the subscription status based on payment success or failure
# FR03 – The system must control the number of consecutive payment failures
def test_br03_fr02_fr03_suspension_after_exactly_three_consecutive_failures():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    failed_payment = Payment(success=False)
    
    # Failure 1
    subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 1
    assert subscription.status == "ACTIVE"
    
    # Failure 2
    subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 2
    assert subscription.status == "ACTIVE"
    
    # Failure 3 - Exactly 3
    subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 3
    assert subscription.status == "SUSPENDED"

# BR04 – A successful payment must reset the consecutive payment failure counter to zero
# FR03 – The system must control the number of consecutive payment failures
def test_br04_fr03_successful_payment_resets_failure_counter():
    subscription = Subscription()
    subscription.payment_failures = 2
    successful_payment = Payment(success=True)
    
    subscription.record_payment(successful_payment)
    
    assert subscription.payment_failures == 0

# BR05 – Billing dates must not be retroactive
# FR05 – The system must raise an exception in case of a failure
def test_br05_fr05_prevent_retroactive_billing_date():
    subscription = Subscription()
    past_date = datetime.now() - timedelta(days=1)
    
    with pytest.raises(Exception):
        # Logic to set or record a payment with a retroactive date
        subscription.billing_date = past_date
        # Or if passed through record_payment
        # subscription.record_payment(Payment(True), billing_date=past_date)

# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal():
    subscription = Subscription()
    payment = Payment(success=True)
    
    result = subscription.record_payment(payment)
    
    # Validating return type as per Class Diagram
    assert isinstance(result, Decimal)

# FR02 – The system must update the subscription status based on payment success or failure
def test_fr02_status_remains_active_on_successful_payment():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    payment = Payment(success=True)
    
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"

# FR03 – The system must control the number of consecutive payment failures
def test_fr03_increment_failure_counter_on_single_failure():
    subscription = Subscription()
    subscription.payment_failures = 0
    payment = Payment(success=False)
    
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 1

# FR04 – The system must prevent invalid state transitions
# Validating that an active subscription does not skip to CANCELED via payment failure logic
def test_fr04_failure_does_not_cause_immediate_cancellation():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    payment = Payment(success=False)
    
    subscription.record_payment(payment)
    
    assert subscription.status != "CANCELED"

# FR05 – The system must raise an exception in case of a failure
# Negative test: Ensure system fails when recording a payment on an already suspended account if rules imply it
def test_fr05_exception_on_invalid_operation():
    subscription = Subscription()
    # Hypothetical scenario where the system fails to record payment for a specific internal error
    # represented by an invalid state/input trigger.
    with pytest.raises(Exception):
        # Action that triggers FR05 requirement
        subscription.record_payment(None) # type: ignore
