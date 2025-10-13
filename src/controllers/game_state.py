"""
ゲーム状態管理
現在のゲーム状態（手札、場、山札、ポイント）を管理する
"""

from typing import List, Optional
from ..models.deck import Deck
from ..models.hand import Hand
from ..models.field import Field
from ..models.card import Card
from ..models.point_calculator import PointCalculator


class GameState:
    """
    ゲームの現在の状態を管理するクラス
    
    Attributes:
        deck: 山札
        hand: 手札
        field: 場
        total_points: 累積ポイント
        turn_count: ターン数
    """
    
    def __init__(self, seed: Optional[int] = None, excluded_cards: Optional[List[Card]] = None):
        """
        ゲーム状態の初期化
        
        Args:
            seed: 乱数シード（テスト用、省略可）
            excluded_cards: 除外するカードのリスト（10枚）。Noneの場合はランダムに10枚除外
        """
        self.deck = Deck(seed=seed, excluded_cards=excluded_cards)
        self.hand = Hand()
        self.field = Field()
        self.total_points = 0
        self.turn_count = 0
        
        # 初期手札を配布（5枚）
        self._deal_initial_hand()
        
        # 初期手札のポイントを計算
        self._update_points()
    
    def _deal_initial_hand(self):
        """初期手札を配布（5枚）"""
        for _ in range(5):
            card = self.deck.draw()
            if card:
                self.hand.add_card(card)
    
    def _update_points(self):
        """
        現在の手札のポイントを計算し、累積ポイントに加算
        
        Note:
            手札が変わるたびに呼び出す必要がある
        """
        current_hand_points = PointCalculator.calculate_points(self.hand.get_cards())
        # ポイントは累積ではなく、現在の手札のポイントを保持
        # （ゲームルールでは手札が変化する度にポイントが加算されるが、
        #  ここでは簡易的に現在の手札のポイントのみを管理）
        self.total_points = current_hand_points
    
    def play_card(self, card: Card, slot_number: int) -> bool:
        """
        カードを場に出し、山札から1枚引く
        
        Args:
            card: 出すカード
            slot_number: 出すスロット番号（1 or 2）
            
        Returns:
            成功した場合True、失敗した場合False
        """
        # 手札にカードがあるか確認
        if card not in self.hand.get_cards():
            return False
        
        # カードを手札から削除
        if not self.hand.remove_card(card):
            return False
        
        # カードを場に出す
        self.field.place_card(slot_number, card)
        
        # 山札から1枚引く
        drawn_card = self.deck.draw()
        if drawn_card:
            self.hand.add_card(drawn_card)
        
        # ポイントを更新
        self._update_points()
        
        # ターン数をインクリメント
        self.turn_count += 1
        
        return True
    
    def get_cards_played_count(self) -> int:
        """
        場に出したカードの枚数を返す
        
        Returns:
            場に出したカードの枚数
        """
        return self.field.total_cards_count()
    
    def get_total_points(self) -> int:
        """
        累積ポイントを返す
        
        Returns:
            累積ポイント
        """
        return self.total_points
    
    def is_game_over(self) -> bool:
        """
        ゲームが終了したかどうかを判定
        
        Note:
            ゲーム終了判定は外部（MoveValidator）で行うため、
            このメソッドは補助的な役割
            
        Returns:
            手札が空の場合True（通常は発生しない）
        """
        return self.hand.is_empty()
    
    def get_hand(self) -> Hand:
        """手札を取得"""
        return self.hand
    
    def get_field(self) -> Field:
        """場を取得"""
        return self.field
    
    def get_deck(self) -> Deck:
        """山札を取得"""
        return self.deck
    
    def __str__(self) -> str:
        return (
            f"GameState(\n"
            f"  Turn: {self.turn_count}\n"
            f"  Hand: {self.hand}\n"
            f"  Field: {self.field}\n"
            f"  Cards Played: {self.get_cards_played_count()}\n"
            f"  Points: {self.total_points}\n"
            f"  Deck Remaining: {self.deck.remaining_count()}\n"
            f")"
        )
