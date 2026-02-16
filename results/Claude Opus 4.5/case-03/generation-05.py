
"""
Automated Test Suite for Subscription Management System
Based on formal specifications provided. 
"""

import pytest
from decimal import Decimal

from cases.case03 import Subscription, Payment
# =============================================================================
# BUSINESS RULE TESTS (BR)
# =============================================================================


class TestBR01SubscriptionStates: 
    """BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED"""

    # BR01 – Subscription can be in ACTIVE state
    def test_subscription_can_have_active_status(self, active_subscription):
        assert active_subscription.status == "ACTIVE"

    # BR01 – Subscription can be in SUSPENDED state
    def test_subscription_can_have_suspended_status(self, suspended_subscription):
        assert suspended_subscription. status == "SUSPENDED"

    # BR01 – Subscription can be in CANCELED state
    def test_subscription_can_have_canceled_status(self, canceled_subscription):
        assert canceled_subscription.status == "CANCELED"


class TestBR02CanceledSubscriptionReactivation:
    """BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances"""

    # BR02 – Canceled subscription must not be reactivated by successful payment
    def test_canceled_subscription_cannot_be_reactivated_by_successful_payment(
        self, canceled_subscription, successful_payment
    ):
        with pytest.raises(Exception):
            canceled_subscription.record_payment(successful_payment)

    # BR02 – Canceled subscription status remains CANCELED after reactivation attempt
    def test_canceled_subscription_status_remains_canceled_after_reactivation_attempt(
        self, canceled_subscription, successful_payment
    ):
        initial_status = canceled_subscription.status
        try:
            canceled_subscription.record_payment(successful_payment)
        except Exception: 
            pass
        assert canceled_subscription. status == initial_status
        assert canceled_subscription.status == "CANCELED"


class TestBR03ConsecutivePaymentFailures: 
    """BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures"""

    # BR03 – Subscription remains ACTIVE after 1 consecutive payment failure
    def test_subscription_remains_active_after_one_payment_failure(
        self, active_subscription, failed_payment
    ):
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status == "ACTIVE"
        assert active_subscription.payment_failures == 1

    # BR03 – Subscription remains ACTIVE after 2 consecutive payment failures
    def test_subscription_remains_active_after_two_payment_failures(
        self, active_subscription, failed_payment
    ):
        active_subscription. record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status == "ACTIVE"
        assert active_subscription.payment_failures == 2

    # BR03 – Subscription is SUSPENDED after exactly 3 consecutive payment failures
    def test_subscription_is_suspended_after_three_consecutive_payment_failures(
        self, active_subscription, failed_payment
    ):
        active_subscription.record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status == "SUSPENDED"
        assert active_subscription.payment_failures == 3

    # BR03 – Suspension occurs at exactly 3 failures, not before
    def test_suspension_does_not_occur_before_three_failures(
        self, active_subscription, failed_payment
    ):
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status != "SUSPENDED"
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status != "SUSPENDED"
        active_subscription.record_payment(failed_payment)
        assert active_subscription.status == "SUSPENDED"


class TestBR04SuccessfulPaymentResetsCounter:
    """BR04 – A successful payment must reset the consecutive payment failure counter to zero"""

    # BR04 – Successful payment resets failure counter from 0 to 0
    def test_successful_payment_keeps_failure_counter_at_zero(
        self, active_subscription, successful_payment
    ):
        assert active_subscription.payment_failures == 0
        active_subscription.record_payment(successful_payment)
        assert active_subscription.payment_failures == 0

    # BR04 – Successful payment resets failure counter from 1 to 0
    def test_successful_payment_resets_failure_counter_from_one(
        self, active_subscription, failed_payment, successful_payment
    ):
        active_subscription.record_payment(failed_payment)
        assert active_subscription.payment_failures == 1
        active_subscription.record_payment(successful_payment)
        assert active_subscription.payment_failures == 0

    # BR04 – Successful payment resets failure counter from 2 to 0
    def test_successful_payment_resets_failure_counter_from_two(
        self, active_subscription, failed_payment, successful_payment
    ):
        active_subscription.record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        assert active_subscription. payment_failures == 2
        active_subscription.record_payment(successful_payment)
        assert active_subscription.payment_failures == 0


