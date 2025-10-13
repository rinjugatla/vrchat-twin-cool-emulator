"""
Streamlitセッション状態管理モジュール
"""

import streamlit as st
import random
from typing import Optional, List

from src.models import Card
from src.controllers import GameState


def initialize_session_state():
    """セッション状態の初期化"""
    if 'game_state' not in st.session_state:
        seed = random.randint(0, 100000)
        st.session_state.game_state = GameState(seed=seed)
        st.session_state.history = []
        st.session_state.turn = 0
        st.session_state.seed = seed
        st.session_state.recommended_move = None  # 推奨手を保存
        st.session_state.excluded_cards = []  # 除外カード選択用
        st.session_state.show_exclude_dialog = False  # 除外カード選択ダイアログ表示フラグ
        st.session_state.initial_hand = []  # 初期手札選択用
        st.session_state.show_hand_dialog = False  # 初期手札選択ダイアログ表示フラグ


def reset_game(excluded_cards: Optional[List[Card]] = None, initial_hand: Optional[List[Card]] = None):
    """
    ゲームをリセット
    
    Args:
        excluded_cards: 除外するカードのリスト（指定しない場合はランダム）
        initial_hand: 初期手札（指定しない場合はランダム）
    """
    seed = random.randint(0, 100000)
    st.session_state.game_state = GameState(seed=seed, excluded_cards=excluded_cards, initial_hand=initial_hand)
    st.session_state.history = []
    st.session_state.turn = 0
    st.session_state.seed = seed
    st.session_state.recommended_move = None  # 推奨手をクリア
    st.session_state.excluded_cards = []  # 除外カード選択をクリア
    st.session_state.show_exclude_dialog = False  # ダイアログを閉じる
    st.session_state.initial_hand = []  # 初期手札選択をクリア
    st.session_state.show_hand_dialog = False  # ダイアログを閉じる
