
"""
Automated Test Cases for E-commerce Order System
Based on formal specifications provided.
"""

from decimal import Decimal
import pytest

# Assuming the module structure based on the class diagram
# These imports would be adjusted based on actual module location
from cases.case02 import Item, Order


class TestBR01OrderMustContainAtLeastOneItem:
    """Tests for BR01: An order must contain at least one item."""

    # BR01 – An order must contain at least one item (violation case)
    def test_order_with_no_items_raises_exception_on_calculate_total(self):
        order = Order()
        with pytest. raises(Exception):
            order.calculate_total()

    # BR01 – An order must contain at least one item (valid case)
    def test_order_with_one_item_is_valid(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")


class TestBR02EachItemMustHaveMinimumQuantityOfOne:
    """Tests for BR02: Each item must have a minimum quantity of 1."""

    # BR02 – Each item must have a minimum quantity of 1 (violation with zero)
    def test_item_with_quantity_zero_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)

    # BR02 – Each item must have a minimum quantity of 1 (violation with negative)
    def test_item_with_negative_quantity_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=-1)

    # BR02 – Each item must have a minimum quantity of 1 (valid case with exactly 1)
    def test_item_with_quantity_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        assert item.quantity == 1

    # BR02 – Each item must have a minimum quantity of 1 (valid case with quantity greater than 1)
    def test_item_with_quantity_greater_than_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=5)
        assert item.quantity == 5


class TestBR03AllItemsMustHavePositivePrice:
    """Tests for BR03: All items must have a positive price."""

    # BR03 – All items must have a positive price (violation with zero)
    def test_item_with_zero_price_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)

    # BR03 – All items must have a positive price (violation with negative)
    def test_item_with_negative_price_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-10.00"), quantity=1)

    # BR03 – All items must have a positive price (valid case)
    def test_item_with_positive_price_is_valid(self):
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        assert item. price == Decimal("0.01")


