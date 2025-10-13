"""
UI補助関数モジュール
スートに対応する絵文字などのUI表示用ヘルパー関数
"""

from src.models import Suit


def get_suit_emoji(suit: Suit) -> str:
    """
    スートに対応する絵文字を取得
    
    Args:
        suit: スート
    
    Returns:
        スートに対応する絵文字
    """
    suit_colors = {
        Suit.SUIT_A: "🔴", 
        Suit.SUIT_B: "🔵", 
        Suit.SUIT_C: "🟢", 
        Suit.SUIT_D: "🟡",
        Suit.SUIT_E: "⚪", 
        Suit.SUIT_F: "🩵",
        Suit.SUIT_G: "🟣", 
        Suit.SUIT_H: "🩷"
    }
    return suit_colors.get(suit, "⬜")
