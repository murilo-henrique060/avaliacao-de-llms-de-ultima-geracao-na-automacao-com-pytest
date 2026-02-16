from decimal import Decimal
import pytest

# The tests assume the existence of Item and Order classes with the API from the specification:
# Item(name: str, price: Decimal, quantity: int)
# Order.add_item(item: Item) -> None
# Order.calculate_total() -> Decimal
from cases.case02 import Item, Order


# BR01 – An order must contain at least one item
def test_br01_order_with_at_least_one_item_is_valid_and_calculable():
    order = Order()
    item = Item(name="A", price=Decimal("10.00"), quantity=1)
    # BR01 – An order must contain at least one item
    order.add_item(item)
    total = order.calculate_total()
    assert isinstance(total, Decimal)


# BR01 – An order must contain at least one item
def test_br01_calculate_total_on_order_with_no_items_raises_exception():
    order = Order()
    # BR01 – An order must contain at least one item
    with pytest.raises(Exception):
        order.calculate_total()


# BR02 – Each item must have a minimum quantity of 1
def test_br02_item_with_quantity_one_can_be_added():
    order = Order()
    item = Item(name="B", price=Decimal("5.00"), quantity=1)
    # BR02 – Each item must have a minimum quantity of 1
    # The behavior validated: adding an item with quantity 1 does not raise.
    order.add_item(item)


# BR02 – Each item must have a minimum quantity of 1
def test_br02_adding_item_with_quantity_zero_raises_exception():
    order = Order()
    invalid_item = Item(name="C", price=Decimal("5.00"), quantity=0)
    # BR02 – Each item must have a minimum quantity of 1
    with pytest.raises(Exception):
        order.add_item(invalid_item)


# BR03 – All items must have a positive price
def test_br03_item_with_positive_price_can_be_added():
    order = Order()
    item = Item(name="D", price=Decimal("0.01"), quantity=1)
    # BR03 – All items must have a positive price
    # The behavior validated: adding an item with positive price does not raise.
    order.add_item(item)


# BR03 – All items must have a positive price
def test_br03_adding_item_with_zero_price_raises_exception():
    order = Order()
    invalid_item = Item(name="E", price=Decimal("0.00"), quantity=1)
    # BR03 – All items must have a positive price
    with pytest.raises(Exception):
        order.add_item(invalid_item)


# BR04 – The total order value is the sum of the items
def test_br04_calculate_total_is_sum_of_item_price_times_quantity():
    order = Order()
    item1 = Item(name="F1", price=Decimal("10.00"), quantity=2)  # 20.00
    item2 = Item(name="F2", price=Decimal("30.00"), quantity=1)  # 30.00
    # BR04 – The total order value is the sum of the items
    order.add_item(item1)
    order.add_item(item2)
    total = order.calculate_total()
    assert total == Decimal("50.00")


# FR01 – Create an order with multiple items
def test_fr01_adding_multiple_items_to_order_succeeds():
    order = Order()
    item1 = Item(name="G1", price=Decimal("1.00"), quantity=1)
    item2 = Item(name="G2", price=Decimal("2.00"), quantity=1)
    # FR01 – Create an order with multiple items
    order.add_item(item1)
    order.add_item(item2)
    # Validate that creation with multiple items succeeded by ensuring calculate_total returns Decimal
    assert isinstance(order.calculate_total(), Decimal)


# FR02 – Correctly calculate the total
def test_fr02_calculate_total_returns_correct_value_for_multiple_items():
    order = Order()
    item1 = Item(name="H1", price=Decimal("7.50"), quantity=2)  # 15.00
    item2 = Item(name="H2", price=Decimal("4.25"), quantity=1)  # 4.25
    # FR02 – Correctly calculate the total
    order.add_item(item1)
    order.add_item(item2)
    total = order.calculate_total()
    assert total == Decimal("19.25")


# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_orders_above_200_receive_10_percent_discount():
    order = Order()
    # Single item totalling 300.00 to be above 200
    item = Item(name="I", price=Decimal("300.00"), quantity=1)
    # BR05 – Orders above R$ 200 receive a 10% discount
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("270.00")


# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_order_equal_200_does_not_receive_discount():
    order = Order()
    item = Item(name="J", price=Decimal("100.00"), quantity=2)  # exactly 200.00
    # BR05 – Orders above R$ 200 receive a 10% discount
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("200.00")


# BR06 – The discount must not be applied more than once
def test_br06_discount_is_not_applied_more_than_once_on_repeated_calculations():
    order = Order()
    item = Item(name="K", price=Decimal("250.00"), quantity=1)  # 250 > 200
    # BR06 – The discount must not be applied more than once
    order.add_item(item)
    first_total = order.calculate_total()
    second_total = order.calculate_total()
    assert first_total == second_total
    assert first_total == Decimal("225.00")


# FR03 – The system must apply the discount correctly when eligible
def test_fr03_system_applies_10_percent_discount_for_totals_strictly_above_200():
    order = Order()
    item = Item(name="L", price=Decimal("201.00"), quantity=1)
    # FR03 – The system must apply the discount correctly when eligible
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("180.90")


# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_decimal_final_value_type():
    order = Order()
    item = Item(name="M", price=Decimal("12.34"), quantity=1)
    # FR04 – The system must display the final order value
    order.add_item(item)
    final_value = order.calculate_total()
    assert isinstance(final_value, Decimal)


# FR05 – The system must raise an exception in case of a failure
def test_fr05_system_raises_exception_on_invalid_negative_price_item():
    order = Order()
    invalid_item = Item(name="N", price=Decimal("-1.00"), quantity=1)
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        order.add_item(invalid_item)