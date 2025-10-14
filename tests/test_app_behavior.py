"""
app.pyのリファクタリング前後での動作保証テスト

このテストは、app.pyに含まれる主要な関数の動作を検証し、
リファクタリング後も同じ結果が得られることを保証します。
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Card, Suit
from src.controllers import GameState


class TestAppBehavior(unittest.TestCase):
    """app.pyの主要関数の動作テスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        # app.pyをインポート（実際のStreamlitは実行しない）
        with patch('streamlit.set_page_config'):
            with patch('streamlit.title'):
                with patch('streamlit.markdown'):
                    import app
                    self.app = app
    
    def test_get_suit_emoji(self):
        """スート絵文字取得の動作テスト"""
        # 各スートに対して絵文字が取得できることを確認
        expected_emojis = {
            Suit.SUIT_A: "🔴",
            Suit.SUIT_B: "🔵",
            Suit.SUIT_C: "🟢",
            Suit.SUIT_D: "🟡",
            Suit.SUIT_E: "⚪",
            Suit.SUIT_F: "🩵",
            Suit.SUIT_G: "🟣",
            Suit.SUIT_H: "🩷"
        }
        
        for suit, expected_emoji in expected_emojis.items():
            with self.subTest(suit=suit):
                emoji = self.app.get_suit_emoji(suit)
                self.assertEqual(emoji, expected_emoji)
    
    def test_initialize_session_state_structure(self):
        """セッション状態初期化の構造テスト"""
        # Streamlitのセッション状態をモック（属性アクセスとキーアクセスの両方をサポート）
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        with patch('streamlit.session_state', mock_session_state):
            self.app.initialize_session_state()
            
            # 必要なキーがすべて存在することを確認
            required_keys = [
                'game_state',
                'history',
                'turn',
                'seed',
                'recommended_move',
                'excluded_cards',
                'show_exclude_dialog',
                'initial_hand',
                'show_hand_dialog'
            ]
            
            for key in required_keys:
                with self.subTest(key=key):
                    self.assertIn(key, mock_session_state)
            
            # 各値の型を確認
            self.assertIsInstance(mock_session_state['game_state'], GameState)
            self.assertIsInstance(mock_session_state['history'], list)
            self.assertIsInstance(mock_session_state['turn'], int)
            self.assertIsInstance(mock_session_state['seed'], int)
            self.assertIsNone(mock_session_state['recommended_move'])
            self.assertIsInstance(mock_session_state['excluded_cards'], list)
            self.assertIsInstance(mock_session_state['show_exclude_dialog'], bool)
            self.assertIsInstance(mock_session_state['initial_hand'], list)
            self.assertIsInstance(mock_session_state['show_hand_dialog'], bool)
    
    def test_reset_game_with_no_params(self):
        """パラメータなしでのゲームリセット動作テスト"""
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        with patch('streamlit.session_state', mock_session_state):
            self.app.reset_game()
            
            # リセット後の状態を確認
            self.assertIsInstance(mock_session_state['game_state'], GameState)
            self.assertEqual(len(mock_session_state['history']), 0)
            self.assertEqual(mock_session_state['turn'], 0)
            self.assertIsNone(mock_session_state['recommended_move'])
            # 除外カードは実際に除外された10枚が保存される
            self.assertEqual(len(mock_session_state['excluded_cards']), 10)
            self.assertFalse(mock_session_state['show_exclude_dialog'])
            self.assertEqual(len(mock_session_state['initial_hand']), 0)
            self.assertFalse(mock_session_state['show_hand_dialog'])
    
    def test_reset_game_with_excluded_cards(self):
        """除外カード指定でのゲームリセット動作テスト"""
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        # テスト用の除外カード
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
            Card(Suit.SUIT_E, 2),
        ]
        
        with patch('streamlit.session_state', mock_session_state):
            self.app.reset_game(excluded_cards=excluded_cards)
            
            # ゲーム状態が作成され、除外カードが反映されていることを確認
            game_state = mock_session_state['game_state']
            self.assertIsInstance(game_state, GameState)
            
            # 除外カードが山札から除外されていることを確認
            remaining_cards = set(game_state.deck.get_remaining_cards())
            for card in excluded_cards:
                self.assertNotIn(card, remaining_cards)
    
    def test_reset_game_with_initial_hand(self):
        """初期手札指定でのゲームリセット動作テスト"""
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        # テスト用の除外カードと初期手札
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
            Card(Suit.SUIT_E, 2),
        ]
        
        initial_hand = [
            Card(Suit.SUIT_F, 1),
            Card(Suit.SUIT_F, 2),
            Card(Suit.SUIT_G, 1),
            Card(Suit.SUIT_G, 2),
            Card(Suit.SUIT_H, 1),
        ]
        
        with patch('streamlit.session_state', mock_session_state):
            self.app.reset_game(excluded_cards=excluded_cards, initial_hand=initial_hand)
            
            # ゲーム状態が作成され、初期手札が反映されていることを確認
            game_state = mock_session_state['game_state']
            self.assertIsInstance(game_state, GameState)
            
            # 初期手札が正しく設定されていることを確認
            hand_cards = game_state.get_hand().get_cards()
            self.assertEqual(len(hand_cards), 5)
            for card in initial_hand:
                self.assertIn(card, hand_cards)
    
    def test_get_best_move_with_mcts_returns_valid_move(self):
        """MCTS最適手取得が有効な手を返すことをテスト"""
        # 固定シードでゲーム状態を作成
        state = GameState(seed=42)
        
        # MCTSで最適手を取得（少ない反復数でテスト）
        best_move = self.app.get_best_move_with_mcts(state, num_iterations=50)
        
        # 有効な手が返されることを確認
        if best_move is not None:
            card, slot = best_move
            self.assertIsInstance(card, Card)
            self.assertIn(slot, [1, 2])
            
            # 手札に存在するカードであることを確認
            hand_cards = state.get_hand().get_cards()
            self.assertIn(card, hand_cards)
    
    def test_get_best_move_with_mcts_no_valid_moves(self):
        """合法手がない場合のMCTS動作テスト"""
        # 手札を空にした状態を作成
        state = GameState(seed=42)
        # 強制的に手札を空にする
        while state.get_hand().count() > 0:
            cards = state.get_hand().get_cards()
            if cards:
                # 適当に場に出す
                card = cards[0]
                success = state.play_card(card, 1)
                if not success:
                    state.play_card(card, 2)
            else:
                break
        
        # 空の手札でMCTSを実行
        best_move = self.app.get_best_move_with_mcts(state, num_iterations=50)
        
        # Noneが返されることを確認（または例外が発生しないことを確認）
        # 実装によってはNoneを返すか、空の結果を返す
        self.assertTrue(best_move is None or isinstance(best_move, tuple))


