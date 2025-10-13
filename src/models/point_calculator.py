"""
ポイント計算ロジック
手札のパターンに基づいてポイントを計算する
"""

from typing import List, Set
from .card import Card


class PointCalculator:
    """
    手札のパターンを検出してポイントを計算するクラス
    """
    
    @staticmethod
    def calculate_points(hand_cards: List[Card]) -> int:
        """
        手札のカードからポイントを計算
        
        Args:
            hand_cards: 手札のカードリスト
            
        Returns:
            獲得ポイント
        """
        if len(hand_cards) < 4:
            return 0
        
        total_points = 0
        
        # 5枚の場合の特別なパターンをチェック
        if len(hand_cards) == 5:
            # 5枚のスートが同じかつ順番に並ぶ（50ポイント）
            if PointCalculator._check_five_same_suit_sequence(hand_cards):
                return 50  # 最高得点なので即座に返す
            # 5枚の数値が同じ（5ポイント）
            elif PointCalculator._check_five_same_value(hand_cards):
                return 5  # 4枚同じのチェックをスキップ
            # 5枚が順番に並ぶ（2ポイント）
            elif PointCalculator._check_five_sequence(hand_cards):
                return 2  # 4枚同じのチェックをスキップ
        
        # 4枚の数値が同じ（1ポイント）
        # 上記の5枚パターンに該当しない場合のみチェック
        if PointCalculator._check_four_same_value(hand_cards):
            total_points += 1
        
        return total_points
    
    @staticmethod
    def _check_four_same_value(cards: List[Card]) -> bool:
        """
        4枚のカードの数値が同じかチェック
        
        Args:
            cards: チェックするカードリスト
            
        Returns:
            4枚同じ数値がある場合True
        """
        if len(cards) < 4:
            return False
        
        value_counts = {}
        for card in cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        
        return any(count >= 4 for count in value_counts.values())
    
    @staticmethod
    def _check_five_sequence(cards: List[Card]) -> bool:
        """
        5枚のカードが順番に並んでいるかチェック（スート問わず）
        
        Args:
            cards: チェックするカードリスト
            
        Returns:
            5枚が連続している場合True
        """
        if len(cards) != 5:
            return False
        
        values = sorted([card.value for card in cards])
        
        # 連続しているかチェック
        for i in range(len(values) - 1):
            if values[i + 1] - values[i] != 1:
                return False
        
        return True
    
    @staticmethod
    def _check_five_same_value(cards: List[Card]) -> bool:
        """
        5枚のカードの数値が同じかチェック
        
        Args:
            cards: チェックするカードリスト
            
        Returns:
            5枚同じ数値の場合True
        """
        if len(cards) != 5:
            return False
        
        first_value = cards[0].value
        return all(card.value == first_value for card in cards)
    
    @staticmethod
    def _check_five_same_suit_sequence(cards: List[Card]) -> bool:
        """
        5枚のカードのスートが同じかつ順番に並んでいるかチェック
        
        Args:
            cards: チェックするカードリスト
            
        Returns:
            5枚が同じスートで連続している場合True
        """
        if len(cards) != 5:
            return False
        
        # 全て同じスートかチェック
        first_suit = cards[0].suit
        if not all(card.suit == first_suit for card in cards):
            return False
        
        # 順番に並んでいるかチェック
        return PointCalculator._check_five_sequence(cards)
