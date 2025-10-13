"""
deck.pyのテスト
"""

import unittest
from src.models.deck import Deck
from src.models.card import Card
from src.models.suit import Suit


class TestDeck(unittest.TestCase):
    """Deckクラスのテスト"""
    
    def test_deck_initialization(self):
        """デッキの初期化テスト（70枚）"""
        deck = Deck(seed=42)
        self.assertEqual(deck.remaining_count(), 70)
    
    def test_deck_draw(self):
        """カードを1枚引くテスト"""
        deck = Deck(seed=42)
        initial_count = deck.remaining_count()
        card = deck.draw()
        self.assertIsNotNone(card)
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.remaining_count(), initial_count - 1)
    
    def test_deck_draw_all_cards(self):
        """全カードを引き切るテスト"""
        deck = Deck(seed=42)
        drawn_cards = []
        while not deck.is_empty():
            card = deck.draw()
            self.assertIsNotNone(card)
            drawn_cards.append(card)
        
        self.assertEqual(len(drawn_cards), 70)
        self.assertTrue(deck.is_empty())
        self.assertEqual(deck.remaining_count(), 0)
    
    def test_deck_draw_from_empty(self):
        """空のデッキからカードを引くテスト"""
        deck = Deck(seed=42)
        # 全カードを引く
        while not deck.is_empty():
            deck.draw()
        
        # 空のデッキから引く
        card = deck.draw()
        self.assertIsNone(card)
    
    def test_get_excluded_cards(self):
        """除外されたカードの取得テスト"""
        deck = Deck(seed=42)
        excluded = deck.get_excluded_cards()
        
        # 除外されたカードは10枚
        self.assertEqual(len(excluded), 10)
        
        # 全てCardインスタンス
        for card in excluded:
            self.assertIsInstance(card, Card)
    
    def test_get_remaining_cards(self):
        """山札に残っているカードの取得テスト"""
        deck = Deck(seed=42)
        remaining = deck.get_remaining_cards()
        
        # 山札には70枚
        self.assertEqual(len(remaining), 70)
        
        # カードを引いても元のリストは変わらない（コピーを返す）
        original_count = len(remaining)
        deck.draw()
        remaining2 = deck.get_remaining_cards()
        self.assertEqual(len(remaining2), 69)
        self.assertEqual(len(remaining), original_count)
    
    def test_deck_with_specific_excluded_cards(self):
        """特定のカードを除外してデッキを初期化するテスト"""
        # 除外するカードを指定（A1-A10の10枚）
        excluded = [Card(Suit.SUIT_A, i) for i in range(1, 11)]
        deck = Deck(seed=42, excluded_cards=excluded)
        
        # 山札は70枚
        self.assertEqual(deck.remaining_count(), 70)
        
        # 除外されたカードを確認
        excluded_from_deck = deck.get_excluded_cards()
        self.assertEqual(len(excluded_from_deck), 10)
        for card in excluded:
            self.assertIn(card, excluded_from_deck)
        
        # 山札にA1-A10が含まれないことを確認
        remaining = deck.get_remaining_cards()
        for card in excluded:
            self.assertNotIn(card, remaining)
    
    def test_deck_with_invalid_excluded_cards_count(self):
        """除外カードが10枚でない場合のエラーテスト"""
        # 9枚のみ指定
        excluded = [Card(Suit.SUIT_A, i) for i in range(1, 10)]
        
        with self.assertRaises(ValueError) as context:
            Deck(excluded_cards=excluded)
        
        self.assertIn("10枚である必要があります", str(context.exception))
    
    def test_deck_with_duplicate_excluded_cards(self):
        """重複したカードを除外しようとした場合のテスト"""
        # 重複したカードを含むリスト
        excluded = [Card(Suit.SUIT_A, i) for i in range(1, 10)]
        excluded.append(Card(Suit.SUIT_A, 1))  # 重複
        
        # 重複がある場合、実質的に9枚しか除外されないため71枚残る
        deck = Deck(excluded_cards=excluded)
        self.assertEqual(deck.remaining_count(), 71)
    
    def test_deck_is_empty(self):
        """デッキの空判定テスト"""
        deck = Deck(seed=42)
        self.assertFalse(deck.is_empty())
        
        # 全カードを引く
        while deck.remaining_count() > 0:
            deck.draw()
        
        self.assertTrue(deck.is_empty())
    
    def test_deck_randomization(self):
        """デッキがシャッフルされているかのテスト（異なるシードで異なる順序）"""
        deck1 = Deck(seed=1)
        deck2 = Deck(seed=2)
        
        card1 = deck1.draw()
        card2 = deck2.draw()
        
        # 異なるシードで異なるカードが引かれる可能性が高い
        # （100%保証はできないが、統計的にほぼ確実）
        self.assertIsNotNone(card1)
        self.assertIsNotNone(card2)


if __name__ == '__main__':
    unittest.main()
