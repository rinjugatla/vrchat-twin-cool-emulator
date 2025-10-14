"""
ObservableGameStateクラスのチE��チE
"""

import unittest
from src.models import Card, Suit
from src.controllers import ObservableGameState, GameState


class TestObservableGameState(unittest.TestCase):
    """ObservableGameStateクラスのテストケース"""
    
    def test_initialization(self):
        """初期化テスト"""
        obs_state = ObservableGameState()
        
        self.assertEqual(len(obs_state.get_hand().get_cards()), 0)
        self.assertEqual(len(obs_state.get_played_cards()), 0)
        self.assertEqual(obs_state.get_total_points(), 0)
        self.assertEqual(obs_state.turn_count, 0)
        self.assertEqual(obs_state.remaining_deck_size, 65)  # 70 - 5
        self.assertEqual(obs_state.excluded_cards_count, 10)
    
    def test_from_game_state(self):
        """GameStateからの変換テスト"""
        # GameStateを作成
        game_state = GameState(seed=42)
        
        # 何枚かプレイしたと仮定
        played_cards = [
            Card(Suit.SUIT_A, 5),
            Card(Suit.SUIT_B, 3)
        ]
        
        # ObservableGameStateに変換
        obs_state = ObservableGameState.from_game_state(game_state, played_cards)
        
        # 検証
        self.assertEqual(len(obs_state.get_hand().get_cards()), 5)  # 初期手札
        self.assertEqual(len(obs_state.get_played_cards()), 2)
        self.assertEqual(obs_state.get_total_points(), game_state.get_total_points())
    
    def test_get_unknown_cards(self):
        """未知カード取得テスト"""
        obs_state = ObservableGameState()

        # 初期状況: 手札0枚、既出0枚
        unknown_cards = obs_state.get_unknown_cards()
        self.assertEqual(len(unknown_cards), 80)  # 全カード数

        # 手札を追加
        obs_state.hand.add_card(Card(Suit.SUIT_A, 1))
        obs_state.hand.add_card(Card(Suit.SUIT_A, 2))
        
        unknown_cards = obs_state.get_unknown_cards()
        self.assertEqual(len(unknown_cards), 78)  # 80 - 2
        
        # 既出カードを追加
        obs_state.played_cards.append(Card(Suit.SUIT_B, 3))
        
        unknown_cards = obs_state.get_unknown_cards()
        self.assertEqual(len(unknown_cards), 77)  # 80 - 3
    
    def test_get_unknown_cards_no_duplicates(self):
        """未知カードに重複がないことを確かめるテスト"""
        game_state = GameState(seed=42)
        played_cards = [
            Card(Suit.SUIT_A, 5),
            Card(Suit.SUIT_B, 3)
        ]
        
        obs_state = ObservableGameState.from_game_state(game_state, played_cards)
        unknown_cards = obs_state.get_unknown_cards()

        # 重複がないことを確かめる
        unique_cards = set(unknown_cards)
        self.assertEqual(len(unknown_cards), len(unique_cards))

        # 手札と既出カードが含まれていないことを確かめる
        hand_cards = obs_state.get_hand().get_cards()
        for card in hand_cards:
            self.assertNotIn(card, unknown_cards)
        
        for card in played_cards:
            self.assertNotIn(card, unknown_cards)
    
    def test_copy(self):
        """コピーのテスト"""
        obs_state = ObservableGameState()
        obs_state.hand.add_card(Card(Suit.SUIT_A, 5))
        obs_state.played_cards.append(Card(Suit.SUIT_B, 3))
        obs_state.total_points = 10
        obs_state.turn_count = 5

        # コピー
        copied = obs_state.copy()

        # 値が同じことを確かめる
        self.assertEqual(len(copied.get_hand().get_cards()), 1)
        self.assertEqual(len(copied.get_played_cards()), 1)
        self.assertEqual(copied.total_points, 10)
        self.assertEqual(copied.turn_count, 5)

        # 独立していることを確かめる
        obs_state.hand.add_card(Card(Suit.SUIT_C, 7))
        self.assertEqual(len(obs_state.get_hand().get_cards()), 2)
        self.assertEqual(len(copied.get_hand().get_cards()), 1)  # コピーは変わらない

    def test_repr(self):
        """文字列表現のテスト"""
        obs_state = ObservableGameState()
        obs_state.turn_count = 3
        obs_state.hand.add_card(Card(Suit.SUIT_A, 5))
        obs_state.played_cards.append(Card(Suit.SUIT_B, 3))
        
        repr_str = repr(obs_state)
        self.assertIn("turn=3", repr_str)
        self.assertIn("hand=1", repr_str)
        self.assertIn("played=1", repr_str)


if __name__ == '__main__':
    unittest.main()
