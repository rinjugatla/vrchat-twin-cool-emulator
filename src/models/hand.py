"""
手札に関するクラスとロジック
"""

from typing import List
from .card import Card


class Hand:
    """
    プレイヤーの手札を表すクラス
    """
    
    def __init__(self):
        """手札の初期化"""
        self._cards: List[Card] = []
    
    def add_card(self, card: Card):
        """
        手札にカードを追加
        
        Args:
            card: 追加するカード
        """
        self._cards.append(card)
    
    def remove_card(self, card: Card) -> bool:
        """
        手札からカードを削除
        
        Args:
            card: 削除するカード
            
        Returns:
            削除に成功した場合True、カードが存在しない場合False
        """
        if card in self._cards:
            self._cards.remove(card)
            return True
        return False
    
    def get_cards(self) -> List[Card]:
        """
        手札のカードリストを取得
        
        Returns:
            カードのリスト（コピー）
        """
        return self._cards.copy()
    
    def count(self) -> int:
        """
        手札の枚数を返す
        
        Returns:
            手札の枚数
        """
        return len(self._cards)
    
    def is_empty(self) -> bool:
        """
        手札が空かどうかを判定
        
        Returns:
            空の場合True
        """
        return len(self._cards) == 0
    
    def __str__(self) -> str:
        return f"Hand({', '.join(str(card) for card in self._cards)})"
