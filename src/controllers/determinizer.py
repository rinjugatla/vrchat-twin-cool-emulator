"""
決定化生成器 (Determinizer)
観測可能状態から完全なゲーム状態をサンプリングする
"""

import random
from typing import List, Optional
from ..models.card import Card
from ..models.suit import Suit
from .observable_game_state import ObservableGameState
from .game_state import GameState


class Determinizer:
    """
    決定化生成器
    
    不完全情報ゲームにおいて、観測可能な情報から
    完全なゲーム状態（決定化）をサンプリングする。
    
    決定化の手順:
    1. 未出現カード（全80枚 - 手札 - 既出カード）を取得
    2. ランダムに10枚を除外カードとして選択
    3. 残りを山札としてシャッフル
    4. GameStateを構築
    """
    
    # カードプールをクラス変数としてキャッシュ（最適化）
    _all_cards_cache: Optional[List[Card]] = None
    
    @classmethod
    def _get_all_cards(cls) -> List[Card]:
        """
        全80枚のカードを取得（キャッシュ付き）
        
        Returns:
            全80枚のカードリスト
        """
        if cls._all_cards_cache is None:
            cls._all_cards_cache = []
            for suit in Suit:
                for value in range(1, 11):
                    cls._all_cards_cache.append(Card(suit, value))
        return cls._all_cards_cache
    
    @staticmethod
    def create_determinization(
        observable_state: ObservableGameState,
        seed: Optional[int] = None
    ) -> GameState:
        """
        決定化を1つ生成
        
        Args:
            observable_state: 観測可能なゲーム状態
            seed: 乱数シード（テスト用）
        
        Returns:
            完全なGameState
        """
        if seed is not None:
            random.seed(seed)
        
        # 未出現カードを取得
        unplayed_cards = Determinizer._get_unplayed_cards(observable_state)
        
        # ランダムに10枚を除外
        shuffled = unplayed_cards.copy()
        random.shuffle(shuffled)
        
        excluded_cards = shuffled[:10]
        deck_cards = shuffled[10:]
        
        # 山札をさらにシャッフル
        random.shuffle(deck_cards)
        
        # 完全なGameStateを構築
        game_state = GameState.from_observable_determinization(
            hand=observable_state.hand,
            field=observable_state.field,
            deck_cards=deck_cards,
            excluded_cards=excluded_cards,
            total_points=observable_state.total_points,
            turn_count=observable_state.turn_count,
            played_cards=observable_state.played_cards
        )
        
        return game_state
    
    @staticmethod
    def _get_unplayed_cards(observable_state: ObservableGameState) -> List[Card]:
        """
        未出現カード（山札候補 + 除外10枚候補）を取得
        
        Args:
            observable_state: 観測可能なゲーム状態
        
        Returns:
            未出現カードのリスト
        """
        all_cards = Determinizer._get_all_cards()
        
        # 既知のカード（手札 + 既出カード）
        hand_cards = observable_state.hand.get_cards()
        played_cards = observable_state.played_cards
        known_cards = set(hand_cards + played_cards)
        
        # 未出現カード = 全カード - 既知カード
        unplayed_cards = [card for card in all_cards if card not in known_cards]
        
        return unplayed_cards
    
    @staticmethod
    def create_multiple_determinizations(
        observable_state: ObservableGameState,
        count: int,
        seed: Optional[int] = None
    ) -> List[GameState]:
        """
        複数の決定化を生成
        
        Args:
            observable_state: 観測可能なゲーム状態
            count: 生成する決定化の数
            seed: 乱数シード（テスト用）
        
        Returns:
            GameStateのリスト
        """
        if seed is not None:
            random.seed(seed)
        
        determinizations = []
        for _ in range(count):
            det = Determinizer.create_determinization(observable_state)
            determinizations.append(det)
        
        return determinizations
    
    @staticmethod
    def get_unplayed_card_count(observable_state: ObservableGameState) -> int:
        """
        未出現カードの枚数を取得
        
        Args:
            observable_state: 観測可能なゲーム状態
        
        Returns:
            未出現カードの枚数
        """
        return 80 - len(observable_state.hand.get_cards()) - len(observable_state.played_cards)
