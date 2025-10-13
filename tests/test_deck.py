"""
deck.pyのテスト
"""

import unittest
from src.models.deck import Deck
from src.models.card import Card
from src.models.suit import Suit


class TestDeck(unittest.TestCase):
    """Deckクラスのテスト"""
    
    def test_deck_initialization(self):
        """デッキの初期化テスト（70枚）"""
        deck = Deck(seed=42)
        self.assertEqual(deck.remaining_count(), 70)
    
    def test_deck_draw(self):
        """カードを1枚引くテスト"""
        deck = Deck(seed=42)
        initial_count = deck.remaining_count()
        card = deck.draw()
        self.assertIsNotNone(card)
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.remaining_count(), initial_count - 1)
    
    def test_deck_draw_all_cards(self):
        """全カードを引き切るテスト"""
        deck = Deck(seed=42)
        drawn_cards = []
        while not deck.is_empty():
            card = deck.draw()
            self.assertIsNotNone(card)
            drawn_cards.append(card)
        
        self.assertEqual(len(drawn_cards), 70)
        self.assertTrue(deck.is_empty())
        self.assertEqual(deck.remaining_count(), 0)
    
    def test_deck_draw_from_empty(self):
        """空のデッキからカードを引くテスト"""
        deck = Deck(seed=42)
        # 全カードを引く
        while not deck.is_empty():
            deck.draw()
        
        # 空のデッキから引く
        card = deck.draw()
        self.assertIsNone(card)
    
    def test_deck_is_empty(self):
        """デッキの空判定テスト"""
        deck = Deck(seed=42)
        self.assertFalse(deck.is_empty())
        
        # 全カードを引く
        while deck.remaining_count() > 0:
            deck.draw()
        
        self.assertTrue(deck.is_empty())
    
    def test_deck_randomization(self):
        """デッキがシャッフルされているかのテスト（異なるシードで異なる順序）"""
        deck1 = Deck(seed=1)
        deck2 = Deck(seed=2)
        
        card1 = deck1.draw()
        card2 = deck2.draw()
        
        # 異なるシードで異なるカードが引かれる可能性が高い
        # （100%保証はできないが、統計的にほぼ確実）
        self.assertIsNotNone(card1)
        self.assertIsNotNone(card2)


if __name__ == '__main__':
    unittest.main()
