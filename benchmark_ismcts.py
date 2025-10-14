"""
IS-MCTSベンチマーク
IS-MCTSと既存戦略の性能比較
"""

import time
import random
from typing import List, Dict, Tuple
from src.controllers.game_state import GameState
from src.controllers.observable_game_state import ObservableGameState
from src.controllers.move_validator import MoveValidator
from src.controllers.heuristic_strategy import HeuristicStrategy
from src.controllers.mcts_strategy import MCTSStrategy
from src.controllers.ismcts_strategy import ISMCTSStrategy


class GameResult:
    """ゲーム結果を保持するクラス"""
    
    def __init__(self, cards_played: int, total_points: int, turns: int, time_taken: float):
        self.cards_played = cards_played
        self.total_points = total_points
        self.turns = turns
        self.time_taken = time_taken
    
    def __repr__(self):
        return (
            f"GameResult(cards={self.cards_played}, "
            f"points={self.total_points}, "
            f"turns={self.turns}, "
            f"time={self.time_taken:.2f}s)"
        )


def play_game_with_random(seed: int) -> GameResult:
    """ランダム戦略でゲームをプレイ"""
    start_time = time.time()
    
    game_state = GameState(seed=seed)
    turn_count = 0
    
    while MoveValidator.has_valid_move(game_state.get_hand(), game_state.get_field()):
        valid_moves = MoveValidator.get_valid_moves(
            game_state.get_hand(),
            game_state.get_field()
        )
        
        if len(valid_moves) == 0:
            break
        
        # ランダムに手を選択
        card, slot = random.choice(valid_moves)
        game_state.play_card(card, slot)
        turn_count += 1
    
    time_taken = time.time() - start_time
    
    return GameResult(
        game_state.get_cards_played_count(),
        game_state.get_total_points(),
        turn_count,
        time_taken
    )


def play_game_with_heuristic(seed: int) -> GameResult:
    """ヒューリスティック戦略でゲームをプレイ"""
    start_time = time.time()
    
    game_state = GameState(seed=seed)
    strategy = HeuristicStrategy()
    turn_count = 0
    
    while MoveValidator.has_valid_move(game_state.get_hand(), game_state.get_field()):
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        best_move = strategy.get_best_move(obs_state)
        
        if best_move is None:
            break
        
        card, slot = best_move
        game_state.play_card(card, slot)
        turn_count += 1
    
    time_taken = time.time() - start_time
    
    return GameResult(
        game_state.get_cards_played_count(),
        game_state.get_total_points(),
        turn_count,
        time_taken
    )


def play_game_with_mcts(seed: int, num_iterations: int = 100) -> GameResult:
    """通常MCTS戦略でゲームをプレイ"""
    start_time = time.time()
    
    game_state = GameState(seed=seed)
    strategy = MCTSStrategy(num_iterations=num_iterations)
    turn_count = 0
    
    while MoveValidator.has_valid_move(game_state.get_hand(), game_state.get_field()):
        best_move = strategy.get_best_move(game_state)
        
        if best_move is None:
            break
        
        card, slot = best_move
        game_state.play_card(card, slot)
        turn_count += 1
    
    time_taken = time.time() - start_time
    
    return GameResult(
        game_state.get_cards_played_count(),
        game_state.get_total_points(),
        turn_count,
        time_taken
    )


def play_game_with_ismcts(seed: int, num_iterations: int = 100) -> GameResult:
    """IS-MCTS戦略でゲームをプレイ"""
    start_time = time.time()
    
    game_state = GameState(seed=seed)
    strategy = ISMCTSStrategy(num_iterations=num_iterations, verbose=False)
    turn_count = 0
    
    while MoveValidator.has_valid_move(game_state.get_hand(), game_state.get_field()):
        # 観測可能状態を構築
        obs_state = ObservableGameState.from_game_state(
            game_state,
            game_state.get_played_cards()
        )
        
        best_move = strategy.get_best_move(obs_state)
        
        if best_move is None:
            break
        
        card, slot = best_move
        game_state.play_card(card, slot)
        turn_count += 1
    
    time_taken = time.time() - start_time
    
    return GameResult(
        game_state.get_cards_played_count(),
        game_state.get_total_points(),
        turn_count,
        time_taken
    )


def calculate_statistics(results: List[GameResult]) -> Dict:
    """結果の統計を計算"""
    if len(results) == 0:
        return {}
    
    cards_played = [r.cards_played for r in results]
    points = [r.total_points for r in results]
    times = [r.time_taken for r in results]
    
    return {
        'avg_cards': sum(cards_played) / len(cards_played),
        'max_cards': max(cards_played),
        'min_cards': min(cards_played),
        'avg_points': sum(points) / len(points),
        'max_points': max(points),
        'min_points': min(points),
        'avg_time': sum(times) / len(times),
        'total_time': sum(times)
    }


