"""
情報セット (Information Set)
プレイヤーから見て区別がつかない状態群を識別する
"""

from typing import Optional
from ..models.hand import Hand
from ..models.field import Field
from ..models.card import Card


class InformationSet:
    """
    情報セット
    
    プレイヤーから見て区別がつかない状態の集合を表現する。
    IS-MCTSでは、同じ情報セットに対応するノードは統計を共有する。
    
    情報セットの構成要素:
    - 手札のカード（順序無視）
    - 場のトップカード（2つのスロット）
    - 場に出したカードの枚数（具体的なカードは含めない）
    
    Note:
        設計レビューに基づき、既出カードの具体的なリストではなく
        枚数のみを使用することで、ノード共有の機会を最大化
    """
    
    def __init__(
        self,
        hand: Hand,
        field: Field,
        cards_played_count: int
    ):
        """
        情報セットの初期化
        
        Args:
            hand: 手札
            field: 場
            cards_played_count: 場に出したカードの枚数
        """
        # 手札をソートして順序無視（タプル化でハッシュ可能に）
        # Cardはdataclass(frozen=True)なのでハッシュ可能
        # ソートはスート、値の順で行う
        self.hand_cards = tuple(sorted(
            hand.get_cards(),
            key=lambda card: (card.suit.value, card.value)
        ))
        
        # 場のトップカードのみを保持（スロット番号は1と2）
        self.field_top_slot1 = field.get_top_card(1)
        self.field_top_slot2 = field.get_top_card(2)
        
        # 既出カードの枚数のみ
        self.cards_played_count = cards_played_count
    
    def __hash__(self) -> int:
        """
        情報セットのハッシュ値を計算
        
        辞書のキーとして使用するために必要
        
        Returns:
            ハッシュ値
        """
        return hash((
            self.hand_cards,
            self.field_top_slot1,
            self.field_top_slot2,
            self.cards_played_count
        ))
    
    def __eq__(self, other: object) -> bool:
        """
        情報セットの同一性判定
        
        Args:
            other: 比較対象
        
        Returns:
            同じ情報セットならTrue
        """
        if not isinstance(other, InformationSet):
            return False
        
        return (
            self.hand_cards == other.hand_cards and
            self.field_top_slot1 == other.field_top_slot1 and
            self.field_top_slot2 == other.field_top_slot2 and
            self.cards_played_count == other.cards_played_count
        )
    
    def __repr__(self) -> str:
        """文字列表現"""
        return (
            f"InformationSet("
            f"hand_size={len(self.hand_cards)}, "
            f"slot1_top={self.field_top_slot1}, "
            f"slot2_top={self.field_top_slot2}, "
            f"played={self.cards_played_count})"
        )
    
    def __str__(self) -> str:
        """ユーザー向け文字列表現"""
        return self.__repr__()
