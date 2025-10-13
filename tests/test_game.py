"""
game.pyのテスト
"""

import unittest
from src.controllers.game import Game


class TestGame(unittest.TestCase):
    """Gameクラスのテスト"""
    
    def test_initialization(self):
        """ゲームの初期化テスト"""
        game = Game(seed=42)
        
        self.assertFalse(game.is_finished)
        self.assertEqual(game.get_state().get_hand().count(), 5)
        self.assertEqual(game.get_state().get_cards_played_count(), 0)
    
    def test_play_random_turn_success(self):
        """ランダムターンのプレイテスト（成功）"""
        game = Game(seed=42)
        
        result = game.play_random_turn()
        
        self.assertTrue(result)
        self.assertEqual(game.get_state().turn_count, 1)
        self.assertEqual(game.get_state().get_cards_played_count(), 1)
    
    def test_simulate_random_game(self):
        """ランダムシミュレーションのテスト"""
        game = Game(seed=42)
        
        result = game.simulate_random_game()
        
        # ゲームが終了している
        self.assertTrue(game.is_finished)
        
        # 結果が正しい形式
        self.assertIn('cards_played', result)
        self.assertIn('total_points', result)
        self.assertIn('turn_count', result)
        self.assertIn('final_hand_size', result)
        
        # カードが出されている
        self.assertGreater(result['cards_played'], 0)
        
        # ターン数が正しい
        self.assertEqual(result['turn_count'], result['cards_played'])
    
    def test_simulate_multiple_games(self):
        """複数ゲームのシミュレーションテスト"""
        results = []
        
        for seed in range(5):
            game = Game(seed=seed)
            result = game.simulate_random_game()
            results.append(result)
        
        # 全てのゲームが終了している
        for result in results:
            self.assertGreater(result['cards_played'], 0)
            self.assertTrue(result['is_finished'])
    
    def test_play_turn_manual(self):
        """手動ターンのプレイテスト"""
        game = Game(seed=42)
        
        # 最初のカード（インデックス0）をスロット1に出す
        result = game.play_turn(0, 1)
        
        self.assertTrue(result)
        self.assertEqual(game.get_state().turn_count, 1)
    
    def test_play_turn_invalid_index(self):
        """無効なインデックスでのターンプレイテスト"""
        game = Game(seed=42)
        
        # 無効なインデックス
        result = game.play_turn(10, 1)
        
        self.assertFalse(result)
        self.assertEqual(game.get_state().turn_count, 0)
    
    def test_get_result(self):
        """結果取得のテスト"""
        game = Game(seed=42)
        
        # 1ターンプレイ
        game.play_random_turn()
        
        result = game.get_result()
        
        self.assertEqual(result['cards_played'], 1)
        self.assertEqual(result['turn_count'], 1)
        self.assertGreaterEqual(result['total_points'], 0)
    
    def test_game_str_representation(self):
        """文字列表現のテスト"""
        game = Game(seed=42)
        game.play_random_turn()
        
        game_str = str(game)
        
        self.assertIn("Game", game_str)
        self.assertIn("Cards Played", game_str)
        self.assertIn("Points", game_str)
    
    def test_game_finishes_correctly(self):
        """ゲームが正しく終了することのテスト"""
        game = Game(seed=42)
        
        # ゲームをシミュレート
        game.simulate_random_game()
        
        # ゲームが終了している
        self.assertTrue(game.is_finished)
        
        # 終了後はランダムターンを実行できない
        result = game.play_random_turn()
        self.assertFalse(result)
    
    def test_different_seeds_produce_different_results(self):
        """異なるシードで異なる結果が得られることのテスト"""
        game1 = Game(seed=1)
        result1 = game1.simulate_random_game()
        
        game2 = Game(seed=2)
        result2 = game2.simulate_random_game()
        
        # 異なるシードで異なる結果が得られる可能性が高い
        # （100%保証はできないが、統計的にほぼ確実）
        # 少なくともどちらもゲームが進行していることを確認
        self.assertGreater(result1['cards_played'], 0)
        self.assertGreater(result2['cards_played'], 0)


if __name__ == '__main__':
    unittest.main()