class TestBR05BillingDatesNotRetroactive: 
    """BR05 – Billing dates must not be retroactive"""

    # BR05 – Retroactive billing date must raise exception
    def test_retroactive_billing_date_raises_exception(
        self, active_subscription, payment_with_retroactive_date
    ):
        with pytest.raises(Exception):
            active_subscription.record_payment(payment_with_retroactive_date)

    # BR05 – Current date billing is valid (non-retroactive)
    def test_current_date_billing_is_valid(
        self, active_subscription, payment_with_current_date
    ):
        # Should not raise exception
        active_subscription.record_payment(payment_with_current_date)

    # BR05 – Future date billing is valid (non-retroactive)
    def test_future_date_billing_is_valid(
        self, active_subscription, payment_with_future_date
    ):
        # Should not raise exception
        active_subscription.record_payment(payment_with_future_date)


# =============================================================================
# FUNCTIONAL REQUIREMENT TESTS (FR)
# =============================================================================


class TestFR01RecordPayments:
    """FR01 – The system must record payments"""

    # FR01 – System records successful payment
    def test_system_records_successful_payment(
        self, active_subscription, successful_payment
    ):
        result = active_subscription. record_payment(successful_payment)
        assert result is not None

    # FR01 – System records failed payment
    def test_system_records_failed_payment(
        self, active_subscription, failed_payment
    ):
        result = active_subscription. record_payment(failed_payment)
        assert result is not None

    # FR01 – record_payment returns Decimal type
    def test_record_payment_returns_decimal(
        self, active_subscription, successful_payment
    ):
        result = active_subscription.record_payment(successful_payment)
        assert isinstance(result, Decimal)


class TestFR02UpdateSubscriptionStatus: 
    """FR02 – The system must update the subscription status based on payment success or failure"""

    # FR02 – Successful payment on ACTIVE subscription keeps status ACTIVE
    def test_successful_payment_on_active_subscription_keeps_active_status(
        self, active_subscription, successful_payment
    ):
        active_subscription.record_payment(successful_payment)
        assert active_subscription.status == "ACTIVE"

    # FR02 – Failed payment updates failure count
    def test_failed_payment_updates_subscription_state(
        self, active_subscription, failed_payment
    ):
        initial_failures = active_subscription. payment_failures
        active_subscription.record_payment(failed_payment)
        assert active_subscription.payment_failures == initial_failures + 1

    # FR02 – Successful payment on SUSPENDED subscription reactivates to ACTIVE
    def test_successful_payment_on_suspended_subscription_reactivates_to_active(
        self, suspended_subscription, successful_payment
    ):
        suspended_subscription. record_payment(successful_payment)
        assert suspended_subscription. status == "ACTIVE"


class TestFR03ControlConsecutivePaymentFailures: 
    """FR03 – The system must control the number of consecutive payment failures"""

    # FR03 – Initial payment failure count is zero
    def test_initial_payment_failure_count_is_zero(self, active_subscription):
        assert active_subscription.payment_failures == 0

    # FR03 – Payment failure count increments by one on failed payment
    def test_payment_failure_count_increments_on_failed_payment(
        self, active_subscription, failed_payment
    ):
        active_subscription. record_payment(failed_payment)
        assert active_subscription. payment_failures == 1

    # FR03 – Payment failure count increments consecutively
    def test_payment_failure_count_increments_consecutively(
        self, active_subscription, failed_payment
    ):
        active_subscription.record_payment(failed_payment)
        active_subscription. record_payment(failed_payment)
        assert active_subscription. payment_failures == 2

    # FR03 – Failure counter tracks exactly 3 consecutive failures
    def test_failure_counter_tracks_three_consecutive_failures(
        self, active_subscription, failed_payment
    ):
        active_subscription. record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        assert active_subscription.payment_failures == 3


