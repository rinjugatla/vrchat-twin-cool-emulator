"""
twin-cool-emulator メインエントリーポイント
オリジナルカードゲーム「最適解探索プログラム」
"""

from src.models import Card, Suit, Deck, Hand, Field, PointCalculator
from src.controllers import Game, MoveValidator, GameState


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
    
    # 1回のゲームシミュレーション
    run_single_game_simulation(seed=42)
    
    print("-" * 60)
    print()
    
    # 複数回のシミュレーション
    run_multiple_simulations(num_games=100)
    
    print("=" * 60)
    print("ステップ2: ゲームロジックの実装が完了しました！")
    print("次のステップ: 最適解探索アルゴリズムの実装")
    print("=" * 60)


if __name__ == "__main__":
    main()
