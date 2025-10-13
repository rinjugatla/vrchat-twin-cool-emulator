"""
カード選択テーブルコンポーネント
"""

import streamlit as st
from typing import Set

from src.models import Card, Suit
from src.views.utils import get_suit_emoji
from src.views.styles import get_card_table_styles


def display_card_selection_table(
    title: str,
    selected_cards: Set[Card],
    disabled_cards: Set[Card],
    on_card_click_key_prefix: str,
    caption: str,
    max_selection: int = 10
) -> Set[Card]:
    """
    カード選択用のテーブルを表示
    
    Args:
        title: テーブルのタイトル
        selected_cards: 選択済みのカード
        disabled_cards: 選択不可のカード
        on_card_click_key_prefix: ボタンのキープレフィックス
        caption: 凡例のキャプション
        max_selection: 最大選択数
    
    Returns:
        選択されたカードのセット
    """
    st.subheader(title)
    
    # セッション状態にカード選択を保存するキー
    selection_key = f"{on_card_click_key_prefix}_selected"
    if selection_key not in st.session_state:
        st.session_state[selection_key] = set(selected_cards)
    
    current_selected = st.session_state[selection_key]
    
    # カスタムCSSでボタンスタイルを定義
    st.markdown(get_card_table_styles(), unsafe_allow_html=True)
    
    # ヘッダー行を表示
    header_cols = st.columns([2] + [1]*10)
    with header_cols[0]:
        st.markdown('<div style="text-align:center; font-weight:bold; padding:10px; background-color:#f0f0f0; border:1px solid #ddd; color:#000000;">スート</div>', unsafe_allow_html=True)
    for i, value in enumerate(range(1, 11), start=1):
        with header_cols[i]:
            st.markdown(f'<div style="text-align:center; font-weight:bold; padding:10px; background-color:#f0f0f0; border:1px solid #ddd; color:#000000;">{value}</div>', unsafe_allow_html=True)
    
    # 各スートの行
    suits = list(Suit)
    for suit in suits:
        emoji = get_suit_emoji(suit)
        cols = st.columns([2] + [1]*10)
        
        # スート列
        with cols[0]:
            st.markdown(f'<div style="text-align:center; font-weight:bold; padding:10px; background-color:#f8f9fa; border:1px solid #ddd; height:50px; display:flex; align-items:center; justify-content:center; color:#000000;">{emoji} {suit.name}</div>', unsafe_allow_html=True)
        
        # 数値列（ボタン）
        for i, value in enumerate(range(1, 11), start=1):
            card = Card(suit, value)
            with cols[i]:
                if card in disabled_cards:
                    # 選択不可のカード（除外済み）
                    st.markdown(f'<div style="text-align:center; padding:10px; background-color:#e0e0e0; border:1px solid #ddd; height:50px; display:flex; align-items:center; justify-content:center; color:#999;">✕</div>', unsafe_allow_html=True)
                else:
                    # 選択可能なカード - ボタンとして実装
                    is_selected = card in current_selected
                    
                    # 背景色を設定
                    if is_selected:
                        button_type = "secondary"
                        label = f"**{value}**"
                    else:
                        button_type = "primary"
                        label = str(value)
                    
                    # ボタンがクリックされたら選択状態をトグル
                    if st.button(
                        label,
                        key=f"{on_card_click_key_prefix}_{suit.name}_{value}",
                        use_container_width=True,
                        type=button_type
                    ):
                        if card in current_selected:
                            # 選択解除
                            current_selected.discard(card)
                        else:
                            # 選択（最大数チェック）
                            if len(current_selected) < max_selection:
                                current_selected.add(card)
                        
                        # セッション状態を更新
                        st.session_state[selection_key] = current_selected
                        st.rerun()
    
    st.caption(caption)
    
    return current_selected