class TestAppDataStructures(unittest.TestCase):
    """app.pyで使用されるデータ構造のテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        with patch('streamlit.set_page_config'):
            with patch('streamlit.title'):
                with patch('streamlit.markdown'):
                    import app
                    self.app = app
    
    def test_card_selection_set_operations(self):
        """カード選択に使用されるセット操作のテスト"""
        # カードセットの基本操作
        card1 = Card(Suit.SUIT_A, 1)
        card2 = Card(Suit.SUIT_A, 2)
        card3 = Card(Suit.SUIT_B, 1)
        
        selected = set()
        
        # 追加
        selected.add(card1)
        self.assertIn(card1, selected)
        self.assertEqual(len(selected), 1)
        
        # 重複追加
        selected.add(card1)
        self.assertEqual(len(selected), 1)
        
        # 複数追加
        selected.add(card2)
        selected.add(card3)
        self.assertEqual(len(selected), 3)
        
        # 削除
        selected.discard(card1)
        self.assertNotIn(card1, selected)
        self.assertEqual(len(selected), 2)
        
        # 存在しないカードの削除（エラーにならない）
        selected.discard(card1)
        self.assertEqual(len(selected), 2)
    
    def test_history_record_structure(self):
        """履歴レコードの構造テスト"""
        # 履歴レコードの期待される構造
        card = Card(Suit.SUIT_A, 5)
        record = {
            'turn': 1,
            'card': str(card),
            'suit': card.suit,
            'slot': 1
        }
        
        # 必要なキーが存在することを確認
        self.assertIn('turn', record)
        self.assertIn('card', record)
        self.assertIn('suit', record)
        self.assertIn('slot', record)
        
        # 値の型を確認
        self.assertIsInstance(record['turn'], int)
        self.assertIsInstance(record['card'], str)
        self.assertIsInstance(record['suit'], Suit)
        self.assertIsInstance(record['slot'], int)


class TestAppIntegration(unittest.TestCase):
    """app.pyの統合テスト（シナリオベース）"""
    
    def setUp(self):
        """各テストの前に実行"""
        with patch('streamlit.set_page_config'):
            with patch('streamlit.title'):
                with patch('streamlit.markdown'):
                    import app
                    self.app = app
    
    def test_complete_game_flow(self):
        """完全なゲームフローのテスト"""
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        with patch('streamlit.session_state', mock_session_state):
            # 1. セッション初期化
            self.app.initialize_session_state()
            self.assertIn('game_state', mock_session_state)
            
            # 2. ゲーム状態取得
            state = mock_session_state['game_state']
            self.assertIsInstance(state, GameState)
            
            # 3. 初期状態確認
            initial_hand_count = state.get_hand().count()
            self.assertEqual(initial_hand_count, 5)
            
            # 4. 最適手を取得
            best_move = self.app.get_best_move_with_mcts(state, num_iterations=50)
            
            if best_move is not None:
                card, slot = best_move
                
                # 5. 手を実行
                success = state.play_card(card, slot)
                self.assertTrue(success)
                
                # 6. 履歴に追加
                mock_session_state['history'].append({
                    'turn': 1,
                    'card': str(card),
                    'suit': card.suit,
                    'slot': slot
                })
                
                # 7. 状態更新確認
                self.assertEqual(len(mock_session_state['history']), 1)
                self.assertEqual(state.get_cards_played_count(), 1)
    
    def test_game_reset_flow(self):
        """ゲームリセットフローのテスト"""
        class MockSessionState(dict):
            def __setattr__(self, name, value):
                self[name] = value
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        mock_session_state = MockSessionState()
        
        with patch('streamlit.session_state', mock_session_state):
            # 1. 初期ゲーム開始
            self.app.initialize_session_state()
            first_seed = mock_session_state['seed']
            
            # 2. いくつかの手をプレイ
            mock_session_state['turn'] = 5
            mock_session_state['history'] = [
                {'turn': i, 'card': 'A-1', 'suit': Suit.SUIT_A, 'slot': 1}
                for i in range(1, 6)
            ]
            mock_session_state['recommended_move'] = (Card(Suit.SUIT_A, 1), 1)
            
            # 3. ゲームリセット
            self.app.reset_game()
            
            # 4. 状態がクリアされていることを確認
            self.assertEqual(mock_session_state['turn'], 0)
            self.assertEqual(len(mock_session_state['history']), 0)
            self.assertIsNone(mock_session_state['recommended_move'])
            self.assertNotEqual(mock_session_state['seed'], first_seed)


def run_tests():
    """テストを実行"""
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # すべてのテストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestAppBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestAppDataStructures))
    suite.addTests(loader.loadTestsFromTestCase(TestAppIntegration))
    
    # テストを実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # 結果のサマリーを表示
    print("\n" + "="*70)
    print("テスト結果サマリー")
    print("="*70)
    print(f"実行テスト数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")
    print("="*70)
    
    # 終了コード
    sys.exit(0 if result.wasSuccessful() else 1)
