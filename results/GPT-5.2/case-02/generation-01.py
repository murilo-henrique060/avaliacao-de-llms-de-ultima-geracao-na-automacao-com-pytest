import pytest
from decimal import Decimal

# NOTE:
# These tests assume the SUT provides classes named `Item` and `Order`
# with the attributes/methods shown in the UML:
# - Item(name: str, price: Decimal, quantity: int)
# - Order.add_item(item: Item) -> None
# - Order.calculate_total() -> Decimal
#
# The tests intentionally do not implement the system.

from cases.case02 import Item, Order

def test_br01_order_with_one_item_is_valid_and_total_is_calculated():
    # BR01 – An order must contain at least one item
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))

    total = order.calculate_total()

    assert total == Decimal("10.00")


def test_br01_order_with_no_items_raises_exception_on_total_calculation():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()

    with pytest.raises(Exception):
        order.calculate_total()


def test_br02_item_with_minimum_quantity_1_is_accepted_and_counted_in_total():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    order.add_item(Item(name="A", price=Decimal("3.00"), quantity=1))

    total = order.calculate_total()

    assert total == Decimal("3.00")


def test_br02_item_with_quantity_0_raises_exception_when_added():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    order = Order()

    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("3.00"), quantity=0))


def test_br03_item_with_positive_price_is_accepted_and_counted_in_total():
    # BR03 – All items must have a positive price
    order = Order()
    order.add_item(Item(name="A", price=Decimal("1.00"), quantity=2))

    total = order.calculate_total()

    assert total == Decimal("2.00")


def test_br03_item_with_zero_price_raises_exception_when_added():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()

    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("0.00"), quantity=1))


def test_br03_item_with_negative_price_raises_exception_when_added():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()

    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("-1.00"), quantity=1))


def test_br04_total_is_sum_of_all_items_price_times_quantity():
    # BR04 – The total order value is the sum of the items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("10.00"), quantity=2))  # 20.00
    order.add_item(Item(name="B", price=Decimal("5.00"), quantity=3))   # 15.00

    total = order.calculate_total()

    assert total == Decimal("35.00")


def test_br05_total_above_200_receives_exactly_10_percent_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))

    total = order.calculate_total()

    assert total == Decimal("180.90")  # 201.00 * 0.90


def test_br05_total_equal_to_200_does_not_receive_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="A", price=Decimal("200.00"), quantity=1))

    total = order.calculate_total()

    assert total == Decimal("200.00")


def test_br06_discount_is_not_applied_more_than_once_when_calculating_total_twice():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))

    total_first = order.calculate_total()
    total_second = order.calculate_total()

    assert total_first == Decimal("180.90")
    assert total_second == Decimal("180.90")  # must not become 162.81


def test_fr01_create_order_with_multiple_items_by_adding_items_without_exception():
    # FR01 – Create an order with multiple items
    order = Order()

    order.add_item(Item(name="A", price=Decimal("1.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("2.00"), quantity=1))

    assert True  # reaching here means no exception was raised while adding multiple items


def test_fr02_calculate_total_correctly_for_multiple_items():
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("50.00"), quantity=2))  # 100.00
    order.add_item(Item(name="B", price=Decimal("25.00"), quantity=1))  # 25.00

    total = order.calculate_total()

    assert total == Decimal("125.00")


def test_fr03_apply_discount_correctly_when_eligible():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="A", price=Decimal("250.00"), quantity=1))

    total = order.calculate_total()

    assert total == Decimal("225.00")  # 250.00 * 0.90


def test_fr04_calculate_total_returns_final_order_value_after_discount():
    # FR04 – The system must display the final order value
    order = Order()
    order.add_item(Item(name="A", price=Decimal("201.00"), quantity=1))

    final_value = order.calculate_total()

    assert final_value == Decimal("180.90")


def test_fr05_raises_exception_when_adding_item_with_invalid_quantity():
    # FR05 – The system must raise an exception in case of a failure
    order = Order()

    with pytest.raises(Exception):
        order.add_item(Item(name="A", price=Decimal("10.00"), quantity=0))