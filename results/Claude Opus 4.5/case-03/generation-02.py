
"""
Automated tests for the Subscription Management System. 
Tests are based exclusively on the provided business rules (BR) and functional requirements (FR).
"""

import pytest
from decimal import Decimal


# =============================================================================
# BUSINESS RULE 01 (BR01) - Subscription states
# A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
# =============================================================================

# BR01 – Subscription can be in ACTIVE state
def test_subscription_can_have_active_status():
    from cases.case03 import Subscription
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    assert subscription.status == "ACTIVE"


# BR01 – Subscription can be in SUSPENDED state
def test_subscription_can_have_suspended_status():
    from cases.case03 import Subscription
    
    subscription = Subscription()
    subscription.status = "SUSPENDED"
    
    assert subscription.status == "SUSPENDED"


# BR01 – Subscription can be in CANCELED state
def test_subscription_can_have_canceled_status():
    from cases.case03 import Subscription
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    assert subscription.status == "CANCELED"


# =============================================================================
# BUSINESS RULE 02 (BR02) - Canceled subscriptions cannot be reactivated
# Subscriptions with status CANCELED must not be reactivated under any circumstances
# =============================================================================

# BR02 – Canceled subscription cannot be reactivated to ACTIVE
def test_canceled_subscription_cannot_be_reactivated_to_active():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    payment = Payment(success=True)
    
    with pytest. raises(Exception):
        subscription.record_payment(payment)


# BR02 – Canceled subscription cannot be changed to SUSPENDED
def test_canceled_subscription_cannot_transition_to_suspended():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    payment = Payment(success=False)
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# =============================================================================
# BUSINESS RULE 03 (BR03) - Automatic suspension after exactly 3 consecutive failures
# The subscription must be automatically suspended after exactly 3 consecutive payment failures
# =============================================================================

# BR03 – Subscription is not suspended after 1 consecutive payment failure
def test_subscription_not_suspended_after_one_failure():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"


# BR03 – Subscription is not suspended after 2 consecutive payment failures
def test_subscription_not_suspended_after_two_failures():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription. payment_failures = 1
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"


# BR03 – Subscription is suspended after exactly 3 consecutive payment failures
def test_subscription_suspended_after_exactly_three_consecutive_failures():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription. payment_failures = 2
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.status == "SUSPENDED"


# BR03 – Subscription suspended after 3 consecutive failures starting from zero
def test_subscription_suspended_after_three_consecutive_failures_from_zero():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription. payment_failures = 0
    
    failed_payment = Payment(success=False)
    
    subscription.record_payment(failed_payment)
    subscription.record_payment(failed_payment)
    subscription.record_payment(failed_payment)
    
    assert subscription.status == "SUSPENDED"


# =============================================================================
# BUSINESS RULE 04 (BR04) - Successful payment resets failure counter
# A successful payment must reset the consecutive payment failure counter to zero
# =============================================================================

# BR04 – Successful payment resets failure counter to zero from one failure
def test_successful_payment_resets_failure_counter_from_one():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 1
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 0


# BR04 – Successful payment resets failure counter to zero from two failures
def test_successful_payment_resets_failure_counter_from_two():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 0


# BR04 – Successful payment on suspended subscription resets failure counter
def test_successful_payment_resets_failure_counter_on_suspended_subscription():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "SUSPENDED"
    subscription.payment_failures = 3
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 0


# =============================================================================
# BUSINESS RULE 05 (BR05) - Billing dates must not be retroactive
# =============================================================================

# BR05 – Retroactive billing date raises exception
def test_retroactive_billing_date_raises_exception():
    from cases.case03 import Subscription, Payment
    from datetime import date
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    # Assuming payment has a billing_date attribute for this validation
    past_date = date(2020, 1, 1)
    
    with pytest.raises(Exception):
        payment = Payment(success=True, billing_date=past_date)
        subscription.record_payment(payment)


# =============================================================================
# FUNCTIONAL REQUIREMENT 01 (FR01) - System must record payments
# =============================================================================

# FR01 – System records a successful payment
def test_system_records_successful_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=True)
    result = subscription.record_payment(payment)
    
    assert isinstance(result, Decimal)


# FR01 – System records a failed payment
def test_system_records_failed_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=False)
    result = subscription.record_payment(payment)
    
    assert isinstance(result, Decimal)


