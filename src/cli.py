"""Command-line interface for expense-split-cli."""

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

from src.calculator import calculate_total, split_expenses


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Expense tracker and bill-splitting CLI utility."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to JSON file containing expenses.",
    )
    parser.add_argument(
        "--split-by",
        type=str,
        required=True,
        help="Comma-separated list of participant names.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="equal",
        choices=["equal", "weighted_double_first"],
        help="Splitting mode (equal or weighted_double_first). Default: equal.",
    )
    return parser.parse_args(args)


def main():
    args = parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    participants = [p.strip() for p in args.split_by.split(",") if p.strip()]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            expenses = json.load(f)
        if not isinstance(expenses, list):
            print("Error: JSON content must be a list of expense objects.", file=sys.stderr)
            sys.exit(1)

        total = calculate_total(expenses)
        splits = split_expenses(total, participants, mode=args.mode)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Total Expenses: ${total:.2f}")
    print(f"Splitting Mode: {args.mode}")
    print("Individual Shares:")
    for person, amount in splits.items():
        print(f"  - {person}: ${amount:.2f}")


if __name__ == "__main__":
    main()
