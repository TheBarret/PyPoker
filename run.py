

from core import Evaluator, Card, Rank, Suit


if __name__ == "__main__":
    # Royal Flush
    hand = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.SPADES),
    ]
    
    hand_type, strength = Evaluator.evaluate(hand)
    print(f"Hand: {hand_type.name}, Strength: {strength}")
    
    # Ace-low straight
    hand = [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.FIVE, Suit.HEARTS),
    ]
    
    hand_type, strength = Evaluator.evaluate(hand)
    print(f"Hand: {hand_type.name}, Strength: {strength}")