def print_statistics(strategy_name: str, stats: Dict):
    """統計を表示"""
    print(f"\n{'='*60}")
    print(f"{strategy_name}")
    print(f"{'='*60}")
    print(f"平均カード数:   {stats['avg_cards']:.2f} (最大: {stats['max_cards']}, 最小: {stats['min_cards']})")
    print(f"平均ポイント:   {stats['avg_points']:.2f} (最大: {stats['max_points']}, 最小: {stats['min_points']})")
    print(f"平均実行時間:   {stats['avg_time']:.3f}秒")
    print(f"合計実行時間:   {stats['total_time']:.2f}秒")


def run_benchmark(num_games: int = 10, mcts_iterations: int = 100, ismcts_iterations: int = 100):
    """
    ベンチマークを実行
    
    Args:
        num_games: 実行するゲーム数
        mcts_iterations: 通常MCTSのイテレーション数
        ismcts_iterations: IS-MCTSのイテレーション数
    """
    print(f"\n{'#'*60}")
    print(f"# IS-MCTS ベンチマーク")
    print(f"# ゲーム数: {num_games}")
    print(f"# MCTS イテレーション: {mcts_iterations}")
    print(f"# IS-MCTS イテレーション: {ismcts_iterations}")
    print(f"{'#'*60}")
    
    # 各戦略でゲームを実行
    seeds = list(range(100, 100 + num_games))
    
    print("\n[1/4] ランダム戦略を実行中...")
    random_results = [play_game_with_random(seed) for seed in seeds]
    
    print("[2/4] ヒューリスティック戦略を実行中...")
    heuristic_results = [play_game_with_heuristic(seed) for seed in seeds]
    
    print("[3/4] 通常MCTS戦略を実行中...")
    mcts_results = [play_game_with_mcts(seed, mcts_iterations) for seed in seeds]
    
    print("[4/4] IS-MCTS戦略を実行中...")
    ismcts_results = [play_game_with_ismcts(seed, ismcts_iterations) for seed in seeds]
    
    # 統計を計算
    random_stats = calculate_statistics(random_results)
    heuristic_stats = calculate_statistics(heuristic_results)
    mcts_stats = calculate_statistics(mcts_results)
    ismcts_stats = calculate_statistics(ismcts_results)
    
    # 結果を表示
    print_statistics("ランダム戦略", random_stats)
    print_statistics("ヒューリスティック戦略", heuristic_stats)
    print_statistics("通常MCTS戦略", mcts_stats)
    print_statistics("IS-MCTS戦略", ismcts_stats)
    
    # 比較表を表示
    print(f"\n{'='*60}")
    print("比較サマリー")
    print(f"{'='*60}")
    print(f"{'戦略':<20} {'平均カード':<12} {'平均ポイント':<12} {'平均時間(秒)':<12}")
    print(f"{'-'*60}")
    print(f"{'ランダム':<20} {random_stats['avg_cards']:<12.2f} {random_stats['avg_points']:<12.2f} {random_stats['avg_time']:<12.3f}")
    print(f"{'ヒューリスティック':<20} {heuristic_stats['avg_cards']:<12.2f} {heuristic_stats['avg_points']:<12.2f} {heuristic_stats['avg_time']:<12.3f}")
    print(f"{'通常MCTS':<20} {mcts_stats['avg_cards']:<12.2f} {mcts_stats['avg_points']:<12.2f} {mcts_stats['avg_time']:<12.3f}")
    print(f"{'IS-MCTS':<20} {ismcts_stats['avg_cards']:<12.2f} {ismcts_stats['avg_points']:<12.2f} {ismcts_stats['avg_time']:<12.3f}")
    
    # 改善率を計算
    print(f"\n{'='*60}")
    print("IS-MCTS vs 他戦略の改善率")
    print(f"{'='*60}")
    
    if random_stats['avg_cards'] > 0:
        improvement_vs_random = ((ismcts_stats['avg_cards'] - random_stats['avg_cards']) / random_stats['avg_cards']) * 100
        print(f"vs ランダム:           {improvement_vs_random:+.1f}% (カード数)")
    
    if heuristic_stats['avg_cards'] > 0:
        improvement_vs_heuristic = ((ismcts_stats['avg_cards'] - heuristic_stats['avg_cards']) / heuristic_stats['avg_cards']) * 100
        print(f"vs ヒューリスティック: {improvement_vs_heuristic:+.1f}% (カード数)")
    
    if mcts_stats['avg_cards'] > 0:
        improvement_vs_mcts = ((ismcts_stats['avg_cards'] - mcts_stats['avg_cards']) / mcts_stats['avg_cards']) * 100
        print(f"vs 通常MCTS:          {improvement_vs_mcts:+.1f}% (カード数)")
    
    print(f"\n{'='*60}\n")
    
    return {
        'random': random_stats,
        'heuristic': heuristic_stats,
        'mcts': mcts_stats,
        'ismcts': ismcts_stats
    }


if __name__ == '__main__':
    # ベンチマークを実行
    # テスト用に少ないゲーム数とイテレーション数で実行
    results = run_benchmark(num_games=10, mcts_iterations=50, ismcts_iterations=50)
