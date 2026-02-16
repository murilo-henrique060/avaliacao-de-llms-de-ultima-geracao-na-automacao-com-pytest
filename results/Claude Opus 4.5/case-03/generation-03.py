
"""
Automated test cases for Subscription Management System
Based on formal specifications provided
"""

import pytest
from decimal import Decimal


# =============================================================================
# BUSINESS RULE TESTS (BR)
# =============================================================================


class TestBR01SubscriptionStates:
    """BR01: A subscription may be in only one of the following states:  ACTIVE, SUSPENDED, or CANCELED"""

    # BR01 – Subscription can have ACTIVE status
    def test_subscription_status_can_be_active(self):
        from cases.case03 import Subscription
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        
        assert subscription.status == "ACTIVE"

    # BR01 – Subscription can have SUSPENDED status
    def test_subscription_status_can_be_suspended(self):
        from cases.case03 import Subscription
        
        subscription = Subscription()
        subscription.status = "SUSPENDED"
        
        assert subscription.status == "SUSPENDED"

    # BR01 – Subscription can have CANCELED status
    def test_subscription_status_can_be_canceled(self):
        from cases.case03 import Subscription
        
        subscription = Subscription()
        subscription.status = "CANCELED"
        
        assert subscription.status == "CANCELED"

    # BR01 – Subscription cannot have an invalid status
    def test_subscription_status_cannot_be_invalid(self):
        from cases.case03 import Subscription
        
        subscription = Subscription()
        
        with pytest. raises(Exception):
            subscription. status = "INVALID_STATUS"