# =============================================================================
# FUNCTIONAL REQUIREMENT 02 (FR02) - System updates subscription status based on payment
# =============================================================================

# FR02 – Subscription status remains ACTIVE after successful payment
def test_subscription_status_remains_active_after_successful_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription. payment_failures = 0
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"


# FR02 – Suspended subscription becomes ACTIVE after successful payment
def test_suspended_subscription_becomes_active_after_successful_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "SUSPENDED"
    subscription. payment_failures = 3
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"


# FR02 – Active subscription becomes SUSPENDED after third consecutive failure
def test_active_subscription_becomes_suspended_after_third_failure():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.status == "SUSPENDED"


# =============================================================================
# FUNCTIONAL REQUIREMENT 03 (FR03) - System controls consecutive payment failures
# =============================================================================

# FR03 – Payment failure counter increments by one on failed payment
def test_payment_failure_counter_increments_on_failed_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 1


# FR03 – Payment failure counter increments from one to two
def test_payment_failure_counter_increments_from_one_to_two():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 1
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 2


# FR03 – Payment failure counter increments from two to three
def test_payment_failure_counter_increments_from_two_to_three():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 3


# FR03 – Payment failure counter remains zero after successful payment with zero failures
def test_payment_failure_counter_remains_zero_after_successful_payment():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.payment_failures == 0


# =============================================================================
# FUNCTIONAL REQUIREMENT 04 (FR04) - System prevents invalid state transitions
# =============================================================================

# FR04 – Invalid transition from CANCELED to ACTIVE is prevented
def test_invalid_transition_from_canceled_to_active_prevented():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    payment = Payment(success=True)
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# FR04 – Invalid transition from CANCELED to SUSPENDED is prevented
def test_invalid_transition_from_canceled_to_suspended_prevented():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    subscription.payment_failures = 2
    
    payment = Payment(success=False)
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# =============================================================================
# FUNCTIONAL REQUIREMENT 05 (FR05) - System raises exception on failure
# =============================================================================

# FR05 – Exception raised when recording payment on canceled subscription
def test_exception_raised_on_payment_for_canceled_subscription():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "CANCELED"
    
    payment = Payment(success=True)
    
    with pytest.raises(Exception):
        subscription.record_payment(payment)


# FR05 – Exception raised for retroactive billing date
def test_exception_raised_for_retroactive_billing_date():
    from cases.case03 import Subscription, Payment
    from datetime import date
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    
    past_date = date(2020, 1, 1)
    
    with pytest.raises(Exception):
        payment = Payment(success=True, billing_date=past_date)
        subscription.record_payment(payment)


# =============================================================================
# EDGE CASES - Explicit boundary conditions from rules
# =============================================================================

# Edge Case – Payment failure counter is exactly 2 before third failure causes suspension
def test_edge_case_exactly_two_failures_before_suspension():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 2
    
    # Before third failure, still ACTIVE
    assert subscription.status == "ACTIVE"
    assert subscription.payment_failures == 2
    
    payment = Payment(success=False)
    subscription.record_payment(payment)
    
    # After exactly third failure, becomes SUSPENDED
    assert subscription. status == "SUSPENDED"
    assert subscription.payment_failures == 3


# Edge Case – Successful payment right before suspension threshold prevents suspension
def test_edge_case_successful_payment_at_two_failures_prevents_suspension():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription. payment_failures = 2
    
    payment = Payment(success=True)
    subscription.record_payment(payment)
    
    assert subscription.status == "ACTIVE"
    assert subscription.payment_failures == 0


# Edge Case – Payment success attribute is exactly True
def test_payment_success_attribute_is_true():
    from cases.case03 import Payment
    
    payment = Payment(success=True)
    
    assert payment.success is True


# Edge Case – Payment success attribute is exactly False
def test_payment_success_attribute_is_false():
    from cases.case03 import Payment
    
    payment = Payment(success=False)
    
    assert payment. success is False


# Edge Case – Subscription payment_failures starts at zero
def test_subscription_payment_failures_initial_value():
    from cases.case03 import Subscription
    
    subscription = Subscription()
    subscription.payment_failures = 0
    
    assert subscription.payment_failures == 0


# Edge Case – record_payment returns Decimal type
def test_record_payment_returns_decimal():
    from cases.case03 import Subscription, Payment
    
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    
    payment = Payment(success=True)
    result = subscription. record_payment(payment)
    
    assert type(result) is Decimal
