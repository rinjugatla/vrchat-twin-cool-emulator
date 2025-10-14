"""
観測可能なゲーム状態
プレイヤーから見て実際に知っている情報のみを保持
"""

import copy
from typing import List
from ..models.card import Card
from ..models.hand import Hand
from ..models.field import Field
from ..models.suit import Suit


class ObservableGameState:
    """
    観測可能なゲーム状態（不完全情報）
    
    実際のゲームプレイでプレイヤーが知っている情報:
    - 現在の手札
    - 場の状態
    - これまでに場に出したカード
    - 累積ポイント
    - ターン数
    - 山札の残り枚数
    
    知らない情報:
    - 山札の具体的な順番
    - 除外された10枚のカード
    """
    
    def __init__(self):
        """観測可能状態の初期化"""
        self.hand: Hand = Hand()
        self.field: Field = Field()
        self.played_cards: List[Card] = []  # 場に出したカード
        self.total_points: int = 0
        self.turn_count: int = 0
        self.remaining_deck_size: int = 65  # 70枚 - 初期手札5枚
        self.excluded_cards_count: int = 10  # ゲーム開始時に除外（固定）
    
    @staticmethod
    def from_game_state(game_state, played_cards: List[Card]) -> 'ObservableGameState':
        """
        既存のGameStateから観測可能状態を構築
        
        Args:
            game_state: 完全情報のGameState
            played_cards: これまでに場に出したカード
        
        Returns:
            ObservableGameState
        """
        obs = ObservableGameState()
        obs.hand = copy.deepcopy(game_state.get_hand())
        obs.field = copy.deepcopy(game_state.get_field())
        obs.played_cards = played_cards.copy()
        obs.total_points = game_state.get_total_points()
        obs.turn_count = game_state.turn_count
        obs.remaining_deck_size = game_state.get_deck().remaining_count()
        return obs
    
    def get_hand(self) -> Hand:
        """手札を取得"""
        return self.hand
    
    def get_field(self) -> Field:
        """場を取得"""
        return self.field
    
    def get_played_cards(self) -> List[Card]:
        """場に出したカードのリストを取得"""
        return self.played_cards.copy()
    
    def get_total_points(self) -> int:
        """累積ポイントを取得"""
        return self.total_points
    
    def get_unknown_cards(self) -> List[Card]:
        """
        未出現カード（山札 + 除外10枚）を取得
        
        Returns:
            全80枚 - (手札 + 場に出したカード)
        """
        all_cards = self._get_all_80_cards()
        
        # 手札と既出カードを除外
        hand_cards = self.hand.get_cards()
        known_cards = hand_cards + self.played_cards
        
        unknown_cards = [c for c in all_cards if c not in known_cards]
        return unknown_cards
    
    def get_deck_candidates(self) -> List[Card]:
        """
        山札の候補カード（除外10枚を含む未出現カード）を取得
        get_unknown_cards()と同じだが、意味的に明確にするためのエイリアス
        
        Returns:
            山札の可能性があるカード
        """
        return self.get_unknown_cards()
    
    @staticmethod
    def _get_all_80_cards() -> List[Card]:
        """全80枚のカードを生成"""
        all_cards = []
        for suit in Suit:
            for value in range(1, 11):
                all_cards.append(Card(suit, value))
        return all_cards
    
    def copy(self) -> 'ObservableGameState':
        """観測可能状態のコピーを作成"""
        obs = ObservableGameState()
        obs.hand = copy.deepcopy(self.hand)
        obs.field = copy.deepcopy(self.field)
        obs.played_cards = self.played_cards.copy()
        obs.total_points = self.total_points
        obs.turn_count = self.turn_count
        obs.remaining_deck_size = self.remaining_deck_size
        obs.excluded_cards_count = self.excluded_cards_count
        return obs
    
    def __repr__(self) -> str:
        return (
            f"ObservableGameState("
            f"turn={self.turn_count}, "
            f"hand={len(self.hand.get_cards())}, "
            f"played={len(self.played_cards)}, "
            f"deck_remaining={self.remaining_deck_size}, "
            f"points={self.total_points})"
        )
