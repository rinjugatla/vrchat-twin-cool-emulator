"""
ヒューリスティック戦略の性能評価スクリプト

このスクリプトは、ヒューリスティック戦略を使用して複数回ゲームをシミュレートし、
統計データを収集します。

実行方法:
    uv run python benchmark_heuristic.py
"""

import time
from typing import List, Dict, Tuple
import statistics

from src.controllers.game import Game
from src.controllers.heuristic_strategy import HeuristicStrategy
from src.controllers.observable_game_state import ObservableGameState


def run_single_game(game_id: int, verbose: bool = False) -> Dict:
    """
    単一のゲームをヒューリスティック戦略で実行
    
    Args:
        game_id: ゲームID（ログ用）
        verbose: 詳細ログを出力するかどうか
        
    Returns:
        ゲーム結果の辞書（cards_played, points, turns, time_taken）
    """
    game = Game()
    strategy = HeuristicStrategy(verbose=verbose)
    played_cards = []
    
    start_time = time.time()
    turn = 0
    
    while True:
        # 現在の状態から観測可能な状態を構築
        obs_state = ObservableGameState.from_game_state(game.state, played_cards)
        
        # 最適手を取得
        best_move = strategy.get_best_move(obs_state)
        
        if best_move is None:
            # ゲーム終了
            break
        
        card, slot = best_move
        
        # 手を実行
        success = game.state.play_card(card, slot)
        
        if not success:
            if verbose:
                print(f"[Game {game_id}] ターン {turn}: カード {card} をスロット {slot} に出せませんでした")
            break
        
        played_cards.append(card)
        turn += 1
        
        if verbose and turn % 10 == 0:
            print(f"[Game {game_id}] ターン {turn}: {len(played_cards)}枚プレイ済み")
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    # 最終結果
    cards_played = len(played_cards)
    points = game.state.total_points
    
    result = {
        'game_id': game_id,
        'cards_played': cards_played,
        'points': points,
        'turns': turn,
        'time_taken': time_taken
    }
    
    if verbose:
        print(f"[Game {game_id}] 終了: {cards_played}枚プレイ, {points}ポイント, {time_taken:.3f}秒")
    
    return result


def run_benchmark(num_games: int = 100, verbose_interval: int = 10) -> List[Dict]:
    """
    複数回ゲームを実行してベンチマークを行う
    
    Args:
        num_games: 実行するゲーム数
        verbose_interval: 詳細ログを出力する間隔（0で無効）
        
    Returns:
        全ゲームの結果リスト
    """
    results = []
    
    print(f"ヒューリスティック戦略の性能評価を開始します（{num_games}回実行）")
    print("-" * 80)
    
    total_start_time = time.time()
    
    for i in range(num_games):
        verbose = (verbose_interval > 0 and (i + 1) % verbose_interval == 0)
        
        if not verbose:
            # 簡易進捗表示
            if (i + 1) % 10 == 0:
                print(f"進捗: {i + 1}/{num_games} ゲーム完了")
        
        result = run_single_game(i + 1, verbose=verbose)
        results.append(result)
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    print("-" * 80)
    print(f"全{num_games}ゲーム完了（合計時間: {total_time:.2f}秒）")
    
    return results


def analyze_results(results: List[Dict]) -> None:
    """
    ベンチマーク結果を分析して統計情報を表示
    
    Args:
        results: ゲーム結果のリスト
    """
    cards_played_list = [r['cards_played'] for r in results]
    points_list = [r['points'] for r in results]
    time_list = [r['time_taken'] for r in results]
    
    print("\n" + "=" * 80)
    print("統計結果")
    print("=" * 80)
    
    # カード枚数の統計
    print("\n【場に出したカード枚数】")
    print(f"  平均:   {statistics.mean(cards_played_list):.2f} 枚")
    print(f"  中央値: {statistics.median(cards_played_list):.2f} 枚")
    print(f"  最小:   {min(cards_played_list)} 枚")
    print(f"  最大:   {max(cards_played_list)} 枚")
    print(f"  標準偏差: {statistics.stdev(cards_played_list):.2f}")
    
    # ポイントの統計
    print("\n【獲得ポイント】")
    print(f"  平均:   {statistics.mean(points_list):.2f} ポイント")
    print(f"  中央値: {statistics.median(points_list):.2f} ポイント")
    print(f"  最小:   {min(points_list)} ポイント")
    print(f"  最大:   {max(points_list)} ポイント")
    print(f"  標準偏差: {statistics.stdev(points_list):.2f}")
    
    # 実行時間の統計
    print("\n【実行時間（1ゲームあたり）】")
    print(f"  平均:   {statistics.mean(time_list):.4f} 秒")
    print(f"  中央値: {statistics.median(time_list):.4f} 秒")
    print(f"  最小:   {min(time_list):.4f} 秒")
    print(f"  最大:   {max(time_list):.4f} 秒")
    
    # カード枚数の分布
    print("\n【カード枚数の分布】")
    distribution = {}
    for count in cards_played_list:
        distribution[count] = distribution.get(count, 0) + 1
    
    for count in sorted(distribution.keys()):
        bar_length = distribution[count]
        bar = "█" * bar_length
        print(f"  {count:2d}枚: {bar} ({distribution[count]}回)")
    
    # ベストゲーム
    print("\n【ベストゲーム（カード枚数）】")
    best_game = max(results, key=lambda r: r['cards_played'])
    print(f"  ゲームID: {best_game['game_id']}")
    print(f"  カード枚数: {best_game['cards_played']} 枚")
    print(f"  ポイント: {best_game['points']}")
    print(f"  実行時間: {best_game['time_taken']:.4f} 秒")
    
    # ワーストゲーム
    print("\n【ワーストゲーム（カード枚数）】")
    worst_game = min(results, key=lambda r: r['cards_played'])
    print(f"  ゲームID: {worst_game['game_id']}")
    print(f"  カード枚数: {worst_game['cards_played']} 枚")
    print(f"  ポイント: {worst_game['points']}")
    print(f"  実行時間: {worst_game['time_taken']:.4f} 秒")
    
    print("\n" + "=" * 80)


def main():
    """メイン処理"""
    # 100回実行
    results = run_benchmark(num_games=100, verbose_interval=0)
    
    # 結果分析
    analyze_results(results)
    
    # 結果をファイルに保存
    output_file = "heuristic_benchmark_results.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ヒューリスティック戦略 ベンチマーク結果\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"Game {result['game_id']:3d}: "
                   f"{result['cards_played']:2d}枚, "
                   f"{result['points']:3d}pts, "
                   f"{result['time_taken']:.4f}秒\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("\n統計サマリー\n")
        f.write("-" * 80 + "\n")
        
        cards_list = [r['cards_played'] for r in results]
        points_list = [r['points'] for r in results]
        time_list = [r['time_taken'] for r in results]
        
        f.write(f"\nカード枚数: 平均={statistics.mean(cards_list):.2f}, "
               f"中央値={statistics.median(cards_list):.2f}, "
               f"最小={min(cards_list)}, "
               f"最大={max(cards_list)}\n")
        
        f.write(f"ポイント: 平均={statistics.mean(points_list):.2f}, "
               f"中央値={statistics.median(points_list):.2f}, "
               f"最小={min(points_list)}, "
               f"最大={max(points_list)}\n")
        
        f.write(f"実行時間: 平均={statistics.mean(time_list):.4f}秒, "
               f"中央値={statistics.median(time_list):.4f}秒\n")
    
    print(f"\n詳細結果を {output_file} に保存しました。")


if __name__ == "__main__":
    main()
