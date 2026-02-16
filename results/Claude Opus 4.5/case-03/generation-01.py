
"""
Automated test cases for Subscription Management System. 
Based exclusively on the formal specifications provided. 
"""
import pytest
from decimal import Decimal


# =============================================================================
# BUSINESS RULE BR01: Subscription states
# =============================================================================

# BR01 – Subscription can be in ACTIVE state
def test_br01_subscription_can_be_in_active_state():
    from cases.case03 import Subscription
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    assert subscription.status == "ACTIVE"


# BR01 – Subscription can be in SUSPENDED state
def test_br01_subscription_can_be_in_suspended_state():
    from cases.case03 import Subscription
    subscription = Subscription(status="SUSPENDED", payment_failures=0)
    assert subscription.status == "SUSPENDED"


# BR01 – Subscription can be in CANCELED state
def test_br01_subscription_can_be_in_canceled_state():
    from cases.case03 import Subscription
    subscription = Subscription(status="CANCELED", payment_failures=0)
    assert subscription.status == "CANCELED"


# BR01 – Subscription must be in only one state at a time
def test_br01_subscription_has_exactly_one_state():
    from cases.case03 import Subscription
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    valid_states = ["ACTIVE", "SUSPENDED", "CANCELED"]
    assert subscription.status in valid_states
    assert sum(1 for state in valid_states if subscription.status == state) == 1


# =============================================================================
# BUSINESS RULE BR02: Canceled subscriptions cannot be reactivated
# =============================================================================

# BR02 – Canceled subscription must not be reactivated by successful payment
def test_br02_canceled_subscription_cannot_be_reactivated_by_successful_payment():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=True)
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# BR02 – Canceled subscription must not be reactivated by failed payment
def test_br02_canceled_subscription_cannot_be_reactivated_by_failed_payment():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=False)
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# BR02 – Canceled subscription status must remain CANCELED
def test_br02_canceled_subscription_status_remains_canceled():
    from cases.case03 import Subscription
    subscription = Subscription(status="CANCELED", payment_failures=0)
    assert subscription.status == "CANCELED"


# =============================================================================
# BUSINESS RULE BR03: Automatic suspension after exactly 3 consecutive failures
# =============================================================================

# BR03 – Subscription is NOT suspended after 1 consecutive payment failure
def test_br03_subscription_not_suspended_after_1_consecutive_failure():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.status == "ACTIVE"
    assert subscription.payment_failures == 1


# BR03 – Subscription is NOT suspended after 2 consecutive payment failures
def test_br03_subscription_not_suspended_after_2_consecutive_failures():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    subscription.record_payment(payment)
    assert subscription.status == "ACTIVE"
    assert subscription.payment_failures == 2


# BR03 – Subscription IS suspended after exactly 3 consecutive payment failures
def test_br03_subscription_suspended_after_exactly_3_consecutive_failures():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    subscription.record_payment(payment)
    subscription.record_payment(payment)
    assert subscription.status == "SUSPENDED"
    assert subscription.payment_failures == 3


# BR03 – Subscription with 2 failures becomes suspended on 3rd failure
def test_br03_subscription_with_2_failures_becomes_suspended_on_third_failure():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=2)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.status == "SUSPENDED"
    assert subscription.payment_failures == 3


# =============================================================================
# BUSINESS RULE BR04: Successful payment resets failure counter to zero
# =============================================================================

# BR04 – Successful payment resets failure counter from 0 to 0
def test_br04_successful_payment_keeps_failure_counter_at_zero():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0


# BR04 – Successful payment resets failure counter from 1 to 0
def test_br04_successful_payment_resets_failure_counter_from_1_to_zero():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=1)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0


# BR04 – Successful payment resets failure counter from 2 to 0
def test_br04_successful_payment_resets_failure_counter_from_2_to_zero():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=2)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0


# BR04 – Successful payment on suspended subscription resets failure counter to zero
def test_br04_successful_payment_on_suspended_subscription_resets_counter():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="SUSPENDED", payment_failures=3)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0


# =============================================================================
# BUSINESS RULE BR05: Billing dates must not be retroactive
# =============================================================================

# BR05 – Retroactive billing date must raise exception
def test_br05_retroactive_billing_date_raises_exception():
    from cases.case03 import Subscription, Payment
    from datetime import date, timedelta
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    retroactive_date = date.today() - timedelta(days=1)
    payment = Payment(success=True)
    with pytest. raises(Exception):
        subscription.record_payment(payment, billing_date=retroactive_date)


# BR05 – Current date billing is valid (not retroactive)
def test_br05_current_date_billing_is_valid():
    from cases.case03 import Subscription, Payment
    from datetime import date
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    current_date = date. today()
    payment = Payment(success=True)
    # Should not raise exception
    subscription.record_payment(payment, billing_date=current_date)


# BR05 – Future date billing is valid (not retroactive)
def test_br05_future_date_billing_is_valid():
    from cases.case03 import Subscription, Payment
    from datetime import date, timedelta
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    future_date = date.today() + timedelta(days=1)
    payment = Payment(success=True)
    # Should not raise exception
    subscription.record_payment(payment, billing_date=future_date)


# =============================================================================
# FUNCTIONAL REQUIREMENT FR01: System must record payments
# =============================================================================

