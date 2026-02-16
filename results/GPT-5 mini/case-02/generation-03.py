from decimal import Decimal
import pytest

# The tests below assume the existence of classes `Order` and `Item`
# with the interfaces described in the specification:
# Item(name: str, price: Decimal, quantity: int)
# Order.add_item(item: Item) -> None
# Order.calculate_total() -> Decimal
from cases.case02 import Order, Item


# BR01 – An order must contain at least one item
def test_br01_empty_order_calculate_total_raises_exception():
    # BR01
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()


# BR01 – An order must contain at least one item (positive case: order with one item allowed)
def test_br01_order_with_one_item_allows_calculation_without_exception():
    # BR01
    order = Order()
    item = Item(name="Single", price=Decimal("10.00"), quantity=1)
    # Adding at least one item should allow calculate_total to run (no exception)
    order.add_item(item)
    # Single behavior: ensure calculate_total does not raise and returns a Decimal
    total = order.calculate_total()
    assert isinstance(total, Decimal)


# BR02 – Each item must have a minimum quantity of 1 (positive case)
def test_br02_add_item_with_quantity_one_is_allowed():
    # BR02
    order = Order()
    item = Item(name="QtyOne", price=Decimal("5.00"), quantity=1)
    result = order.add_item(item)
    # Expectation: add_item returns None on success (as per UML signature)
    assert result is None


# BR02 – Each item must have a minimum quantity of 1 (negative case)
def test_br02_add_item_with_quantity_zero_raises_exception():
    # BR02
    order = Order()
    item = Item(name="ZeroQty", price=Decimal("5.00"), quantity=0)
    with pytest.raises(Exception):
        order.add_item(item)


# BR03 – All items must have a positive price (positive case)
def test_br03_add_item_with_positive_price_is_allowed():
    # BR03
    order = Order()
    item = Item(name="PositivePrice", price=Decimal("0.01"), quantity=1)
    result = order.add_item(item)
    # Expectation: add_item returns None on success
    assert result is None


# BR03 – All items must have a positive price (negative case: zero price)
def test_br03_add_item_with_zero_price_raises_exception():
    # BR03
    order = Order()
    item = Item(name="ZeroPrice", price=Decimal("0.00"), quantity=1)
    with pytest.raises(Exception):
        order.add_item(item)


# BR03 – All items must have a positive price (negative case: negative price)
def test_br03_add_item_with_negative_price_raises_exception():
    # BR03
    order = Order()
    item = Item(name="NegativePrice", price=Decimal("-1.00"), quantity=1)
    with pytest.raises(Exception):
        order.add_item(item)


# BR04 – The total order value is the sum of the items
def test_br04_calculate_total_is_exact_sum_of_price_times_quantity_without_discount():
    # BR04
    order = Order()
    # Choose values that do not trigger discount (>200) to isolate BR04
    item1 = Item(name="A", price=Decimal("30.00"), quantity=2)  # 60.00
    item2 = Item(name="B", price=Decimal("20.50"), quantity=1)  # 20.50
    order.add_item(item1)
    order.add_item(item2)
    expected = Decimal("80.50")
    total = order.calculate_total()
    assert total == expected


# FR02 – Correctly calculate the total (single item)
def test_fr02_calculate_total_for_single_item_returns_price_times_quantity():
    # FR02
    order = Order()
    item = Item(name="SingleCalc", price=Decimal("12.34"), quantity=3)  # 37.02
    order.add_item(item)
    total = order.calculate_total()
    assert total == Decimal("37.02")


# FR01 – Create an order with multiple items
def test_fr01_adding_multiple_items_succeeds_for_each_add_call():
    # FR01
    order = Order()
    item1 = Item(name="Multi1", price=Decimal("1.00"), quantity=1)
    item2 = Item(name="Multi2", price=Decimal("2.00"), quantity=1)
    res1 = order.add_item(item1)
    res2 = order.add_item(item2)
    # Both add_item calls should succeed and return None
    assert res1 is None
    assert res2 is None


# FR03 – The system must apply the discount correctly when eligible
def test_fr03_apply_10_percent_discount_for_orders_above_200():
    # BR05 and FR03
    order = Order()
    # Subtotal > 200 to trigger discount
    item = Item(name="Expensive", price=Decimal("250.00"), quantity=1)
    order.add_item(item)
    total = order.calculate_total()
    # Expected: 10% discount applied once -> 250.00 * (1 - 0.10) = 225.00
    assert total == Decimal("225.00")


# BR05 – Orders above R$ 200 receive a 10% discount (edge negative case: exactly 200)
def test_br05_no_discount_for_orders_equal_to_200():
    # BR05
    order = Order()
    item = Item(name="Edge", price=Decimal("200.00"), quantity=1)
    order.add_item(item)
    total = order.calculate_total()
    # Exactly 200 should NOT receive discount according to BR05 ("above R$ 200")
    assert total == Decimal("200.00")


# BR06 – The discount must not be applied more than once
def test_br06_discount_not_applied_more_than_once_on_multiple_calculations():
    # BR06
    order = Order()
    item = Item(name="DoubleCheck", price=Decimal("300.00"), quantity=1)
    order.add_item(item)
    first_total = order.calculate_total()
    second_total = order.calculate_total()
    # Both calls must produce the same final value, ensuring the discount wasn't stacked
    assert first_total == second_total
    assert first_total == Decimal("270.00")  # 300.00 with 10% discount


# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_final_order_value_including_discount_if_applicable():
    # FR04
    order = Order()
    item = Item(name="DisplayFinal", price=Decimal("220.00"), quantity=1)
    order.add_item(item)
    final_value = order.calculate_total()
    # Final order value for 220.00 with 10% discount should be 198.00
    assert final_value == Decimal("198.00")


# FR05 – The system must raise an exception in case of a failure (explicit example: invalid item present)
def test_fr05_system_raises_exception_when_adding_invalid_item_then_calculating():
    # FR05
    order = Order()
    # Create an item that violates BR02 (quantity 0)
    invalid_item = Item(name="Bad", price=Decimal("10.00"), quantity=0)
    with pytest.raises(Exception):
        order.add_item(invalid_item)