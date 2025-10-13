"""
mcts_node.pyのテスト
"""

import unittest
import math
from src.controllers.mcts_node import MCTSNode
from src.controllers.game_state import GameState
from src.models.card import Card
from src.models.suit import Suit


class TestMCTSNode(unittest.TestCase):
    """MCTSNodeクラスのテスト"""
    
    def test_initialization(self):
        """ノードの初期化テスト"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        self.assertEqual(node.visits, 0)
        self.assertEqual(node.total_reward, 0.0)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.move)
        self.assertEqual(len(node.children), 0)
        self.assertGreater(len(node.untried_moves), 0)
    
    def test_is_fully_expanded_false(self):
        """完全に展開されていない場合"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        self.assertFalse(node.is_fully_expanded())
    
    def test_is_fully_expanded_true(self):
        """完全に展開されている場合"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        node.untried_moves = []
        
        self.assertTrue(node.is_fully_expanded())
    
    def test_is_terminal_false(self):
        """終端ノードでない場合"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        self.assertFalse(node.is_terminal())
    
    def test_ucb1_score_unvisited(self):
        """未訪問ノードのUCB1スコア"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        score = node.ucb1_score()
        
        self.assertEqual(score, float('inf'))
    
    def test_ucb1_score_visited(self):
        """訪問済みノードのUCB1スコア"""
        state = GameState(seed=42)
        parent = MCTSNode(state)
        parent.visits = 10
        
        child = MCTSNode(state, parent=parent)
        child.visits = 5
        child.total_reward = 10.0
        
        score = child.ucb1_score()
        
        # exploitation = 10.0 / 5 = 2.0
        # exploration = 1.41 * sqrt(log(10) / 5)
        expected_exploitation = 2.0
        expected_exploration = 1.41 * math.sqrt(math.log(10) / 5)
        expected_score = expected_exploitation + expected_exploration
        
        self.assertAlmostEqual(score, expected_score, places=5)
    
    def test_expand(self):
        """ノードの展開テスト"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        initial_untried_count = len(node.untried_moves)
        
        child = node.expand()
        
        self.assertEqual(len(node.untried_moves), initial_untried_count - 1)
        self.assertEqual(len(node.children), 1)
        self.assertIn(child, node.children)
        self.assertEqual(child.parent, node)
        self.assertIsNotNone(child.move)
    
    def test_update(self):
        """ノードの更新テスト"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        node.update(10.0)
        
        self.assertEqual(node.visits, 1)
        self.assertEqual(node.total_reward, 10.0)
        
        node.update(20.0)
        
        self.assertEqual(node.visits, 2)
        self.assertEqual(node.total_reward, 30.0)
    
    def test_select_best_child(self):
        """最良の子ノードを選択"""
        state = GameState(seed=42)
        parent = MCTSNode(state)
        parent.visits = 10
        
        # 子ノード1
        child1 = MCTSNode(state, parent=parent)
        child1.visits = 3
        child1.total_reward = 6.0
        parent.children.append(child1)
        
        # 子ノード2（より良い）
        child2 = MCTSNode(state, parent=parent)
        child2.visits = 5
        child2.total_reward = 15.0
        parent.children.append(child2)
        
        best_child = parent.select_best_child()
        
        # child2の方がスコアが高いはず
        self.assertEqual(best_child, child2)
    
    def test_get_best_move_no_children(self):
        """子ノードがない場合"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        
        best_move = node.get_best_move()
        
        self.assertIsNone(best_move)
    
    def test_get_best_move_with_children(self):
        """子ノードがある場合"""
        state = GameState(seed=42)
        parent = MCTSNode(state)
        
        # 子ノードを作成
        child1 = parent.expand()
        child1.visits = 3
        
        child2 = parent.expand()
        child2.visits = 7  # より多く訪問
        
        best_move = parent.get_best_move()
        
        # child2の手が返されるべき
        self.assertEqual(best_move, child2.move)
    
    def test_str_representation(self):
        """文字列表現のテスト"""
        state = GameState(seed=42)
        node = MCTSNode(state)
        node.visits = 5
        node.total_reward = 10.5
        
        node_str = str(node)
        
        self.assertIn("MCTSNode", node_str)
        self.assertIn("visits=5", node_str)
        self.assertIn("10.5", node_str)


if __name__ == '__main__':
    unittest.main()
