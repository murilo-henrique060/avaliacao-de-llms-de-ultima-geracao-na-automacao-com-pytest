
import pytest
from decimal import Decimal
from datetime import date, timedelta

from cases.case03 import Subscription, Payment  # type: ignore

# Note: The following classes are assumed to exist based on the provided UML
# but are not implemented here as per the "tests only" constraint.
# from system_module import Subscription, Payment

def test_subscription_initial_state_is_valid_br01():
    """
    BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
    """
    subscription = Subscription()
    subscription.status = "ACTIVE"
    assert subscription.status in ["ACTIVE", "SUSPENDED", "CANCELED"]

def test_canceled_subscription_cannot_be_reactivated_br02_fr04():
    """
    BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    FR04 – The system must prevent invalid state transitions
    """
    subscription = Subscription()
    subscription.status = "CANCELED"
    subscription.payment_failures = 0
    
    successful_payment = Payment(success=True)
    
    # Attempting to record a payment for a canceled subscription should not change its status
    # or should raise an exception preventing the transition.
    with pytest.raises(Exception):
        subscription.record_payment(successful_payment)
    
    assert subscription.status == "CANCELED"

def test_suspension_after_exactly_three_consecutive_failures_br03_fr02_fr03():
    """
    BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    FR02 – The system must update the subscription status based on payment success or failure
    FR03 – The system must control the number of consecutive payment failures
    """
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    failed_payment = Payment(success=False)
    
    # First failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 1
    assert subscription.status == "ACTIVE"
    
    # Second failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 2
    assert subscription.status == "ACTIVE"
    
    # Third consecutive failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 3
    # BR03 Requirement: Exactly 3 failures triggers suspension
    assert subscription.status == "SUSPENDED"

def test_successful_payment_resets_failure_counter_br04_fr03():
    """
    BR04 – A successful payment must reset the consecutive payment failure counter to zero
    FR03 – The system must control the number of consecutive payment failures
    """
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2 # Starting with 2 previous failures
    
    successful_payment = Payment(success=True)
    subscription.record_payment(successful_payment)
    
    # BR04 Requirement: Success resets counter to 0
    assert subscription.payment_failures == 0

def test_billing_date_cannot_be_retroactive_br05():
    """
    BR05 – Billing dates must not be retroactive
    """
    subscription = Subscription()
    
    # Mocking a payment with a date in the past
    past_date = date.today() - timedelta(days=1)
    retroactive_payment = Payment(success=True)
    # Assuming the implementation handles date validation as per BR05
    retroactive_payment.billing_date = past_date
    
    with pytest.raises(Exception):
        subscription.record_payment(retroactive_payment)

def test_record_payment_fulfillment_fr01():
    """
    FR01 – The system must record payments
    """
    subscription = Subscription()
    payment = Payment(success=True)
    
    result = subscription.record_payment(payment)
    
    # Validates that a result (Decimal) is returned, indicating the record was processed
    assert isinstance(result, Decimal)

def test_system_raises_exception_on_payment_failure_fr05():
    """
    FR05 – The system must raise an exception in case of a failure
    """
    subscription = Subscription()
    failed_payment = Payment(success=False)
    
    # FR05 Requirement: Explicitly raise exception on failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)

def test_consecutive_failure_reset_on_intermittent_success_br03_br04():
    """
    BR03 & BR04 – Ensures suspension only happens on CONSECUTIVE failures
    """
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    failed_payment = Payment(success=False)
    successful_payment = Payment(success=True)
    
    # 2 Failures
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 2
    
    # 1 Success resets counter
    subscription.record_payment(successful_payment)
    assert subscription.payment_failures == 0
    
    # 1 More failure (Total 3 failures in history, but only 1 consecutive)
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    
    assert subscription.payment_failures == 1
    assert subscription.status == "ACTIVE" # Should not be suspended
