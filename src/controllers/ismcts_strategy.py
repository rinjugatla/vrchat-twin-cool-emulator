"""
IS-MCTS戦略
WebUIから利用できる戦略インターフェース
"""

from typing import Optional, Tuple
from ..models.card import Card
from .observable_game_state import ObservableGameState
from .ismcts_engine import ISMCTSEngine


class ISMCTSStrategy:
    """
    IS-MCTS戦略（不完全情報対応）
    
    既存のMCTSStrategyと同じインターフェースを提供し、
    WebUIから簡単に利用できるようにする。
    
    Usage:
        strategy = ISMCTSStrategy(num_iterations=1000)
        best_move = strategy.get_best_move(observable_state)
    """
    
    def __init__(
        self,
        num_iterations: int = 1000,
        exploration_weight: float = 1.41,
        verbose: bool = False
    ):
        """
        IS-MCTS戦略の初期化
        
        Args:
            num_iterations: 探索回数（デフォルト: 1000）
            exploration_weight: UCB1の探索重み（デフォルト: sqrt(2)）
            verbose: 詳細ログを出力するか
        """
        self.num_iterations = num_iterations
        self.exploration_weight = exploration_weight
        self.verbose = verbose
        
        # エンジンを初期化
        self.engine = ISMCTSEngine(
            exploration_weight=exploration_weight,
            verbose=verbose
        )
    
    def get_best_move(
        self,
        observable_state: ObservableGameState
    ) -> Optional[Tuple[Card, int]]:
        """
        最適な手を取得
        
        Args:
            observable_state: 観測可能なゲーム状態
        
        Returns:
            最良の手（カード、スロット番号）、手が無ければNone
        """
        # IS-MCTS探索を実行
        best_move, stats = self.engine.search(
            observable_state,
            num_iterations=self.num_iterations
        )
        
        if self.verbose:
            self._print_statistics(stats)
        
        # 探索完了後、キャッシュをクリア（メモリ管理）
        self.engine.clear_cache()
        
        return best_move
    
    def _print_statistics(self, stats: dict):
        """
        統計情報を出力
        
        Args:
            stats: 統計情報の辞書
        """
        print("\n" + "=" * 50)
        print("IS-MCTS Statistics")
        print("=" * 50)
        print(f"Total visits: {stats['total_visits']}")
        print(f"Children: {stats['num_children']}")
        print(f"Info set cache size: {stats['info_set_cache_size']}")
        print(f"Best move: {stats['best_move']}")
        print(f"Best move visits: {stats['best_move_visits']}")
        print(f"Best move avg reward: {stats['best_move_reward']:.2f}")
        print("=" * 50 + "\n")
    
    def set_num_iterations(self, num_iterations: int):
        """
        探索回数を設定
        
        Args:
            num_iterations: 新しい探索回数
        """
        self.num_iterations = num_iterations
    
    def set_exploration_weight(self, exploration_weight: float):
        """
        探索重みを設定
        
        Args:
            exploration_weight: 新しい探索重み
        """
        self.exploration_weight = exploration_weight
        self.engine.exploration_weight = exploration_weight
    
    def set_verbose(self, verbose: bool):
        """
        詳細ログ出力を設定
        
        Args:
            verbose: 詳細ログを出力するか
        """
        self.verbose = verbose
        self.engine.verbose = verbose
