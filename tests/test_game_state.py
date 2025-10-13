"""
game_state.pyのテスト
"""

import unittest
from src.controllers.game_state import GameState
from src.models.card import Card, Suit


class TestGameState(unittest.TestCase):
    """GameStateクラスのテスト"""
    
    def test_initialization(self):
        """ゲーム状態の初期化テスト"""
        state = GameState(seed=42)
        
        # 初期手札は5枚
        self.assertEqual(state.get_hand().count(), 5)
        
        # 山札は70枚 - 5枚（初期手札）= 65枚
        self.assertEqual(state.get_deck().remaining_count(), 65)
        
        # 場は空
        self.assertEqual(state.get_cards_played_count(), 0)
        
        # ターン数は0
        self.assertEqual(state.turn_count, 0)
        
        # ゲームは終了していない
        self.assertFalse(state.is_game_over())
    
    def test_play_card_success(self):
        """カードを正常に出すテスト"""
        state = GameState(seed=42)
        
        # 手札から1枚取得
        hand_cards = state.get_hand().get_cards()
        card_to_play = hand_cards[0]
        
        # カードを出す
        result = state.play_card(card_to_play, 1)
        
        self.assertTrue(result)
        self.assertEqual(state.get_cards_played_count(), 1)
        self.assertEqual(state.turn_count, 1)
        
        # 手札は5枚のまま（1枚出して1枚引いた）
        self.assertEqual(state.get_hand().count(), 5)
        
        # 山札は1枚減っている
        self.assertEqual(state.get_deck().remaining_count(), 64)
    
    def test_play_card_not_in_hand(self):
        """手札にないカードを出そうとするテスト"""
        state = GameState(seed=42)
        
        # 手札にないカードを作成
        fake_card = Card(Suit.SUIT_H, 10)
        
        # カードを出そうとする
        result = state.play_card(fake_card, 1)
        
        self.assertFalse(result)
        self.assertEqual(state.get_cards_played_count(), 0)
        self.assertEqual(state.turn_count, 0)
    
    def test_play_multiple_cards(self):
        """複数のカードを出すテスト"""
        state = GameState(seed=42)
        
        initial_deck_count = state.get_deck().remaining_count()
        
        # 3枚カードを出す
        for i in range(3):
            hand_cards = state.get_hand().get_cards()
            card_to_play = hand_cards[0]
            slot = (i % 2) + 1  # スロット1と2を交互に使用
            
            result = state.play_card(card_to_play, slot)
            self.assertTrue(result)
        
        self.assertEqual(state.get_cards_played_count(), 3)
        self.assertEqual(state.turn_count, 3)
        self.assertEqual(state.get_hand().count(), 5)
        self.assertEqual(state.get_deck().remaining_count(), initial_deck_count - 3)
    
    def test_play_card_until_deck_empty(self):
        """山札が空になるまでカードを出すテスト"""
        state = GameState(seed=42)
        
        # 山札が空になるまでカードを出す
        # 初期: 山札65枚、手札5枚
        # カードを出すたびに山札から1枚引くので、65枚出せる
        max_plays = state.get_deck().remaining_count()
        
        for i in range(max_plays):
            hand_cards = state.get_hand().get_cards()
            if len(hand_cards) == 0:
                break
            
            card_to_play = hand_cards[0]
            slot = (i % 2) + 1
            state.play_card(card_to_play, slot)
        
        # 山札は空
        self.assertTrue(state.get_deck().is_empty())
        
        # 場に出したカードは65枚
        self.assertEqual(state.get_cards_played_count(), 65)
    
    def test_get_total_points(self):
        """ポイント取得のテスト"""
        state = GameState(seed=42)
        
        # 初期ポイントを取得
        initial_points = state.get_total_points()
        
        # ポイントは0以上
        self.assertGreaterEqual(initial_points, 0)
    
    def test_play_card_to_both_slots(self):
        """両方のスロットにカードを出すテスト"""
        state = GameState(seed=42)
        
        # スロット1にカードを出す
        hand_cards = state.get_hand().get_cards()
        card1 = hand_cards[0]
        state.play_card(card1, 1)
        
        # スロット2にカードを出す
        hand_cards = state.get_hand().get_cards()
        card2 = hand_cards[0]
        state.play_card(card2, 2)
        
        self.assertEqual(state.get_cards_played_count(), 2)
        self.assertIsNotNone(state.get_field().get_top_card(1))
        self.assertIsNotNone(state.get_field().get_top_card(2))
    
    def test_str_representation(self):
        """文字列表現のテスト"""
        state = GameState(seed=42)
        
        state_str = str(state)
        
        self.assertIn("GameState", state_str)
        self.assertIn("Turn", state_str)
        self.assertIn("Hand", state_str)
        self.assertIn("Field", state_str)


if __name__ == '__main__':
    unittest.main()
