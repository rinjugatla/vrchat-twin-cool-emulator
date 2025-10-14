"""
card.pyのテスト
"""

import unittest
from src.models.card import Card
from src.models.suit import Suit


class TestCard(unittest.TestCase):
    """Cardクラスのテスト"""
    
    def test_card_creation_valid(self):
        """正常なカードの生成"""
        card = Card(Suit.SUIT_A, 5)
        self.assertEqual(card.suit, Suit.SUIT_A)
        self.assertEqual(card.value, 5)
    
    def test_card_creation_min_value(self):
        """最小値（1）でのカード生成"""
        card = Card(Suit.SUIT_B, 1)
        self.assertEqual(card.value, 1)
    
    def test_card_creation_max_value(self):
        """最大値（10）でのカード生成"""
        card = Card(Suit.SUIT_C, 10)
        self.assertEqual(card.value, 10)
    
    def test_card_creation_invalid_value_too_low(self):
        """無効な数値（0以下）でのカード生成"""
        with self.assertRaises(ValueError):
            Card(Suit.SUIT_D, 0)
    
    def test_card_creation_invalid_value_too_high(self):
        """無効な数値（11以上）でのカード生成"""
        with self.assertRaises(ValueError):
            Card(Suit.SUIT_E, 11)
    
    def test_card_str(self):
        """カードの文字列表現"""
        card = Card(Suit.SUIT_F, 7)
        self.assertEqual(str(card), "F7")
    
    def test_card_equality(self):
        """カードの等価性"""
        card1 = Card(Suit.SUIT_G, 3)
        card2 = Card(Suit.SUIT_G, 3)
        card3 = Card(Suit.SUIT_H, 3)
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)


if __name__ == '__main__':
    unittest.main()
