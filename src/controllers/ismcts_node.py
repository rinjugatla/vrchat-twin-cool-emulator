"""
IS-MCTSの探索ノード
情報セット単位で統計を管理する
"""

import math
from typing import Dict, List, Optional, Tuple
from ..models.card import Card
from .information_set import InformationSet


class ISMCTSNode:
    """
    IS-MCTSの探索ノード
    
    従来のMCTSNodeとの違い:
    - 状態ではなく情報セットを保持
    - 複数の決定化で統計を共有
    - 子ノードは手（move）でインデックス化
    """
    
    def __init__(
        self,
        info_set: InformationSet,
        parent: Optional['ISMCTSNode'] = None,
        move: Optional[Tuple[Card, int]] = None
    ):
        """
        IS-MCTSノードの初期化
        
        Args:
            info_set: このノードが表す情報セット
            parent: 親ノード
            move: 親から このノードへの手
        """
        self.info_set = info_set
        self.parent = parent
        self.move = move
        
        # 統計情報（全決定化で共有）
        self.visits = 0
        self.total_reward = 0.0
        
        # 子ノード: 手 -> ISMCTSNode
        self.children: Dict[Tuple[Card, int], 'ISMCTSNode'] = {}
        
        # 未試行の手
        self.untried_moves: List[Tuple[Card, int]] = []
        self._initialized_moves = False
    
    def initialize_untried_moves(self, valid_moves: List[Tuple[Card, int]]):
        """
        有効手を初期化
        
        最初の決定化で呼ばれ、以降は再初期化しない
        
        Args:
            valid_moves: 有効な手のリスト
        """
        if not self._initialized_moves:
            self.untried_moves = valid_moves.copy()
            self._initialized_moves = True
    
    def is_fully_expanded(self) -> bool:
        """
        全ての手が試されたか判定
        
        Returns:
            全て試されていればTrue
        """
        return len(self.untried_moves) == 0
    
    def is_terminal(self) -> bool:
        """
        終端ノード（ゲーム終了）か判定
        
        Returns:
            終端ノードならTrue
        """
        # 未試行の手が初期化され、かつ子ノードが無い場合は終端
        return self._initialized_moves and len(self.untried_moves) == 0 and len(self.children) == 0
    
    def ucb1_score(self, exploration_weight: float = 1.41) -> float:
        """
        UCB1スコアを計算
        
        UCB1 = 活用項 + 探索項
             = (平均報酬) + c * sqrt(log(親訪問数) / 訪問数)
        
        Args:
            exploration_weight: 探索の重み（デフォルト: sqrt(2)）
        
        Returns:
            UCB1スコア
        """
        if self.visits == 0:
            return float('inf')
        
        if self.parent is None or self.parent.visits == 0:
            # 親が無いか親の訪問回数が0の場合は平均報酬のみ
            return self.total_reward / self.visits
        
        # 活用項（exploitation）
        exploitation = self.total_reward / self.visits
        
        # 探索項（exploration）
        exploration = exploration_weight * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        
        return exploitation + exploration
    
    def select_best_child(self, exploration_weight: float = 1.41) -> 'ISMCTSNode':
        """
        UCB1スコアが最大の子ノードを選択
        
        Args:
            exploration_weight: 探索の重み
        
        Returns:
            最良の子ノード
        
        Raises:
            ValueError: 子ノードが無い場合
        """
        if len(self.children) == 0:
            raise ValueError("子ノードが存在しません")
        
        return max(
            self.children.values(),
            key=lambda child: child.ucb1_score(exploration_weight)
        )
    
    def get_best_move(self) -> Optional[Tuple[Card, int]]:
        """
        最も訪問回数が多い手を返す（最良の手）
        
        Returns:
            最良の手（カード、スロット番号）、子ノードが無ければNone
        """
        if len(self.children) == 0:
            return None
        
        best_child = max(self.children.values(), key=lambda c: c.visits)
        return best_child.move
    
    def update(self, reward: float):
        """
        統計情報を更新
        
        Args:
            reward: 報酬値
        """
        self.visits += 1
        self.total_reward += reward
    
    def get_average_reward(self) -> float:
        """
        平均報酬を取得
        
        Returns:
            平均報酬、訪問回数が0ならば0.0
        """
        if self.visits == 0:
            return 0.0
        return self.total_reward / self.visits
    
    def __repr__(self) -> str:
        """文字列表現"""
        return (
            f"ISMCTSNode("
            f"visits={self.visits}, "
            f"avg_reward={self.get_average_reward():.2f}, "
            f"children={len(self.children)}, "
            f"move={self.move})"
        )
    
    def __str__(self) -> str:
        """ユーザー向け文字列表現"""
        return self.__repr__()
