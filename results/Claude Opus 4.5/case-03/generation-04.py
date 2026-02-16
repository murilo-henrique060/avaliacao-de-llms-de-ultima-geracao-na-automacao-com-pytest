
"""
Automated test cases for Subscription Management System. 
Tests are based exclusively on provided specifications. 
Uses only pytest library. 
"""

import pytest
from decimal import Decimal


# =============================================================================
# BUSINESS RULE TESTS (BR)
# =============================================================================


class TestBR01SubscriptionStates: 
    """BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED"""

    # BR01 – Subscription can have ACTIVE status
    def test_subscription_can_have_active_status(self, subscription_class):
        subscription = subscription_class(status="ACTIVE")
        assert subscription. status == "ACTIVE"

    # BR01 – Subscription can have SUSPENDED status
    def test_subscription_can_have_suspended_status(self, subscription_class):
        subscription = subscription_class(status="SUSPENDED")
        assert subscription. status == "SUSPENDED"

    # BR01 – Subscription can have CANCELED status
    def test_subscription_can_have_canceled_status(self, subscription_class):
        subscription = subscription_class(status="CANCELED")
        assert subscription.status == "CANCELED"

    # BR01 – Subscription must not accept invalid status
    def test_subscription_rejects_invalid_status(self, subscription_class):
        with pytest.raises(Exception):
            subscription_class(status="INVALID")

    # BR01 – Subscription must not accept empty status
    def test_subscription_rejects_empty_status(self, subscription_class):
        with pytest.raises(Exception):
            subscription_class(status="")


class TestBR02CanceledSubscriptionReactivation:
    """BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances"""

    # BR02 – Canceled subscription cannot transition to ACTIVE via successful payment
    def test_canceled_subscription_cannot_be_reactivated_by_successful_payment(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=True)
        with pytest.raises(Exception):
            subscription. record_payment(payment)

    # BR02 – Canceled subscription cannot transition to SUSPENDED
    def test_canceled_subscription_cannot_transition_to_suspended(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=False)
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # BR02 – Canceled subscription status remains CANCELED after any operation attempt
    def test_canceled_subscription_status_remains_canceled(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=True)
        try:
            subscription. record_payment(payment)
        except Exception:
            pass
        assert subscription.status == "CANCELED"


