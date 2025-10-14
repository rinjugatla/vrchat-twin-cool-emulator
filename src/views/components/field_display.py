"""
場表示コンポーネント
"""

import streamlit as st
from src.controllers import GameState
from src.views.utils import get_suit_emoji


def display_field(state: GameState):
    """
    場を表示
    
    Args:
        state: ゲーム状態
    """
    st.subheader("🎯 場（2つのスロット）")
    
    field = state.get_field()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### スロット 1")
        slot1_top = field.get_top_card(1)
        if slot1_top:
            emoji = get_suit_emoji(slot1_top.suit)
            st.success(f"トップカード: {emoji} {slot1_top}")
            st.caption(f"枚数: {field.get_slot_count(1)}枚")
        else:
            st.info("空（任意のカードを出せます）")
    
    with col2:
        st.markdown("#### スロット 2")
        slot2_top = field.get_top_card(2)
        if slot2_top:
            emoji = get_suit_emoji(slot2_top.suit)
            st.success(f"トップカード: {emoji} {slot2_top}")
            st.caption(f"枚数: {field.get_slot_count(2)}枚")
        else:
            st.info("空（任意のカードを出せます）")
