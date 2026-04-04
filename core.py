from enum import IntEnum
from dataclasses import dataclass

class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

class Rank(IntEnum):
    TWO = 2; THREE = 3; FOUR = 4; FIVE = 5; SIX = 6
    SEVEN = 7; EIGHT = 8; NINE = 9; TEN = 10; JACK = 11
    QUEEN = 12; KING = 13; ACE = 14

class Suit(IntEnum):
    CLUBS = 1; DIAMONDS = 2; HEARTS = 3; SPADES = 4

@dataclass(slots=True)
class Card:
    rank: Rank
    suit: Suit

class Evaluator:
    """High-performance 5-card poker hand evaluator."""
    __slots__ = ()      # Class is stateless
    _RANK_BITS = 4      # 2^4 = 16 > max rank (14)
    _HAND_BITS = 20     # 5 cards * 4 bits = 20 bits for kickers/ranks

    @classmethod
    def evaluate(cls, cards: list[Card]) -> tuple[HandType, int]:
        if len(cards) != 5:
            raise ValueError("Exactly 5 cards required")

        # 1. Extract ranks & detect flush in a single pass
        ranks = [c.rank for c in cards]
        ranks.sort(reverse=True)
        suits = {c.suit for c in cards}
        is_flush = len(suits) == 1

        # 2. Count frequencies efficiently
        counts = {}
        for r in ranks:
            counts[r] = counts.get(r, 0) + 1

        # 3. Group by (count DESC, rank DESC) for deterministic tie-breaking
        groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        count_pattern = [g[1] for g in groups]
        rank_groups = [g[0] for g in groups]

        # 4. Straight detection
        is_straight = False
        straight_high = 0
        if len(count_pattern) == 5:  # All ranks unique
            # Use sorted ranks for straight detection, not rank_groups order
            unique_ranks_sorted_desc = sorted(ranks, reverse=True)
            if unique_ranks_sorted_desc[0] - unique_ranks_sorted_desc[4] == 4:
                is_straight = True
                straight_high = unique_ranks_sorted_desc[0]
            elif set(ranks) == {Rank.ACE, Rank.FIVE, Rank.FOUR, Rank.THREE, Rank.TWO}:
                is_straight = True
                straight_high = Rank.FIVE  # 5-high straight (wheel)

        # 5. Hand type determination & value packing
        if is_flush and is_straight:
            ht = HandType.ROYAL_FLUSH if straight_high == Rank.ACE else HandType.STRAIGHT_FLUSH
            return ht, cls._pack(ht, straight_high)

        pattern = tuple(count_pattern)
        if pattern == (4, 1):
            return HandType.FOUR_OF_KIND, cls._pack(HandType.FOUR_OF_KIND, rank_groups[0], rank_groups[1])
        if pattern == (3, 2):
            return HandType.FULL_HOUSE, cls._pack(HandType.FULL_HOUSE, rank_groups[0], rank_groups[1])
        if is_flush:
            # Pass actual ranks in correct order, not rank_groups
            return HandType.FLUSH, cls._pack(HandType.FLUSH, *ranks)
        if is_straight:
            return HandType.STRAIGHT, cls._pack(HandType.STRAIGHT, straight_high)
        if pattern == (3, 1, 1):
            return HandType.THREE_OF_KIND, cls._pack(HandType.THREE_OF_KIND, rank_groups[0], rank_groups[1], rank_groups[2])
        if pattern == (2, 2, 1):
            return HandType.TWO_PAIR, cls._pack(HandType.TWO_PAIR, rank_groups[0], rank_groups[1], rank_groups[2])
        if pattern == (2, 1, 1, 1):
            return HandType.ONE_PAIR, cls._pack(HandType.ONE_PAIR, rank_groups[0], rank_groups[1], rank_groups[2], rank_groups[3])

        return HandType.HIGH_CARD, cls._pack(HandType.HIGH_CARD, *ranks)

    @staticmethod
    def _pack(hand_type: HandType, *ranks: int) -> int:
        """
        Pack hand type and ranks into a single comparable 64-bit integer.
        Higher bits = hand type, lower bits = ranks in descending importance.
        """
        val = hand_type << Evaluator._HAND_BITS
        for r in ranks:
            val = (val << Evaluator._RANK_BITS) | int(r)
        return val