"""
ゲーム状態の評価関数
ゲーム終了時の状態を評価してスコアを算出
"""

from typing import Dict, Any


class Evaluator:
    """
    ゲーム状態を評価するクラス
    
    評価基準:
    1. 場に出したカードの枚数（最優先）
    2. 獲得ポイント（次点）
    """
    
    # 重み係数
    CARDS_WEIGHT = 10.0  # カード枚数の重み
    POINTS_WEIGHT = 1.0  # ポイントの重み
    
    @staticmethod
    def evaluate(result: Dict[str, Any]) -> float:
        """
        ゲーム結果を評価してスコアを算出
        
        Args:
            result: ゲーム結果の辞書
                {
                    'cards_played': 場に出したカードの枚数,
                    'total_points': 獲得ポイント,
                    'turn_count': ターン数,
                    'final_hand_size': 最終手札枚数
                }
        
        Returns:
            評価スコア（高いほど良い）
        """
        cards_played = result.get('cards_played', 0)
        total_points = result.get('total_points', 0)
        
        # スコア = (カード枚数 × 重み) + (ポイント × 重み)
        score = (cards_played * Evaluator.CARDS_WEIGHT) + (total_points * Evaluator.POINTS_WEIGHT)
        
        return score
    
    @staticmethod
    def compare_results(result1: Dict[str, Any], result2: Dict[str, Any]) -> int:
        """
        2つのゲーム結果を比較
        
        Args:
            result1: 1つ目のゲーム結果
            result2: 2つ目のゲーム結果
        
        Returns:
            1: result1の方が良い
            0: 同じ
            -1: result2の方が良い
        """
        score1 = Evaluator.evaluate(result1)
        score2 = Evaluator.evaluate(result2)
        
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            return 0
    
    @staticmethod
    def normalize_score(cards_played: int, total_points: int, max_cards: int = 70) -> float:
        """
        スコアを0-1の範囲に正規化
        
        Args:
            cards_played: 場に出したカードの枚数
            total_points: 獲得ポイント
            max_cards: 理論上の最大カード枚数（デフォルト: 70）
        
        Returns:
            正規化されたスコア（0.0〜1.0）
        """
        # カード枚数の正規化（0〜1）
        cards_score = cards_played / max_cards
        
        # ポイントの正規化（0〜1）※50ポイントを最大と仮定
        points_score = min(total_points / 50.0, 1.0)
        
        # 重み付き平均（カード枚数を重視）
        normalized = (cards_score * 0.8) + (points_score * 0.2)
        
        return normalized
