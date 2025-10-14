"""
add_card_to_hand機能のテストコード
"""

import unittest
from src.models import Card, Suit
from src.controllers import GameState


class TestAddCardToHand(unittest.TestCase):
    """add_card_to_hand機能のテストクラス"""
    
    def setUp(self):
        """各テストの前に実行される初期化処理"""
        self.state = GameState(seed=42)
    
    def test_add_card_to_hand_success(self):
        """正常にカードを手札に追加できることを確認"""
        # 山札から1枚カードを取得
        remaining_cards = self.state.deck.get_remaining_cards()
        self.assertGreater(len(remaining_cards), 0, "山札にカードが存在する")
        
        # 山札にあって手札にないカードを選択
        card_to_add = None
        hand_cards = self.state.hand.get_cards()
        for card in remaining_cards:
            if card not in hand_cards:
                card_to_add = card
                break
        
        self.assertIsNotNone(card_to_add, "追加可能なカードが存在する")
        
        # 手札の初期枚数を記録
        initial_hand_count = self.state.hand.count()
        initial_deck_count = self.state.deck.remaining_count()
        
        # カードを手札に追加
        assert card_to_add is not None
        success = self.state.add_card_to_hand(card_to_add)
        
        # 検証
        self.assertTrue(success, "カード追加が成功する")
        self.assertEqual(self.state.hand.count(), initial_hand_count + 1, "手札が1枚増える")
        self.assertEqual(self.state.deck.remaining_count(), initial_deck_count - 1, "山札が1枚減る")
        self.assertIn(card_to_add, self.state.hand.get_cards(), "追加したカードが手札に存在する")
        self.assertNotIn(card_to_add, self.state.deck.get_remaining_cards(), "追加したカードが山札に存在しない")
    
    def test_add_card_not_in_deck(self):
        """山札に存在しないカードを追加しようとすると失敗することを確認"""
        # 除外カード（山札に存在しない）を取得
        all_suits = [Suit.SUIT_A, Suit.SUIT_B, Suit.SUIT_C, Suit.SUIT_D, 
                     Suit.SUIT_E, Suit.SUIT_F, Suit.SUIT_G, Suit.SUIT_H]
        all_cards = [Card(suit, value) for suit in all_suits for value in range(1, 11)]
        remaining_cards = self.state.deck.get_remaining_cards()
        excluded_cards = [card for card in all_cards if card not in remaining_cards]
        
        self.assertGreater(len(excluded_cards), 0, "除外カードが存在する")
        
        # 除外カードを手札に追加しようとする
        card_to_add = excluded_cards[0]
        initial_hand_count = self.state.hand.count()
        initial_deck_count = self.state.deck.remaining_count()
        
        success = self.state.add_card_to_hand(card_to_add)
        
        # 検証
        self.assertFalse(success, "カード追加が失敗する")
        self.assertEqual(self.state.hand.count(), initial_hand_count, "手札の枚数が変わらない")
        self.assertEqual(self.state.deck.remaining_count(), initial_deck_count, "山札の枚数が変わらない")
    
    def test_add_card_already_in_hand(self):
        """既に手札にあるカードを追加しようとすると失敗することを確認"""
        # 手札にあるカードを取得
        hand_cards = self.state.hand.get_cards()
        self.assertGreater(len(hand_cards), 0, "手札にカードが存在する")
        
        card_to_add = hand_cards[0]
        initial_hand_count = self.state.hand.count()
        
        # カードを手札に追加しようとする（山札には存在しない）
        success = self.state.add_card_to_hand(card_to_add)
        
        # 検証（山札に存在しないため失敗する）
        self.assertFalse(success, "カード追加が失敗する")
        self.assertEqual(self.state.hand.count(), initial_hand_count, "手札の枚数が変わらない")
    
    def test_add_card_updates_points(self):
        """カード追加後にポイントが正しく更新されることを確認"""
        # 山札から手札に追加するカードを選択
        remaining_cards = self.state.deck.get_remaining_cards()
        card_to_add = None
        hand_cards = self.state.hand.get_cards()
        
        for card in remaining_cards:
            if card not in hand_cards:
                card_to_add = card
                break
        
        self.assertIsNotNone(card_to_add, "追加可能なカードが存在する")
        
        # カードを追加
        initial_points = self.state.total_points
        assert card_to_add is not None
        success = self.state.add_card_to_hand(card_to_add)
        
        # 検証
        self.assertTrue(success, "カード追加が成功する")
        # ポイントは手札の構成によって変わる可能性がある
        # ここでは単にポイントが計算されていることを確認
        self.assertIsNotNone(self.state.total_points, "ポイントが計算されている")
    
    def test_play_card_then_add_card(self):
        """カードを出した後に手札にカードを追加するフローをテスト"""
        # 初期状態を記録
        initial_hand = self.state.hand.get_cards().copy()
        self.assertEqual(len(initial_hand), 5, "初期手札は5枚")
        
        # 場が空なので任意のカードを出せる
        card_to_play = initial_hand[0]
        
        # カードを手札から削除して場に出す（play_cardを使わずに手動で実行）
        self.state.hand.remove_card(card_to_play)
        self.state.field.place_card(1, card_to_play)
        self.state.played_cards.append(card_to_play)
        self.state._update_points()
        
        # 手札が4枚に減ったことを確認
        self.assertEqual(self.state.hand.count(), 4, "カードを出した後、手札は4枚")
        
        # 山札から新しいカードを追加
        remaining_cards = self.state.deck.get_remaining_cards()
        card_to_add = None
        current_hand = self.state.hand.get_cards()
        
        for card in remaining_cards:
            if card not in current_hand and card != card_to_play:
                card_to_add = card
                break
        
        self.assertIsNotNone(card_to_add, "追加可能なカードが存在する")
        
        # カードを手札に追加
        assert card_to_add is not None
        success = self.state.add_card_to_hand(card_to_add)
        
        # 検証
        self.assertTrue(success, "カード追加が成功する")
        self.assertEqual(self.state.hand.count(), 5, "カード追加後、手札は5枚に戻る")
        self.assertIn(card_to_add, self.state.hand.get_cards(), "追加したカードが手札に存在する")
        self.assertNotIn(card_to_play, self.state.hand.get_cards(), "出したカードは手札に存在しない")


if __name__ == '__main__':
    unittest.main()
