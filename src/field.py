"""
場（Field）に関するクラスとロジック
場には2つの独立したスロット（カードの山）が存在する
"""

from typing import Optional, List
from .card import Card


class Slot:
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
            return "Slot(empty)"
        return f"Slot(top: {self.get_top_card()}, count: {self.count()})"


class Field:
    """
    場（2つのスロット）を表すクラス
    """
    
    def __init__(self):
        """場の初期化（2つのスロットを作成）"""
        self._slot1 = Slot()
        self._slot2 = Slot()
    
    def get_slot(self, slot_number: int) -> Slot:
        """
        指定したスロットを取得
        
        Args:
            slot_number: スロット番号（1 or 2）
            
        Returns:
            指定されたスロット
            
        Raises:
            ValueError: slot_numberが1または2以外の場合
        """
        if slot_number == 1:
            return self._slot1
        elif slot_number == 2:
            return self._slot2
        else:
            raise ValueError(f"スロット番号は1または2である必要があります: {slot_number}")
    
    def place_card(self, slot_number: int, card: Card):
        """
        指定したスロットにカードを置く
        
        Args:
            slot_number: スロット番号（1 or 2）
            card: 置くカード
        """
        slot = self.get_slot(slot_number)
        slot.place_card(card)
    
    def get_top_card(self, slot_number: int) -> Optional[Card]:
        """
        指定したスロットの一番上のカードを取得
        
        Args:
            slot_number: スロット番号（1 or 2）
            
        Returns:
            一番上のカード。スロットが空の場合はNone
        """
        slot = self.get_slot(slot_number)
        return slot.get_top_card()
    
    def total_cards_count(self) -> int:
        """
        場に出された全カードの枚数を返す
        
        Returns:
            全カードの枚数
        """
        return self._slot1.count() + self._slot2.count()
    
    def __str__(self) -> str:
        return f"Field(Slot1: {self._slot1}, Slot2: {self._slot2})"
