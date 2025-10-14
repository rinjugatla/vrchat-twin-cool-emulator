"""
カードクラスの定義
"""

from dataclasses import dataclass
from .suit import Suit


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
