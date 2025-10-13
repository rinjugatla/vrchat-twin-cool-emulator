"""
合法手判定ロジック
手札のカードが場に出せるかどうかを判定する
"""

from typing import List, Tuple, Optional
from ..models.card import Card
from ..models.hand import Hand
from ..models.field import Field


class MoveValidator:
    """
    合法手（カードを出せるか）を判定するクラス
    
    ルール:
    - スロットが空の場合: 任意のカードを出せる
    - スロットにカードがある場合: トップカードと同じスートまたは同じ数値のカードのみ出せる
    """
    
    @staticmethod
    def can_play_card(card: Card, top_card: Optional[Card]) -> bool:
        """
        指定したカードが場に出せるかどうかを判定
        
        Args:
            card: 出したいカード
            top_card: 場のトップカード（Noneの場合はスロットが空）
            
        Returns:
            出せる場合True、出せない場合False
        """
        # スロットが空の場合は任意のカードを出せる
        if top_card is None:
            return True
        
        # 同じスートまたは同じ数値の場合は出せる
        return card.suit == top_card.suit or card.value == top_card.value
    
    @staticmethod
    def get_valid_moves(hand: Hand, field: Field) -> List[Tuple[Card, int]]:
        """
        現在の手札と場の状態から、出せる全ての合法手を取得
        
        Args:
            hand: 手札
            field: 場
            
        Returns:
            (カード, スロット番号)のタプルのリスト
            例: [(Card(A, 5), 1), (Card(B, 3), 2)]
        """
        valid_moves = []
        hand_cards = hand.get_cards()
        
        for card in hand_cards:
            # スロット1に出せるかチェック
            top_card_1 = field.get_top_card(1)
            if MoveValidator.can_play_card(card, top_card_1):
                valid_moves.append((card, 1))
            
            # スロット2に出せるかチェック
            top_card_2 = field.get_top_card(2)
            if MoveValidator.can_play_card(card, top_card_2):
                # 既にスロット1に追加されている場合は、スロット2にも追加
                # （同じカードを2つのスロットのいずれかに出せる場合）
                if (card, 1) in valid_moves:
                    # 重複を避けるため、別のタプルとして追加
                    valid_moves.append((card, 2))
                else:
                    valid_moves.append((card, 2))
        
        return valid_moves
    
    @staticmethod
    def has_valid_move(hand: Hand, field: Field) -> bool:
        """
        現在の手札と場の状態から、出せるカードがあるかどうかを判定
        
        Args:
            hand: 手札
            field: 場
            
        Returns:
            出せるカードがある場合True、ない場合False（ゲーム終了）
        """
        return len(MoveValidator.get_valid_moves(hand, field)) > 0
