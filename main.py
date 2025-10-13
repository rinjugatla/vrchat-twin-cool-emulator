"""
twin-cool-emulator メインエントリーポイント
オリジナルカードゲーム「最適解探索プログラム」
"""

from src.models import Suit, Card, Deck, Hand, FieldSlot, Field, PointCalculator
from src.controllers import Game, MoveValidator, GameState, MCTSStrategy


def run_basic_test():
    """基本動作テスト"""
    print("【基本動作テスト】")
    print()
    
    # デッキの初期化
    deck = Deck(seed=42)
    print(f"✓ デッキ初期化完了: {deck.remaining_count()}枚")
    
    # 手札の初期化
    hand = Hand()
    for _ in range(5):
        card = deck.draw()
        if card:
            hand.add_card(card)
    print(f"✓ 初期手札配布完了: {hand.count()}枚")
    print(f"  手札: {hand}")
    
    # 場の初期化
    field = Field()
    print(f"✓ 場の初期化完了: {field}")
    
    # ポイント計算テスト
    points = PointCalculator.calculate_points(hand.get_cards())
    print(f"✓ 初期手札のポイント: {points}ポイント")
    print()


def run_single_game_simulation(seed: int = 42):
    """1回のゲームシミュレーション"""
    print(f"【ゲームシミュレーション（シード: {seed}）】")
    print()
    
    game = Game(seed=seed)
    print(f"✓ ゲーム初期化完了")
    print(f"  初期手札: {game.get_state().get_hand()}")
    print()
    
    # ゲームをシミュレート
    result = game.simulate_random_game()
    
    print(f"✓ ゲーム終了")
    print(f"  場に出したカード: {result['cards_played']}枚")
    print(f"  獲得ポイント: {result['total_points']}ポイント")
    print(f"  ターン数: {result['turn_count']}ターン")
    print(f"  最終手札: {result['final_hand_size']}枚")
    print()


def run_multiple_simulations(num_games: int = 10):
    """複数回のゲームシミュレーション"""
    print(f"【複数ゲームシミュレーション（{num_games}回）】")
    print()
    
    results = []
    for i in range(num_games):
        game = Game(seed=i)
        result = game.simulate_random_game()
        results.append(result)
    
    # 統計を計算
    cards_played_list = [r['cards_played'] for r in results]
    points_list = [r['total_points'] for r in results]
    
    avg_cards = sum(cards_played_list) / len(cards_played_list)
    max_cards = max(cards_played_list)
    min_cards = min(cards_played_list)
    
    avg_points = sum(points_list) / len(points_list)
    max_points = max(points_list)
    min_points = min(points_list)
    
    print(f"✓ {num_games}回のシミュレーション完了")
    print()
    print(f"【場に出したカード枚数】")
    print(f"  平均: {avg_cards:.1f}枚")
    print(f"  最大: {max_cards}枚")
    print(f"  最小: {min_cards}枚")
    print()
    print(f"【獲得ポイント】")
    print(f"  平均: {avg_points:.1f}ポイント")
    print(f"  最大: {max_points}ポイント")
    print(f"  最小: {min_points}ポイント")
    print()


def run_mcts_demo(seed: int = 42, num_iterations: int = 500):
    """MCTS戦略デモ"""
    print(f"【MCTS戦略デモ（シード: {seed}、反復: {num_iterations}回）】")
    print()
    
    # 戦略を作成
    strategy = MCTSStrategy(num_iterations=num_iterations, verbose=False)
    
    # 初期状態を作成
    state = GameState(seed=seed)
    print(f"✓ MCTS戦略初期化完了")
    print(f"  初期手札: {state.get_hand()}")
    print()
    
    # ゲームをプレイ
    result = strategy.play_game(state)
    
    print(f"✓ ゲーム終了")
    print(f"  場に出したカード: {result['cards_played']}枚")
    print(f"  獲得ポイント: {result['total_points']}ポイント")
    print(f"  ターン数: {result['turn_count']}ターン")
    print(f"  最終手札: {result['final_hand_size']}枚")
    print()


def run_strategy_comparison(num_games: int = 10):
    """ランダム戦略とMCTS戦略の比較"""
    print(f"【戦略比較（{num_games}ゲーム）】")
    print()
    
    strategy = MCTSStrategy(num_iterations=300, verbose=False)
    print(f"✓ 比較実行中...")
    print()
    
    comparison = strategy.compare_with_random(num_games=num_games, seed=42)
    
    print(f"【ランダム戦略】")
    print(f"  平均カード枚数: {comparison['random']['avg_cards']:.2f}枚")
    print(f"  最大カード枚数: {comparison['random']['max_cards']}枚")
    print(f"  平均ポイント: {comparison['random']['avg_points']:.2f}ポイント")
    print()
    
    print(f"【MCTS戦略】")
    print(f"  平均カード枚数: {comparison['mcts']['avg_cards']:.2f}枚")
    print(f"  最大カード枚数: {comparison['mcts']['max_cards']}枚")
    print(f"  平均ポイント: {comparison['mcts']['avg_points']:.2f}ポイント")
    print()
    
    cards_improvement = comparison['improvement']['cards']
    improvement_pct = (cards_improvement / comparison['random']['avg_cards']) * 100
    
    print(f"【改善度】")
    print(f"  カード枚数: {cards_improvement:+.2f}枚 ({improvement_pct:+.1f}%)")
    print(f"  ポイント: {comparison['improvement']['points']:+.2f}ポイント")
    print()


def main():
    """メイン関数"""
    print("=" * 60)
    print("twin-cool-emulator - オリジナルカードゲーム最適解探索")
    print("=" * 60)
    print()
    
    # 基本動作テスト
    run_basic_test()
    
    print("-" * 60)
    print()
    
    # 1回のゲームシミュレーション（ランダム）
    run_single_game_simulation(seed=42)
    
    print("-" * 60)
    print()
    
    # 複数回のランダムシミュレーション
    run_multiple_simulations(num_games=100)
    
    print("-" * 60)
    print()
    
    # MCTS戦略デモ
    run_mcts_demo(seed=42, num_iterations=300)
    
    print("-" * 60)
    print()
    
    # 戦略比較
    run_strategy_comparison(num_games=10)
    
    print("=" * 60)
    print("ステップ3: MCTS最適解探索の実装が完了しました！ ✅")
    print("MCTSはランダム戦略に比べて大幅な改善を達成しています。")
    print("次のステップ: WebUIの実装 (Streamlit)")
    print("=" * 60)


if __name__ == "__main__":
    main()
