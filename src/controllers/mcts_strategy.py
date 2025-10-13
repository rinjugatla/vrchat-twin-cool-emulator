"""
戦略クラス
MCTSを使用して最適な手を提案
"""

from typing import Optional, Tuple, Dict, Any
from ..models.card import Card
from .game_state import GameState
from .mcts_engine import MCTSEngine
from .game import Game
from .evaluator import Evaluator
import copy


class MCTSStrategy:
    """
    MCTS戦略を使用してゲームをプレイするクラス
    """
    
    def __init__(
        self,
        num_iterations: int = 1000,
        exploration_weight: float = 1.41,
        verbose: bool = False
    ):
        """
        MCTS戦略の初期化
        
        Args:
            num_iterations: MCTS探索回数（デフォルト: 1000）
            exploration_weight: UCB1の探索重み
            verbose: 詳細ログを出力するか
        """
        self.num_iterations = num_iterations
        self.exploration_weight = exploration_weight
        self.verbose = verbose
        self.engine = MCTSEngine(exploration_weight=exploration_weight)
    
    def get_best_move(self, state: GameState) -> Optional[Tuple[Card, int]]:
        """
        現在の状態から最適な手を取得
        
        Args:
            state: 現在のゲーム状態
        
        Returns:
            最適な手（カード、スロット番号）、または None
        """
        best_move, root = self.engine.search(state, self.num_iterations)
        
        if self.verbose and best_move is not None:
            stats = self.engine.get_statistics(root)
            card, slot = best_move
            print(f"[MCTS] Best move: {card} → Slot {slot}")
            print(f"[MCTS] Visits: {stats['best_move_visits']}/{stats['total_visits']}")
            print(f"[MCTS] Avg reward: {stats['best_move_reward']:.2f}")
        
        return best_move
    
    def play_game(self, initial_state: GameState) -> Dict[str, Any]:
        """
        MCTS戦略を使用してゲーム全体をプレイ
        
        Args:
            initial_state: 初期ゲーム状態
        
        Returns:
            ゲーム結果の辞書
        """
        state = copy.deepcopy(initial_state)
        turn = 0
        
        while True:
            # 最適な手を取得
            best_move = self.get_best_move(state)
            
            if best_move is None:
                # ゲーム終了
                break
            
            card, slot_number = best_move
            
            # 手を実行
            success = state.play_card(card, slot_number)
            
            if not success:
                # 手の実行に失敗（通常は発生しないはず）
                break
            
            turn += 1
            
            if self.verbose:
                print(f"[Turn {turn}] Played {card} to Slot {slot_number}")
        
        # 結果を返す
        result = {
            'cards_played': state.get_cards_played_count(),
            'total_points': state.get_total_points(),
            'turn_count': state.turn_count,
            'final_hand_size': state.get_hand().count()
        }
        
        if self.verbose:
            print(f"[Game Over] Cards: {result['cards_played']}, Points: {result['total_points']}")
        
        return result
    
    def compare_with_random(self, num_games: int = 10, seed: int = 42) -> Dict[str, Any]:
        """
        ランダム戦略とMCTS戦略を比較
        
        Args:
            num_games: 比較するゲーム数
            seed: 乱数シード
        
        Returns:
            比較結果の辞書
        """
        mcts_results = []
        random_results = []
        
        for i in range(num_games):
            # 同じ初期状態を使用
            state_seed = seed + i
            
            # MCTS戦略
            mcts_state = GameState(seed=state_seed)
            mcts_result = self.play_game(mcts_state)
            mcts_results.append(mcts_result)
            
            # ランダム戦略
            random_game = Game(seed=state_seed)
            random_result = random_game.simulate_random_game()
            random_results.append(random_result)
        
        # 統計を計算
        mcts_cards = [r['cards_played'] for r in mcts_results]
        mcts_points = [r['total_points'] for r in mcts_results]
        random_cards = [r['cards_played'] for r in random_results]
        random_points = [r['total_points'] for r in random_results]
        
        return {
            'mcts': {
                'avg_cards': sum(mcts_cards) / len(mcts_cards),
                'max_cards': max(mcts_cards),
                'min_cards': min(mcts_cards),
                'avg_points': sum(mcts_points) / len(mcts_points),
                'max_points': max(mcts_points),
            },
            'random': {
                'avg_cards': sum(random_cards) / len(random_cards),
                'max_cards': max(random_cards),
                'min_cards': min(random_cards),
                'avg_points': sum(random_points) / len(random_points),
                'max_points': max(random_points),
            },
            'improvement': {
                'cards': (sum(mcts_cards) / len(mcts_cards)) - (sum(random_cards) / len(random_cards)),
                'points': (sum(mcts_points) / len(mcts_points)) - (sum(random_points) / len(random_points)),
            }
        }
