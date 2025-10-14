"""
セッション状態での除外カード管理のテスト
"""

import unittest
from src.models import Card, Suit
from src.controllers import GameState


class TestExcludedCardsInSession(unittest.TestCase):
    """除外カードがセッション状態で正しく管理されているかをテスト"""
    
    def test_excluded_cards_stored_after_initialization(self):
        """ゲーム初期化後、除外カードが正しく取得できることを確認"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 除外カードを取得
        excluded_cards = game_state.deck.get_excluded_cards()
        
        # 除外カードが10枚であることを確認
        self.assertEqual(len(excluded_cards), 10)
        
        # 除外カードが重複していないことを確認
        self.assertEqual(len(set(excluded_cards)), 10)
    
    def test_excluded_cards_not_in_remaining_deck(self):
        """除外カードが山札に含まれていないことを確認"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 除外カードを取得
        excluded_cards = game_state.deck.get_excluded_cards()
        
        # 山札の残りカードを取得
        remaining_cards = game_state.deck.get_remaining_cards()
        
        # 除外カードが山札に含まれていないことを確認
        for card in excluded_cards:
            self.assertNotIn(card, remaining_cards)
    
    def test_excluded_cards_not_in_hand(self):
        """除外カードが初期手札に含まれていないことを確認"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 除外カードを取得
        excluded_cards = game_state.deck.get_excluded_cards()
        
        # 初期手札を取得
        hand_cards = game_state.hand.get_cards()
        
        # 除外カードが手札に含まれていないことを確認
        for card in excluded_cards:
            self.assertNotIn(card, hand_cards)
    
    def test_specific_excluded_cards(self):
        """指定した除外カードでゲームが初期化できることを確認"""
        # 除外するカードを指定
        excluded_cards = [
            Card(Suit.SUIT_A, 1),
            Card(Suit.SUIT_A, 2),
            Card(Suit.SUIT_B, 1),
            Card(Suit.SUIT_B, 2),
            Card(Suit.SUIT_C, 1),
            Card(Suit.SUIT_C, 2),
            Card(Suit.SUIT_D, 1),
            Card(Suit.SUIT_D, 2),
            Card(Suit.SUIT_E, 1),
            Card(Suit.SUIT_E, 2)
        ]
        
        # ゲーム状態を作成
        game_state = GameState(seed=42, excluded_cards=excluded_cards)
        
        # 除外カードが正しく設定されていることを確認
        actual_excluded = game_state.deck.get_excluded_cards()
        self.assertEqual(set(excluded_cards), set(actual_excluded))
        
        # 山札に除外カードが含まれていないことを確認
        remaining_cards = game_state.deck.get_remaining_cards()
        for card in excluded_cards:
            self.assertNotIn(card, remaining_cards)
    
    def test_add_card_to_hand_from_remaining_only(self):
        """手札追加は山札の残りカードからのみ可能であることを確認"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 除外カードを取得
        excluded_cards = game_state.deck.get_excluded_cards()
        
        # 除外カードを手札に追加しようとする（失敗するはず）
        excluded_card = excluded_cards[0]
        result = game_state.add_card_to_hand(excluded_card)
        
        # 追加が失敗することを確認
        self.assertFalse(result)
        
        # 手札に除外カードが含まれていないことを確認
        hand_cards = game_state.hand.get_cards()
        self.assertNotIn(excluded_card, hand_cards)
    
    def test_add_card_to_hand_from_remaining_succeeds(self):
        """山札の残りカードは手札に追加できることを確認"""
        # ゲーム状態を作成
        game_state = GameState(seed=42)
        
        # 山札の残りカードを取得
        remaining_cards = game_state.deck.get_remaining_cards()
        
        # 残りカードから1枚を手札に追加
        card_to_add = remaining_cards[0]
        
        # 手札に既に含まれていないことを確認
        hand_cards_before = game_state.hand.get_cards()
        if card_to_add in hand_cards_before:
            # 既に手札にある場合は別のカードを選択
            for card in remaining_cards:
                if card not in hand_cards_before:
                    card_to_add = card
                    break
        
        result = game_state.add_card_to_hand(card_to_add)
        
        # 追加が成功することを確認
        self.assertTrue(result)
        
        # 手札にカードが含まれていることを確認
        hand_cards_after = game_state.hand.get_cards()
        self.assertIn(card_to_add, hand_cards_after)


if __name__ == '__main__':
    unittest.main()
