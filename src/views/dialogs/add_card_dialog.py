"""
手札追加カード選択ダイアログ
カードを場に出した後、山札から手札に1枚追加する
"""

import streamlit as st

from src.views.components import display_card_selection_table


def show_add_card_dialog():
    """手札追加カード選択ダイアログを表示"""
    st.info("💡 山札から手札に追加する1枚のカードを選択してください。セルをクリックして選択します。")
    
    # 山札に残っていないカード（除外カード + 既に手札にあるカード + 場に出したカード）を取得
    state = st.session_state.game_state
    disabled_cards = set()
    
    # 除外カード
    if hasattr(st.session_state, 'excluded_cards'):
        disabled_cards.update(st.session_state.excluded_cards)
    
    # 手札のカード
    for card in state.get_hand().get_cards():
        disabled_cards.add(card)
    
    # 場に出したカード
    for card in state.played_cards:
        disabled_cards.add(card)
    
    # カード選択テーブルを表示
    selected_cards = display_card_selection_table(
        title="🎴 山札から手札に追加するカードを1枚選択",
        selected_cards=set(),
        disabled_cards=disabled_cards,
        on_card_click_key_prefix="add_card",
        caption="**凡例:** クリックで選択/解除 | ✕=選択不可（除外済み/手札/場に出済み） | 濃い色=選択済み",
        max_selection=1
    )
    
    st.markdown("---")
    st.markdown(f"### **選択中: {len(selected_cards)}/1枚**")
    
    if len(selected_cards) > 1:
        st.error(f"⚠️ 1枚のみ選択できます（現在: {len(selected_cards)}枚）")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ このカードを手札に追加", use_container_width=True, type="primary", disabled=(len(selected_cards) != 1)):
            if len(selected_cards) == 1:
                # 選択されたカードを取得
                selected_card = list(selected_cards)[0]
                
                # 手札に追加
                success = state.add_card_to_hand(selected_card)
                
                if success:
                    # ダイアログを閉じる
                    st.session_state.show_add_card_dialog = False
                    # 選択状態をクリア
                    if "add_card_selected" in st.session_state:
                        del st.session_state["add_card_selected"]
                    # 自動計算フラグを立てる
                    st.session_state.auto_calculate_next_move = True
                    st.success(f"✅ {selected_card} を手札に追加しました！")
                    st.rerun()
                else:
                    st.error("⚠️ カードの追加に失敗しました")
    
    with col2:
        if st.button("❌ キャンセル", use_container_width=True):
            st.session_state.show_add_card_dialog = False
            # 選択状態をクリア
            if "add_card_selected" in st.session_state:
                del st.session_state["add_card_selected"]
            st.rerun()
    
    st.markdown("---")
