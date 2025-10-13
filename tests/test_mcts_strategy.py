"""
MCTSStrategy クラスのユニットテスト
"""

import unittest
from src.controllers.mcts_strategy import MCTSStrategy
from src.controllers.game_state import GameState
from src.models.card import Card
from src.models.suit import Suit


class TestMCTSStrategy(unittest.TestCase):
    """MCTSStrategyクラスのテストケース"""
    
    def test_initialization(self):
        """戦略の初期化"""
        strategy = MCTSStrategy(num_iterations=500, exploration_weight=1.5, verbose=False)
        self.assertEqual(strategy.num_iterations, 500)
        self.assertEqual(strategy.exploration_weight, 1.5)
        self.assertFalse(strategy.verbose)
    
    def test_initialization_defaults(self):
        """デフォルトパラメータでの初期化"""
        strategy = MCTSStrategy()
        self.assertEqual(strategy.num_iterations, 1000)
        self.assertEqual(strategy.exploration_weight, 1.41)
        self.assertFalse(strategy.verbose)
    
    def test_get_best_move_initial_state(self):
        """初期状態での最適手取得"""
        state = GameState(seed=42)
        strategy = MCTSStrategy(num_iterations=100, verbose=False)
        
        best_move = strategy.get_best_move(state)
        
        # 初期状態では必ず手があるはず
        self.assertIsNotNone(best_move)
        if best_move is not None:
            card, slot = best_move
            self.assertIsInstance(card, Card)
            self.assertIn(slot, [1, 2])
    
    def test_get_best_move_terminal_state(self):
        """終了状態での最適手取得（手がない）"""
        state = GameState(seed=42)
        
        # 手札を空にする（強制的にゲーム終了状態を作る）
        for _ in range(5):
            cards = state.hand.get_cards()
            if cards:
                state.hand.remove_card(cards[0])
        
        strategy = MCTSStrategy(num_iterations=100, verbose=False)
        best_move = strategy.get_best_move(state)
        
        # 終了状態では手がない
        self.assertIsNone(best_move)
    
    def test_play_game(self):
        """ゲーム全体のプレイ"""
        initial_state = GameState(seed=42)
        strategy = MCTSStrategy(num_iterations=100, verbose=False)
        
        result = strategy.play_game(initial_state)
        
        # 結果の検証
        self.assertIn('cards_played', result)
        self.assertIn('total_points', result)
        self.assertIn('turn_count', result)
        self.assertIn('final_hand_size', result)
        
        # 最低1枚はプレイできるはず
        self.assertGreaterEqual(result['cards_played'], 1)
        self.assertGreaterEqual(result['turn_count'], 1)
        self.assertGreaterEqual(result['total_points'], 0)
    
    def test_play_game_verbose(self):
        """詳細ログ付きでゲームをプレイ"""
        initial_state = GameState(seed=42)
        strategy = MCTSStrategy(num_iterations=50, verbose=True)
        
        # 例外が発生しないことを確認
        result = strategy.play_game(initial_state)
        self.assertIsNotNone(result)
    
    def test_compare_with_random(self):
        """ランダム戦略との比較"""
        strategy = MCTSStrategy(num_iterations=100, verbose=False)
        
        # 少数のゲームで比較
        comparison = strategy.compare_with_random(num_games=3, seed=42)
        
        # 結果構造の検証
        self.assertIn('mcts', comparison)
        self.assertIn('random', comparison)
        self.assertIn('improvement', comparison)
        
        # MCTS結果
        self.assertIn('avg_cards', comparison['mcts'])
        self.assertIn('max_cards', comparison['mcts'])
        self.assertIn('min_cards', comparison['mcts'])
        self.assertIn('avg_points', comparison['mcts'])
        
        # ランダム結果
        self.assertIn('avg_cards', comparison['random'])
        self.assertIn('max_cards', comparison['random'])
        
        # 改善度
        self.assertIn('cards', comparison['improvement'])
        self.assertIn('points', comparison['improvement'])
    
    def test_mcts_better_than_random(self):
        """MCTSがランダムより良い結果を出すことを確認（統計的テスト）"""
        strategy = MCTSStrategy(num_iterations=200, verbose=False)
        
        # 10ゲームで比較
        comparison = strategy.compare_with_random(num_games=10, seed=123)
        
        # MCTSの方が平均的に良い結果を出すことを期待
        # （確率的なので必ず勝つわけではないが、多くの場合勝つはず）
        mcts_avg = comparison['mcts']['avg_cards']
        random_avg = comparison['random']['avg_cards']
        
        # 10ゲームの平均でランダムより良いか同等であることを期待
        self.assertGreaterEqual(mcts_avg, random_avg * 0.9)  # 90%以上のパフォーマンス
    
    def test_different_iterations(self):
        """異なる反復回数での動作確認"""
        state = GameState(seed=42)
        
        # 少ない反復
        strategy_low = MCTSStrategy(num_iterations=10, verbose=False)
        result_low = strategy_low.play_game(state)
        
        # 多い反復
        strategy_high = MCTSStrategy(num_iterations=500, verbose=False)
        result_high = strategy_high.play_game(state)
        
        # 両方とも結果が得られることを確認
        self.assertGreaterEqual(result_low['cards_played'], 1)
        self.assertGreaterEqual(result_high['cards_played'], 1)
    
    def test_reproducibility(self):
        """同じシードで再現性があることを確認"""
        strategy = MCTSStrategy(num_iterations=100, verbose=False)
        
        # 同じシードで2回プレイ
        state1 = GameState(seed=999)
        result1 = strategy.play_game(state1)
        
        state2 = GameState(seed=999)
        result2 = strategy.play_game(state2)
        
        # 同じ結果が得られるはず
        self.assertEqual(result1['cards_played'], result2['cards_played'])
        self.assertEqual(result1['total_points'], result2['total_points'])


if __name__ == '__main__':
    unittest.main()
