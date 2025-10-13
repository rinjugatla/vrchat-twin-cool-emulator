"""
evaluator.pyのテスト
"""

import unittest
from src.controllers.evaluator import Evaluator


class TestEvaluator(unittest.TestCase):
    """Evaluatorクラスのテスト"""
    
    def test_evaluate_basic(self):
        """基本的な評価テスト"""
        result = {
            'cards_played': 10,
            'total_points': 5,
            'turn_count': 10,
            'final_hand_size': 5
        }
        
        score = Evaluator.evaluate(result)
        
        # スコア = (10 * 10.0) + (5 * 1.0) = 105.0
        self.assertEqual(score, 105.0)
    
    def test_evaluate_only_cards(self):
        """カードのみのスコア"""
        result = {
            'cards_played': 20,
            'total_points': 0,
        }
        
        score = Evaluator.evaluate(result)
        
        # スコア = (20 * 10.0) + (0 * 1.0) = 200.0
        self.assertEqual(score, 200.0)
    
    def test_evaluate_only_points(self):
        """ポイントのみのスコア"""
        result = {
            'cards_played': 0,
            'total_points': 10,
        }
        
        score = Evaluator.evaluate(result)
        
        # スコア = (0 * 10.0) + (10 * 1.0) = 10.0
        self.assertEqual(score, 10.0)
    
    def test_compare_results_result1_better(self):
        """result1の方が良い場合"""
        result1 = {'cards_played': 20, 'total_points': 5}
        result2 = {'cards_played': 10, 'total_points': 5}
        
        comparison = Evaluator.compare_results(result1, result2)
        
        self.assertEqual(comparison, 1)
    
    def test_compare_results_result2_better(self):
        """result2の方が良い場合"""
        result1 = {'cards_played': 10, 'total_points': 5}
        result2 = {'cards_played': 20, 'total_points': 5}
        
        comparison = Evaluator.compare_results(result1, result2)
        
        self.assertEqual(comparison, -1)
    
    def test_compare_results_equal(self):
        """同じスコアの場合"""
        result1 = {'cards_played': 10, 'total_points': 5}
        result2 = {'cards_played': 10, 'total_points': 5}
        
        comparison = Evaluator.compare_results(result1, result2)
        
        self.assertEqual(comparison, 0)
    
    def test_normalize_score_zero(self):
        """スコアが0の場合"""
        score = Evaluator.normalize_score(0, 0)
        
        self.assertEqual(score, 0.0)
    
    def test_normalize_score_max_cards(self):
        """最大カード枚数の場合"""
        score = Evaluator.normalize_score(70, 0)
        
        # (70/70 * 0.8) + (0 * 0.2) = 0.8
        self.assertAlmostEqual(score, 0.8)
    
    def test_normalize_score_max_points(self):
        """最大ポイントの場合"""
        score = Evaluator.normalize_score(0, 50)
        
        # (0 * 0.8) + (50/50 * 0.2) = 0.2
        self.assertAlmostEqual(score, 0.2)
    
    def test_normalize_score_perfect(self):
        """完璧なスコアの場合"""
        score = Evaluator.normalize_score(70, 50)
        
        # (70/70 * 0.8) + (50/50 * 0.2) = 1.0
        self.assertAlmostEqual(score, 1.0)
    
    def test_normalize_score_typical(self):
        """典型的なスコアの場合"""
        score = Evaluator.normalize_score(20, 5)
        
        # (20/70 * 0.8) + (5/50 * 0.2) = 0.228...
        expected = (20/70 * 0.8) + (5/50 * 0.2)
        self.assertAlmostEqual(score, expected)


if __name__ == '__main__':
    unittest.main()
