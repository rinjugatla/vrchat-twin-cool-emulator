"""
IS-MCTS統合テスト
実際のゲーム状況でIS-MCTSが正しく動作するかを確認
"""

import unittest
from src.models.card import Card
from src.models.suit import Suit
from src.controllers.game_state import GameState
from src.controllers.observable_game_state import ObservableGameState
from src.controllers.determinizer import Determinizer
from src.controllers.information_set import InformationSet
from src.controllers.ismcts_engine import ISMCTSEngine
from src.controllers.ismcts_strategy import ISMCTSStrategy


class TestISMCTSIntegration(unittest.TestCase):
    """IS-MCTS統合テストケース"""
    
    def test_determinizer_basic(self):
        """決定化が正しく生成される"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 何手かプレイ
        for _ in range(5):
            hand = game_state.get_hand()
            field = game_state.get_field()
            
            if len(hand.get_cards()) > 0:
                card = hand.get_cards()[0]
                game_state.play_card(card, 1)
        
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        # 決定化を生成
        det_state = Determinizer.create_determinization(obs_state, seed=123)
        
        # 手札と場は保持されている
        self.assertEqual(
            len(det_state.get_hand().get_cards()),
            len(obs_state.hand.get_cards())
        )
        
        # 山札が生成されている
        self.assertGreater(det_state.get_deck().remaining_count(), 0)
        
        # 未出現カード数の確認
        unplayed_count = Determinizer.get_unplayed_card_count(obs_state)
        expected_count = 80 - len(obs_state.hand.get_cards()) - len(obs_state.played_cards)
        self.assertEqual(unplayed_count, expected_count)
    
    def test_information_set_from_game_state(self):
        """ゲーム状態から情報セットを正しく生成できる"""
        game_state = GameState(seed=42)
        
        # 何手かプレイ
        for _ in range(3):
            hand = game_state.get_hand()
            if len(hand.get_cards()) > 0:
                card = hand.get_cards()[0]
                game_state.play_card(card, 1)
        
        # 情報セットを作成
        info_set = InformationSet(
            game_state.get_hand(),
            game_state.get_field(),
            len(game_state.get_played_cards())
        )
        
        # 情報セットが作成されている
        self.assertIsNotNone(info_set)
        self.assertEqual(len(info_set.hand_cards), len(game_state.get_hand().get_cards()))
    
    def test_ismcts_engine_search(self):
        """ISMCTSEngineが探索を実行できる"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 数手プレイして途中の状態を作る
        for _ in range(3):
            hand = game_state.get_hand()
            if len(hand.get_cards()) > 0:
                card = hand.get_cards()[0]
                game_state.play_card(card, 1)
        
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        # IS-MCTS探索を実行（少ないイテレーション数でテスト）
        engine = ISMCTSEngine(verbose=False)
        best_move, stats = engine.search(obs_state, num_iterations=50)
        
        # 最良の手が返される
        self.assertIsNotNone(best_move)
        
        # 統計情報が正しく返される
        self.assertIn('total_visits', stats)
        self.assertIn('num_children', stats)
        self.assertIn('best_move', stats)
        self.assertIn('info_set_cache_size', stats)
        
        # 訪問回数が記録されている
        self.assertGreater(stats['total_visits'], 0)
        
        # 情報セットキャッシュが構築されている
        self.assertGreater(stats['info_set_cache_size'], 0)
        
        print(f"\n  IS-MCTS統計:")
        print(f"    訪問回数: {stats['total_visits']}")
        print(f"    子ノード数: {stats['num_children']}")
        print(f"    キャッシュサイズ: {stats['info_set_cache_size']}")
        print(f"    最良の手: {stats['best_move']}")
    
    def test_ismcts_strategy_interface(self):
        """ISMCTSStrategyインターフェースが正しく動作する"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 数手プレイ
        for _ in range(3):
            hand = game_state.get_hand()
            if len(hand.get_cards()) > 0:
                card = hand.get_cards()[0]
                game_state.play_card(card, 1)
        
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        # IS-MCTS戦略を使用
        strategy = ISMCTSStrategy(num_iterations=30, verbose=False)
        best_move = strategy.get_best_move(obs_state)
        
        # 最良の手が返される
        self.assertIsNotNone(best_move)
        self.assertEqual(len(best_move), 2)  # (card, slot_number)
        
        card, slot_number = best_move
        self.assertIsInstance(card, Card)
        self.assertIn(slot_number, [1, 2])
        
        print(f"\n  推奨された手: {card} をスロット{slot_number}に配置")
    
    def test_multiple_determinizations(self):
        """複数の決定化が異なる山札を生成する"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 数手プレイ
        for _ in range(5):
            hand = game_state.get_hand()
            if len(hand.get_cards()) > 0:
                card = hand.get_cards()[0]
                game_state.play_card(card, 1)
        
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        # 複数の決定化を生成
        determinizations = Determinizer.create_multiple_determinizations(
            obs_state,
            count=10
        )
        
        self.assertEqual(len(determinizations), 10)
        
        # 各決定化で山札が異なる可能性が高い
        deck_sizes = [det.get_deck().remaining_count() for det in determinizations]
        
        # 全て同じサイズであるべき（未出現カード - 除外10枚）
        self.assertEqual(len(set(deck_sizes)), 1)
        
        print(f"\n  決定化数: {len(determinizations)}")
        print(f"  各山札サイズ: {deck_sizes[0]}枚")
    
    def test_ismcts_full_game_simulation(self):
        """IS-MCTSを使って1ゲームをシミュレート"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # IS-MCTS戦略を作成
        strategy = ISMCTSStrategy(num_iterations=20, verbose=False)
        
        turn_count = 0
        max_turns = 10  # テストなので10ターンで制限
        
        while turn_count < max_turns:
            # 有効な手があるか確認
            from src.controllers.move_validator import MoveValidator
            if not MoveValidator.has_valid_move(game_state.get_hand(), game_state.get_field()):
                break
            
            # 観測可能状態を構築
            obs_state = ObservableGameState.from_game_state(
                game_state,
                game_state.get_played_cards()
            )
            
            # IS-MCTSで最良の手を取得
            best_move = strategy.get_best_move(obs_state)
            
            if best_move is None:
                break
            
            card, slot = best_move
            
            # 手を実行
            success = game_state.play_card(card, slot)
            self.assertTrue(success)
            
            turn_count += 1
        
        # ゲームが進行した
        self.assertGreater(turn_count, 0)
        self.assertGreater(game_state.get_cards_played_count(), 0)
        
        print(f"\n  ゲームシミュレーション:")
        print(f"    ターン数: {turn_count}")
        print(f"    場に出したカード: {game_state.get_cards_played_count()}枚")
        print(f"    獲得ポイント: {game_state.get_total_points()}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
