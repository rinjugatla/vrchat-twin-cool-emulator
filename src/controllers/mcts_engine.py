"""
MCTS探索エンジン
モンテカルロ木探索のメインロジック
"""

import random
import copy
from typing import Optional, Tuple
from ..models.card import Card
from .game_state import GameState
from .mcts_node import MCTSNode
from .move_validator import MoveValidator
from .evaluator import Evaluator
from .game import Game


class MCTSEngine:
    """
    モンテカルロ木探索エンジン
    
    MCTSの4つのフェーズを実行:
    1. Selection（選択）
    2. Expansion（展開）
    3. Simulation（シミュレーション）
    4. Backpropagation（逆伝播）
    """
    
    def __init__(
        self,
        exploration_weight: float = 1.41,
        simulation_seed: Optional[int] = None
    ):
        """
        MCTS探索エンジンの初期化
        
        Args:
            exploration_weight: UCB1の探索重み（デフォルト: sqrt(2)）
            simulation_seed: シミュレーションの乱数シード（デバッグ用）
        """
        self.exploration_weight = exploration_weight
        self.simulation_seed = simulation_seed
        if simulation_seed is not None:
            random.seed(simulation_seed)
    
    def search(
        self,
        root_state: GameState,
        num_iterations: int = 1000
    ) -> Tuple[Optional[Tuple[Card, int]], MCTSNode]:
        """
        MCTS探索を実行し、最良の手を返す
        
        Args:
            root_state: 探索開始時のゲーム状態
            num_iterations: 探索回数
        
        Returns:
            (最良の手, ルートノード)
        """
        root = MCTSNode(root_state)
        
        for _ in range(num_iterations):
            # 1. Selection: UCB1で最良のノードを選択
            node = self._select(root)
            
            # 2. Expansion: 子ノードを追加
            if not node.is_terminal() and not node.is_fully_expanded():
                node = self._expand(node)
            
            # 3. Simulation: ランダムプレイアウト
            reward = self._simulate(node.state)
            
            # 4. Backpropagation: 報酬を親ノードに伝播
            self._backpropagate(node, reward)
        
        # 最も訪問回数が多い手を返す
        best_move = root.get_best_move()
        return best_move, root
    
    def _select(self, node: MCTSNode) -> MCTSNode:
        """
        Selection: UCB1で最も有望なノードを選択
        
        Args:
            node: 現在のノード
        
        Returns:
            選択されたノード
        """
        while not node.is_terminal():
            if not node.is_fully_expanded():
                # まだ展開できる手がある
                return node
            else:
                # 完全に展開済み → UCB1で最良の子を選択
                node = node.select_best_child(self.exploration_weight)
        
        return node
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """
        Expansion: 未試行の手を1つ選んで子ノードを作成
        
        Args:
            node: 展開するノード
        
        Returns:
            新しく作成された子ノード
        """
        return node.expand()
    
    def _simulate(self, state: GameState) -> float:
        """
        Simulation: ゲーム終了までランダムプレイ
        
        Args:
            state: シミュレーション開始時の状態
        
        Returns:
            報酬値（評価スコア）
        """
        # 状態をコピーして破壊的に変更
        sim_state = copy.deepcopy(state)
        
        # ゲーム終了までランダムにプレイ
        while MoveValidator.has_valid_move(sim_state.get_hand(), sim_state.get_field()):
            valid_moves = MoveValidator.get_valid_moves(
                sim_state.get_hand(),
                sim_state.get_field()
            )
            
            if len(valid_moves) == 0:
                break
            
            # ランダムに手を選択
            card, slot_number = random.choice(valid_moves)
            sim_state.play_card(card, slot_number)
        
        # 結果を評価
        result = {
            'cards_played': sim_state.get_cards_played_count(),
            'total_points': sim_state.get_total_points()
        }
        
        reward = Evaluator.evaluate(result)
        return reward
    
    def _backpropagate(self, node: Optional[MCTSNode], reward: float):
        """
        Backpropagation: 報酬をルートまで伝播
        
        Args:
            node: 開始ノード
            reward: 報酬値
        """
        while node is not None:
            node.update(reward)
            node = node.parent
    
    def get_statistics(self, root: MCTSNode) -> dict:
        """
        探索の統計情報を取得
        
        Args:
            root: ルートノード
        
        Returns:
            統計情報の辞書
        """
        if len(root.children) == 0:
            return {
                'total_visits': root.visits,
                'num_children': 0,
                'best_move': None,
                'best_move_visits': 0,
                'best_move_reward': 0.0
            }
        
        best_child = max(root.children, key=lambda c: c.visits)
        
        return {
            'total_visits': root.visits,
            'num_children': len(root.children),
            'best_move': best_child.move,
            'best_move_visits': best_child.visits,
            'best_move_reward': best_child.total_reward / best_child.visits if best_child.visits > 0 else 0.0
        }
