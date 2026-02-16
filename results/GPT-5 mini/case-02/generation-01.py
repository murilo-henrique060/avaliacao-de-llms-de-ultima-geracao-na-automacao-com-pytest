from decimal import Decimal
import pytest

# The tests below assume the system under test exposes Item and Order classes
# with the signatures described in the specification:
# Item(name: str, price: Decimal, quantity: int)
# Order.add_item(item: Item) -> None
# Order.calculate_total() -> Decimal
from cases.case02 import Item, Order


# BR01 – An order must contain at least one item
def test_br01_add_single_item_returns_none():
    # BR01 positive: adding a single valid item to an order must be allowed (no exception)
    order = Order()
    item = Item(name="A", price=Decimal("10.00"), quantity=1)
    result = order.add_item(item)
    assert result is None


def test_br01_calculate_total_raises_when_no_items():
    # BR01 negative: calculating total for an order with zero items must raise an exception (failure)
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


# BR02 – Each item must have a minimum quantity of 1
def test_br02_add_item_with_quantity_one_is_valid():
    # BR02 positive: adding an item with quantity exactly 1 must be allowed (no exception)
    order = Order()
    item = Item(name="B", price=Decimal("5.00"), quantity=1)
    result = order.add_item(item)
    assert result is None


def test_br02_calculate_total_raises_for_item_with_quantity_zero():
    # BR02 negative: if an item has quantity 0, calculating the order total must raise an exception (failure)
    order = Order()
    item = Item(name="B-invalid", price=Decimal("5.00"), quantity=0)
    order.add_item(item)
    with pytest.raises(Exception):
        order.calculate_total()


# BR03 – All items must have a positive price
def test_br03_add_item_with_positive_price_is_valid():
    # BR03 positive: adding an item with a positive price must be allowed (no exception)
    order = Order()
    item = Item(name="C", price=Decimal("1.00"), quantity=1)
    result = order.add_item(item)
    assert result is None


def test_br03_calculate_total_raises_for_item_with_non_positive_price():
    # BR03 negative: if an item has a non-positive price (0.00), calculating the order total must raise an exception (failure)
    order = Order()
    item = Item(name="C-invalid", price=Decimal("0.00"), quantity=1)
    order.add_item(item)
    with pytest.raises(Exception):
        order.calculate_total()


# BR04 – The total order value is the sum of the items
def test_br04_calculate_total_is_exact_sum_of_items_without_discount():
    # BR04 positive: calculate_total must return the exact sum of (price * quantity) for all items when no discount applies
    order = Order()
    item1 = Item(name="D1", price=Decimal("10.00"), quantity=1)   # 10.00
    item2 = Item(name="D2", price=Decimal("5.00"), quantity=2)    # 10.00
    order.add_item(item1)
    order.add_item(item2)
    total = order.calculate_total()
    assert total == Decimal("20.00")


# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_discount_applied_for_order_total_above_200():
    # BR05 positive: orders with pre-discount total strictly greater than 200 receive a single 10% discount
    order = Order()
    item1 = Item(name="E1", price=Decimal("150.00"), quantity=1)  # 150.00
    item2 = Item(name="E2", price=Decimal("60.00"), quantity=1)   # 60.00
    order.add_item(item1)
    order.add_item(item2)
    total = order.calculate_total()  # pre-discount 210.00 -> after 10% discount 189.00
    assert total == Decimal("189.00")


def test_br05_no_discount_for_order_equal_200():
    # BR05 negative: orders with pre-discount total exactly 200 must NOT receive the 10% discount
    order = Order()
    item = Item(name="E-eq", price=Decimal("200.00"), quantity=1)  # 200.00
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("200.00")


# BR06 – The discount must not be applied more than once
def test_br06_discount_not_applied_more_than_once_across_multiple_calculations():
    # BR06 positive: calling calculate_total multiple times must not apply the 10% discount more than once
    order = Order()
    item1 = Item(name="F1", price=Decimal("120.00"), quantity=1)  # 120.00
    item2 = Item(name="F2", price=Decimal("90.00"), quantity=1)   # 90.00 -> pre-discount 210.00
    order.add_item(item1)
    order.add_item(item2)
    first_total = order.calculate_total()   # expected 189.00
    second_total = order.calculate_total()  # must remain 189.00, not 170.10
    assert first_total == Decimal("189.00")
    assert second_total == Decimal("189.00")


# FR01 – Create an order with multiple items
def test_fr01_add_multiple_items_returns_none_each_call():
    # FR01 positive: add_item can be called multiple times to add multiple items and must return None on each call
    order = Order()
    item1 = Item(name="G1", price=Decimal("10.00"), quantity=1)
    item2 = Item(name="G2", price=Decimal("20.00"), quantity=1)
    res1 = order.add_item(item1)
    res2 = order.add_item(item2)
    assert res1 is None
    assert res2 is None


# FR02 – Correctly calculate the total
def test_fr02_calculate_total_correct_for_multiple_items_without_discount():
    # FR02 positive: calculate_total must compute correct final total when no discount eligibility (sum of items)
    order = Order()
    item1 = Item(name="H1", price=Decimal("50.00"), quantity=2)   # 100.00
    item2 = Item(name="H2", price=Decimal("25.00"), quantity=1)   # 25.00
    order.add_item(item1)
    order.add_item(item2)
    total = order.calculate_total()
    assert total == Decimal("125.00")


# FR03 – The system must apply the discount correctly when eligible
def test_fr03_calculate_total_applies_10_percent_discount_when_eligible():
    # FR03 positive: when pre-discount total is strictly greater than 200, calculate_total must return the 10%-discounted value
    order = Order()
    item = Item(name="I", price=Decimal("201.00"), quantity=1)   # 201.00 -> after 10% discount 180.90
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("180.90")


# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_decimal_final_value():
    # FR04 positive: calculate_total must return the final order value as a Decimal object
    order = Order()
    item = Item(name="J", price=Decimal("30.00"), quantity=1)
    order.add_item(item)
    total = order.calculate_total()
    assert isinstance(total, Decimal)


# FR05 – The system must raise an exception in case of a failure
def test_fr05_calculate_total_raises_on_invalid_item_price_failure():
    # FR05 negative: an invalid item price should cause calculate_total to raise an exception (demonstrating failure handling)
    order = Order()
    invalid_item = Item(name="K-invalid", price=Decimal("-10.00"), quantity=1)
    order.add_item(invalid_item)
    with pytest.raises(Exception):
        order.calculate_total()