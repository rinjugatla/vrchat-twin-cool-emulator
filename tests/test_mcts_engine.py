"""
mcts_engine.pyのテスト
"""

import unittest
from src.controllers.mcts_engine import MCTSEngine
from src.controllers.game_state import GameState


class TestMCTSEngine(unittest.TestCase):
    """MCTSEngineクラスのテスト"""
    
    def test_initialization(self):
        """エンジンの初期化テスト"""
        engine = MCTSEngine()
        
        self.assertEqual(engine.exploration_weight, 1.41)
    
    def test_search_basic(self):
        """基本的な探索テスト"""
        state = GameState(seed=42)
        engine = MCTSEngine(simulation_seed=42)
        
        best_move, root = engine.search(state, num_iterations=10)
        
        # 何かしらの手が返される
        self.assertIsNotNone(best_move)
        
        # ルートノードが訪問されている
        self.assertGreater(root.visits, 0)
    
    def test_search_many_iterations(self):
        """多数回の探索テスト"""
        state = GameState(seed=42)
        engine = MCTSEngine(simulation_seed=42)
        
        best_move, root = engine.search(state, num_iterations=100)
        
        self.assertIsNotNone(best_move)
        self.assertEqual(root.visits, 100)
    
    def test_select(self):
        """Selectionフェーズのテスト"""
        state = GameState(seed=42)
        engine = MCTSEngine()
        
        from src.controllers.mcts_node import MCTSNode
        root = MCTSNode(state)
        
        selected = engine._select(root)
        
        # 未展開なのでルートが返される
        self.assertEqual(selected, root)
    
    def test_expand(self):
        """Expansionフェーズのテスト"""
        state = GameState(seed=42)
        engine = MCTSEngine()
        
        from src.controllers.mcts_node import MCTSNode
        node = MCTSNode(state)
        
        child = engine._expand(node)
        
        self.assertIn(child, node.children)
        self.assertEqual(child.parent, node)
    
    def test_simulate(self):
        """Simulationフェーズのテスト"""
        state = GameState(seed=42)
        engine = MCTSEngine(simulation_seed=42)
        
        reward = engine._simulate(state)
        
        # 報酬は0以上
        self.assertGreaterEqual(reward, 0)
    
    def test_backpropagate(self):
        """Backpropagationフェーズのテスト"""
        state = GameState(seed=42)
        engine = MCTSEngine()
        
        from src.controllers.mcts_node import MCTSNode
        root = MCTSNode(state)
        child = root.expand()
        
        engine._backpropagate(child, 100.0)
        
        # 子ノードと親ノードの両方が更新される
        self.assertEqual(child.visits, 1)
        self.assertEqual(child.total_reward, 100.0)
        self.assertEqual(root.visits, 1)
        self.assertEqual(root.total_reward, 100.0)
    
    def test_get_statistics(self):
        """統計情報取得のテスト"""
        state = GameState(seed=42)
        engine = MCTSEngine(simulation_seed=42)
        
        best_move, root = engine.search(state, num_iterations=50)
        stats = engine.get_statistics(root)
        
        self.assertEqual(stats['total_visits'], 50)
        self.assertGreater(stats['num_children'], 0)
        self.assertIsNotNone(stats['best_move'])
        self.assertGreater(stats['best_move_visits'], 0)
    
    def test_get_statistics_no_children(self):
        """子ノードがない場合の統計情報"""
        state = GameState(seed=42)
        engine = MCTSEngine()
        
        from src.controllers.mcts_node import MCTSNode
        root = MCTSNode(state)
        root.visits = 5
        
        stats = engine.get_statistics(root)
        
        self.assertEqual(stats['total_visits'], 5)
        self.assertEqual(stats['num_children'], 0)
        self.assertIsNone(stats['best_move'])
    
    def test_different_seeds_produce_different_results(self):
        """異なるシードで異なる結果"""
        state1 = GameState(seed=1)
        state2 = GameState(seed=1)  # 同じ初期状態
        
        engine1 = MCTSEngine(simulation_seed=1)
        engine2 = MCTSEngine(simulation_seed=2)
        
        best_move1, _ = engine1.search(state1, num_iterations=50)
        best_move2, _ = engine2.search(state2, num_iterations=50)
        
        # 何かしらの手が返される
        self.assertIsNotNone(best_move1)
        self.assertIsNotNone(best_move2)


if __name__ == '__main__':
    unittest.main()
