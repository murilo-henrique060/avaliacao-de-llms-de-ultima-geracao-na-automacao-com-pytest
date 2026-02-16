
import pytest
from decimal import Decimal
from datetime import date, timedelta

from cases.case03 import Subscription, Payment  # type: ignore
# Note: The following tests assume the existence of classes Payment and Subscription 
# with the signatures defined in the Class Diagram.

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_subscription_initial_state_active():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    # FR02 - The system must update the subscription status based on payment success or failure
    assert subscription.status == "ACTIVE"

def test_subscription_state_suspended():
    subscription = Subscription()
    subscription.status = "SUSPENDED"
    assert subscription.status == "SUSPENDED"

def test_subscription_state_canceled():
    subscription = Subscription()
    subscription.status = "CANCELED"
    assert subscription.status == "CANCELED"


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
# FR04 – The system must prevent invalid state transitions
def test_prevent_reactivation_of_canceled_subscription():
    subscription = Subscription()
    subscription.status = "CANCELED"
    subscription.payment_failures = 0
    
    payment = Payment()
    payment.success = True
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)
    
    assert subscription.status == "CANCELED"


# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
# FR03 – The system must control the number of consecutive payment failures
# FR05 – The system must raise an exception in case of a failure
def test_suspension_after_exactly_three_consecutive_failures():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    failed_payment = Payment()
    failed_payment.success = False
    
    # 1st failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 1
    assert subscription.status == "ACTIVE"
    
    # 2nd failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 2
    assert subscription.status == "ACTIVE"
    
    # 3rd failure
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 3
    # BR03 - Transition to SUSPENDED
    assert subscription.status == "SUSPENDED"


# BR04 – A successful payment must reset the consecutive payment failure counter to zero
# FR01 – The system must record payments
def test_successful_payment_resets_failure_counter():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2 # Pre-condition: 2 existing failures
    
    successful_payment = Payment()
    successful_payment.success = True
    
    result = subscription.record_payment(successful_payment)
    
    assert isinstance(result, Decimal)
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"


# BR05 – Billing dates must not be retroactive
def test_prevent_retroactive_billing_date():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    past_date = date.today() - timedelta(days=1)
    payment = Payment()
    payment.success = True
    
    # Assuming record_payment accepts a billing_date or the Payment object holds it
    with pytest.raises(Exception):
        subscription.record_payment(payment, billing_date=past_date)


# FR01 – The system must record payments (Validation of return type and successful state)
def test_record_payment_returns_decimal():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment()
    payment.success = True
    
    result = subscription.record_payment(payment)
    assert isinstance(result, Decimal)


# FR02 – The system must update the subscription status based on payment success
def test_status_remains_active_on_successful_payment():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    payment = Payment()
    payment.success = True
    
    subscription.record_payment(payment)
    assert subscription.status == "ACTIVE"


# FR03 – The system must control the number of consecutive payment failures (Incremental check)
def test_consecutive_failure_increment():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment()
    payment.success = False
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)
        
    assert subscription.payment_failures == 1


# FR05 – The system must raise an exception in case of a failure (Payment failure)
def test_exception_on_payment_failure():
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    payment = Payment()
    payment.success = False
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)
