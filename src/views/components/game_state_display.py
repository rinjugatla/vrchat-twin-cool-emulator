"""
ゲーム状態表示コンポーネント
"""

import streamlit as st
from src.controllers import GameState


def display_game_state(state: GameState):
    """
    ゲーム状態を表示
    
    Args:
        state: ゲーム状態
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("ターン数", state.turn_count)
        st.metric("場に出したカード", state.get_cards_played_count())
    
    with col2:
        st.metric("獲得ポイント", state.get_total_points())
        st.metric("手札枚数", state.get_hand().count())
    
    with col3:
        st.metric("山札残り", state.deck.remaining_count())
        
        # スコア計算
        score = state.get_cards_played_count() * 10 + state.get_total_points()
        st.metric("総合スコア", score)
