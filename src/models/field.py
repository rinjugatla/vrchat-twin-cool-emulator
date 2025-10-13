"""
フィールドクラスの定義
場には2つの独立したスロット（カードの山）が存在する
"""

from typing import Optional
from .card import Card
from .field_slot import FieldSlot


class Field:
    """
    場（2つのスロット）を表すクラス
    """
    
    def __init__(self):
        """場の初期化（2つのスロットを作成）"""
        self._slot1 = FieldSlot()
        self._slot2 = FieldSlot()
    
    def get_slot(self, slot_number: int) -> FieldSlot:
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
    
    def get_slot_count(self, slot_number: int) -> int:
        """
        指定したスロットのカード枚数を取得
        
        Args:
            slot_number: スロット番号（1 or 2）
            
        Returns:
            スロットのカード枚数
        """
        slot = self.get_slot(slot_number)
        return slot.count()
    
    def total_cards_count(self) -> int:
        """
        場に出された全カードの枚数を返す
        
        Returns:
            全カードの枚数
        """
        return self._slot1.count() + self._slot2.count()
    
    def get_all_cards(self, slot_number: int):
        """
        指定したスロットの全カードを取得
        
        Args:
            slot_number: スロット番号（1 or 2）
            
        Returns:
            カードのリスト
        """
        slot = self.get_slot(slot_number)
        return slot.get_all_cards()
    
    def __str__(self) -> str:
        return f"Field(Slot1: {self._slot1}, Slot2: {self._slot2})"
