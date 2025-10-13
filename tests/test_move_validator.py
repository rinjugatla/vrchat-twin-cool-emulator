"""
move_validator.pyのテスト
"""

import unittest
from src.controllers.move_validator import MoveValidator
from src.models.card import Card, Suit
from src.models.hand import Hand
from src.models.field import Field


class TestMoveValidator(unittest.TestCase):
    """MoveValidatorクラスのテスト"""
    
    def test_can_play_card_empty_slot(self):
        """空のスロットには任意のカードを出せる"""
        card = Card(Suit.SUIT_A, 5)
        result = MoveValidator.can_play_card(card, None)
        self.assertTrue(result)
    
    def test_can_play_card_same_suit(self):
        """同じスートのカードは出せる"""
        card = Card(Suit.SUIT_A, 5)
        top_card = Card(Suit.SUIT_A, 8)
        result = MoveValidator.can_play_card(card, top_card)
        self.assertTrue(result)
    
    def test_can_play_card_same_value(self):
        """同じ数値のカードは出せる"""
        card = Card(Suit.SUIT_A, 5)
        top_card = Card(Suit.SUIT_B, 5)
        result = MoveValidator.can_play_card(card, top_card)
        self.assertTrue(result)
    
    def test_can_play_card_same_suit_and_value(self):
        """同じスートかつ同じ数値のカードは出せる"""
        card = Card(Suit.SUIT_A, 5)
        top_card = Card(Suit.SUIT_A, 5)
        result = MoveValidator.can_play_card(card, top_card)
        self.assertTrue(result)
    
    def test_can_play_card_different_suit_and_value(self):
        """異なるスートかつ異なる数値のカードは出せない"""
        card = Card(Suit.SUIT_A, 5)
        top_card = Card(Suit.SUIT_B, 8)
        result = MoveValidator.can_play_card(card, top_card)
        self.assertFalse(result)
    
    def test_get_valid_moves_empty_field(self):
        """空の場には全ての手札カードを出せる"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 1))
        hand.add_card(Card(Suit.SUIT_B, 2))
        hand.add_card(Card(Suit.SUIT_C, 3))
        
        field = Field()
        
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        # 3枚のカード × 2スロット = 6通りの手
        self.assertEqual(len(valid_moves), 6)
    
    def test_get_valid_moves_one_slot_occupied(self):
        """1つのスロットが埋まっている場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 1))
        hand.add_card(Card(Suit.SUIT_A, 2))  # スロット1に出せる（同じスート）
        hand.add_card(Card(Suit.SUIT_B, 5))  # スロット1に出せない
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 5))  # スロット1にA5を配置
        
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        # A1: スロット1(同じスート)、スロット2(空)
        # A2: スロット1(同じスート)、スロット2(空)
        # B5: スロット1(同じ数値)、スロット2(空)
        self.assertEqual(len(valid_moves), 6)
    
    def test_get_valid_moves_both_slots_occupied(self):
        """両方のスロットが埋まっている場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 3))  # スロット1に出せる（同じスート）
        hand.add_card(Card(Suit.SUIT_B, 5))  # スロット2に出せる（同じ数値）
        hand.add_card(Card(Suit.SUIT_C, 7))  # どちらにも出せない
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 1))  # スロット1にA1
        field.place_card(2, Card(Suit.SUIT_D, 5))  # スロット2にD5
        
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        # A3: スロット1(同じスート)
        # B5: スロット2(同じ数値)
        self.assertEqual(len(valid_moves), 2)
    
    def test_get_valid_moves_no_valid_moves(self):
        """出せるカードがない場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_C, 3))
        hand.add_card(Card(Suit.SUIT_D, 4))
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 1))
        field.place_card(2, Card(Suit.SUIT_B, 2))
        
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        self.assertEqual(len(valid_moves), 0)
    
    def test_has_valid_move_true(self):
        """出せるカードがある場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 5))
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 1))
        
        result = MoveValidator.has_valid_move(hand, field)
        self.assertTrue(result)
    
    def test_has_valid_move_false(self):
        """出せるカードがない場合（ゲーム終了）"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_C, 3))
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 1))
        field.place_card(2, Card(Suit.SUIT_B, 2))
        
        result = MoveValidator.has_valid_move(hand, field)
        self.assertFalse(result)
    
    def test_get_valid_moves_card_playable_on_both_slots(self):
        """1枚のカードが両方のスロットに出せる場合"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 5))
        
        field = Field()
        field.place_card(1, Card(Suit.SUIT_A, 1))  # 同じスート
        field.place_card(2, Card(Suit.SUIT_B, 5))  # 同じ数値
        
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        # A5はスロット1にもスロット2にも出せる
        self.assertEqual(len(valid_moves), 2)
        self.assertIn((Card(Suit.SUIT_A, 5), 1), valid_moves)
        self.assertIn((Card(Suit.SUIT_A, 5), 2), valid_moves)


if __name__ == '__main__':
    unittest.main()