class TestFR04PreventInvalidStateTransitions: 
    """FR04 – The system must prevent invalid state transitions"""

    # FR04 – CANCELED to ACTIVE transition is prevented
    def test_canceled_to_active_transition_is_prevented(
        self, canceled_subscription, successful_payment
    ):
        with pytest.raises(Exception):
            canceled_subscription.record_payment(successful_payment)
        assert canceled_subscription.status == "CANCELED"

    # FR04 – CANCELED subscription cannot process any payment
    def test_canceled_subscription_cannot_process_failed_payment(
        self, canceled_subscription, failed_payment
    ):
        with pytest.raises(Exception):
            canceled_subscription.record_payment(failed_payment)
        assert canceled_subscription.status == "CANCELED"


class TestFR05RaiseExceptionOnFailure:
    """FR05 – The system must raise an exception in case of a failure"""

    # FR05 – Exception raised when attempting to reactivate CANCELED subscription
    def test_exception_raised_on_canceled_subscription_reactivation_attempt(
        self, canceled_subscription, successful_payment
    ):
        with pytest. raises(Exception):
            canceled_subscription. record_payment(successful_payment)

    # FR05 – Exception raised for retroactive billing date
    def test_exception_raised_for_retroactive_billing_date(
        self, active_subscription, payment_with_retroactive_date
    ):
        with pytest.raises(Exception):
            active_subscription.record_payment(payment_with_retroactive_date)


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCases:
    """Edge cases explicitly required by the rules"""

    # Edge case – Failure counter reset followed by new failures sequence
    def test_failure_counter_reset_then_new_failure_sequence(
        self, active_subscription, failed_payment, successful_payment
    ):
        # Two failures
        active_subscription. record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        assert active_subscription.payment_failures == 2
        
        # Reset with successful payment
        active_subscription.record_payment(successful_payment)
        assert active_subscription.payment_failures == 0
        
        # New failure sequence
        active_subscription.record_payment(failed_payment)
        assert active_subscription.payment_failures == 1
        assert active_subscription.status == "ACTIVE"

    # Edge case – Exactly 3 failures required for suspension, not 4
    def test_suspension_requires_exactly_three_failures(
        self, active_subscription, failed_payment
    ):
        active_subscription.record_payment(failed_payment)
        active_subscription.record_payment(failed_payment)
        # Before third failure, still ACTIVE
        assert active_subscription.status == "ACTIVE"
        active_subscription. record_payment(failed_payment)
        # After exactly third failure, SUSPENDED
        assert active_subscription.status == "SUSPENDED"

    # Edge case – Payment success attribute is boolean true
    def test_payment_success_attribute_is_true(self, successful_payment):
        assert successful_payment. success is True

    # Edge case – Payment success attribute is boolean false
    def test_payment_success_attribute_is_false(self, failed_payment):
        assert failed_payment.success is False


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def successful_payment():
    """Creates a successful payment instance"""
    return Payment(success=True)


@pytest.fixture
def failed_payment():
    """Creates a failed payment instance"""
    return Payment(success=False)


@pytest.fixture
def active_subscription():
    """Creates an active subscription with zero payment failures"""
    subscription = Subscription()
    subscription.status = "ACTIVE"
    subscription.payment_failures = 0
    return subscription


@pytest.fixture
def suspended_subscription():
    """Creates a suspended subscription"""
    subscription = Subscription()
    subscription.status = "SUSPENDED"
    subscription.payment_failures = 3
    return subscription


@pytest.fixture
def canceled_subscription():
    """Creates a canceled subscription"""
    subscription = Subscription()
    subscription.status = "CANCELED"
    subscription.payment_failures = 0
    return subscription


@pytest.fixture
def payment_with_retroactive_date():
    """Creates a payment with a retroactive billing date"""
    payment = Payment(success=True)
    payment.billing_date = "retroactive"
    return payment


@pytest.fixture
def payment_with_current_date():
    """Creates a payment with current billing date"""
    payment = Payment(success=True)
    payment.billing_date = "current"
    return payment


@pytest.fixture
def payment_with_future_date():
    """Creates a payment with future billing date"""
    payment = Payment(success=True)
    payment.billing_date = "future"
    return payment
