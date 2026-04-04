import unittest
from core import Evaluator, Card, Rank, Suit, HandType

class TestPokerHands(unittest.TestCase):
    """Basic poker hand detection tests, 10 essential cases."""
    
    def setUp(self):
        """Helper method to create cards easily."""
        def card(rank: Rank, suit: Suit) -> Card:
            return Card(rank, suit)
        self.card = card
    
    def test_royal_flush(self):
        """Royal Flush: A♠ K♠ Q♠ J♠ 10♠"""
        hand = [
            self.card(Rank.ACE, Suit.SPADES),
            self.card(Rank.KING, Suit.SPADES),
            self.card(Rank.QUEEN, Suit.SPADES),
            self.card(Rank.JACK, Suit.SPADES),
            self.card(Rank.TEN, Suit.SPADES),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.ROYAL_FLUSH)
    
    def test_straight_flush(self):
        """Straight Flush: 9♥ 8♥ 7♥ 6♥ 5♥"""
        hand = [
            self.card(Rank.NINE, Suit.HEARTS),
            self.card(Rank.EIGHT, Suit.HEARTS),
            self.card(Rank.SEVEN, Suit.HEARTS),
            self.card(Rank.SIX, Suit.HEARTS),
            self.card(Rank.FIVE, Suit.HEARTS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.STRAIGHT_FLUSH)
    
    def test_four_of_a_kind(self):
        """Four of a Kind: 9♣ 9♦ 9♥ 9♠ 2♣"""
        hand = [
            self.card(Rank.NINE, Suit.CLUBS),
            self.card(Rank.NINE, Suit.DIAMONDS),
            self.card(Rank.NINE, Suit.HEARTS),
            self.card(Rank.NINE, Suit.SPADES),
            self.card(Rank.TWO, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.FOUR_OF_KIND)
    
    def test_full_house(self):
        """Full House: 10♣ 10♦ 10♥ 4♠ 4♣"""
        hand = [
            self.card(Rank.TEN, Suit.CLUBS),
            self.card(Rank.TEN, Suit.DIAMONDS),
            self.card(Rank.TEN, Suit.HEARTS),
            self.card(Rank.FOUR, Suit.SPADES),
            self.card(Rank.FOUR, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.FULL_HOUSE)
    
    def test_flush(self):
        """Flush: A♦ J♦ 7♦ 4♦ 2♦"""
        hand = [
            self.card(Rank.ACE, Suit.DIAMONDS),
            self.card(Rank.JACK, Suit.DIAMONDS),
            self.card(Rank.SEVEN, Suit.DIAMONDS),
            self.card(Rank.FOUR, Suit.DIAMONDS),
            self.card(Rank.TWO, Suit.DIAMONDS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.FLUSH)
    
    def test_straight(self):
        """Straight: 8♣ 7♦ 6♥ 5♠ 4♣"""
        hand = [
            self.card(Rank.EIGHT, Suit.CLUBS),
            self.card(Rank.SEVEN, Suit.DIAMONDS),
            self.card(Rank.SIX, Suit.HEARTS),
            self.card(Rank.FIVE, Suit.SPADES),
            self.card(Rank.FOUR, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.STRAIGHT)
    
    def test_three_of_a_kind(self):
        """Three of a Kind: Q♣ Q♦ Q♥ 5♠ 2♣"""
        hand = [
            self.card(Rank.QUEEN, Suit.CLUBS),
            self.card(Rank.QUEEN, Suit.DIAMONDS),
            self.card(Rank.QUEEN, Suit.HEARTS),
            self.card(Rank.FIVE, Suit.SPADES),
            self.card(Rank.TWO, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.THREE_OF_KIND)
    
    def test_two_pair(self):
        """Two Pair: J♣ J♦ 8♥ 8♠ 3♣"""
        hand = [
            self.card(Rank.JACK, Suit.CLUBS),
            self.card(Rank.JACK, Suit.DIAMONDS),
            self.card(Rank.EIGHT, Suit.HEARTS),
            self.card(Rank.EIGHT, Suit.SPADES),
            self.card(Rank.THREE, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.TWO_PAIR)
    
    def test_one_pair(self):
        """One Pair: 7♣ 7♦ 5♥ 4♠ 2♣"""
        hand = [
            self.card(Rank.SEVEN, Suit.CLUBS),
            self.card(Rank.SEVEN, Suit.DIAMONDS),
            self.card(Rank.FIVE, Suit.HEARTS),
            self.card(Rank.FOUR, Suit.SPADES),
            self.card(Rank.TWO, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.ONE_PAIR)
    
    def test_high_card(self):
        """High Card: A♣ K♦ 10♥ 6♠ 3♣"""
        hand = [
            self.card(Rank.ACE, Suit.CLUBS),
            self.card(Rank.KING, Suit.DIAMONDS),
            self.card(Rank.TEN, Suit.HEARTS),
            self.card(Rank.SIX, Suit.SPADES),
            self.card(Rank.THREE, Suit.CLUBS),
        ]
        hand_type, strength = Evaluator.evaluate(hand)
        self.assertEqual(hand_type, HandType.HIGH_CARD)

if __name__ == '__main__':
    unittest.main()