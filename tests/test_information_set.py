"""
InformationSetクラスのテスト
"""

import unittest
from src.models.card import Card
from src.models.hand import Hand
from src.models.field import Field
from src.models.suit import Suit
from src.controllers.information_set import InformationSet


class TestInformationSet(unittest.TestCase):
    """InformationSetクラスのテストケース"""
    
    def test_hash_consistency(self):
        """同じ情報セットは同じハッシュ値を持つ"""
        # 手札を作成
        hand1 = Hand()
        hand1.add_card(Card(Suit.SUIT_A, 1))
        hand1.add_card(Card(Suit.SUIT_B, 2))
        
        hand2 = Hand()
        hand2.add_card(Card(Suit.SUIT_A, 1))
        hand2.add_card(Card(Suit.SUIT_B, 2))
        
        # 場を作成
        field1 = Field()
        field1.place_card(1, Card(Suit.SUIT_C, 3))
        
        field2 = Field()
        field2.place_card(1, Card(Suit.SUIT_C, 3))
        
        # 情報セットを作成
        info1 = InformationSet(hand1, field1, 10)
        info2 = InformationSet(hand2, field2, 10)
        
        # 同じハッシュ値を持つ
        self.assertEqual(hash(info1), hash(info2))
    
    def test_equality(self):
        """同じ情報セットは等しい"""
        hand1 = Hand()
        hand1.add_card(Card(Suit.SUIT_A, 1))
        
        hand2 = Hand()
        hand2.add_card(Card(Suit.SUIT_A, 1))
        
        field1 = Field()
        field2 = Field()
        
        info1 = InformationSet(hand1, field1, 5)
        info2 = InformationSet(hand2, field2, 5)
        
        self.assertEqual(info1, info2)
    
    def test_hand_order_independence(self):
        """手札の順序が異なっても同じ情報セット"""
        # 異なる順序で手札を追加
        hand1 = Hand()
        hand1.add_card(Card(Suit.SUIT_A, 1))
        hand1.add_card(Card(Suit.SUIT_B, 2))
        hand1.add_card(Card(Suit.SUIT_C, 3))
        
        hand2 = Hand()
        hand2.add_card(Card(Suit.SUIT_C, 3))
        hand2.add_card(Card(Suit.SUIT_A, 1))
        hand2.add_card(Card(Suit.SUIT_B, 2))
        
        field = Field()
        
        info1 = InformationSet(hand1, field, 0)
        info2 = InformationSet(hand2, field, 0)
        
        # 順序が違っても同じ情報セット
        self.assertEqual(info1, info2)
        self.assertEqual(hash(info1), hash(info2))
    
    def test_different_hand_different_infoset(self):
        """異なる手札は異なる情報セット"""
        hand1 = Hand()
        hand1.add_card(Card(Suit.SUIT_A, 1))
        
        hand2 = Hand()
        hand2.add_card(Card(Suit.SUIT_A, 2))
        
        field = Field()
        
        info1 = InformationSet(hand1, field, 0)
        info2 = InformationSet(hand2, field, 0)
        
        self.assertNotEqual(info1, info2)
    
    def test_different_played_count_different_infoset(self):
        """既出枚数が異なれば異なる情報セット"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 1))
        
        field = Field()
        
        info1 = InformationSet(hand, field, 10)
        info2 = InformationSet(hand, field, 11)
        
        self.assertNotEqual(info1, info2)
    
    def test_usable_as_dict_key(self):
        """辞書のキーとして使用可能"""
        hand = Hand()
        hand.add_card(Card(Suit.SUIT_A, 1))
        
        field = Field()
        
        info = InformationSet(hand, field, 5)
        
        # 辞書のキーとして使用
        cache = {info: "test_value"}
        
        # 同じ情報セットで取得可能
        hand2 = Hand()
        hand2.add_card(Card(Suit.SUIT_A, 1))
        field2 = Field()
        info2 = InformationSet(hand2, field2, 5)
        
        self.assertEqual(cache[info2], "test_value")


if __name__ == '__main__':
    unittest.main()
