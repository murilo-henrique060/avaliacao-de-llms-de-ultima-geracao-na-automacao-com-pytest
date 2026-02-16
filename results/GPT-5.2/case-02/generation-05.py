import pytest
from decimal import Decimal

# Tests assume Item and Order are provided by the system under test.
from cases.case02 import Item, Order


def test_br01_order_must_contain_at_least_one_item_raises_exception_when_empty():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


def test_br01_order_with_one_item_is_allowed():
    # BR01 – An order must contain at least one item
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("10")


def test_br02_item_minimum_quantity_is_1_allows_quantity_1():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("10")


def test_br02_item_quantity_0_raises_exception():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10"), quantity=0))


def test_br03_item_price_must_be_positive_allows_positive_price():
    # BR03 – All items must have a positive price
    order = Order()
    order.add_item(Item(name="A", price=Decimal("0.01"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("0.01")


def test_br03_item_price_zero_raises_exception():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("0"), quantity=1))


def test_br04_total_order_value_is_sum_of_items_without_discount_at_or_below_200():
    # BR04 – The total order value is the sum of the items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("50"), quantity=2))   # 100
    order.add_item(Item(name="B", price=Decimal("25"), quantity=4))   # 100
    total = order.calculate_total()
    assert total == Decimal("200")


def test_br05_orders_above_200_receive_10_percent_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("180.9")


def test_br05_orders_equal_to_200_do_not_receive_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="A", price=Decimal("200"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("200")


def test_br06_discount_must_not_be_applied_more_than_once_across_multiple_calculations():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201"), quantity=1))

    total_first = order.calculate_total()
    assert total_first == Decimal("180.9")

    total_second = order.calculate_total()
    assert total_second == Decimal("180.9")


def test_fr01_create_order_with_multiple_items():
    # FR01 – Create an order with multiple items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("20"), quantity=2))
    total = order.calculate_total()
    assert total == Decimal("50")


def test_fr02_correctly_calculate_total_without_discount():
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("12.34"), quantity=2))  # 24.68
    order.add_item(Item(name="B", price=Decimal("0.01"), quantity=1))   # 0.01
    total = order.calculate_total()
    assert total == Decimal("24.69")


def test_fr03_apply_discount_correctly_when_eligible():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="A", price=Decimal("250"), quantity=1))
    total = order.calculate_total()
    assert total == Decimal("225")


def test_fr04_display_final_order_value_returns_decimal():
    # FR04 – The system must display the final order value
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10"), quantity=1))
    final_value = order.calculate_total()
    assert isinstance(final_value, Decimal)


def test_fr05_raise_exception_on_failure_when_adding_invalid_item_quantity():
    # FR05 – The system must raise an exception in case of a failure
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10"), quantity=-1))