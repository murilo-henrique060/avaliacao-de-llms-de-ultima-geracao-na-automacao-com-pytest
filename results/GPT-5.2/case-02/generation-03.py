import pytest
from decimal import Decimal

# NOTE: These tests assume the SUT provides the classes below as specified:
# - Item(name: str, price: Decimal, quantity: int)
# - Order.add_item(item: Item) -> None
# - Order.calculate_total() -> Decimal
from cases.case02 import Item, Order  # type: ignore


def test_br01_order_must_contain_at_least_one_item_raises_exception_on_calculate_total_with_no_items():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


def test_br01_order_with_one_item_is_allowed_and_calculates_total():
    # BR01 – An order must contain at least one item
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
    assert order.calculate_total() == Decimal("10.00")


def test_br02_item_quantity_minimum_1_raises_exception_on_add_item_with_quantity_zero():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10.00"), quantity=0))


def test_br02_item_quantity_equal_1_is_allowed_and_calculates_total():
    # BR02 – Each item must have a minimum quantity of 1
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("7.50"), quantity=1))
    assert order.calculate_total() == Decimal("7.50")


def test_br03_item_price_must_be_positive_raises_exception_on_add_item_with_price_zero():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("0.00"), quantity=1))


def test_br03_item_price_positive_is_allowed_and_calculates_total():
    # BR03 – All items must have a positive price
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("0.01"), quantity=1))
    assert order.calculate_total() == Decimal("0.01")


def test_br04_total_order_value_is_sum_of_items_without_discount_when_not_above_200():
    # BR04 – The total order value is the sum of the items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("50.00"), quantity=2))  # 100.00
    order.add_item(Item(name="B", price=Decimal("20.00"), quantity=5))  # 100.00
    assert order.calculate_total() == Decimal("200.00")


def test_fr01_create_order_with_multiple_items_add_item_accepts_multiple_items():
    # FR01 – Create an order with multiple items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("20.00"), quantity=2))
    assert order.calculate_total() == Decimal("50.00")


def test_fr02_correctly_calculate_total_for_single_item_quantity_multiple():
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("12.00"), quantity=3))
    assert order.calculate_total() == Decimal("36.00")


def test_br05_orders_above_200_receive_10_percent_discount_exactly_above_threshold():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))
    assert order.calculate_total() == Decimal("180.90")


def test_br05_no_discount_applied_when_total_is_exactly_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="A", price=Decimal("200.00"), quantity=1))
    assert order.calculate_total() == Decimal("200.00")


def test_fr03_apply_discount_correctly_for_multiple_items_total_above_200():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="A", price=Decimal("100.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("105.00"), quantity=1))
    # Pre-discount total: 205.00 -> discounted: 184.50
    assert order.calculate_total() == Decimal("184.50")


def test_fr04_display_final_order_value_returns_final_value_from_calculate_total():
    # FR04 – The system must display the final order value
    # (Interpreted strictly: calculate_total returns the final order value as a Decimal.)
    order = Order()
    order.add_item(Item(name="A", price=Decimal("250.00"), quantity=1))
    assert order.calculate_total() == Decimal("225.00")


def test_br06_discount_must_not_be_applied_more_than_once_when_calculate_total_called_twice():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="A", price=Decimal("300.00"), quantity=1))
    first = order.calculate_total()
    second = order.calculate_total()
    assert first == Decimal("270.00")
    assert second == Decimal("270.00")


def test_fr05_raise_exception_in_case_of_failure_when_adding_item_with_negative_price():
    # FR05 – The system must raise an exception in case of a failure
    # BR03 – All items must have a positive price
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("-1.00"), quantity=1))