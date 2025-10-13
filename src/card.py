"""
カード、デッキ、手札に関するクラスとロジック
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Suit(Enum):
    """カードのスート（8種類）"""
    SUIT_A = "A"
    SUIT_B = "B"
    SUIT_C = "C"
    SUIT_D = "D"
    SUIT_E = "E"
    SUIT_F = "F"
    SUIT_G = "G"
    SUIT_H = "H"


@dataclass(frozen=True)
class Card:
    """
    カードを表すクラス
    
    Attributes:
        suit: カードのスート
        value: カードの数値 (1-10)
    """
    suit: Suit
    value: int
    
    def __post_init__(self):
        if not 1 <= self.value <= 10:
            raise ValueError(f"カードの数値は1-10の範囲である必要があります: {self.value}")
    
    def __str__(self) -> str:
        return f"{self.suit.value}{self.value}"
    
    def __repr__(self) -> str:
        return f"Card({self.suit.value}, {self.value})"
