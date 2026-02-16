
import pytest
from decimal import Decimal

from cases.case03 import Subscription, Payment  # type: ignore

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_subscription_allowed_states():
    # Validating ACTIVE state
    sub_active = Subscription(status="ACTIVE")
    assert sub_active.status == "ACTIVE"
    
    # Validating SUSPENDED state
    sub_suspended = Subscription(status="SUSPENDED")
    assert sub_suspended.status == "SUSPENDED"
    
    # Validating CANCELED state
    sub_canceled = Subscription(status="CANCELED")
    assert sub_canceled.status == "CANCELED"

# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
# FR04 – The system must prevent invalid state transitions
def test_br02_fr04_canceled_status_cannot_be_reactivated():
    sub = Subscription(status="CANCELED")
    payment = Payment(success=True)
    
    with pytest.raises(Exception):
        sub.record_payment(payment)
    
    assert sub.status == "CANCELED"

# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
# FR02 – The system must update the subscription status based on payment success or failure
def test_br03_fr02_suspension_after_exactly_three_consecutive_failures():
    sub = Subscription(status="ACTIVE", payment_failures=0)
    failed_payment = Payment(success=False)
    
    # Failure 1
    try: sub.record_payment(failed_payment)
    except: pass
    assert sub.status == "ACTIVE"
    
    # Failure 2
    try: sub.record_payment(failed_payment)
    except: pass
    assert sub.status == "ACTIVE"
    
    # Failure 3 - Exactly 3rd failure triggers suspension
    try: sub.record_payment(failed_payment)
    except: pass
    assert sub.status == "SUSPENDED"

# BR04 – A successful payment must reset the consecutive payment failure counter to zero
# FR03 – The system must control the number of consecutive payment failures
def test_br04_fr03_successful_payment_resets_failure_counter():
    sub = Subscription(status="ACTIVE", payment_failures=2)
    success_payment = Payment(success=True)
    
    sub.record_payment(success_payment)
    
    assert sub.payment_failures == 0

# BR05 – Billing dates must not be retroactive
def test_br05_billing_date_not_retroactive():
    sub = Subscription(status="ACTIVE")
    # Assuming the implementation requires a date for the payment as per BR05
    retroactive_payment = Payment(success=True, date="2020-01-01") 
    
    with pytest.raises(Exception):
        sub.record_payment(retroactive_payment)

# FR01 – The system must record payments
def test_fr01_system_records_payment_returns_decimal():
    sub = Subscription(status="ACTIVE")
    payment = Payment(success=True)
    
    result = sub.record_payment(payment)
    
    assert isinstance(result, Decimal)

# FR03 – The system must control the number of consecutive payment failures
def test_fr03_consecutive_failure_increment():
    sub = Subscription(status="ACTIVE", payment_failures=0)
    failed_payment = Payment(success=False)
    
    try: sub.record_payment(failed_payment)
    except: pass
    
    assert sub.payment_failures == 1

# FR05 – The system must raise an exception in case of a failure
def test_fr05_exception_on_payment_failure():
    sub = Subscription(status="ACTIVE")
    failed_payment = Payment(success=False)
    
    with pytest.raises(Exception):
        sub.record_payment(failed_payment)

# FR04 – The system must prevent invalid state transitions (Specific to Suspended to Canceled if not defined)
# Note: Rule BR02 specifically forbids CANCELED -> ACTIVE/SUSPENDED. 
# This test ensures transitions outside defined rules (if any) are blocked.
def test_fr04_prevent_activation_of_canceled_subscription():
    sub = Subscription(status="CANCELED")
    success_payment = Payment(success=True)
    
    with pytest.raises(Exception):
        sub.record_payment(success_payment)
    
    assert sub.status != "ACTIVE"

# Edge case for BR03: 2 failures followed by 1 success should NOT suspend on the next failure
def test_br03_edge_case_non_consecutive_failures():
    sub = Subscription(status="ACTIVE", payment_failures=0)
    failed_payment = Payment(success=False)
    success_payment = Payment(success=True)
    
    # 2 failures
    try: sub.record_payment(failed_payment)
    except: pass
    try: sub.record_payment(failed_payment)
    except: pass
    
    # 1 success resets counter (BR04)
    sub.record_payment(success_payment)
    
    # Next failure is the 1st consecutive one, not the 3rd
    try: sub.record_payment(failed_payment)
    except: pass
    
    assert sub.status == "ACTIVE"
    assert sub.payment_failures == 1
