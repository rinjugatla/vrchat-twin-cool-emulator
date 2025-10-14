"""
HeuristicStrategyクラスのテスト
"""

import unittest
from src.models import Card, Suit
from src.controllers import HeuristicStrategy, ObservableGameState, GameState


class TestHeuristicStrategy(unittest.TestCase):
    """HeuristicStrategyクラスのテスト"""
    
    def test_get_best_move_returns_valid_move(self):
        """有効な手が返されることを確認"""
        # GameStateを作成
        game_state = GameState(seed=42)
        obs_state = ObservableGameState.from_game_state(game_state, [])
        
        strategy = HeuristicStrategy(verbose=False)
        best_move = strategy.get_best_move(obs_state)
        
        # 何かしらの手が返ることを確認
        self.assertIsNotNone(best_move)
        if best_move is not None:
            self.assertEqual(len(best_move), 2)  # (Card, int) のタプル
            
            card, slot = best_move
            self.assertIsInstance(card, Card)
            self.assertIn(slot, [0, 1])  # スロットは0または1
    
    def test_get_best_move_no_valid_moves(self):
        """出せるカードがない場合"""
        # 手札が空の状態を作成
        obs_state = ObservableGameState()
        
        strategy = HeuristicStrategy(verbose=False)
        best_move = strategy.get_best_move(obs_state)
        
        # None が返ることを確認
        self.assertIsNone(best_move)
    
    def test_explanation_generation(self):
        """説明文が生成されることを確認"""
        game_state = GameState(seed=42)
        obs_state = ObservableGameState.from_game_state(game_state, [])
        
        strategy = HeuristicStrategy(verbose=False)
        best_move = strategy.get_best_move(obs_state)
        
        # 説明文を取得
        explanation = strategy.explain()
        
        self.assertIsNotNone(explanation)
        self.assertIsInstance(explanation, str)
        self.assertIn("ヒューリスティック", explanation)
        
        if best_move:
            card, slot = best_move
            self.assertIn(str(card), explanation)
            self.assertIn(f"スロット{slot + 1}", explanation)
    
    def test_explanation_before_move(self):
        """手を選択する前の説明"""
        strategy = HeuristicStrategy(verbose=False)
        explanation = strategy.explain()
        
        self.assertEqual(explanation, "まだ判断を行っていません")
    
    def test_verbose_mode(self):
        """verboseモードのテスト（エラーが出ないことを確認）"""
        game_state = GameState(seed=42)
        obs_state = ObservableGameState.from_game_state(game_state, [])
        
        # verboseモードで実行（標準出力に出るが、エラーは出ないはず）
        strategy = HeuristicStrategy(verbose=True)
        best_move = strategy.get_best_move(obs_state)
        
        self.assertIsNotNone(best_move)
    
    def test_get_flexibility_analysis(self):
        """柔軟性分析データの取得"""
        game_state = GameState(seed=42)
        obs_state = ObservableGameState.from_game_state(game_state, [])
        
        strategy = HeuristicStrategy(verbose=False)
        analysis = strategy.get_flexibility_analysis(obs_state)
        
        # 必要なキーが含まれることを確認
        self.assertIn('hand_scores', analysis)
        self.assertIn('valid_moves', analysis)
        self.assertIn('unknown_count', analysis)
        
        # hand_scoresは辞書
        self.assertIsInstance(analysis['hand_scores'], dict)
        
        # valid_movesはリスト
        self.assertIsInstance(analysis['valid_moves'], list)
        
        # unknown_countは整数
        self.assertIsInstance(analysis['unknown_count'], int)
        self.assertGreater(analysis['unknown_count'], 0)
    
    def test_consistency_multiple_calls(self):
        """同じ状態で複数回呼び出しても一貫性があることを確認"""
        game_state = GameState(seed=42)
        obs_state = ObservableGameState.from_game_state(game_state, [])
        
        strategy = HeuristicStrategy(verbose=False)
        
        # 同じ状態で2回呼び出す
        move1 = strategy.get_best_move(obs_state)
        move2 = strategy.get_best_move(obs_state)
        
        # 同じ手が返ることを確認
        self.assertEqual(move1, move2)
    
    def test_different_seeds_different_states(self):
        """異なるシードで異なる状態が作られることを確認"""
        game_state1 = GameState(seed=42)
        game_state2 = GameState(seed=123)
        
        obs_state1 = ObservableGameState.from_game_state(game_state1, [])
        obs_state2 = ObservableGameState.from_game_state(game_state2, [])
        
        strategy = HeuristicStrategy(verbose=False)
        
        move1 = strategy.get_best_move(obs_state1)
        move2 = strategy.get_best_move(obs_state2)
        
        # 手札が異なるので、選択される手も異なる可能性が高い
        # （ただし、偶然同じになる可能性もあるので、assertNotEqualは使わない）
        self.assertIsNotNone(move1)
        self.assertIsNotNone(move2)


if __name__ == '__main__':
    unittest.main()