class TestBR04TotalOrderValueIsSumOfItems:
    """Tests for BR04: The total order value is the sum of the items."""

    # BR04 – The total order value is the sum of the items (single item)
    def test_total_with_single_item_equals_item_value(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("25.00")

    # BR04 – The total order value is the sum of the items (single item with quantity > 1)
    def test_total_with_single_item_multiple_quantity(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=4)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("100.00")

    # BR04 – The total order value is the sum of the items (multiple items)
    def test_total_with_multiple_items_equals_sum_of_all_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("30.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        assert total == Decimal("50.00")

    # BR04 – The total order value is the sum of the items (multiple items with varying quantities)
    def test_total_with_multiple_items_and_quantities(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("15.00"), quantity=3)
        order.add_item(item1)
        order.add_item(item2)
        # Total = (10. 00 * 2) + (15.00 * 3) = 20.00 + 45.00 = 65.00
        total = order.calculate_total()
        assert total == Decimal("65.00")


class TestBR05OrdersAbove200ReceiveTenPercentDiscount:
    """Tests for BR05: Orders above R$ 200 receive a 10% discount."""

    # BR05 – Orders above R$ 200 receive a 10% discount (exactly R$ 200 - no discount)
    def test_order_exactly_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("200.00")

    # BR05 – Orders above R$ 200 receive a 10% discount (just above R$ 200)
    def test_order_above_200_receives_ten_percent_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Discount = 200.01 * 0.10 = 20.001
        # Final = 200.01 - 20.001 = 180.009
        expected = Decimal("200.01") - (Decimal("200.01") * Decimal("0.10"))
        assert total == expected

    # BR05 – Orders above R$ 200 receive a 10% discount (below R$ 200 - no discount)
    def test_order_below_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("199.99"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("199.99")

    # BR05 – Orders above R$ 200 receive a 10% discount (significantly above R$ 200)
    def test_order_significantly_above_200_receives_ten_percent_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("500.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Discount = 500.00 * 0.10 = 50.00
        # Final = 500.00 - 50.00 = 450.00
        assert total == Decimal("450.00")


class TestBR06DiscountMustNotBeAppliedMoreThanOnce: 
    """Tests for BR06: The discount must not be applied more than once."""

    # BR06 – The discount must not be applied more than once
    def test_discount_applied_only_once_on_multiple_calculate_total_calls(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        # First calculation
        total_first = order.calculate_total()
        # Second calculation
        total_second = order.calculate_total()
        # Discount = 300.00 * 0.10 = 30.00
        # Final = 300.00 - 30.00 = 270.00
        expected = Decimal("270.00")
        assert total_first == expected
        assert total_second == expected

    # BR06 – The discount must not be applied more than once (third call)
    def test_discount_applied_only_once_on_three_calculate_total_calls(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        # Multiple calculations
        total_first = order.calculate_total()
        total_second = order. calculate_total()
        total_third = order.calculate_total()
        # Discount = 250.00 * 0.10 = 25.00
        # Final = 250.00 - 25.00 = 225.00
        expected = Decimal("225.00")
        assert total_first == expected
        assert total_second == expected
        assert total_third == expected


class TestFR01CreateOrderWithMultipleItems: 
    """Tests for FR01: Create an order with multiple items."""

    # FR01 – Create an order with multiple items
    def test_create_order_with_two_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("40.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("60.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        assert total == Decimal("100.00")

    # FR01 – Create an order with multiple items (three items)
    def test_create_order_with_three_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        item3 = Item(name="Product C", price=Decimal("30.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        total = order.calculate_total()
        assert total == Decimal("60.00")


class TestFR02CorrectlyCalculateTotal:
    """Tests for FR02: Correctly calculate the total."""

    # FR02 – Correctly calculate the total (simple case)
    def test_calculate_total_correctly_for_single_item(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("75.50"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("75.50")

    # FR02 – Correctly calculate the total (with quantity)
    def test_calculate_total_correctly_with_item_quantity(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("12.50"), quantity=4)
        order.add_item(item)
        total = order.calculate_total()
        # 12.50 * 4 = 50.00
        assert total == Decimal("50.00")

    # FR02 – Correctly calculate the total (multiple items with quantities)
    def test_calculate_total_correctly_for_multiple_items_with_quantities(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("5.00"), quantity=3)
        item2 = Item(name="Product B", price=Decimal("7.50"), quantity=2)
        order.add_item(item1)
        order.add_item(item2)
        # Total = (5.00 * 3) + (7.50 * 2) = 15.00 + 15.00 = 30.00
        total = order.calculate_total()
        assert total == Decimal("30.00")


class TestFR03ApplyDiscountCorrectlyWhenEligible: 
    """Tests for FR03: The system must apply the discount correctly when eligible."""

    # FR03 – The system must apply the discount correctly when eligible
    def test_discount_applied_correctly_for_eligible_order(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("220.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Discount = 220.00 * 0.10 = 22.00
        # Final = 220.00 - 22.00 = 198.00
        assert total == Decimal("198.00")

    # FR03 – The system must not apply discount when not eligible
    def test_discount_not_applied_for_ineligible_order(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("150.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("150.00")


class TestFR04DisplayFinalOrderValue: 
    """Tests for FR04: The system must display the final order value."""

    # FR04 – The system must display the final order value (without discount)
    def test_final_order_value_displayed_without_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("100.00")

    # FR04 – The system must display the final order value (with discount)
    def test_final_order_value_displayed_with_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("400.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Discount = 400.00 * 0.10 = 40.00
        # Final = 400.00 - 40.00 = 360.00
        assert total == Decimal("360.00")


class TestFR05RaiseExceptionOnFailure: 
    """Tests for FR05: The system must raise an exception in case of a failure."""

    # FR05 – The system must raise an exception for empty order
    def test_exception_raised_for_empty_order_on_calculate_total(self):
        order = Order()
        with pytest.raises(Exception):
            order. calculate_total()

    # FR05 – The system must raise an exception for invalid item quantity
    def test_exception_raised_for_item_with_invalid_quantity(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)

    # FR05 – The system must raise an exception for invalid item price
    def test_exception_raised_for_item_with_invalid_price(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-5.00"), quantity=1)


class TestEdgeCases: 
    """Edge case tests based on explicit rules."""

    # BR04/BR05 – Edge case: Total exactly at discount threshold boundary
    def test_order_total_exactly_at_200_boundary_no_discount(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("100.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        assert total == Decimal("200.00")

    # BR04/BR05 – Edge case: Total just above discount threshold with multiple items
    def test_order_total_just_above_200_with_multiple_items_receives_discount(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("100.01"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        # Sum = 200.01
        # Discount = 200.01 * 0.10 = 20.001
        # Final = 200.01 - 20.001 = 180.009
        expected = Decimal("200.01") - (Decimal("200.01") * Decimal("0.10"))
        assert total == expected

    # BR02 – Edge case: Item with exactly quantity 1 (minimum valid)
    def test_item_with_minimum_valid_quantity_one(self):
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order = Order()
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")

    # BR03 – Edge case:  Item with smallest positive price
    def test_item_with_smallest_positive_price(self):
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        order = Order()
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("0.01")
