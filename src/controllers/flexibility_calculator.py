"""
柔軟性計算器
各カードの「柔軟性スコア」を計算
柔軟性 = 未知の山札で接続可能なカードの数
"""

from typing import List, Dict, Tuple
from ..models.card import Card
from ..models.hand import Hand
from ..models.field import Field
from ..models.suit import Suit


class FlexibilityCalculator:
    """
    カードの柔軟性スコアを計算
    
    柔軟性スコア = 未知の山札の中で、このカードと接続できるカードの数
    接続 = 同じスートまたは同じ数値
    
    柔軟性が高い = 多くのカードと繋げられる = 手札に残す価値が高い
    柔軟性が低い = 繋げられるカードが少ない = 早めに出すべき
    """
    
    @staticmethod
    def calculate_flexibility_score(
        card: Card,
        unknown_cards: List[Card]
    ) -> int:
        """
        1枚のカードの柔軟性スコアを計算
        
        Args:
            card: 評価対象のカード
            unknown_cards: 未知のカード（山札候補）
        
        Returns:
            柔軟性スコア（接続可能なカードの数）
        """
        if not unknown_cards:  # エッジケース: 未知カードが0枚
            return 0
        
        compatible_count = 0
        
        for unknown_card in unknown_cards:
            if FlexibilityCalculator._is_compatible(card, unknown_card):
                compatible_count += 1
        
        return compatible_count
    
    @staticmethod
    def _is_compatible(card1: Card, card2: Card) -> bool:
        """
        2枚のカードが接続可能か判定
        
        Args:
            card1: カード1
            card2: カード2
        
        Returns:
            同じスートまたは同じ数値ならTrue
        """
        return card1.suit == card2.suit or card1.value == card2.value
    
    @staticmethod
    def calculate_all_flexibility_scores(
        hand: Hand,
        unknown_cards: List[Card]
    ) -> Dict[Card, int]:
        """
        手札全体の柔軟性スコアを計算（最適化版）
        
        最適化:
        - 未知カードをスートと数値でインデックス化
        - O(n*m) -> O(n+m) に改善
        
        Args:
            hand: 手札
            unknown_cards: 未知のカード
        
        Returns:
            カード -> 柔軟性スコア のマップ
        """
        if not unknown_cards:
            return {card: 0 for card in hand.get_cards()}
        
        # 未知カードをスートと数値でインデックス化
        by_suit: Dict[Suit, int] = {}
        by_value: Dict[int, int] = {}
        
        for card in unknown_cards:
            by_suit[card.suit] = by_suit.get(card.suit, 0) + 1
            by_value[card.value] = by_value.get(card.value, 0) + 1
        
        # 各手札カードのスコアを計算
        scores = {}
        for card in hand.get_cards():
            # 同じスートのカード数
            suit_count = by_suit.get(card.suit, 0)
            # 同じ数値のカード数
            value_count = by_value.get(card.value, 0)
            
            # 合計（重複は自然に排除される）
            scores[card] = suit_count + value_count
        
        return scores
    
    @staticmethod
    def evaluate_move_flexibility(
        card: Card,
        slot: int,
        hand: Hand,
        unknown_cards: List[Card]
    ) -> Tuple[int, int]:
        """
        ある手を打った後の手札全体の柔軟性を評価
        
        Args:
            card: 出すカード
            slot: 出すスロット
            hand: 現在の手札
            unknown_cards: 未知のカード
        
        Returns:
            (残った手札の合計柔軟性, 出すカードの柔軟性)
        """
        # 出すカードの柔軟性
        card_flexibility = FlexibilityCalculator.calculate_flexibility_score(
            card, unknown_cards
        )
        
        # 残りの手札の柔軟性合計
        remaining_flexibility = 0
        for hand_card in hand.get_cards():
            if hand_card != card:  # 出すカード以外
                remaining_flexibility += FlexibilityCalculator.calculate_flexibility_score(
                    hand_card, unknown_cards
                )
        
        return remaining_flexibility, card_flexibility
    
    @staticmethod
    def get_card_compatibility_details(
        card: Card,
        unknown_cards: List[Card]
    ) -> Dict[str, int]:
        """
        カードの接続性の詳細情報を取得（デバッグ・説明用）
        
        Args:
            card: 対象カード
            unknown_cards: 未知のカード
        
        Returns:
            {
                'same_suit': 同じスートのカード数,
                'same_value': 同じ数値のカード数,
                'total': 合計接続可能数（重複なし）
            }
        """
        same_suit_count = 0
        same_value_count = 0
        total_count = 0
        
        for unknown_card in unknown_cards:
            is_suit_match = card.suit == unknown_card.suit
            is_value_match = card.value == unknown_card.value
            
            if is_suit_match:
                same_suit_count += 1
            if is_value_match:
                same_value_count += 1
            if is_suit_match or is_value_match:
                total_count += 1
        
        return {
            'same_suit': same_suit_count,
            'same_value': same_value_count,
            'total': total_count
        }
