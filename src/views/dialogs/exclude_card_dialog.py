"""
除外カード選択ダイアログ
"""

import streamlit as st

from src.views.components import display_card_selection_table
from src.views.utils import reset_game


def show_exclude_card_dialog():
    """除外カード選択ダイアログを表示"""
    st.info("💡 山札から除外する10枚のカードを選択してください。セルをクリックして選択します。選択したセルは灰色になります。")
    
    # カード選択テーブルを表示
    selected_cards = display_card_selection_table(
        title="🎯 ステップ1: 除外するカードを10枚選択",
        selected_cards=set(),
        disabled_cards=set(),
        on_card_click_key_prefix="exclude",
        caption="**凡例:** クリックで選択/解除 | ✕=選択不可 | 濃い色=選択済み",
        max_selection=10
    )
    
    st.markdown("---")
    st.markdown(f"### **選択中: {len(selected_cards)}/10枚**")
    
    if len(selected_cards) > 10:
        st.error(f"⚠️ 10枚まで選択できます（現在: {len(selected_cards)}枚）")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➡️ 次へ（初期手札を選択）", use_container_width=True, type="primary", disabled=(len(selected_cards) != 10)):
            if len(selected_cards) == 10:
                st.session_state.excluded_cards = list(selected_cards)
                st.session_state.show_exclude_dialog = False
                st.session_state.show_hand_dialog = True
                # 除外カードの選択状態をクリア
                if "exclude_selected" in st.session_state:
                    del st.session_state["exclude_selected"]
                st.rerun()
    
    with col2:
        if st.button("✅ ランダムな手札で開始", use_container_width=True, disabled=(len(selected_cards) != 10)):
            if len(selected_cards) == 10:
                reset_game(excluded_cards=list(selected_cards))
                # 除外カードの選択状態をクリア
                if "exclude_selected" in st.session_state:
                    del st.session_state["exclude_selected"]
                st.success("ゲームを開始しました！")
                st.rerun()
    
    with col3:
        if st.button("❌ キャンセル", use_container_width=True):
            st.session_state.show_exclude_dialog = False
            # 選択状態をクリア
            if "exclude_selected" in st.session_state:
                del st.session_state["exclude_selected"]
            st.rerun()
    
    st.markdown("---")
