"""
手札表示コンポーネント
"""

import streamlit as st
from src.controllers import GameState
from src.views.utils import get_suit_emoji


def display_hand(state: GameState):
    """
    手札を表示
    
    Args:
        state: ゲーム状態
    """
    st.subheader("🎴 手札")
    
    hand = state.get_hand()
    cards = hand.get_cards()
    
    if not cards:
        st.info("手札にカードがありません")
        return
    
    # カードを横並びで表示
    cols = st.columns(min(len(cards), 5))
    for i, card in enumerate(cards):
        with cols[i % 5]:
            color = get_suit_emoji(card.suit)
            st.markdown(f"### {color} {card}")
