"""
ゲーム状態管理
現在のゲーム状態（手札、場、山札、ポイント）を管理する
"""

import copy
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
        played_cards: 場に出したカード（IS-MCTS用）
    """
    
    def __init__(self, seed: Optional[int] = None, excluded_cards: Optional[List[Card]] = None, 
                 initial_hand: Optional[List[Card]] = None):
        """
        ゲーム状態の初期化
        
        Args:
            seed: 乱数シード（テスト用、省略可）
            excluded_cards: 除外するカードのリスト（10枚）。Noneの場合はランダムに10枚除外
            initial_hand: 初期手札のリスト（5枚）。Noneの場合は山札からランダムに5枚配布
        """
        self.deck = Deck(seed=seed, excluded_cards=excluded_cards)
        self.hand = Hand()
        self.field = Field()
        self.total_points = 0
        self.turn_count = 0
        self.played_cards: List[Card] = []  # 場に出したカードの履歴
        
        # 初期手札を配布（5枚）
        self._deal_initial_hand(initial_hand)
        
        # 初期手札のポイントを計算
        self._update_points()
    
    def _deal_initial_hand(self, initial_hand: Optional[List[Card]] = None):
        """
        初期手札を配布（5枚）
        
        Args:
            initial_hand: 初期手札のリスト（5枚）。Noneの場合は山札からランダムに5枚配布
        """
        if initial_hand is not None:
            # 指定された手札を配布
            if len(initial_hand) != 5:
                raise ValueError(f"初期手札は5枚である必要があります: {len(initial_hand)}枚")
            
            # 指定されたカードが山札に含まれているか確認
            remaining_cards = self.deck.get_remaining_cards()
            for card in initial_hand:
                if card not in remaining_cards:
                    raise ValueError(f"初期手札のカードが山札に含まれていません: {card}")
            
            # 山札から指定されたカードを除去して手札に追加
            for card in initial_hand:
                # 山札から該当カードを探して除去
                deck_cards = self.deck.get_remaining_cards()
                if card in deck_cards:
                    # 内部リストから直接削除（通常のdraw()を使わない）
                    self.deck._cards.remove(card)
                    self.hand.add_card(card)
        else:
            # ランダムに配布
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
        
        # 場に出したカードを記録
        self.played_cards.append(card)
        
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
    
    def get_played_cards(self) -> List[Card]:
        """場に出したカードのリストを取得"""
        return self.played_cards.copy()
    
    @staticmethod
    def from_observable_determinization(
        hand: Hand,
        field: Field,
        deck_cards: List[Card],
        excluded_cards: List[Card],
        total_points: int,
        turn_count: int,
        played_cards: Optional[List[Card]] = None
    ) -> 'GameState':
        """
        観測可能状態と決定化から完全なGameStateを構築
        IS-MCTS用の特殊コンストラクタ
        
        Args:
            hand: 手札
            field: 場
            deck_cards: 山札のカード（順序付き）
            excluded_cards: 除外カード10枚
            total_points: 累積ポイント
            turn_count: ターン数
            played_cards: 場に出したカードの履歴
        
        Returns:
            完全なGameState
        """
        # 新しいインスタンスを作成（__init__を呼ばない）
        state = GameState.__new__(GameState)
        
        # Deckを構築
        state.deck = Deck(excluded_cards=excluded_cards)
        state.deck._cards = deck_cards.copy()  # 順序を保持
        
        # その他の属性をディープコピー
        state.hand = copy.deepcopy(hand)
        state.field = copy.deepcopy(field)
        state.total_points = total_points
        state.turn_count = turn_count
        state.played_cards = played_cards.copy() if played_cards else []
        
        return state
    
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
