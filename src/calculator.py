"""Expense and split calculation logic."""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List

CENT = Decimal("0.01")


def calculate_total(expenses: List[Dict[str, Any]]) -> Decimal:
    """Calculate the total of all expense amounts."""
    total = Decimal("0.00")
    for item in expenses:
        if not isinstance(item, dict) or "amount" not in item:
            raise ValueError(f"Malformed expense record (missing 'amount'): {item}")
        try:
            amount = Decimal(str(item["amount"]))
        except Exception as e:
            raise ValueError(f"Invalid monetary amount in record: {item}") from e
        if amount < Decimal("0.00"):
            raise ValueError(f"Expense amount cannot be negative: {amount}")
        total += amount
    return total.quantize(CENT, rounding=ROUND_HALF_UP)


class SplitStrategy(ABC):
    """Abstract base strategy for splitting expenses among participants."""

    @abstractmethod
    def split(self, total: Decimal, participants: List[str]) -> Dict[str, Decimal]:
        """Compute individual shares for the participants."""
        pass


class EqualSplitStrategy(SplitStrategy):
    """Splits the total evenly across all participants, conserving all pennies."""

    def split(self, total: Decimal, participants: List[str]) -> Dict[str, Decimal]:
        n = len(participants)
        base_share = (total / Decimal(n)).quantize(CENT, rounding=ROUND_HALF_UP)
        result = {p: base_share for p in participants}

        allocated = sum(result.values())
        remainder = total - allocated
        if remainder != Decimal("0.00"):
            cents_count = int(remainder / CENT)
            step = CENT if cents_count > 0 else -CENT
            for i in range(abs(cents_count)):
                p = participants[i % n]
                result[p] += step

        return result


class WeightedDoubleFirstStrategy(SplitStrategy):
    """The first participant pays two shares, others pay one share, conserving pennies."""

    def split(self, total: Decimal, participants: List[str]) -> Dict[str, Decimal]:
        n = len(participants)
        total_shares = Decimal(n + 1)
        base_share = (total / total_shares).quantize(CENT, rounding=ROUND_HALF_UP)
        double_share = (base_share * 2).quantize(CENT, rounding=ROUND_HALF_UP)

        result = {}
        for idx, p in enumerate(participants):
            if idx == 0:
                result[p] = double_share
            else:
                result[p] = base_share

        allocated = sum(result.values())
        remainder = total - allocated
        if remainder != Decimal("0.00"):
            cents_count = int(remainder / CENT)
            step = CENT if cents_count > 0 else -CENT
            for i in range(abs(cents_count)):
                p = participants[i % n]
                result[p] += step

        return result


STRATEGIES: Dict[str, SplitStrategy] = {
    "equal": EqualSplitStrategy(),
    "weighted_double_first": WeightedDoubleFirstStrategy(),
}


def split_expenses(
    total: Decimal,
    participants: List[str],
    mode: str = "equal",
) -> Dict[str, Decimal]:
    """Split the total amount among participants based on the chosen mode.

    Supported modes:
    - 'equal': splits evenly across all participants.
    - 'weighted_double_first': the first participant pays two shares, others pay one share.
    """
    if not participants:
        raise ValueError("At least one participant is required.")
    if len(participants) != len(set(participants)):
        raise ValueError(
            f"Duplicate participant names are not allowed: {participants}"
        )

    strategy = STRATEGIES.get(mode)
    if not strategy:
        raise ValueError(f"Unknown split mode: {mode}")
    return strategy.split(total, participants)

