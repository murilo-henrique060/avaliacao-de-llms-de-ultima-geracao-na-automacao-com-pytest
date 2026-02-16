
"""
Automated Test Cases for E-commerce Order System
Based on formal specifications provided.
"""

from decimal import Decimal
import pytest

# Assuming the module is named 'order_system' with classes Item and Order
from cases.case02 import Item, Order


# =============================================================================
# BR01: An order must contain at least one item
# =============================================================================

class TestBR01OrderMustContainAtLeastOneItem: 
    
    # BR01 – An order must contain at least one item (violation:  empty order)
    def test_calculate_total_on_empty_order_raises_exception(self):
        order = Order()
        with pytest. raises(Exception):
            order.calculate_total()
    
    # BR01 – An order must contain at least one item (valid:  one item)
    def test_order_with_one_item_is_valid(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        result = order.calculate_total()
        assert result == Decimal("50.00")


# =============================================================================
# BR02: Each item must have a minimum quantity of 1
# =============================================================================

class TestBR02ItemMinimumQuantityOfOne:
    
    # BR02 – Each item must have a minimum quantity of 1 (violation:  quantity 0)
    def test_item_with_quantity_zero_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)
    
    # BR02 – Each item must have a minimum quantity of 1 (violation: negative quantity)
    def test_item_with_negative_quantity_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=-1)
    
    # BR02 – Each item must have a minimum quantity of 1 (valid:  quantity 1)
    def test_item_with_quantity_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        assert item.quantity == 1
    
    # BR02 – Each item must have a minimum quantity of 1 (valid: quantity greater than 1)
    def test_item_with_quantity_greater_than_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=5)
        assert item.quantity == 5


# =============================================================================
# BR03: All items must have a positive price
# =============================================================================

class TestBR03ItemsMusthavePositivePrice: 
    
    # BR03 – All items must have a positive price (violation: price zero)
    def test_item_with_price_zero_raises_exception(self):
        with pytest. raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)
    
    # BR03 – All items must have a positive price (violation:  negative price)
    def test_item_with_negative_price_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-10.00"), quantity=1)
    
    # BR03 – All items must have a positive price (valid: positive price)
    def test_item_with_positive_price_is_valid(self):
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        assert item. price == Decimal("0.01")


# =============================================================================
# BR04: The total order value is the sum of the items
# =============================================================================

