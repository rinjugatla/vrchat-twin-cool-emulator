"""
フィールドスロットクラスの定義
場の1つのスロット（カードの山）
"""

from typing import Optional, List
from .card import Card


class FieldSlot:
    """
    場の1つのスロット（カードの山）を表すクラス
    """
    
    def __init__(self):
        """スロットの初期化"""
        self._cards: List[Card] = []
    
    def place_card(self, card: Card):
        """
        カードをスロットに置く（一番上に重ねる）
        
        Args:
            card: 置くカード
        """
        self._cards.append(card)
    
    def get_top_card(self) -> Optional[Card]:
        """
        スロットの一番上のカードを取得
        
        Returns:
            一番上のカード。スロットが空の場合はNone
        """
        if len(self._cards) > 0:
            return self._cards[-1]
        return None
    
    def is_empty(self) -> bool:
        """
        スロットが空かどうかを判定
        
        Returns:
            空の場合True
        """
        return len(self._cards) == 0
    
    def count(self) -> int:
        """
        スロットに置かれたカードの枚数を返す
        
        Returns:
            カードの枚数
        """
        return len(self._cards)
    
    def get_all_cards(self) -> List[Card]:
        """
        スロットの全カードを取得（コピー）
        
        Returns:
            カードのリスト
        """
        return self._cards.copy()
    
    def __str__(self) -> str:
        if self.is_empty():
            return "FieldSlot(empty)"
        return f"FieldSlot(top: {self.get_top_card()}, count: {self.count()})"