class TestBR02CanceledSubscriptionReactivation:
    """BR02: Subscriptions with status CANCELED must not be reactivated under any circumstances"""

    # BR02 – Canceled subscription cannot transition to ACTIVE
    def test_canceled_subscription_cannot_be_reactivated_to_active(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "CANCELED"
        
        payment = Payment()
        payment.success = True
        
        with pytest.raises(Exception):
            subscription. record_payment(payment)

    # BR02 – Canceled subscription cannot transition to SUSPENDED
    def test_canceled_subscription_cannot_transition_to_suspended(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "CANCELED"
        
        payment = Payment()
        payment.success = False
        
        with pytest.raises(Exception):
            subscription. record_payment(payment)


class TestBR03SuspensionAfterThreeFailures:
    """BR03: The subscription must be automatically suspended after exactly 3 consecutive payment failures"""

    # BR03 – Subscription is NOT suspended after 1 consecutive payment failure
    def test_subscription_not_suspended_after_one_failure(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"
        assert subscription. payment_failures == 1

    # BR03 – Subscription is NOT suspended after 2 consecutive payment failures
    def test_subscription_not_suspended_after_two_failures(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 1
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"
        assert subscription. payment_failures == 2

    # BR03 – Subscription IS suspended after exactly 3 consecutive payment failures
    def test_subscription_suspended_after_exactly_three_failures(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription. payment_failures = 2
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.status == "SUSPENDED"
        assert subscription. payment_failures == 3

    # BR03 – Subscription suspended after 3 consecutive failures starting from zero
    def test_subscription_suspended_after_three_consecutive_failures_from_zero(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        failed_payment = Payment()
        failed_payment.success = False
        
        subscription. record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        
        assert subscription.status == "SUSPENDED"
        assert subscription.payment_failures == 3


class TestBR04SuccessfulPaymentResetsFailureCounter: 
    """BR04: A successful payment must reset the consecutive payment failure counter to zero"""

    # BR04 – Successful payment resets failure counter from 1 to 0
    def test_successful_payment_resets_failure_counter_from_one(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 1
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 0

    # BR04 – Successful payment resets failure counter from 2 to 0
    def test_successful_payment_resets_failure_counter_from_two(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = True
        
        subscription. record_payment(payment)
        
        assert subscription.payment_failures == 0

    # BR04 – Successful payment keeps failure counter at zero when already zero
    def test_successful_payment_keeps_failure_counter_at_zero(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 0


class TestBR05BillingDateNotRetroactive:
    """BR05: Billing dates must not be retroactive"""

    # BR05 – Recording payment with retroactive billing date raises exception
    def test_retroactive_billing_date_raises_exception(self):
        from cases.case03 import Subscription, Payment
        from datetime import date
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        
        payment = Payment()
        payment.success = True
        payment.billing_date = date(2025, 1, 1)  # Past date relative to current date 2026-01-12
        
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # BR05 – Recording payment with current billing date does not raise exception
    def test_current_billing_date_does_not_raise_exception(self):
        from cases.case03 import Subscription, Payment
        from datetime import date
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        payment.billing_date = date(2026, 1, 12)  # Current date
        
        result = subscription.record_payment(payment)
        
        assert isinstance(result, Decimal)

    # BR05 – Recording payment with future billing date does not raise exception
    def test_future_billing_date_does_not_raise_exception(self):
        from cases.case03 import Subscription, Payment
        from datetime import date
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        payment.billing_date = date(2026, 2, 1)  # Future date
        
        result = subscription.record_payment(payment)
        
        assert isinstance(result, Decimal)


# =============================================================================
# FUNCTIONAL REQUIREMENTS TESTS (FR)
# =============================================================================


class TestFR01RecordPayments:
    """FR01: The system must record payments"""

    # FR01 – System records a successful payment
    def test_system_records_successful_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        
        result = subscription.record_payment(payment)
        
        assert isinstance(result, Decimal)

    # FR01 – System records a failed payment
    def test_system_records_failed_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = False
        
        result = subscription.record_payment(payment)
        
        assert isinstance(result, Decimal)


class TestFR02UpdateSubscriptionStatus:
    """FR02: The system must update the subscription status based on payment success or failure"""

    # FR02 – Subscription status remains ACTIVE after successful payment
    def test_status_remains_active_after_successful_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"

    # FR02 – Subscription status changes to SUSPENDED after third consecutive failure
    def test_status_changes_to_suspended_after_third_failure(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.status == "SUSPENDED"

    # FR02 – Suspended subscription can be reactivated with successful payment
    def test_suspended_subscription_reactivated_with_successful_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "SUSPENDED"
        subscription.payment_failures = 3
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"


class TestFR03ControlConsecutivePaymentFailures: 
    """FR03: The system must control the number of consecutive payment failures"""

    # FR03 – Payment failure increments the consecutive failure counter
    def test_payment_failure_increments_failure_counter(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 1

    # FR03 – Multiple consecutive failures increment the counter correctly
    def test_multiple_failures_increment_counter_correctly(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 2

    # FR03 – Successful payment resets consecutive failure counter
    def test_successful_payment_resets_consecutive_failure_counter(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 0


class TestFR04PreventInvalidStateTransitions:
    """FR04: The system must prevent invalid state transitions"""

    # FR04 – Transition from CANCELED to ACTIVE is prevented
    def test_transition_from_canceled_to_active_is_prevented(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "CANCELED"
        
        payment = Payment()
        payment.success = True
        
        with pytest.raises(Exception):
            subscription. record_payment(payment)

    # FR04 – Transition from CANCELED to SUSPENDED is prevented
    def test_transition_from_canceled_to_suspended_is_prevented(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "CANCELED"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = False
        
        with pytest.raises(Exception):
            subscription. record_payment(payment)


class TestFR05RaiseExceptionOnFailure:
    """FR05: The system must raise an exception in case of a failure"""

    # FR05 – Exception raised when recording payment on canceled subscription
    def test_exception_raised_for_canceled_subscription_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription. status = "CANCELED"
        
        payment = Payment()
        payment.success = True
        
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # FR05 – Exception raised for retroactive billing date
    def test_exception_raised_for_retroactive_billing_date(self):
        from cases.case03 import Subscription, Payment
        from datetime import date
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        
        payment = Payment()
        payment.success = True
        payment.billing_date = date(2020, 1, 1)  # Retroactive date
        
        with pytest. raises(Exception):
            subscription.record_payment(payment)

    # FR05 – Exception raised for invalid subscription status assignment
    def test_exception_raised_for_invalid_status_assignment(self):
        from cases.case03 import Subscription
        
        subscription = Subscription()
        
        with pytest. raises(Exception):
            subscription.status = "UNKNOWN"


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCasesPaymentFailureCounter:
    """Edge cases for payment failure counter behavior"""

    # Edge case – Failure counter at exactly 2, then successful payment resets to 0
    def test_failure_counter_at_two_reset_by_successful_payment(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 0
        assert subscription.status == "ACTIVE"

    # Edge case – Failure counter at exactly 3 after suspension
    def test_failure_counter_exactly_three_after_suspension(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 2
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.payment_failures == 3
        assert subscription. status == "SUSPENDED"


class TestEdgeCasesSuspendedSubscription:
    """Edge cases for suspended subscription behavior"""

    # Edge case – Suspended subscription reactivated by successful payment resets counter
    def test_suspended_subscription_successful_payment_resets_counter(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "SUSPENDED"
        subscription.payment_failures = 3
        
        payment = Payment()
        payment.success = True
        
        subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"
        assert subscription. payment_failures == 0

    # Edge case – Suspended subscription with failed payment
    def test_suspended_subscription_failed_payment_increments_counter(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "SUSPENDED"
        subscription.payment_failures = 3
        
        payment = Payment()
        payment.success = False
        
        subscription.record_payment(payment)
        
        assert subscription.status == "SUSPENDED"
        assert subscription.payment_failures == 4


class TestEdgeCasesPaymentSuccess:
    """Edge cases for payment success attribute"""

    # Edge case – Payment with success=True on active subscription
    def test_payment_success_true_on_active_subscription(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = True
        
        result = subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"
        assert subscription.payment_failures == 0
        assert isinstance(result, Decimal)

    # Edge case – Payment with success=False on active subscription
    def test_payment_success_false_on_active_subscription(self):
        from cases.case03 import Subscription, Payment
        
        subscription = Subscription()
        subscription.status = "ACTIVE"
        subscription.payment_failures = 0
        
        payment = Payment()
        payment.success = False
        
        result = subscription.record_payment(payment)
        
        assert subscription.status == "ACTIVE"
        assert subscription. payment_failures == 1
        assert isinstance(result, Decimal)
