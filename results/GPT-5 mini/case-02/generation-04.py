from decimal import Decimal
import pytest

# The system under test is expected to provide Item and Order according to the UML.
# Tests assume they are importable from order_system module.
from cases.case02 import Item, Order


# BR01 – An order must contain at least one item
def test_br01_order_with_at_least_one_item_is_allowed():
    # BR01 – An order must contain at least one item
    order = Order()
    item = Item(name="Widget", price=Decimal("10.00"), quantity=1)
    order.add_item(item)
    result = order.calculate_total()
    # Validate exactly one behavior: calculate_total returns a Decimal when order has at least one item
    assert isinstance(result, Decimal)


# BR01 – An order must contain at least one item (negative)
def test_br01_calculate_total_raises_when_order_has_no_items():
    # BR01 – An order must contain at least one item
    order = Order()
    with pytest.raises(Exception):
        # Validate exactly one behavior: calculating total on an empty order raises an exception
        order.calculate_total()


# BR02 – Each item must have a minimum quantity of 1 (positive)
def test_br02_item_with_quantity_one_is_allowed():
    # BR02 – Each item must have a minimum quantity of 1
    item = Item(name="Single", price=Decimal("5.00"), quantity=1)
    # Validate exactly one behavior: item.quantity is preserved as provided when valid
    assert item.quantity == 1


# BR02 – Each item must have a minimum quantity of 1 (negative)
def test_br02_adding_item_with_zero_quantity_raises_exception():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    item = Item(name="ZeroQty", price=Decimal("5.00"), quantity=0)
    with pytest.raises(Exception):
        # Validate exactly one behavior: adding an item with quantity 0 causes an exception
        order.add_item(item)


# BR03 – All items must have a positive price (positive)
def test_br03_item_with_positive_price_is_allowed():
    # BR03 – All items must have a positive price
    item = Item(name="Priced", price=Decimal("10.00"), quantity=1)
    # Validate exactly one behavior: item.price is preserved as provided when positive
    assert item.price == Decimal("10.00")


# BR03 – All items must have a positive price (negative)
def test_br03_adding_item_with_zero_price_raises_exception():
    # BR03 – All items must have a positive price
    order = Order()
    item = Item(name="Freebie", price=Decimal("0.00"), quantity=1)
    with pytest.raises(Exception):
        # Validate exactly one behavior: adding an item with non-positive price causes an exception
        order.add_item(item)


# BR04 – The total order value is the sum of the items
def test_br04_total_is_exact_sum_of_item_price_times_quantity():
    # BR04 – The total order value is the sum of the items
    order = Order()
    item1 = Item(name="A", price=Decimal("10.00"), quantity=2)  # 20.00
    item2 = Item(name="B", price=Decimal("5.00"), quantity=3)   # 15.00
    order.add_item(item1)
    order.add_item(item2)
    # Validate exactly one behavior: total equals 20.00 + 15.00 = 35.00 (no discount applied)
    assert order.calculate_total() == Decimal("35.00")


# BR05 – Orders above R$ 200 receive a 10% discount (positive)
def test_br05_orders_above_200_receive_ten_percent_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    expensive = Item(name="Expensive", price=Decimal("250.00"), quantity=1)
    order.add_item(expensive)
    # Validate exactly one behavior: 250.00 with 10% discount => 225.00
    assert order.calculate_total() == Decimal("225.00")


# BR05 – Orders above R$ 200 receive a 10% discount (negative)
def test_br05_order_equal_200_does_not_receive_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    exact = Item(name="Exact200", price=Decimal("200.00"), quantity=1)
    order.add_item(exact)
    # Validate exactly one behavior: order total exactly 200.00 does not get discounted
    assert order.calculate_total() == Decimal("200.00")


# BR06 – The discount must not be applied more than once
def test_br06_calculate_total_is_idempotent_and_discount_not_applied_twice():
    # BR06 – The discount must not be applied more than once
    order = Order()
    item = Item(name="Bulk", price=Decimal("300.00"), quantity=1)
    order.add_item(item)
    first = order.calculate_total()
    second = order.calculate_total()
    # Validate exactly one behavior: repeating calculate_total does not change the final value (no double discount)
    assert second == first


# FR01 – Create an order with multiple items
def test_fr01_adding_multiple_items_to_order_is_supported():
    # FR01 – Create an order with multiple items
    order = Order()
    item1 = Item(name="One", price=Decimal("10.00"), quantity=1)
    item2 = Item(name="Two", price=Decimal("20.00"), quantity=1)
    order.add_item(item1)
    order.add_item(item2)
    # Validate exactly one behavior: order with multiple items produces a Decimal total (operation allowed)
    assert isinstance(order.calculate_total(), Decimal)


# FR02 – Correctly calculate the total
def test_fr02_calculates_total_for_price_times_quantity():
    # FR02 – Correctly calculate the total
    order = Order()
    item = Item(name="Multiply", price=Decimal("12.34"), quantity=3)  # 12.34 * 3 = 37.02
    order.add_item(item)
    # Validate exactly one behavior: calculation uses price * quantity precisely
    assert order.calculate_total() == Decimal("37.02")


# FR03 – The system must apply the discount correctly when eligible
def test_fr03_discount_applied_for_minimally_above_200_total():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    item = Item(name="Boundary", price=Decimal("201.00"), quantity=1)
    order.add_item(item)
    # Validate exactly one behavior: 201.00 -> 10% discount -> 180.90
    assert order.calculate_total() == Decimal("180.90")


# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_final_order_value_without_discount():
    # FR04 – The system must display the final order value
    order = Order()
    item = Item(name="Simple", price=Decimal("50.00"), quantity=1)
    order.add_item(item)
    # Validate exactly one behavior: calculate_total returns the final order value (no discount case)
    assert order.calculate_total() == Decimal("50.00")


# FR05 – The system must raise an exception in case of a failure
def test_fr05_calculate_total_raises_exception_for_empty_order_failure():
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        # Validate exactly one behavior: calculating total on an invalid/failed state (empty order) raises an exception
        order.calculate_total()