"""
デッキ（山札）に関するクラスとロジック
"""

import random
from typing import List, Optional
from .card import Card
from .suit import Suit


class Deck:
    """
    デッキ（山札）を表すクラス
    
    初期化時に全80枚のカードを生成し、ランダムに10枚を除外して70枚にする
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        デッキの初期化
        
        Args:
            seed: 乱数シード（テスト用、省略可）
        """
        if seed is not None:
            random.seed(seed)
        
        self._cards: List[Card] = []
        self._excluded_cards: List[Card] = []  # 除外されたカード
        self._initialize_deck()
    
    def _initialize_deck(self):
        """全80枚のカードを生成し、10枚を除外して70枚にする"""
        # 全80枚のカードを生成
        all_cards = []
        for suit in Suit:
            for value in range(1, 11):
                all_cards.append(Card(suit, value))
        
        # シャッフル
        random.shuffle(all_cards)
        
        # 最初の10枚を除外して、残りの70枚を山札とする
        self._excluded_cards = all_cards[:10]  # 除外されたカードを保存
        self._cards = all_cards[10:]
        
        # さらにシャッフル
        random.shuffle(self._cards)
    
    def draw(self) -> Optional[Card]:
        """
        山札から1枚引く
        
        Returns:
            引いたカード。山札が空の場合はNone
        """
        if len(self._cards) > 0:
            return self._cards.pop()
        return None
    
    def remaining_count(self) -> int:
        """
        山札の残り枚数を返す
        
        Returns:
            残り枚数
        """
        return len(self._cards)
    
    def is_empty(self) -> bool:
        """
        山札が空かどうかを判定
        
        Returns:
            空の場合True
        """
        return len(self._cards) == 0
    
    def get_excluded_cards(self) -> List[Card]:
        """
        除外されたカード（初期の10枚）を取得
        
        Returns:
            除外されたカードのリスト
        """
        return self._excluded_cards.copy()
    
    def get_remaining_cards(self) -> List[Card]:
        """
        山札に残っているカードを取得
        
        Returns:
            残っているカードのリスト
        """
        return self._cards.copy()
