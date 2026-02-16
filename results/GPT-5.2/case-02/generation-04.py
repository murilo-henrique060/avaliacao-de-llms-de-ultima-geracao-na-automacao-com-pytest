import pytest
from decimal import Decimal

# NOTE:
# These tests assume the SUT provides the following classes exactly as specified:
# - Item(name: str, price: Decimal, quantity: int)
# - Order with methods:
#   - add_item(item: Item) -> None
#   - calculate_total() -> Decimal

from cases.case02 import Item, Order

def test_br01_order_must_contain_at_least_one_item_raises_exception_when_empty():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    from order_system import Order  # type: ignore

    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


def test_fr01_create_order_with_multiple_items_add_item_accepts_multiple_items():
    # FR01 – Create an order with multiple items
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("20.00"), quantity=2))


def test_br02_item_minimum_quantity_is_1_allows_quantity_equal_to_1():
    # BR02 – Each item must have a minimum quantity of 1
    # FR01 – Create an order with multiple items
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("1.00"), quantity=1))


def test_br02_item_minimum_quantity_is_1_raises_exception_when_quantity_is_0():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    from order_system import Order, Item  # type: ignore

    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("1.00"), quantity=0))


def test_br03_item_price_must_be_positive_allows_price_greater_than_0():
    # BR03 – All items must have a positive price
    # FR01 – Create an order with multiple items
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("0.01"), quantity=1))


def test_br03_item_price_must_be_positive_raises_exception_when_price_is_0():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    from order_system import Order, Item  # type: ignore

    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("0.00"), quantity=1))


def test_br03_item_price_must_be_positive_raises_exception_when_price_is_negative():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    from order_system import Order, Item  # type: ignore

    order = Order()
    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("-0.01"), quantity=1))


def test_br04_total_order_value_is_sum_of_items_when_not_discount_eligible():
    # BR04 – The total order value is the sum of the items
    # FR02 – Correctly calculate the total
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("50.00"), quantity=2))  # 100.00
    order.add_item(Item(name="B", price=Decimal("20.00"), quantity=3))  # 60.00

    total = order.calculate_total()
    assert total == Decimal("160.00")


def test_fr02_calculate_total_returns_decimal():
    # FR02 – Correctly calculate the total
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("1.00"), quantity=1))

    total = order.calculate_total()
    assert isinstance(total, Decimal)


def test_br05_orders_above_200_receive_10_percent_discount_exact_example_210_to_189():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    # FR04 – The system must display the final order value
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("210.00"), quantity=1))

    total = order.calculate_total()
    assert total == Decimal("189.00")


def test_br05_orders_equal_to_200_do_not_receive_discount_total_is_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    # FR04 – The system must display the final order value
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("200.00"), quantity=1))

    total = order.calculate_total()
    assert total == Decimal("200.00")


def test_br06_discount_must_not_be_applied_more_than_once_when_calculate_total_called_twice():
    # BR06 – The discount must not be applied more than once
    # FR03 – The system must apply the discount correctly when eligible
    # FR04 – The system must display the final order value
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("210.00"), quantity=1))

    first_total = order.calculate_total()
    second_total = order.calculate_total()

    assert first_total == Decimal("189.00")
    assert second_total == Decimal("189.00")


def test_fr04_display_final_order_value_returns_final_amount_including_discount_when_eligible():
    # FR04 – The system must display the final order value
    # BR05 – Orders above R$ 200 receive a 10% discount
    from order_system import Order, Item  # type: ignore

    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))

    total = order.calculate_total()
    assert total == Decimal("180.90")