"""
MCTSノードクラス
モンテカルロ木探索の各ノードを表現
"""

import math
from typing import Optional, List, Tuple
from ..models.card import Card
from .game_state import GameState
from .move_validator import MoveValidator


class MCTSNode:
    """
    MCTSの探索木のノード
    
    Attributes:
        state: ゲーム状態
        parent: 親ノード
        move: このノードに至った手（カード、スロット番号）
        children: 子ノードのリスト
        visits: 訪問回数
        total_reward: 累積報酬
        untried_moves: まだ試していない手のリスト
    """
    
    def __init__(
        self,
        state: GameState,
        parent: Optional['MCTSNode'] = None,
        move: Optional[Tuple[Card, int]] = None
    ):
        """
        MCTSノードの初期化
        
        Args:
            state: ゲーム状態
            parent: 親ノード
            move: このノードに至った手
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.children: List[MCTSNode] = []
        self.visits = 0
        self.total_reward = 0.0
        
        # まだ試していない手を取得
        self.untried_moves = MoveValidator.get_valid_moves(
            state.get_hand(),
            state.get_field()
        )
    
    def is_fully_expanded(self) -> bool:
        """
        ノードが完全に展開されているか（全ての子ノードが作成済みか）
        
        Returns:
            完全に展開されている場合True
        """
        return len(self.untried_moves) == 0
    
    def is_terminal(self) -> bool:
        """
        このノードが終端ノードか（ゲーム終了状態か）
        
        Returns:
            終端ノードの場合True
        """
        return not MoveValidator.has_valid_move(
            self.state.get_hand(),
            self.state.get_field()
        )
    
    def ucb1_score(self, exploration_weight: float = 1.41) -> float:
        """
        UCB1スコアを計算（Upper Confidence Bound）
        
        Args:
            exploration_weight: 探索の重み（デフォルト: sqrt(2)）
        
        Returns:
            UCB1スコア
        """
        if self.visits == 0:
            return float('inf')  # 未訪問ノードは最優先
        
        if self.parent is None:
            return self.total_reward / self.visits
        
        # UCB1 = 平均報酬 + 探索項
        exploitation = self.total_reward / self.visits
        exploration = exploration_weight * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        
        return exploitation + exploration
    
    def select_best_child(self, exploration_weight: float = 1.41) -> 'MCTSNode':
        """
        UCB1スコアが最も高い子ノードを選択
        
        Args:
            exploration_weight: 探索の重み
        
        Returns:
            選択された子ノード
        """
        return max(self.children, key=lambda child: child.ucb1_score(exploration_weight))
    
    def expand(self) -> 'MCTSNode':
        """
        未試行の手を1つ選んで子ノードを作成
        
        Returns:
            新しく作成された子ノード
        """
        if len(self.untried_moves) == 0:
            raise ValueError("展開できる手がありません")
        
        # 未試行の手を1つ選ぶ
        move = self.untried_moves.pop()
        card, slot_number = move
        
        # 新しい状態を作成（状態をコピーして手を適用）
        import copy
        new_state = copy.deepcopy(self.state)
        new_state.play_card(card, slot_number)
        
        # 子ノードを作成
        child_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child_node)
        
        return child_node
    
    def update(self, reward: float):
        """
        ノードの統計情報を更新（バックプロパゲーション）
        
        Args:
            reward: 報酬値
        """
        self.visits += 1
        self.total_reward += reward
    
    def get_best_move(self) -> Optional[Tuple[Card, int]]:
        """
        最も訪問回数が多い子ノードの手を返す
        
        Returns:
            最良の手（カード、スロット番号）
        """
        if len(self.children) == 0:
            return None
        
        best_child = max(self.children, key=lambda child: child.visits)
        return best_child.move
    
    def __str__(self) -> str:
        return (
            f"MCTSNode(visits={self.visits}, "
            f"reward={self.total_reward:.2f}, "
            f"children={len(self.children)}, "
            f"untried={len(self.untried_moves)})"
        )
