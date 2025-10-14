"""
山札状況表示コンポーネント
"""

import streamlit as st
from typing import Optional

from src.models import Card, Suit
from src.controllers import GameState
from src.views.utils import get_suit_emoji


def display_deck_status(state: GameState, recommended_card: Optional[Card] = None):
    """
    山札の状況を表形式で表示
    
    Args:
        state: ゲーム状態
        recommended_card: 推奨カード（強調表示する）
    """
    st.subheader("📊 山札状況")
    
    # 全カードのセットを作成
    all_cards = set()
    for suit in Suit:
        for value in range(1, 11):
            all_cards.add(Card(suit, value))
    
    # 除外されたカードを取得（初期の10枚）
    excluded_cards = state.deck.get_excluded_cards()
    
    # 山札に残っているカードを取得
    remaining_cards = set(state.deck.get_remaining_cards())
    
    # 手札のカードを取得
    hand_cards = set(state.get_hand().get_cards())
    
    # 場に出たカードを取得（使用済み）
    played_cards = set()
    field = state.get_field()
    for slot_num in [1, 2]:
        played_cards.update(field.get_all_cards(slot_num))
    
    # 表を作成
    suits = list(Suit)
    
    # HTMLテーブルを構築
    html = '<table style="width:100%; border-collapse: collapse; text-align: center;">'
    
    # ヘッダー行
    html += '<tr style="background-color: #f0f0f0;">'
    html += '<th style="border: 1px solid #ddd; padding: 8px; color: #000000; font-weight: bold;">スート</th>'
    for value in range(1, 11):
        html += f'<th style="border: 1px solid #ddd; padding: 8px; color: #000000; font-weight: bold;">{value}</th>'
    html += '</tr>'
    
    # 各スートの行
    for suit in suits:
        emoji = get_suit_emoji(suit)
        html += '<tr>'
        html += f'<td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; background-color: #f8f9fa; color: #000000;">{emoji} {suit.name}</td>'
        
        for value in range(1, 11):
            card = Card(suit, value)
            cell_style = 'border: 1px solid #ddd; padding: 8px;'
            cell_content = str(value)
            
            # カードの状態に応じてスタイルを変更
            if card in excluded_cards:
                # 除外されたカード（山札に含まれない）
                cell_content = ''
                cell_style += ' background-color: #e0e0e0;'
            elif recommended_card and card == recommended_card:
                # 推奨カード（赤色）
                cell_style += ' background-color: #ff4444; color: #ffffff; font-weight: bold;'
            elif card in hand_cards:
                # 手札のカード（黄色）
                cell_style += ' background-color: #ffeb3b; color: #000000; font-weight: bold;'
            elif card in played_cards:
                # 使用済みカード（薄く表示）
                cell_style += ' color: #999999; background-color: #ffffff;'
            elif card in remaining_cards:
                # 山札に残っているカード
                cell_style += ' background-color: #ffffff; color: #000000;'
            
            html += f'<td style="{cell_style}">{cell_content}</td>'
        
        html += '</tr>'
    
    html += '</table>'
    
    # 凡例を追加
    st.markdown(html, unsafe_allow_html=True)
    
    st.caption("**凡例:** 🟥推奨カード | 🟨手札 | 薄い数値=使用済み | 空欄=山札に含まれない | 通常=山札に残存")
