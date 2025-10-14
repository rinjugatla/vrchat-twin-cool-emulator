"""
FlexibilityCalculatorクラスのテスト
"""

import unittest
from src.models import Card, Suit
from src.models.hand import Hand
from src.controllers import FlexibilityCalculator


class TestFlexibilityCalculator(unittest.TestCase):
    """FlexibilityCalculatorクラスのテスト"""
    
    def test_calculate_flexibility_score_basic(self):
        """基本的な柔軟性計算"""
        card = Card(Suit.SUIT_A, 5)
        unknown_cards = [
            Card(Suit.SUIT_A, 3),  # 同じスート
            Card(Suit.SUIT_B, 5),  # 同じ数値
            Card(Suit.SUIT_C, 7),  # 無関係
        ]
        
        score = FlexibilityCalculator.calculate_flexibility_score(card, unknown_cards)
        self.assertEqual(score, 2)  # SUIT_A:3 と SUIT_B:5
    
    def test_calculate_flexibility_score_all_compatible(self):
        """全て接続可能な場合"""
        card = Card(Suit.SUIT_A, 5)
        unknown_cards = [
            Card(Suit.SUIT_A, 1),
            Card(Suit.SUIT_A, 2),
            Card(Suit.SUIT_B, 5),
            Card(Suit.SUIT_C, 5),
        ]
        
        score = FlexibilityCalculator.calculate_flexibility_score(card, unknown_cards)
        self.assertEqual(score, 4)
    
    def test_calculate_flexibility_score_none_compatible(self):
        """接続不可能な場合"""
        card = Card(Suit.SUIT_A, 5)
        unknown_cards = [
            Card(Suit.SUIT_B, 3),
            Card(Suit.SUIT_C, 7),
        ]
        
        score = FlexibilityCalculator.calculate_flexibility_score(card, unknown_cards)
        self.assertEqual(score, 0)
    
    def test_calculate_flexibility_score_empty_unknown(self):
        """未知カードが空の場合"""
        card = Card(Suit.SUIT_A, 5)
        unknown_cards = []
        
        score = FlexibilityCalculator.calculate_flexibility_score(card, unknown_cards)
        self.assertEqual(score, 0)
    
    def test_is_compatible_same_suit(self):
        """同じスートで接続可能"""
        card1 = Card(Suit.SUIT_A, 5)
        card2 = Card(Suit.SUIT_A, 3)
        
        self.assertTrue(FlexibilityCalculator._is_compatible(card1, card2))
    
    def test_is_compatible_same_value(self):
        """同じ数値で接続可能"""
        card1 = Card(Suit.SUIT_A, 5)
        card2 = Card(Suit.SUIT_B, 5)
        
        self.assertTrue(FlexibilityCalculator._is_compatible(card1, card2))
    
    def test_is_compatible_neither(self):
        """スートも数値も異なる"""
        card1 = Card(Suit.SUIT_A, 5)
        card2 = Card(Suit.SUIT_B, 3)
        
        self.assertFalse(FlexibilityCalculator._is_compatible(card1, card2))
    
    def test_calculate_all_flexibility_scores(self):
        """手札全体のスコア計算"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 5))
        hand.add_card(Card(Suit.SUIT_B, 3))
        
        unknown_cards = [
            Card(Suit.SUIT_A, 1),  # SUIT_A:5 と接続
            Card(Suit.SUIT_B, 7),  # SUIT_B:3 と接続
            Card(Suit.SUIT_C, 5),  # SUIT_A:5 と接続
            Card(Suit.SUIT_D, 3),  # SUIT_B:3 と接続
        ]
        
        scores = FlexibilityCalculator.calculate_all_flexibility_scores(hand, unknown_cards)
        
        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[Card(Suit.SUIT_A, 5)], 2)  # SUIT_A:1, SUIT_C:5
        self.assertEqual(scores[Card(Suit.SUIT_B, 3)], 2)  # SUIT_B:7, SUIT_D:3
    
    def test_calculate_all_flexibility_scores_empty_hand(self):
        """手札が空の場合"""
        hand = Hand()
        unknown_cards = [Card(Suit.SUIT_A, 1)]
        
        scores = FlexibilityCalculator.calculate_all_flexibility_scores(hand, unknown_cards)
        self.assertEqual(len(scores), 0)
    
    def test_calculate_all_flexibility_scores_empty_unknown(self):
        """未知カードが空の場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 5))
        
        scores = FlexibilityCalculator.calculate_all_flexibility_scores(hand, [])
        self.assertEqual(scores[Card(Suit.SUIT_A, 5)], 0)
    
    def test_evaluate_move_flexibility(self):
        """手を打った後の柔軟性評価"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 5))
        hand.add_card(Card(Suit.SUIT_B, 3))
        hand.add_card(Card(Suit.SUIT_C, 7))
        
        unknown_cards = [
            Card(Suit.SUIT_A, 1),  # SUIT_A:5 と接続
            Card(Suit.SUIT_B, 9),  # SUIT_B:3 と接続
            Card(Suit.SUIT_C, 2),  # SUIT_C:7 と接続
        ]
        
        # SUIT_A:5 を出す場合
        card_to_play = Card(Suit.SUIT_A, 5)
        remaining_flex, card_flex = FlexibilityCalculator.evaluate_move_flexibility(
            card_to_play, 0, hand, unknown_cards
        )
        
        # SUIT_A:5 の柔軟性は1
        self.assertEqual(card_flex, 1)
        
        # 残りの手札 (SUIT_B:3, SUIT_C:7) の柔軟性は 1 + 1 = 2
        self.assertEqual(remaining_flex, 2)
    
    def test_get_card_compatibility_details(self):
        """互換性詳細情報の取得"""
        card = Card(Suit.SUIT_A, 5)
        unknown_cards = [
            Card(Suit.SUIT_A, 1),  # 同じスート
            Card(Suit.SUIT_A, 2),  # 同じスート
            Card(Suit.SUIT_B, 5),  # 同じ数値
            Card(Suit.SUIT_C, 5),  # 同じ数値
            Card(Suit.SUIT_D, 7),  # 無関係
        ]
        
        details = FlexibilityCalculator.get_card_compatibility_details(card, unknown_cards)
        
        self.assertEqual(details['same_suit'], 2)  # SUIT_A:1, SUIT_A:2
        self.assertEqual(details['same_value'], 2)  # SUIT_B:5, SUIT_C:5
        self.assertEqual(details['total'], 4)  # 合計4枚


if __name__ == '__main__':
    unittest.main()
