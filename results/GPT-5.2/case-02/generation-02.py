import pytest
from decimal import Decimal

# NOTE:
# These tests assume the SUT provides classes named Item and Order as specified.
# They intentionally do not implement the system.
from cases.case02 import Item, Order  # type: ignore


def test_br01_order_must_contain_at_least_one_item_raises_exception_when_no_items():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


def test_br01_order_with_one_item_is_allowed():
    # BR01 – An order must contain at least one item
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("10.00")


def test_br02_item_quantity_minimum_1_raises_exception_when_quantity_is_zero():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10.00"), quantity=0))


def test_br02_item_quantity_minimum_1_allows_quantity_1():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("10.00")


def test_br03_item_price_must_be_positive_raises_exception_when_price_is_zero():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("0.00"), quantity=1))


def test_br03_item_price_must_be_positive_raises_exception_when_price_is_negative():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("-1.00"), quantity=1))


def test_br03_item_price_must_be_positive_allows_positive_price():
    # BR03 – All items must have a positive price
    order = Order()
    order.add_item(Item(name="A", price=Decimal("0.01"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("0.01")


def test_br04_total_order_value_is_sum_of_items():
    # BR04 – The total order value is the sum of the items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=2))  # 20.00
    order.add_item(Item(name="B", price=Decimal("5.00"), quantity=3))   # 15.00
    total = order.calculate_total()
    assert total == Decimal("35.00")


def test_br05_orders_above_200_receive_10_percent_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    # Total before discount = 201.00
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))
    total = order.calculate_total()
    # Expected after 10% discount = 180.90
    assert total == Decimal("180.90")


def test_br05_discount_not_applied_when_total_is_exactly_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    # Total = 200.00 (not above 200)
    order.add_item(Item(name="A", price=Decimal("200.00"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("200.00")


def test_br06_discount_must_not_be_applied_more_than_once_on_repeated_calculation():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))
    first_total = order.calculate_total()
    second_total = order.calculate_total()
    assert first_total == second_total


def test_fr01_create_order_with_multiple_items():
    # FR01 – Create an order with multiple items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("1.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("2.00"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("3.00")


def test_fr02_correctly_calculate_total_without_discount_when_not_eligible():
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("50.00"), quantity=2))  # 100.00
    order.add_item(Item(name="B", price=Decimal("99.99"), quantity=1))  # 99.99
    total = order.calculate_total()
    assert total == Decimal("199.99")


def test_fr03_apply_discount_correctly_when_eligible():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    # Total before discount = 300.00
    order.add_item(Item(name="A", price=Decimal("100.00"), quantity=3))
    total = order.calculate_total()
    # Expected after 10% discount = 270.00
    assert total == Decimal("270.00")


def test_fr04_display_final_order_value_as_return_value_of_calculate_total():
    # FR04 – The system must display the final order value
    # Interpreted strictly from the provided interface: calculate_total() returns the final value.
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))
    final_value = order.calculate_total()
    assert final_value == Decimal("180.90")


def test_fr05_raise_exception_on_failure_invalid_item_quantity():
    # FR05 – The system must raise an exception in case of a failure
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10.00"), quantity=-1))