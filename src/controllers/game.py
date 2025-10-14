"""
ゲーム全体のフロー制御
ゲームのメインループとランダムシミュレーション
"""

import random
from typing import Optional, Dict, Any
from .game_state import GameState
from .move_validator import MoveValidator


class Game:
    """
    ゲーム全体のフロー制御を行うクラス
    
    Attributes:
        state: ゲーム状態
        is_finished: ゲームが終了したかどうか
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        ゲームの初期化
        
        Args:
            seed: 乱数シード（テスト用、省略可）
        """
        self.state = GameState(seed=seed)
        self.is_finished = False
        
        if seed is not None:
            random.seed(seed)
    
    def play_turn(self, card_index: int, slot_number: int) -> bool:
        """
        1ターンをプレイ（手動）
        
        Args:
            card_index: 手札のカードのインデックス（0始まり）
            slot_number: 出すスロット番号（1 or 2）
            
        Returns:
            成功した場合True、失敗した場合False
        """
        if self.is_finished:
            return False
        
        hand_cards = self.state.get_hand().get_cards()
        
        if card_index < 0 or card_index >= len(hand_cards):
            return False
        
        card = hand_cards[card_index]
        
        # カードを出せるかチェック
        top_card = self.state.get_field().get_top_card(slot_number)
        if not MoveValidator.can_play_card(card, top_card):
            return False
        
        # カードを出す
        success = self.state.play_card(card, slot_number)
        
        if success:
            # ゲーム終了判定
            if not MoveValidator.has_valid_move(self.state.get_hand(), self.state.get_field()):
                self.is_finished = True
        
        return success
    
    def play_random_turn(self) -> bool:
        """
        1ターンをランダムにプレイ
        
        Returns:
            成功した場合True、失敗した場合（ゲーム終了）False
        """
        if self.is_finished:
            return False
        
        # 合法手を取得
        valid_moves = MoveValidator.get_valid_moves(
            self.state.get_hand(),
            self.state.get_field()
        )
        
        # 合法手がない場合はゲーム終了
        if len(valid_moves) == 0:
            self.is_finished = True
            return False
        
        # ランダムに1つの合法手を選択
        card, slot_number = random.choice(valid_moves)
        
        # カードを出す
        success = self.state.play_card(card, slot_number)
        
        if success:
            # ゲーム終了判定
            if not MoveValidator.has_valid_move(self.state.get_hand(), self.state.get_field()):
                self.is_finished = True
        
        return success
    
    def simulate_random_game(self) -> Dict[str, Any]:
        """
        ゲームをランダムにシミュレートし、最後まで実行
        
        Returns:
            ゲーム結果の辞書
            {
                'cards_played': 場に出したカードの枚数,
                'total_points': 獲得ポイント,
                'turn_count': ターン数,
                'final_hand_size': 最終手札枚数
            }
        """
        while not self.is_finished:
            if not self.play_random_turn():
                break
        
        return self.get_result()
    
    def get_result(self) -> Dict[str, Any]:
        """
        ゲーム結果を取得
        
        Returns:
            ゲーム結果の辞書
        """
        return {
            'cards_played': self.state.get_cards_played_count(),
            'total_points': self.state.get_total_points(),
            'turn_count': self.state.turn_count,
            'final_hand_size': self.state.get_hand().count(),
            'is_finished': self.is_finished
        }
    
    def get_state(self) -> GameState:
        """
        現在のゲーム状態を取得
        
        Returns:
            ゲーム状態
        """
        return self.state
    
    def __str__(self) -> str:
        result = self.get_result()
        return (
            f"Game(\n"
            f"  Finished: {self.is_finished}\n"
            f"  Cards Played: {result['cards_played']}\n"
            f"  Points: {result['total_points']}\n"
            f"  Turns: {result['turn_count']}\n"
            f")"
        )
