"""
hand.pyのテスト
"""

import unittest
from src.models.hand import Hand
from src.models.card import Card
from src.models.suit import Suit


class TestHand(unittest.TestCase):
    """Handクラスのテスト"""
    
    def test_hand_initialization(self):
        """手札の初期化テスト"""
        hand = Hand()
        self.assertEqual(hand.count(), 0)
        self.assertTrue(hand.is_empty())
    
    def test_hand_add_card(self):
        """手札にカードを追加するテスト"""
        hand = Hand()
        card = Card(Suit.SUIT_A, 5)
        hand.add_card(card)
        
        self.assertEqual(hand.count(), 1)
        self.assertFalse(hand.is_empty())
        self.assertIn(card, hand.get_cards())
    
    def test_hand_add_multiple_cards(self):
        """複数のカードを追加するテスト"""
        hand = Hand()
        card1 = Card(Suit.SUIT_A, 1)
        card2 = Card(Suit.SUIT_B, 2)
        card3 = Card(Suit.SUIT_C, 3)
        
        hand.add_card(card1)
        hand.add_card(card2)
        hand.add_card(card3)
        
        self.assertEqual(hand.count(), 3)
        cards = hand.get_cards()
        self.assertIn(card1, cards)
        self.assertIn(card2, cards)
        self.assertIn(card3, cards)
    
    def test_hand_remove_card_success(self):
        """手札からカードを削除するテスト（成功）"""
        hand = Hand()
        card = Card(Suit.SUIT_D, 7)
        hand.add_card(card)
        
        result = hand.remove_card(card)
        self.assertTrue(result)
        self.assertEqual(hand.count(), 0)
        self.assertTrue(hand.is_empty())
    
    def test_hand_remove_card_failure(self):
        """手札からカードを削除するテスト（失敗：存在しないカード）"""
        hand = Hand()
        card1 = Card(Suit.SUIT_E, 4)
        card2 = Card(Suit.SUIT_F, 8)
        hand.add_card(card1)
        
        result = hand.remove_card(card2)
        self.assertFalse(result)
        self.assertEqual(hand.count(), 1)
    
    def test_hand_get_cards_is_copy(self):
        """get_cards()がコピーを返すことのテスト"""
        hand = Hand()
        card = Card(Suit.SUIT_G, 9)
        hand.add_card(card)
        
        cards1 = hand.get_cards()
        cards2 = hand.get_cards()
        
        # 異なるリストオブジェクトである
        self.assertIsNot(cards1, cards2)
        # 内容は同じ
        self.assertEqual(cards1, cards2)
    
    def test_hand_str(self):
        """手札の文字列表現テスト"""
        hand = Hand()
        card1 = Card(Suit.SUIT_A, 1)
        card2 = Card(Suit.SUIT_B, 2)
        hand.add_card(card1)
        hand.add_card(card2)
        
        hand_str = str(hand)
        self.assertIn("A1", hand_str)
        self.assertIn("B2", hand_str)


if __name__ == '__main__':
    unittest.main()
