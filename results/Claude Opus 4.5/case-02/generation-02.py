
"""
Automated Test Suite for E-commerce Order System
Based on formal specifications provided. 
"""

import pytest
from decimal import Decimal

# Assuming the module is named 'order_system' with classes Item and Order
from cases.case02 import Item, Order


# =============================================================================
# BR01 – An order must contain at least one item
# =============================================================================

class TestBR01OrderMustContainAtLeastOneItem: 
    
    # BR01 – An order must contain at least one item (violation)
    def test_calculate_total_on_empty_order_raises_exception(self):
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()
    
    # BR01 – An order must contain at least one item (valid)
    def test_order_with_one_item_is_valid(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")


# =============================================================================
# BR02 – Each item must have a minimum quantity of 1
# =============================================================================

class TestBR02ItemMinimumQuantity:
    
    # BR02 – Each item must have a minimum quantity of 1 (violation with zero)
    def test_item_with_quantity_zero_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)
    
    # BR02 – Each item must have a minimum quantity of 1 (violation with negative)
    def test_item_with_negative_quantity_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=-1)
    
    # BR02 – Each item must have a minimum quantity of 1 (valid edge case)
    def test_item_with_quantity_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        assert item.quantity == 1
    
    # BR02 – Each item must have a minimum quantity of 1 (valid with quantity greater than one)
    def test_item_with_quantity_greater_than_one_is_valid(self):
        item = Item(name="Product A", price=Decimal("10.00"), quantity=5)
        assert item.quantity == 5


# =============================================================================
# BR03 – All items must have a positive price
# =============================================================================

class TestBR03ItemPositivePrice:
    
    # BR03 – All items must have a positive price (violation with zero)
    def test_item_with_zero_price_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)
    
    # BR03 – All items must have a positive price (violation with negative)
    def test_item_with_negative_price_raises_exception(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-10.00"), quantity=1)
    
    # BR03 – All items must have a positive price (valid)
    def test_item_with_positive_price_is_valid(self):
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        assert item. price == Decimal("0.01")


# =============================================================================
# BR04 – The total order value is the sum of the items
# =============================================================================

class TestBR04TotalOrderValueIsSumOfItems: 
    
    # BR04 – The total order value is the sum of the items (single item)
    def test_total_with_single_item_equals_item_value(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=2)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")
    
    # BR04 – The total order value is the sum of the items (multiple items)
    def test_total_with_multiple_items_equals_sum_of_all_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("30.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=2)
        item3 = Item(name="Product C", price=Decimal("10.00"), quantity=3)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        # 30 + 40 + 30 = 100
        total = order. calculate_total()
        assert total == Decimal("100.00")


# =============================================================================
# BR05 – Orders above R$ 200 receive a 10% discount
# =============================================================================

class TestBR05DiscountForOrdersAbove200:
    
    # BR05 – Orders above R$ 200 receive a 10% discount (order exactly 200 - no discount)
    def test_order_exactly_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("200.00")
    
    # BR05 – Orders above R$ 200 receive a 10% discount (order above 200 - receives discount)
    def test_order_above_200_receives_10_percent_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 200.01 - 10% = 200.01 - 20. 001 = 180.009
        expected = Decimal("200.01") - (Decimal("200.01") * Decimal("0.10"))
        assert total == expected
    
    # BR05 – Orders above R$ 200 receive a 10% discount (order below 200 - no discount)
    def test_order_below_200_does_not_receive_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("199.99"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("199.99")
    
    # BR05 – Orders above R$ 200 receive a 10% discount (higher value order)
    def test_order_300_receives_10_percent_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        total = order. calculate_total()
        # 300 - 10% = 300 - 30 = 270
        assert total == Decimal("270.00")


# =============================================================================
# BR06 – The discount must not be applied more than once
# =============================================================================

class TestBR06DiscountAppliedOnlyOnce:
    
    # BR06 – The discount must not be applied more than once (multiple calculate_total calls)
    def test_discount_not_applied_multiple_times_on_repeated_calculation(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        # 300 - 10% = 270
        first_total = order. calculate_total()
        second_total = order. calculate_total()
        third_total = order. calculate_total()
        assert first_total == Decimal("270.00")
        assert second_total == Decimal("270.00")
        assert third_total == Decimal("270.00")


# =============================================================================
# FR01 – Create an order with multiple items
# =============================================================================

class TestFR01CreateOrderWithMultipleItems: 
    
    # FR01 – Create an order with multiple items (two items)
    def test_create_order_with_two_items(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("75.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order.calculate_total()
        assert total == Decimal("125.00")
    
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


# =============================================================================
# FR02 – Correctly calculate the total
# =============================================================================

class TestFR02CorrectlyCalculateTotal:
    
    # FR02 – Correctly calculate the total (price multiplied by quantity)
    def test_total_calculation_considers_quantity(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("15.00"), quantity=4)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("60.00")
    
    # FR02 – Correctly calculate the total (multiple items with different quantities)
    def test_total_calculation_with_multiple_items_and_quantities(self):
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("5.00"), quantity=3)
        order.add_item(item1)
        order.add_item(item2)
        # (10 * 2) + (5 * 3) = 20 + 15 = 35
        total = order.calculate_total()
        assert total == Decimal("35.00")


# =============================================================================
# FR03 – The system must apply the discount correctly when eligible
# =============================================================================

class TestFR03ApplyDiscountCorrectlyWhenEligible:
    
    # FR03 – The system must apply the discount correctly when eligible (eligible order)
    def test_discount_applied_correctly_on_eligible_order(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 250 - 10% = 250 - 25 = 225
        assert total == Decimal("225.00")
    
    # FR03 – The system must apply the discount correctly when eligible (non-eligible order)
    def test_no_discount_applied_on_non_eligible_order(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("100.00")


# =============================================================================
# FR04 – The system must display the final order value
# =============================================================================

class TestFR04DisplayFinalOrderValue: 
    
    # FR04 – The system must display the final order value (without discount)
    def test_calculate_total_returns_final_value_without_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("150.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("150.00")
    
    # FR04 – The system must display the final order value (with discount)
    def test_calculate_total_returns_final_value_with_discount(self):
        order = Order()
        item = Item(name="Product A", price=Decimal("400.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 400 - 10% = 400 - 40 = 360
        assert total == Decimal("360.00")


# =============================================================================
# FR05 – The system must raise an exception in case of a failure
# =============================================================================

class TestFR05RaiseExceptionOnFailure:
    
    # FR05 – The system must raise an exception in case of a failure (empty order)
    def test_exception_raised_for_empty_order(self):
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()
    
    # FR05 – The system must raise an exception in case of a failure (invalid item quantity)
    def test_exception_raised_for_item_with_invalid_quantity(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)
    
    # FR05 – The system must raise an exception in case of a failure (invalid item price)
    def test_exception_raised_for_item_with_invalid_price(self):
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-5.00"), quantity=1)
