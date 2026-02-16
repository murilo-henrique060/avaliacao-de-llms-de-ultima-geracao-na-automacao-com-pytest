
import pytest
from decimal import Decimal
from datetime import date

from cases.case03 import Subscription, Payment  # type: ignore

# Note: As per the task instructions, the implementation of the classes 
# Payment and Subscription is not included here. The tests assume 
# an implementation that adheres to the provided Class Diagram and rules.

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
# FR05 – The system must raise an exception in case of a failure
def test_br01_fr05_invalid_state_transition_raises_exception():
    sub = Subscription()
    with pytest.raises(Exception):
        sub.status = "EXPIRED"

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_state_active_is_allowed():
    sub = Subscription()
    sub.status = "ACTIVE"
    assert sub.status == "ACTIVE"

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_state_suspended_is_allowed():
    sub = Subscription()
    sub.status = "SUSPENDED"
    assert sub.status == "SUSPENDED"

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_state_canceled_is_allowed():
    sub = Subscription()
    sub.status = "CANCELED"
    assert sub.status == "CANCELED"

# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
# FR02 – The system must update the subscription status based on payment success or failure
# FR03 – The system must control the number of consecutive payment failures
def test_br03_fr02_fr03_suspension_on_exactly_third_consecutive_failure():
    sub = Subscription()
    sub.status = "ACTIVE"
    sub.payment_failures = 2
    payment = Payment(success=False)
    
    sub.record_payment(payment)
    
    assert sub.payment_failures == 3
    assert sub.status == "SUSPENDED"

# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
# FR03 – The system must control the number of consecutive payment failures
def test_br03_fr03_no_suspension_on_second_consecutive_failure():
    sub = Subscription()
    sub.status = "ACTIVE"
    sub.payment_failures = 1
    payment = Payment(success=False)
    
    sub.record_payment(payment)
    
    assert sub.payment_failures == 2
    assert sub.status == "ACTIVE"

# BR04 – A successful payment must reset the consecutive payment failure counter to zero
# FR03 – The system must control the number of consecutive payment failures
def test_br04_fr03_reset_failures_on_successful_payment():
    sub = Subscription()
    sub.status = "ACTIVE"
    sub.payment_failures = 2
    payment = Payment(success=True)
    
    sub.record_payment(payment)
    
    assert sub.payment_failures == 0

# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
# FR04 – The system must prevent invalid state transitions
# FR05 – The system must raise an exception in case of a failure
def test_br02_fr04_fr05_canceled_subscription_cannot_be_reactivated_by_payment():
    sub = Subscription()
    sub.status = "CANCELED"
    payment = Payment(success=True)
    
    with pytest.raises(Exception):
        sub.record_payment(payment)
    
    assert sub.status == "CANCELED"

# BR05 – Billing dates must not be retroactive
# FR05 – The system must raise an exception in case of a failure
def test_br05_fr05_retroactive_billing_date_raises_exception():
    sub = Subscription()
    # Current Date: 2026-01-12. Retroactive Date: 2026-01-11
    payment = Payment(success=True)
    payment.date = date(2026, 1, 11)
    
    with pytest.raises(Exception):
        sub.record_payment(payment)

# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_value():
    sub = Subscription()
    sub.status = "ACTIVE"
    payment = Payment(success=True)
    
    result = sub.record_payment(payment)
    
    assert isinstance(result, Decimal)

# FR02 – The system must update the subscription status based on payment success or failure
# FR03 – The system must control the number of consecutive payment failures
def test_fr02_fr03_failure_increments_counter_and_maintains_status_if_under_limit():
    sub = Subscription()
    sub.status = "ACTIVE"
    sub.payment_failures = 0
    payment = Payment(success=False)
    
    sub.record_payment(payment)
    
    assert sub.payment_failures == 1
    assert sub.status == "ACTIVE"