# FR01 – System records successful payment
def test_fr01_system_records_successful_payment():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=True)
    result = subscription.record_payment(payment)
    assert result is not None


# FR01 – System records failed payment
def test_fr01_system_records_failed_payment():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    result = subscription.record_payment(payment)
    assert result is not None


# FR01 – Payment object has success attribute set to True
def test_fr01_payment_success_attribute_true():
    from cases.case03 import Payment
    payment = Payment(success=True)
    assert payment. success is True


# FR01 – Payment object has success attribute set to False
def test_fr01_payment_success_attribute_false():
    from cases.case03 import Payment
    payment = Payment(success=False)
    assert payment.success is False


# =============================================================================
# FUNCTIONAL REQUIREMENT FR02: System updates subscription status based on payment
# =============================================================================

# FR02 – Failed payment increments failure counter
def test_fr02_failed_payment_increments_failure_counter():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 1


# FR02 – Successful payment on active subscription keeps status active
def test_fr02_successful_payment_keeps_active_status():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription. status == "ACTIVE"


# FR02 – Successful payment on suspended subscription reactivates subscription
def test_fr02_successful_payment_reactivates_suspended_subscription():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="SUSPENDED", payment_failures=3)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.status == "ACTIVE"


# FR02 – Failed payment on suspended subscription keeps suspended status
def test_fr02_failed_payment_on_suspended_keeps_suspended():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="SUSPENDED", payment_failures=3)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.status == "SUSPENDED"


# =============================================================================
# FUNCTIONAL REQUIREMENT FR03: System controls consecutive payment failures
# =============================================================================

# FR03 – Consecutive failure counter starts at zero
def test_fr03_consecutive_failure_counter_starts_at_zero():
    from cases.case03 import Subscription
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    assert subscription.payment_failures == 0


# FR03 – Consecutive failures increment by 1 for each failed payment
def test_fr03_consecutive_failures_increment_by_one():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription. payment_failures == 1
    subscription.record_payment(payment)
    assert subscription.payment_failures == 2


# FR03 – Successful payment breaks consecutive failure sequence
def test_fr03_successful_payment_breaks_consecutive_failures():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=2)
    success_payment = Payment(success=True)
    subscription.record_payment(success_payment)
    assert subscription.payment_failures == 0
    failed_payment = Payment(success=False)
    subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 1


# =============================================================================
# FUNCTIONAL REQUIREMENT FR04: System prevents invalid state transitions
# =============================================================================

# FR04 – Transition from CANCELED to ACTIVE is invalid
def test_fr04_transition_from_canceled_to_active_is_invalid():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=True)
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# FR04 – Transition from CANCELED to SUSPENDED is invalid
def test_fr04_transition_from_canceled_to_suspended_is_invalid():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=False)
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# FR04 – Transition from ACTIVE to SUSPENDED is valid after 3 failures
def test_fr04_transition_from_active_to_suspended_is_valid():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=2)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.status == "SUSPENDED"


# FR04 – Transition from SUSPENDED to ACTIVE is valid with successful payment
def test_fr04_transition_from_suspended_to_active_is_valid():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="SUSPENDED", payment_failures=3)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.status == "ACTIVE"


# =============================================================================
# FUNCTIONAL REQUIREMENT FR05: System raises exception on failure
# =============================================================================

# FR05 – Exception raised when attempting to record payment on canceled subscription
def test_fr05_exception_raised_on_payment_for_canceled_subscription():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=True)
    with pytest.raises(Exception):
        subscription. record_payment(payment)


# FR05 – Exception raised for retroactive billing date
def test_fr05_exception_raised_for_retroactive_billing_date():
    from cases.case03 import Subscription, Payment
    from datetime import date, timedelta
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    retroactive_date = date.today() - timedelta(days=1)
    payment = Payment(success=True)
    with pytest.raises(Exception):
        subscription.record_payment(payment, billing_date=retroactive_date)


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

# Edge case – Subscription at exactly 2 failures receiving successful payment
def test_edge_case_2_failures_then_success_resets_counter():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=2)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"


# Edge case – Suspended subscription receiving additional failed payment
def test_edge_case_suspended_subscription_failure_increments_counter():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="SUSPENDED", payment_failures=3)
    payment = Payment(success=False)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 4
    assert subscription.status == "SUSPENDED"


# Edge case – record_payment returns Decimal type
def test_edge_case_record_payment_returns_decimal():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=True)
    result = subscription.record_payment(payment)
    assert isinstance(result, Decimal)


# Edge case – Multiple successful payments in sequence keep counter at zero
def test_edge_case_multiple_successful_payments_keep_counter_zero():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    payment = Payment(success=True)
    subscription.record_payment(payment)
    subscription.record_payment(payment)
    subscription.record_payment(payment)
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"


# Edge case – Alternating success and failure resets counter each time
def test_edge_case_alternating_payments_reset_counter():
    from cases.case03 import Subscription, Payment
    subscription = Subscription(status="ACTIVE", payment_failures=0)
    failed = Payment(success=False)
    success = Payment(success=True)
    subscription.record_payment(failed)
    assert subscription.payment_failures == 1
    subscription.record_payment(success)
    assert subscription.payment_failures == 0
    subscription.record_payment(failed)
    assert subscription.payment_failures == 1
    subscription.record_payment(failed)
    assert subscription.payment_failures == 2
    subscription.record_payment(success)
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"
