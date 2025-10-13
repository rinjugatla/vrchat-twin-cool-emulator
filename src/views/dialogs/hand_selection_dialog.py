"""
初期手札選択ダイアログ
"""

import streamlit as st

from src.views.components import display_card_selection_table
from src.views.utils import reset_game


def show_hand_selection_dialog():
    """初期手札選択ダイアログを表示"""
    st.info("💡 山札（70枚）から初期手札となる5枚のカードを選択してください。セルをクリックして選択します。除外カードは✕で表示されます。")
    
    # 除外カードを除いた残りのカードから選択
    excluded = set(st.session_state.excluded_cards)
    
    # カード選択テーブルを表示
    selected_hand = display_card_selection_table(
        title="🎴 ステップ2: 初期手札を5枚選択",
        selected_cards=set(),
        disabled_cards=excluded,
        on_card_click_key_prefix="hand",
        caption="**凡例:** クリックで選択/解除 | ✕=除外カード（選択不可） | 濃い色=選択済み",
        max_selection=5
    )
    
    st.markdown("---")
    st.markdown(f"### **選択中: {len(selected_hand)}/5枚**")
    
    if len(selected_hand) > 5:
        st.error(f"⚠️ 5枚まで選択できます（現在: {len(selected_hand)}枚）")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ この設定でゲーム開始", use_container_width=True, type="primary", disabled=(len(selected_hand) != 5)):
            if len(selected_hand) == 5:
                reset_game(excluded_cards=st.session_state.excluded_cards, initial_hand=list(selected_hand))
                # 手札の選択状態をクリア
                if "hand_selected" in st.session_state:
                    del st.session_state["hand_selected"]
                st.success("ゲームを開始しました！")
                st.rerun()
    
    with col2:
        if st.button("❌ キャンセル", use_container_width=True):
            st.session_state.show_hand_dialog = False
            st.session_state.show_exclude_dialog = True  # 除外カード選択に戻る
            # 選択状態をクリア
            if "hand_selected" in st.session_state:
                del st.session_state["hand_selected"]
            st.rerun()
    
    st.markdown("---")
