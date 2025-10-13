"""
twin-cool-emulator Streamlit WebUIアプリケーション
オリジナルカードゲームの最適解を提示
"""

import streamlit as st
import random
from typing import Optional, Tuple, Set

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
        st.session_state.excluded_cards = []  # 除外カード選択用
        st.session_state.show_exclude_dialog = False  # 除外カード選択ダイアログ表示フラグ
        st.session_state.initial_hand = []  # 初期手札選択用
        st.session_state.show_hand_dialog = False  # 初期手札選択ダイアログ表示フラグ


def reset_game(excluded_cards=None, initial_hand=None):
    """ゲームをリセット"""
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
    st.markdown("""
    <style>
    .card-table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        margin-bottom: 20px;
    }
    .card-table th {
        border: 1px solid #ddd;
        padding: 10px;
        background-color: #f0f0f0;
        color: #000000;
        font-weight: bold;
    }
    .card-table td {
        border: 1px solid #ddd;
        padding: 0;
        height: 50px;
    }
    .card-table .suit-cell {
        font-weight: bold;
        background-color: #f8f9fa;
        color: #000000;
        padding: 10px;
    }
    div[data-testid="column"] > div > div > div > button {
        width: 100%;
        height: 50px;
        border: none;
        border-radius: 0;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
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


def display_deck_status(state: GameState, recommended_card: Optional[Card] = None):
    """山札の状況を表形式で表示"""
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
        if st.button("🔄 新しいゲームを開始（ランダム）", use_container_width=True):
            reset_game()
            st.rerun()
        
        # 除外カード指定ボタン
        if st.button("🎯 除外カードを指定して開始", use_container_width=True):
            st.session_state.show_exclude_dialog = True
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
    
    # 除外カード選択ダイアログ
    if st.session_state.show_exclude_dialog:
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
    
    # 初期手札選択ダイアログ
    if st.session_state.show_hand_dialog:
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
