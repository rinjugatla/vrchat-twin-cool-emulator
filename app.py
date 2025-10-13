"""
twin-cool-emulator Streamlit WebUIアプリケーション
オリジナルカードゲームの最適解を提示

リファクタリング版: MVCモデルに基づく分割構造
"""

import streamlit as st
from typing import Optional, Tuple

from src.models import Card
from src.controllers import GameState, MCTSStrategy
from src.views import (
    initialize_session_state,
    reset_game,
    get_suit_emoji,
    display_game_state,
    display_hand,
    display_field,
    display_deck_status,
    show_exclude_card_dialog,
    show_hand_selection_dialog
)


def get_best_move_with_mcts(state: GameState, num_iterations: int) -> Optional[Tuple[Card, int]]:
    """MCTSを使って最適な手を取得"""
    strategy = MCTSStrategy(num_iterations=num_iterations, verbose=False)
    return strategy.get_best_move(state)


def main():
    """メイン関数"""
    st.set_page_config(
        page_title="twin-cool-emulator",
        page_icon="",
        layout="wide"
    )
    
    st.title(" twin-cool-emulator")
    st.markdown("**オリジナルカードゲーム 最適解探索プログラム**")
    st.markdown("---")
    
    # セッション状態の初期化
    initialize_session_state()
    
    # サイドバー設定
    with st.sidebar:
        st.header(" 設定")
        
        # MCTS設定
        num_iterations = st.slider(
            "MCTS探索回数",
            min_value=50,
            max_value=2000,
            value=500,
            step=50,
            help="探索回数を増やすと精度が上がりますが、時間がかかります"
        )
        
        st.markdown("---")
        
        # ゲーム情報
        st.header(" ゲーム情報")
        st.caption(f"シード値: {st.session_state.seed}")
        st.caption(f"ターン: {st.session_state.turn}")
        
        st.markdown("---")
        
        # リセットボタン
        if st.button(" 新しいゲームを開始（ランダム）", use_container_width=True):
            reset_game()
            st.rerun()
        
        # 除外カード指定ボタン
        if st.button(" 除外カードを指定して開始", use_container_width=True):
            st.session_state.show_exclude_dialog = True
            st.rerun()
        
        st.markdown("---")
        
        # ルール説明
        with st.expander(" ゲームルール"):
            st.markdown("""
            ### カード構成
            - 8種類のスート (A-H)
            - 各スート1-10の数値
            - 合計80枚  10枚除外  70枚使用
            
            ### 出せるカードの条件
            - スロットが空：任意のカード
            - スロットにカードあり：
              - 同じスート **または**
              - 同じ数値
            
            ### 目標
            1. **場に出したカード枚数を最大化**（最優先）
            2. 特別なポイントを最大化（次点）
            
            ### 特別なポイント
            - 4枚同じ数値：1pt
            - 5枚連番：2pt
            - 5枚同じ数値：5pt
            - 5枚同じスート連番：50pt
            """)
    
    # メインコンテンツ
    state = st.session_state.game_state
    
    # 除外カード選択ダイアログ
    if st.session_state.show_exclude_dialog:
        show_exclude_card_dialog()
        return
    
    # 初期手札選択ダイアログ
    if st.session_state.show_hand_dialog:
        show_hand_selection_dialog()
        return
    
    # ゲーム状態表示
    display_game_state(state)
    
    st.markdown("---")
    
    # 場の表示
    display_field(state)
    
    st.markdown("---")
    
    # 手札の表示
    display_hand(state)
    
    st.markdown("---")
    
    # 山札状況の表示
    recommended_card = st.session_state.recommended_move[0] if st.session_state.recommended_move else None
    display_deck_status(state, recommended_card)
    
    st.markdown("---")
    
    # 最適解の取得と表示
    st.subheader(" 次の最適な手")
    
    if state.get_hand().count() == 0:
        st.warning(" 手札がありません。ゲーム終了です。")
        st.balloons()
    else:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            analyze_button = st.button(
                " 最適解を分析",
                use_container_width=True,
                type="primary"
            )
        
        # 分析ボタンが押された場合
        if analyze_button:
            with st.spinner(f"MCTS探索中... ({num_iterations}回反復)"):
                best_move = get_best_move_with_mcts(state, num_iterations)
            
            if best_move is None:
                st.error(" 出せるカードがありません。ゲーム終了です。")
                st.session_state.recommended_move = None
                st.balloons()
            else:
                # 推奨手をセッション状態に保存
                st.session_state.recommended_move = best_move
                st.rerun()
        
        # 推奨手が存在する場合、表示して実行ボタンを配置
        if st.session_state.recommended_move is not None:
            card, slot = st.session_state.recommended_move
            
            st.success(f" **推奨: {card} をスロット{slot}に出す**")
            
            col_exec1, col_exec2 = st.columns([1, 1])
            
            with col_exec1:
                # 実行ボタン
                if st.button(" この手を実行", use_container_width=True, type="secondary"):
                    # 手を実行
                    success = state.play_card(card, slot)
                    
                    if success:
                        st.session_state.turn += 1
                        st.session_state.history.append({
                            'turn': st.session_state.turn,
                            'card': str(card),
                            'suit': card.suit,  # スート情報も保存
                            'slot': slot
                        })
                        st.session_state.recommended_move = None  # 推奨手をクリア
                        st.success(" 手を実行しました！")
                        st.rerun()
                    else:
                        st.error(" 手の実行に失敗しました")
            
            with col_exec2:
                # キャンセルボタン
                if st.button(" キャンセル", use_container_width=True):
                    st.session_state.recommended_move = None
                    st.rerun()
    
    # 履歴表示
    if st.session_state.history:
        st.markdown("---")
        st.subheader(" 履歴")
        
        with st.expander(f"履歴を表示 ({len(st.session_state.history)}手)"):
            for record in reversed(st.session_state.history[-10:]):
                # スート情報がある場合は絵文字を表示
                if 'suit' in record:
                    emoji = get_suit_emoji(record['suit'])
                    st.caption(
                        f"ターン {record['turn']}: "
                        f"{emoji} {record['card']}  スロット{record['slot']}"
                    )
                else:
                    # 後方互換性のため、スート情報がない場合は絵文字なしで表示
                    st.caption(
                        f"ターン {record['turn']}: "
                        f"{record['card']}  スロット{record['slot']}"
                    )


if __name__ == "__main__":
    main()
