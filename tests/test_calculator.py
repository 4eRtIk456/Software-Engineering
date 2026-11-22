"""Unit tests for calculator module."""

import unittest
from decimal import Decimal

from src.calculator import (
    calculate_total,
    split_expenses,
    EqualSplitStrategy,
    WeightedDoubleFirstStrategy,
)


class TestCalculator(unittest.TestCase):
    def test_calculate_total_basic(self):
        expenses = [
            {"description": "Groceries", "amount": "45.50", "paid_by": "Alex"},
            {"description": "Dinner", "amount": "60.25", "paid_by": "Sam"},
            {"description": "Snacks", "amount": "14.25", "paid_by": "Alex"},
        ]
        total = calculate_total(expenses)
        self.assertEqual(total, Decimal("120.00"))

    def test_calculate_total_empty(self):
        expenses = []
        total = calculate_total(expenses)
        self.assertEqual(total, Decimal("0.00"))

    def test_split_expenses_equal(self):
        total = Decimal("120.00")
        participants = ["Alex", "Sam"]
        splits = split_expenses(total, participants, mode="equal")
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("60.00"),
                "Sam": Decimal("60.00"),
            },
        )

    def test_split_expenses_equal_three_way(self):
        total = Decimal("90.00")
        participants = ["Alex", "Sam", "Taylor"]
        splits = split_expenses(total, participants, mode="equal")
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("30.00"),
                "Sam": Decimal("30.00"),
                "Taylor": Decimal("30.00"),
            },
        )

    def test_split_expenses_weighted_double_first(self):
        total = Decimal("120.00")
        participants = ["Alex", "Sam"]
        splits = split_expenses(total, participants, mode="weighted_double_first")
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("80.00"),
                "Sam": Decimal("40.00"),
            },
        )

    def test_strategy_weighted_double_first_direct(self):
        strategy = WeightedDoubleFirstStrategy()
        splits = strategy.split(Decimal("120.00"), ["Alex", "Sam"])
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("80.00"),
                "Sam": Decimal("40.00"),
            },
        )

    def test_split_expenses_unknown_mode(self):
        with self.assertRaises(ValueError):
            split_expenses(Decimal("100.00"), ["Alex", "Sam"], mode="invalid_mode")

    def test_split_expenses_equal_penny_conservation(self):
        total = Decimal("100.00")
        participants = ["Alex", "Sam", "Taylor"]
        splits = split_expenses(total, participants, mode="equal")
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("33.34"),
                "Sam": Decimal("33.33"),
                "Taylor": Decimal("33.33"),
            },
        )
        self.assertEqual(sum(splits.values()), total)

    def test_split_expenses_weighted_double_first_penny_conservation(self):
        total = Decimal("100.00")
        participants = ["Alex", "Sam"]
        splits = split_expenses(total, participants, mode="weighted_double_first")
        self.assertEqual(
            splits,
            {
                "Alex": Decimal("66.67"),
                "Sam": Decimal("33.33"),
            },
        )
        self.assertEqual(sum(splits.values()), total)

    def test_split_expenses_empty_participants_raises(self):
        with self.assertRaises(ValueError) as ctx:
            split_expenses(Decimal("100.00"), [], mode="equal")
        self.assertIn("At least one participant is required", str(ctx.exception))

    def test_split_expenses_duplicate_participants_raises(self):
        with self.assertRaises(ValueError) as ctx:
            split_expenses(Decimal("100.00"), ["Alex", "Alex"], mode="equal")
        self.assertIn("Duplicate participant names are not allowed", str(ctx.exception))

    def test_calculate_total_negative_amount_raises(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_total([{"description": "Refund", "amount": "-10.00"}])
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_calculate_total_malformed_record_raises(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_total([{"description": "No amount"}])
        self.assertIn("missing 'amount'", str(ctx.exception))




if __name__ == "__main__":
    unittest.main()
