"""
twin-cool-emulator Streamlit WebUIアプリケーション
オリジナルカードゲームの最適解を提示
"""

import streamlit as st
import random
from typing import Optional, Tuple

from src.models import Card, Suit
from src.controllers import GameState, MCTSStrategy


def initialize_session_state():
    """セッション状態の初期化"""
    if 'game_state' not in st.session_state:
        seed = random.randint(0, 100000)
        st.session_state.game_state = GameState(seed=seed)
        st.session_state.history = []
        st.session_state.turn = 0
        st.session_state.seed = seed
        st.session_state.recommended_move = None  # 推奨手を保存


def reset_game():
    """ゲームをリセット"""
    seed = random.randint(0, 100000)
    st.session_state.game_state = GameState(seed=seed)
    st.session_state.history = []
    st.session_state.turn = 0
    st.session_state.seed = seed
    st.session_state.recommended_move = None  # 推奨手をクリア


def display_game_state(state: GameState):
    """ゲーム状態を表示"""
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


def get_suit_emoji(suit: Suit) -> str:
    """スートに対応する絵文字を取得"""
    suit_colors = {
        Suit.SUIT_A: "🔴", Suit.SUIT_B: "🔵", 
        Suit.SUIT_C: "🟢", Suit.SUIT_D: "🟡",
        Suit.SUIT_E: "⚪", Suit.SUIT_F: "🩵",
        Suit.SUIT_G: "🟣", Suit.SUIT_H: "🩷"
    }
    return suit_colors.get(suit, "⬜")


def display_hand(state: GameState):
    """手札を表示"""
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


def display_field(state: GameState):
    """場を表示"""
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


def get_best_move_with_mcts(state: GameState, num_iterations: int) -> Optional[Tuple[Card, int]]:
    """MCTSを使って最適な手を取得"""
    strategy = MCTSStrategy(num_iterations=num_iterations, verbose=False)
    return strategy.get_best_move(state)


def main():
    """メイン関数"""
    st.set_page_config(
        page_title="twin-cool-emulator",
        page_icon="🎴",
        layout="wide"
    )
    
    st.title("🎴 twin-cool-emulator")
    st.markdown("**オリジナルカードゲーム 最適解探索プログラム**")
    st.markdown("---")
    
    # セッション状態の初期化
    initialize_session_state()
    
    # サイドバー設定
    with st.sidebar:
        st.header("⚙️ 設定")
        
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
        st.header("📊 ゲーム情報")
        st.caption(f"シード値: {st.session_state.seed}")
        st.caption(f"ターン: {st.session_state.turn}")
        
        st.markdown("---")
        
        # リセットボタン
        if st.button("🔄 新しいゲームを開始", use_container_width=True):
            reset_game()
            st.rerun()
        
        st.markdown("---")
        
        # ルール説明
        with st.expander("📖 ゲームルール"):
            st.markdown("""
            ### カード構成
            - 8種類のスート (A-H)
            - 各スート1-10の数値
            - 合計80枚 → 10枚除外 → 70枚使用
            
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
    
    # ゲーム状態表示
    display_game_state(state)
    
    st.markdown("---")
    
    # 場の表示
    display_field(state)
    
    st.markdown("---")
    
    # 手札の表示
    display_hand(state)
    
    st.markdown("---")
    
    # 最適解の取得と表示
    st.subheader("🎯 次の最適な手")
    
    if state.get_hand().count() == 0:
        st.warning("⚠️ 手札がありません。ゲーム終了です。")
        st.balloons()
    else:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            analyze_button = st.button(
                "🔍 最適解を分析",
                use_container_width=True,
                type="primary"
            )
        
        # 分析ボタンが押された場合
        if analyze_button:
            with st.spinner(f"MCTS探索中... ({num_iterations}回反復)"):
                best_move = get_best_move_with_mcts(state, num_iterations)
            
            if best_move is None:
                st.error("❌ 出せるカードがありません。ゲーム終了です。")
                st.session_state.recommended_move = None
                st.balloons()
            else:
                # 推奨手をセッション状態に保存
                st.session_state.recommended_move = best_move
                st.rerun()
        
        # 推奨手が存在する場合、表示して実行ボタンを配置
        if st.session_state.recommended_move is not None:
            card, slot = st.session_state.recommended_move
            
            st.success(f"✅ **推奨: {card} をスロット{slot}に出す**")
            
            col_exec1, col_exec2 = st.columns([1, 1])
            
            with col_exec1:
                # 実行ボタン
                if st.button("▶️ この手を実行", use_container_width=True, type="secondary"):
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
                        st.success("✅ 手を実行しました！")
                        st.rerun()
                    else:
                        st.error("❌ 手の実行に失敗しました")
            
            with col_exec2:
                # キャンセルボタン
                if st.button("❌ キャンセル", use_container_width=True):
                    st.session_state.recommended_move = None
                    st.rerun()
    
    # 履歴表示
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📜 履歴")
        
        with st.expander(f"履歴を表示 ({len(st.session_state.history)}手)"):
            for record in reversed(st.session_state.history[-10:]):
                # スート情報がある場合は絵文字を表示
                if 'suit' in record:
                    emoji = get_suit_emoji(record['suit'])
                    st.caption(
                        f"ターン {record['turn']}: "
                        f"{emoji} {record['card']} → スロット{record['slot']}"
                    )
                else:
                    # 後方互換性のため、スート情報がない場合は絵文字なしで表示
                    st.caption(
                        f"ターン {record['turn']}: "
                        f"{record['card']} → スロット{record['slot']}"
                    )


if __name__ == "__main__":
    main()