class TestBR04TotalOrderValueIsSumOfItems: 
    
    # BR04 – The total order value is the sum of the items (single item)
    def test_total_with_single_item_equals_item_value(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=1)
        order.add_item(item)
        result = order.calculate_total()
        assert result == Decimal("25.00")
    
    # BR04 – The total order value is the sum of the items (single item with quantity > 1)
    def test_total_with_single_item_multiple_quantity(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=4)
        order.add_item(item)
        result = order.calculate_total()
        assert result == Decimal("100.00")
    
    # BR04 – The total order value is the sum of the items (multiple items)
    def test_total_with_multiple_items_equals_sum(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("30.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        result = order.calculate_total()
        assert result == Decimal("50.00")
    
    # BR04 – The total order value is the sum of the items (multiple items with varying quantities)
    def test_total_with_multiple_items_and_quantities(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=3)
        item2 = Item(name="Product B", price=Decimal("15.00"), quantity=2)
        order.add_item(item1)
        order.add_item(item2)
        # Total: (10 * 3) + (15 * 2) = 30 + 30 = 60
        result = order.calculate_total()
        assert result == Decimal("60.00")


# =============================================================================
# BR05: Orders above R$ 200 receive a 10% discount
# =============================================================================

class TestBR05OrdersAbove200ReceiveDiscount:
    
    # BR05 – Orders above R$ 200 receive a 10% discount (eligible: above 200)
    def test_order_above_200_receives_10_percent_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        result = order.calculate_total()
        # 250 - 10% = 250 - 25 = 225
        assert result == Decimal("225.00")
    
    # BR05 – Orders above R$ 200 receive a 10% discount (not eligible: exactly 200)
    def test_order_exactly_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        result = order. calculate_total()
        assert result == Decimal("200.00")
    
    # BR05 – Orders above R$ 200 receive a 10% discount (not eligible:  below 200)
    def test_order_below_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("199.99"), quantity=1)
        order.add_item(item)
        result = order.calculate_total()
        assert result == Decimal("199.99")
    
    # BR05 – Orders above R$ 200 receive a 10% discount (edge case: just above 200)
    def test_order_just_above_200_receives_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        result = order.calculate_total()
        # 200.01 - 10% = 200.01 - 20. 001 = 180.009
        assert result == Decimal("180.009")


# =============================================================================
# BR06: The discount must not be applied more than once
# =============================================================================

class TestBR06DiscountMustNotBeAppliedMoreThanOnce:
    
    # BR06 – The discount must not be applied more than once (multiple calculate_total calls)
    def test_discount_applied_only_once_on_multiple_calculations(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        # First call
        result1 = order.calculate_total()
        # Second call
        result2 = order.calculate_total()
        # Both should return 270 (300 - 10%), not 243 (270 - 10%)
        assert result1 == Decimal("270.00")
        assert result2 == Decimal("270.00")
    
    # BR06 – The discount must not be applied more than once (third calculation)
    def test_discount_applied_only_once_on_three_calculations(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("400.00"), quantity=1)
        order.add_item(item)
        result1 = order. calculate_total()
        result2 = order.calculate_total()
        result3 = order.calculate_total()
        # All should return 360 (400 - 10%)
        assert result1 == Decimal("360.00")
        assert result2 == Decimal("360.00")
        assert result3 == Decimal("360.00")


# =============================================================================
# FR01: Create an order with multiple items
# =============================================================================

class TestFR01CreateOrderWithMultipleItems: 
    
    # FR01 – Create an order with multiple items
    def test_create_order_with_two_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        result = order. calculate_total()
        assert result == Decimal("30.00")
    
    # FR01 – Create an order with multiple items (three items)
    def test_create_order_with_three_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("15.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("25.00"), quantity=1)
        item3 = Item(name="Product C", price=Decimal("35.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        result = order.calculate_total()
        assert result == Decimal("75.00")


# =============================================================================
# FR02: Correctly calculate the total
# =============================================================================

class TestFR02CorrectlyCalculateTotal:
    
    # FR02 – Correctly calculate the total (simple calculation)
    def test_calculate_total_correctly_simple(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("33.33"), quantity=3)
        order.add_item(item)
        result = order.calculate_total()
        # 33.33 * 3 = 99.99
        assert result == Decimal("99.99")
    
    # FR02 – Correctly calculate the total (complex calculation with multiple items)
    def test_calculate_total_correctly_complex(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("12.50"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("7.75"), quantity=4)
        order.add_item(item1)
        order.add_item(item2)
        # (12.50 * 2) + (7.75 * 4) = 25.00 + 31.00 = 56.00
        result = order.calculate_total()
        assert result == Decimal("56.00")


# =============================================================================
# FR03: The system must apply the discount correctly when eligible
# =============================================================================

class TestFR03ApplyDiscountCorrectlyWhenEligible:
    
    # FR03 – The system must apply the discount correctly when eligible
    def test_apply_discount_correctly_when_above_200(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=3)
        order.add_item(item)
        result = order.calculate_total()
        # 300 - 10% = 270
        assert result == Decimal("270.00")
    
    # FR03 – The system must not apply discount when not eligible
    def test_no_discount_when_below_200(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=3)
        order.add_item(item)
        result = order.calculate_total()
        # 150, no discount
        assert result == Decimal("150.00")


# =============================================================================
# FR04: The system must display the final order value
# =============================================================================

class TestFR04DisplayFinalOrderValue: 
    
    # FR04 – The system must display the final order value (without discount)
    def test_final_order_value_without_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("75.00"), quantity=2)
        order.add_item(item)
        result = order.calculate_total()
        assert result == Decimal("150.00")
    
    # FR04 – The system must display the final order value (with discount)
    def test_final_order_value_with_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("110.00"), quantity=2)
        order.add_item(item)
        result = order.calculate_total()
        # 220 - 10% = 198
        assert result == Decimal("198.00")


# =============================================================================
# FR05: The system must raise an exception in case of a failure
# =============================================================================

class TestFR05RaiseExceptionOnFailure:
    
    # FR05 – The system must raise an exception in case of a failure (empty order)
    def test_exception_raised_for_empty_order(self):
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()
    
    # FR05 – The system must raise an exception in case of a failure (invalid item quantity)
    def test_exception_raised_for_invalid_item_quantity(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)
    
    # FR05 – The system must raise an exception in case of a failure (invalid item price)
    def test_exception_raised_for_invalid_item_price(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-5.00"), quantity=1)
