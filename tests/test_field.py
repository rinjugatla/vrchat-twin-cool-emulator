"""
field.pyのテスト
"""

import unittest
from src.models.field import Field
from src.models.field_slot import FieldSlot
from src.models.card import Card
from src.models.suit import Suit


class TestFieldSlot(unittest.TestCase):
    """FieldSlotクラスのテスト"""
    
    def test_slot_initialization(self):
        """スロットの初期化テスト"""
        slot = FieldSlot()
        self.assertTrue(slot.is_empty())
        self.assertEqual(slot.count(), 0)
        self.assertIsNone(slot.get_top_card())
    
    def test_slot_place_card(self):
        """カードを置くテスト"""
        slot = FieldSlot()
        card = Card(Suit.SUIT_A, 5)
        slot.place_card(card)
        
        self.assertFalse(slot.is_empty())
        self.assertEqual(slot.count(), 1)
        self.assertEqual(slot.get_top_card(), card)
    
    def test_slot_place_multiple_cards(self):
        """複数のカードを置くテスト"""
        slot = FieldSlot()
        card1 = Card(Suit.SUIT_A, 1)
        card2 = Card(Suit.SUIT_B, 2)
        card3 = Card(Suit.SUIT_C, 3)
        
        slot.place_card(card1)
        slot.place_card(card2)
        slot.place_card(card3)
        
        self.assertEqual(slot.count(), 3)
        self.assertEqual(slot.get_top_card(), card3)  # 最後に置いたカードが一番上
    
    def test_slot_get_all_cards(self):
        """全カードを取得するテスト"""
        slot = FieldSlot()
        card1 = Card(Suit.SUIT_D, 4)
        card2 = Card(Suit.SUIT_E, 5)
        
        slot.place_card(card1)
        slot.place_card(card2)
        
        all_cards = slot.get_all_cards()
        self.assertEqual(len(all_cards), 2)
        self.assertEqual(all_cards[0], card1)
        self.assertEqual(all_cards[1], card2)


class TestField(unittest.TestCase):
    """Fieldクラスのテスト"""
    
    def test_field_initialization(self):
        """場の初期化テスト"""
        field = Field()
        self.assertIsNone(field.get_top_card(1))
        self.assertIsNone(field.get_top_card(2))
        self.assertEqual(field.total_cards_count(), 0)
    
    def test_field_place_card_slot1(self):
        """スロット1にカードを置くテスト"""
        field = Field()
        card = Card(Suit.SUIT_F, 6)
        field.place_card(1, card)
        
        self.assertEqual(field.get_top_card(1), card)
        self.assertIsNone(field.get_top_card(2))
        self.assertEqual(field.total_cards_count(), 1)
    
    def test_field_place_card_slot2(self):
        """スロット2にカードを置くテスト"""
        field = Field()
        card = Card(Suit.SUIT_G, 7)
        field.place_card(2, card)
        
        self.assertIsNone(field.get_top_card(1))
        self.assertEqual(field.get_top_card(2), card)
        self.assertEqual(field.total_cards_count(), 1)
    
    def test_field_place_cards_both_slots(self):
        """両方のスロットにカードを置くテスト"""
        field = Field()
        card1 = Card(Suit.SUIT_H, 8)
        card2 = Card(Suit.SUIT_A, 9)
        
        field.place_card(1, card1)
        field.place_card(2, card2)
        
        self.assertEqual(field.get_top_card(1), card1)
        self.assertEqual(field.get_top_card(2), card2)
        self.assertEqual(field.total_cards_count(), 2)
    
    def test_field_invalid_slot_number(self):
        """無効なスロット番号のテスト"""
        field = Field()
        card = Card(Suit.SUIT_B, 3)
        
        with self.assertRaises(ValueError):
            field.place_card(0, card)
        
        with self.assertRaises(ValueError):
            field.place_card(3, card)
    
    def test_field_get_slot(self):
        """スロット取得のテスト"""
        field = Field()
        slot1 = field.get_slot(1)
        slot2 = field.get_slot(2)
        
        self.assertIsInstance(slot1, FieldSlot)
        self.assertIsInstance(slot2, FieldSlot)
        self.assertIsNot(slot1, slot2)
    
    def test_field_get_slot_count(self):
        """スロットのカード枚数取得のテスト"""
        field = Field()
        
        # 初期状態
        self.assertEqual(field.get_slot_count(1), 0)
        self.assertEqual(field.get_slot_count(2), 0)
        
        # スロット1にカードを追加
        field.place_card(1, Card(Suit.SUIT_A, 1))
        field.place_card(1, Card(Suit.SUIT_A, 2))
        self.assertEqual(field.get_slot_count(1), 2)
        self.assertEqual(field.get_slot_count(2), 0)
        
        # スロット2にカードを追加
        field.place_card(2, Card(Suit.SUIT_B, 3))
        self.assertEqual(field.get_slot_count(1), 2)
        self.assertEqual(field.get_slot_count(2), 1)
    
    def test_get_all_cards(self):
        """スロットの全カードを取得するテスト"""
        field = Field()
        
        # カードを追加
        card1 = Card(Suit.SUIT_A, 1)
        card2 = Card(Suit.SUIT_A, 2)
        card3 = Card(Suit.SUIT_B, 3)
        
        field.place_card(1, card1)
        field.place_card(1, card2)
        field.place_card(2, card3)
        
        # スロット1の全カード取得
        slot1_cards = field.get_all_cards(1)
        self.assertEqual(len(slot1_cards), 2)
        self.assertEqual(slot1_cards[0], card1)
        self.assertEqual(slot1_cards[1], card2)
        
        # スロット2の全カード取得
        slot2_cards = field.get_all_cards(2)
        self.assertEqual(len(slot2_cards), 1)
        self.assertEqual(slot2_cards[0], card3)


if __name__ == '__main__':
    unittest.main()
