"""
IS-MCTS探索エンジン
情報セットMCTSのメインアルゴリズムを実行
"""

import copy
import random
from typing import Dict, Optional, Tuple
from ..models.card import Card
from .game_state import GameState
from .observable_game_state import ObservableGameState
from .information_set import InformationSet
from .ismcts_node import ISMCTSNode
from .determinizer import Determinizer
from .move_validator import MoveValidator
from .evaluator import Evaluator


class ISMCTSEngine:
    """
    情報セットMCTS探索エンジン
    
    IS-MCTSの4つのフェーズを複数の決定化で実行:
    1. Selection（選択）- 情報セット単位でUCB1選択
    2. Expansion（展開）- 未試行の手を試す
    3. Simulation（シミュレーション）- ランダムプレイアウト
    4. Backpropagation（逆伝播）- 情報セット単位で統計更新
    """
    
    def __init__(
        self,
        exploration_weight: float = 1.41,
        verbose: bool = False
    ):
        """
        IS-MCTS探索エンジンの初期化
        
        Args:
            exploration_weight: UCB1の探索重み（デフォルト: sqrt(2)）
            verbose: 詳細ログを出力するか
        """
        self.exploration_weight = exploration_weight
        self.verbose = verbose
        
        # 情報セット -> ノード のマッピング（木の共有）
        self.info_set_tree: Dict[InformationSet, ISMCTSNode] = {}
    
    def search(
        self,
        observable_state: ObservableGameState,
        num_iterations: int = 1000
    ) -> Tuple[Optional[Tuple[Card, int]], Dict]:
        """
        IS-MCTS探索を実行
        
        各イテレーションで:
        1. 決定化を1つ生成（山札の可能性をサンプリング）
        2. その決定化でMCTS 1回実行（情報セットノードを共有）
        3. 統計を更新
        
        Args:
            observable_state: 観測可能なゲーム状態
            num_iterations: 探索回数
        
        Returns:
            (最良の手, 統計情報)
        """
        # ルート情報セットを取得
        root_info_set = self._get_information_set_from_observable(observable_state)
        root_node = self._get_or_create_node(root_info_set)
        
        for iteration in range(num_iterations):
            # 1. 決定化を生成
            determinized_state = Determinizer.create_determinization(observable_state)
            
            # 2. この決定化でMCTS 1イテレーション
            self._run_one_iteration(root_node, determinized_state)
            
            if self.verbose and iteration % 100 == 0:
                print(f"IS-MCTS Iteration {iteration}/{num_iterations}")
        
        # 最良の手を返す
        best_move = root_node.get_best_move()
        stats = self._get_statistics(root_node)
        
        return best_move, stats
    
    def _run_one_iteration(
        self,
        root_node: ISMCTSNode,
        determinized_state: GameState
    ):
        """
        決定化1つでMCTSイテレーション1回実行
        
        Args:
            root_node: ルートノード
            determinized_state: 決定化されたゲーム状態
        """
        # Selection
        node, state = self._select(root_node, determinized_state)
        
        # Expansion
        if not self._is_terminal(state) and not node.is_fully_expanded():
            node, state = self._expand(node, state)
        
        # Simulation
        reward = self._simulate(state)
        
        # Backpropagation
        self._backpropagate(node, reward)
    
    def _select(
        self,
        node: ISMCTSNode,
        state: GameState
    ) -> Tuple[ISMCTSNode, GameState]:
        """
        Selection フェーズ: UCB1で最も有望なノードを選択
        
        Args:
            node: 現在のノード
            state: 現在の状態
        
        Returns:
            (選択されたノード, 対応する状態)
        """
        current_state = copy.deepcopy(state)
        current_node = node
        
        while not self._is_terminal(current_state):
            # 有効手を取得
            valid_moves = MoveValidator.get_valid_moves(
                current_state.get_hand(),
                current_state.get_field()
            )
            
            # 未試行の手を初期化
            if not current_node._initialized_moves:
                current_node.initialize_untried_moves(valid_moves)
            
            # まだ展開できる手がある場合は、このノードを返す
            if not current_node.is_fully_expanded():
                return current_node, current_state
            
            # 完全に展開済み → UCB1で最良の子を選択
            current_node = current_node.select_best_child(self.exploration_weight)
            
            # 状態を進める
            if current_node.move is not None:
                card, slot = current_node.move
                current_state.play_card(card, slot)
        
        return current_node, current_state
    
    def _expand(
        self,
        node: ISMCTSNode,
        state: GameState
    ) -> Tuple[ISMCTSNode, GameState]:
        """
        Expansion フェーズ: 未試行の手を1つ選んで子ノードを作成
        
        Args:
            node: 展開するノード
            state: 現在の状態
        
        Returns:
            (新しく作成された子ノード, 対応する状態)
        """
        # 未試行の手を1つ選択
        move = node.untried_moves.pop()
        card, slot = move
        
        # 状態を進める
        new_state = copy.deepcopy(state)
        new_state.play_card(card, slot)
        
        # 新しい情報セットとノードを作成
        new_info_set = self._get_information_set(new_state)
        new_node = self._get_or_create_node(new_info_set, parent=node, move=move)
        
        # 親の子として登録
        node.children[move] = new_node
        
        return new_node, new_state
    
    def _simulate(self, state: GameState) -> float:
        """
        Simulation フェーズ: ゲーム終了までランダムプレイ
        
        Args:
            state: シミュレーション開始時の状態
        
        Returns:
            報酬値（評価スコア）
        """
        sim_state = copy.deepcopy(state)
        
        # ゲーム終了までランダムにプレイ
        while MoveValidator.has_valid_move(
            sim_state.get_hand(),
            sim_state.get_field()
        ):
            valid_moves = MoveValidator.get_valid_moves(
                sim_state.get_hand(),
                sim_state.get_field()
            )
            
            if len(valid_moves) == 0:
                break
            
            # ランダムに手を選択
            card, slot = random.choice(valid_moves)
            sim_state.play_card(card, slot)
        
        # 結果を評価
        result = {
            'cards_played': sim_state.get_cards_played_count(),
            'total_points': sim_state.get_total_points()
        }
        
        return Evaluator.evaluate(result)
    
    def _backpropagate(self, node: Optional[ISMCTSNode], reward: float):
        """
        Backpropagation フェーズ: 報酬をルートまで伝播
        
        Args:
            node: 開始ノード
            reward: 報酬値
        """
        current = node
        while current is not None:
            current.update(reward)
            current = current.parent
    
    def _get_or_create_node(
        self,
        info_set: InformationSet,
        parent: Optional[ISMCTSNode] = None,
        move: Optional[Tuple[Card, int]] = None
    ) -> ISMCTSNode:
        """
        情報セットに対応するノードを取得または作成
        
        同じ情報セットは同じノードを共有する（キャッシュ）
        
        Args:
            info_set: 情報セット
            parent: 親ノード
            move: 親からの手
        
        Returns:
            ISMCTSNode
        """
        if info_set not in self.info_set_tree:
            self.info_set_tree[info_set] = ISMCTSNode(
                info_set,
                parent=parent,
                move=move
            )
        return self.info_set_tree[info_set]
    
    def _get_information_set(self, state: GameState) -> InformationSet:
        """
        GameStateから情報セットを抽出
        
        Args:
            state: ゲーム状態
        
        Returns:
            InformationSet
        """
        return InformationSet(
            hand=state.get_hand(),
            field=state.get_field(),
            cards_played_count=len(state.get_played_cards())
        )
    
    def _get_information_set_from_observable(
        self,
        obs_state: ObservableGameState
    ) -> InformationSet:
        """
        ObservableGameStateから情報セットを抽出
        
        Args:
            obs_state: 観測可能なゲーム状態
        
        Returns:
            InformationSet
        """
        return InformationSet(
            hand=obs_state.hand,
            field=obs_state.field,
            cards_played_count=len(obs_state.played_cards)
        )
    
    def _is_terminal(self, state: GameState) -> bool:
        """
        終端状態（ゲーム終了）判定
        
        Args:
            state: ゲーム状態
        
        Returns:
            終端状態ならTrue
        """
        return not MoveValidator.has_valid_move(
            state.get_hand(),
            state.get_field()
        )
    
    def _get_statistics(self, root: ISMCTSNode) -> dict:
        """
        探索の統計情報を取得
        
        Args:
            root: ルートノード
        
        Returns:
            統計情報の辞書
        """
        best_move = root.get_best_move()
        
        if best_move and best_move in root.children:
            best_child = root.children[best_move]
            best_move_visits = best_child.visits
            best_move_reward = best_child.get_average_reward()
        else:
            best_move_visits = 0
            best_move_reward = 0.0
        
        return {
            'total_visits': root.visits,
            'num_children': len(root.children),
            'best_move': best_move,
            'best_move_visits': best_move_visits,
            'best_move_reward': best_move_reward,
            'info_set_cache_size': len(self.info_set_tree)
        }
    
    def clear_cache(self):
        """
        情報セットツリーのキャッシュをクリア
        
        メモリ管理のため、探索完了後に呼び出すことを推奨
        """
        self.info_set_tree.clear()
