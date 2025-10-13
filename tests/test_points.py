"""
points.pyのテスト
"""

import unittest
from src.points import PointCalculator
from src.card import Card, Suit


class TestPointCalculator(unittest.TestCase):
    """PointCalculatorクラスのテスト"""
    
    def test_no_points_empty_hand(self):
        """空の手札でのポイント計算"""
        cards = []
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 0)
    
    def test_no_points_less_than_four_cards(self):
        """4枚未満の手札でのポイント計算"""
        cards = [
            Card(Suit.SUIT_A, 1),
            Card(Suit.SUIT_B, 2),
            Card(Suit.SUIT_C, 3)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 0)
    
    def test_four_same_value(self):
        """4枚の数値が同じ（1ポイント）"""
        cards = [
            Card(Suit.SUIT_A, 5),
            Card(Suit.SUIT_B, 5),
            Card(Suit.SUIT_C, 5),
            Card(Suit.SUIT_D, 5)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 1)
    
    def test_five_sequence(self):
        """5枚が順番に並ぶ（2ポイント）"""
        cards = [
            Card(Suit.SUIT_A, 3),
            Card(Suit.SUIT_B, 4),
            Card(Suit.SUIT_C, 5),
            Card(Suit.SUIT_D, 6),
            Card(Suit.SUIT_E, 7)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 2)
    
    def test_five_sequence_unordered(self):
        """5枚が順番に並ぶ（順不同で入力）"""
        cards = [
            Card(Suit.SUIT_A, 7),
            Card(Suit.SUIT_B, 3),
            Card(Suit.SUIT_C, 5),
            Card(Suit.SUIT_D, 4),
            Card(Suit.SUIT_E, 6)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 2)
    
    def test_five_same_value(self):
        """5枚の数値が同じ（5ポイント）"""
        cards = [
            Card(Suit.SUIT_A, 8),
            Card(Suit.SUIT_B, 8),
            Card(Suit.SUIT_C, 8),
            Card(Suit.SUIT_D, 8),
            Card(Suit.SUIT_E, 8)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 5)
    
    def test_five_same_suit_sequence(self):
        """5枚のスートが同じかつ順番に並ぶ（50ポイント）"""
        cards = [
            Card(Suit.SUIT_A, 2),
            Card(Suit.SUIT_A, 3),
            Card(Suit.SUIT_A, 4),
            Card(Suit.SUIT_A, 5),
            Card(Suit.SUIT_A, 6)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 50)
    
    def test_five_same_suit_not_sequence(self):
        """5枚のスートが同じだが順番に並ばない（ポイントなし）"""
        cards = [
            Card(Suit.SUIT_B, 1),
            Card(Suit.SUIT_B, 3),
            Card(Suit.SUIT_B, 5),
            Card(Suit.SUIT_B, 7),
            Card(Suit.SUIT_B, 9)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 0)
    
    def test_no_pattern_match(self):
        """パターンにマッチしない5枚"""
        cards = [
            Card(Suit.SUIT_A, 1),
            Card(Suit.SUIT_B, 3),
            Card(Suit.SUIT_C, 5),
            Card(Suit.SUIT_D, 7),
            Card(Suit.SUIT_E, 9)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 0)
    
    def test_four_same_value_in_five_cards(self):
        """5枚中4枚が同じ数値（1ポイント）"""
        cards = [
            Card(Suit.SUIT_A, 4),
            Card(Suit.SUIT_B, 4),
            Card(Suit.SUIT_C, 4),
            Card(Suit.SUIT_D, 4),
            Card(Suit.SUIT_E, 9)
        ]
        points = PointCalculator.calculate_points(cards)
        self.assertEqual(points, 1)


if __name__ == '__main__':
    unittest.main()