class TestBR03AutomaticSuspensionAfterThreeFailures:
    """BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures"""

    # BR03 – Subscription is NOT suspended after 1 consecutive payment failure
    def test_subscription_not_suspended_after_one_failure(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.status == "ACTIVE"

    # BR03 – Subscription is NOT suspended after 2 consecutive payment failures
    def test_subscription_not_suspended_after_two_failures(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=1)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.status == "ACTIVE"

    # BR03 – Subscription IS suspended after exactly 3 consecutive payment failures
    def test_subscription_suspended_after_exactly_three_failures(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.status == "SUSPENDED"

    # BR03 – Payment failures counter reaches exactly 3 when suspended
    def test_payment_failures_counter_is_three_when_suspended(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 3

    # BR03 – Subscription suspended from ACTIVE after 3 sequential failed payments
    def test_subscription_suspended_after_three_sequential_failed_payments(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        failed_payment = payment_class(success=False)
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        subscription.record_payment(failed_payment)
        assert subscription.status == "SUSPENDED"
        assert subscription.payment_failures == 3


class TestBR04SuccessfulPaymentResetsFailureCounter: 
    """BR04 – A successful payment must reset the consecutive payment failure counter to zero"""

    # BR04 – Successful payment resets failure counter from 1 to 0
    def test_successful_payment_resets_counter_from_one_to_zero(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=1)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 0

    # BR04 – Successful payment resets failure counter from 2 to 0
    def test_successful_payment_resets_counter_from_two_to_zero(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=True)
        subscription. record_payment(payment)
        assert subscription.payment_failures == 0

    # BR04 – Successful payment on subscription with zero failures keeps counter at zero
    def test_successful_payment_keeps_counter_at_zero(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription. payment_failures == 0

    # BR04 – Successful payment on SUSPENDED subscription resets failure counter to zero
    def test_successful_payment_on_suspended_resets_counter(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="SUSPENDED", payment_failures=3)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 0


class TestBR05BillingDatesNotRetroactive: 
    """BR05 – Billing dates must not be retroactive"""

    # BR05 – Payment with retroactive billing date must raise exception
    def test_payment_with_retroactive_billing_date_raises_exception(
        self, subscription_class, payment_class_with_billing_date
    ):
        from datetime import date, timedelta

        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        past_date = date.today() - timedelta(days=1)
        payment = payment_class_with_billing_date(success=True, billing_date=past_date)
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # BR05 – Payment with current billing date is accepted
    def test_payment_with_current_billing_date_is_accepted(
        self, subscription_class, payment_class_with_billing_date
    ):
        from datetime import date

        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        current_date = date.today()
        payment = payment_class_with_billing_date(success=True, billing_date=current_date)
        # Should not raise exception
        result = subscription.record_payment(payment)
        assert result is not None or subscription.payment_failures == 0

    # BR05 – Payment with future billing date is accepted
    def test_payment_with_future_billing_date_is_accepted(
        self, subscription_class, payment_class_with_billing_date
    ):
        from datetime import date, timedelta

        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        future_date = date.today() + timedelta(days=1)
        payment = payment_class_with_billing_date(success=True, billing_date=future_date)
        # Should not raise exception
        result = subscription.record_payment(payment)
        assert result is not None or subscription.payment_failures == 0


# =============================================================================
# FUNCTIONAL REQUIREMENT TESTS (FR)
# =============================================================================


class TestFR01RecordPayments:
    """FR01 – The system must record payments"""

    # FR01 – System records a successful payment
    def test_system_records_successful_payment(self, subscription_class, payment_class):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=True)
        result = subscription.record_payment(payment)
        assert isinstance(result, Decimal)

    # FR01 – System records a failed payment
    def test_system_records_failed_payment(self, subscription_class, payment_class):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=False)
        result = subscription.record_payment(payment)
        assert result is not None or subscription.payment_failures == 1

    # FR01 – Payment object has success attribute set to True
    def test_payment_has_success_attribute_true(self, payment_class):
        payment = payment_class(success=True)
        assert payment. success is True

    # FR01 – Payment object has success attribute set to False
    def test_payment_has_success_attribute_false(self, payment_class):
        payment = payment_class(success=False)
        assert payment.success is False


class TestFR02UpdateSubscriptionStatus: 
    """FR02 – The system must update the subscription status based on payment success or failure"""

    # FR02 – Successful payment on ACTIVE subscription keeps status ACTIVE
    def test_successful_payment_keeps_active_status(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription.status == "ACTIVE"

    # FR02 – Successful payment on SUSPENDED subscription changes status to ACTIVE
    def test_successful_payment_reactivates_suspended_subscription(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="SUSPENDED", payment_failures=3)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription.status == "ACTIVE"

    # FR02 – Failed payment causing 3rd failure changes status to SUSPENDED
    def test_failed_payment_causes_suspension_on_third_failure(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.status == "SUSPENDED"


class TestFR03ControlConsecutivePaymentFailures:
    """FR03 – The system must control the number of consecutive payment failures"""

    # FR03 – Failed payment increments failure counter by 1
    def test_failed_payment_increments_failure_counter(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 1

    # FR03 – Failed payment increments failure counter from 1 to 2
    def test_failed_payment_increments_counter_from_one_to_two(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=1)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 2

    # FR03 – Failed payment increments failure counter from 2 to 3
    def test_failed_payment_increments_counter_from_two_to_three(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription. payment_failures == 3

    # FR03 – Successful payment after failures resets counter
    def test_successful_payment_resets_failure_counter_after_failures(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 0


class TestFR04PreventInvalidStateTransitions: 
    """FR04 – The system must prevent invalid state transitions"""

    # FR04 – Transition from CANCELED to ACTIVE is prevented
    def test_transition_from_canceled_to_active_is_prevented(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=True)
        with pytest.raises(Exception):
            subscription. record_payment(payment)

    # FR04 – Transition from CANCELED to SUSPENDED is prevented
    def test_transition_from_canceled_to_suspended_is_prevented(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=False)
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # FR04 – Valid transition from ACTIVE to SUSPENDED is allowed
    def test_valid_transition_from_active_to_suspended(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=False)
        subscription. record_payment(payment)
        assert subscription.status == "SUSPENDED"

    # FR04 – Valid transition from SUSPENDED to ACTIVE is allowed
    def test_valid_transition_from_suspended_to_active(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="SUSPENDED", payment_failures=3)
        payment = payment_class(success=True)
        subscription. record_payment(payment)
        assert subscription.status == "ACTIVE"


class TestFR05RaiseExceptionOnFailure:
    """FR05 – The system must raise an exception in case of a failure"""

    # FR05 – Exception raised when attempting to reactivate CANCELED subscription
    def test_exception_raised_on_canceled_subscription_reactivation(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="CANCELED")
        payment = payment_class(success=True)
        with pytest.raises(Exception):
            subscription.record_payment(payment)

    # FR05 – Exception raised for invalid subscription status
    def test_exception_raised_for_invalid_subscription_status(self, subscription_class):
        with pytest. raises(Exception):
            subscription_class(status="UNKNOWN")

    # FR05 – Exception raised for retroactive billing date
    def test_exception_raised_for_retroactive_billing_date(
        self, subscription_class, payment_class_with_billing_date
    ):
        from datetime import date, timedelta

        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        past_date = date.today() - timedelta(days=1)
        payment = payment_class_with_billing_date(success=True, billing_date=past_date)
        with pytest.raises(Exception):
            subscription.record_payment(payment)


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCases: 
    """Edge cases explicitly required by the rules"""

    # Edge Case – Subscription with exactly 0 payment failures receiving failed payment
    def test_zero_failures_receiving_first_failed_payment(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription. payment_failures == 1
        assert subscription.status == "ACTIVE"

    # Edge Case – Subscription at boundary (2 failures) receiving successful payment
    def test_boundary_two_failures_receiving_successful_payment(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=2)
        payment = payment_class(success=True)
        subscription. record_payment(payment)
        assert subscription.payment_failures == 0
        assert subscription.status == "ACTIVE"

    # Edge Case – SUSPENDED subscription with 3 failures receiving failed payment
    def test_suspended_subscription_receiving_failed_payment(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="SUSPENDED", payment_failures=3)
        payment = payment_class(success=False)
        subscription.record_payment(payment)
        assert subscription. status == "SUSPENDED"
        assert subscription. payment_failures == 4

    # Edge Case – Multiple successful payments in sequence on ACTIVE subscription
    def test_multiple_successful_payments_keep_counter_at_zero(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        payment = payment_class(success=True)
        subscription.record_payment(payment)
        subscription.record_payment(payment)
        subscription.record_payment(payment)
        assert subscription.payment_failures == 0
        assert subscription.status == "ACTIVE"

    # Edge Case – Alternating successful and failed payments
    def test_alternating_successful_and_failed_payments(
        self, subscription_class, payment_class
    ):
        subscription = subscription_class(status="ACTIVE", payment_failures=0)
        failed_payment = payment_class(success=False)
        successful_payment = payment_class(success=True)

        subscription.record_payment(failed_payment)
        assert subscription.payment_failures == 1

        subscription.record_payment(successful_payment)
        assert subscription. payment_failures == 0

        subscription. record_payment(failed_payment)
        assert subscription.payment_failures == 1

        assert subscription.status == "ACTIVE"


# =============================================================================
# FIXTURES (to be provided by the implementation)
# =============================================================================


@pytest.fixture
def payment_class():
    """
    Fixture that provides the Payment class. 
    Must be replaced with actual implementation import.
    """
    from cases.case03 import Payment

    return Payment


@pytest. fixture
def payment_class_with_billing_date():
    """
    Fixture that provides the Payment class with billing_date support.
    Must be replaced with actual implementation import.
    """
    from cases.case03 import Payment

    return Payment


@pytest. fixture
def subscription_class():
    """
    Fixture that provides the Subscription class.
    Must be replaced with actual implementation import.
    """
    from cases.case03 import Subscription

    return Subscription
