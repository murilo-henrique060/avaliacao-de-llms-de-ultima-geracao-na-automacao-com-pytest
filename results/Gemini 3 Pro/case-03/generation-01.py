
import pytest
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from cases.case03 import Subscription, Payment  # type: ignore

# -------------------------------------------------------------------------
# BUSINESS RULES (BR) TESTS
# -------------------------------------------------------------------------

def test_br01_subscription_valid_states():
    # BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
    # Validate that a new subscription initializes in one of the allowed states (implicitly ACTIVE)
    subscription = Subscription()
    
    assert subscription.status in {"ACTIVE", "SUSPENDED", "CANCELED"}, \
        f"Invalid state found: {subscription.status}"

def test_br02_canceled_subscription_cannot_be_reactivated():
    # BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    # FR04 – The system must prevent invalid state transitions
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    successful_payment = Payment(success=True)
    
    # Expecting an exception prevents the transition
    with pytest.raises(Exception):
        subscription.record_payment(successful_payment)
    
    # Double check state persistence
    assert subscription.status == "CANCELED"

def test_br03_suspension_after_exactly_3_consecutive_failures():
    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    subscription = Subscription()
    subscription.payment_failures = 2
    subscription.status = "ACTIVE"
    
    failed_payment = Payment(success=False)
    
    subscription.record_payment(failed_payment)
    
    assert subscription.status == "SUSPENDED"
    assert subscription.payment_failures == 3

def test_br04_success_resets_failure_counter():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    subscription = Subscription()
    subscription.payment_failures = 2
    
    successful_payment = Payment(success=True)
    
    subscription.record_payment(successful_payment)
    
    assert subscription.payment_failures == 0

def test_br05_billing_date_cannot_be_retroactive():
    # BR05 – Billing dates must not be retroactive
    # FR05 – The system must raise an exception in case of a failure
    subscription = Subscription()
    
    # Date in the past
    past_date = date.today() - timedelta(days=1)
    retroactive_payment = Payment(success=True, billing_date=past_date)
    
    with pytest.raises(Exception):
        subscription.record_payment(retroactive_payment)

# -------------------------------------------------------------------------
# FUNCTIONAL REQUIREMENTS (FR) TESTS
# -------------------------------------------------------------------------

def test_fr01_system_must_record_payments_return_value():
    # FR01 – The system must record payments
    subscription = Subscription()
    payment = Payment(success=True)
    
    result = subscription.record_payment(payment)
    
    # Validates that the method executes and returns the expected type per Class Diagram
    # Note: Using assert isinstance checks the contract fulfillment
    assert isinstance(result, Decimal)

def test_fr02_system_updates_status_on_failure_sequence():
    # FR02 – The system must update the subscription status based on payment success or failure
    # Validates specifically that status CHANGES when conditions are met
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2
    
    failed_payment = Payment(success=False)
    subscription.record_payment(failed_payment)
    
    assert subscription.status != "ACTIVE"

def test_fr03_system_controls_consecutive_payment_failures_increment():
    # FR03 – The system must control the number of consecutive payment failures
    # Validates the increment logic specifically (distinct from the threshold logic in BR03)
    subscription = Subscription()
    subscription.payment_failures = 0
    
    failed_payment = Payment(success=False)
    subscription.record_payment(failed_payment)
    
    assert subscription.payment_failures == 1

def test_fr04_prevent_invalid_state_transition_from_suspended_to_canceled_via_payment():
    # FR04 – The system must prevent invalid state transitions
    # Note: While business rules are specific about CANCELED->ACTIVE, 
    # generic invalid transitions not defined by BR should also be rejected or handled.
    # Assuming standard behavior where payment logic purely handles payment, 
    # trying to process payment on a final state (if CANCELED is final) is tested here.
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    # Even a failed payment should probably raise exception or strictly not change state
    # when in CANCELED state.
    failed_payment = Payment(success=False)
    
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)

def test_fr05_raise_exception_on_general_failure():
    # FR05 – The system must raise an exception in case of a failure
    # Using a generic failure case to validate the mechanism
    subscription = Subscription()
    
    # Using a None payment object to trigger a generic system failure/validation error
    # This validates the exception raising mechanism itself
    with pytest.raises(Exception):
        subscription.record_payment(None)

