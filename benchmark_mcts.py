"""
MCTSパフォーマンスベンチマーク
ランダム戦略 vs MCTS戦略の比較
"""

from src.controllers.mcts_strategy import MCTSStrategy


def run_benchmark():
    """ベンチマーク実行"""
    print("=" * 60)
    print("MCTS パフォーマンスベンチマーク")
    print("=" * 60)
    
    # 設定
    num_games = 20
    num_iterations = 500
    
    print(f"\n設定:")
    print(f"  ゲーム数: {num_games}")
    print(f"  MCTS反復回数: {num_iterations}")
    
    # 戦略を作成
    strategy = MCTSStrategy(num_iterations=num_iterations, verbose=False)
    
    # 比較実行
    print(f"\n実行中... (これには数分かかる場合があります)")
    comparison = strategy.compare_with_random(num_games=num_games, seed=42)
    
    # 結果表示
    print("\n" + "=" * 60)
    print("結果")
    print("=" * 60)
    
    print("\n[ランダム戦略]")
    print(f"  平均カード枚数: {comparison['random']['avg_cards']:.2f}")
    print(f"  最大カード枚数: {comparison['random']['max_cards']}")
    print(f"  最小カード枚数: {comparison['random']['min_cards']}")
    print(f"  平均ポイント: {comparison['random']['avg_points']:.2f}")
    print(f"  最大ポイント: {comparison['random']['max_points']}")
    
    print("\n[MCTS戦略]")
    print(f"  平均カード枚数: {comparison['mcts']['avg_cards']:.2f}")
    print(f"  最大カード枚数: {comparison['mcts']['max_cards']}")
    print(f"  最小カード枚数: {comparison['mcts']['min_cards']}")
    print(f"  平均ポイント: {comparison['mcts']['avg_points']:.2f}")
    print(f"  最大ポイント: {comparison['mcts']['max_points']}")
    
    print("\n[改善度]")
    cards_improvement = comparison['improvement']['cards']
    points_improvement = comparison['improvement']['points']
    
    print(f"  カード枚数: {cards_improvement:+.2f} ({cards_improvement / comparison['random']['avg_cards'] * 100:+.1f}%)")
    print(f"  ポイント: {points_improvement:+.2f}")
    
    print("\n" + "=" * 60)
    
    # 結論
    if cards_improvement > 5:
        print("結論: MCTSは大幅な改善を示しています！ ✅")
    elif cards_improvement > 2:
        print("結論: MCTSは顕著な改善を示しています。 ✅")
    elif cards_improvement > 0:
        print("結論: MCTSは軽微な改善を示しています。 ⚠️")
    else:
        print("結論: MCTSは期待通りの改善を示していません。 ❌")
    
    print("=" * 60)


if __name__ == '__main__':
    run_benchmark()
