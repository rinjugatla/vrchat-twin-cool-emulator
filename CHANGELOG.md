# 変更履歴 (CHANGELOG)

このファイルには、プロジェクトの重要な変更履歴を記録します。

---

## [2025-10-14] - 除外カード選択制限の修正

### 修正

- **🐛 手札追加時の除外カード選択制限**
  - WebUIで手札にカードを追加する際、最初に山札から除外した10枚のカードが選択できないように修正
  - `initialize_session_state()`と`reset_game()`でゲーム初期化後に実際に除外されたカードを取得して`st.session_state.excluded_cards`に保存するよう変更
  - これにより、カード追加ダイアログで除外カードが正しく無効化される

### 変更したファイル

- `src/views/utils/session_manager.py`: 除外カードをセッション状態に保存
- `tests/test_excluded_cards_in_session.py`: 除外カード管理の新規テストを追加

### テスト結果

- 新規テスト6件追加、全て成功 ✅
- 除外カードが山札に含まれないことを確認
- 除外カードが手札に追加できないことを確認

---

## [2025-10-14] - WebUI自動計算機能の追加

### 追加

- **🎯 自動最適解計算機能**
  - 手札を場に出し、山札からカードを追加すると、自動的に次の最適解を計算
  - 戦略を変更（ヒューリスティック⇔MCTS、または探索回数変更）すると、即座に最適解を再計算
  - 毎回「最適解を分析」ボタンを押す必要がなくなり、スムーズなプレイ体験を実現

### 変更したファイル

- `app.py`: 戦略変更検出ロジック、自動計算フラグ処理を追加
- `src/views/dialogs/add_card_dialog.py`: 手札追加後に自動計算フラグを設定
- `README.md`: WebUI機能セクションに自動計算機能を追加
- `WEBUI_GUIDE.md`: 自動計算機能の詳細説明とプレイフローを追加
- `PROJECT_STRUCTURE.md`: WebUI機能リストに自動計算機能を追加
- `DEVELOPMENT.md`: 変更履歴に実装内容を記録

### テスト結果

- 全177テスト成功 ✅
- 既存機能への影響なし

---

## [2025-10-14] - IS-MCTS（不完全情報対応）の実装

### 追加

- **IS-MCTS戦略**: Information Set Monte Carlo Tree Search
  - 不完全情報ゲームに対応した探索アルゴリズム
  - 決定化（Determinization）による探索
  - 平均9.9枚/ゲーム（ランダム比+43.5%改善）

### 新規ファイル

- `src/controllers/information_set.py`: InformationSetクラス
- `src/controllers/determinizer.py`: Determinizerクラス
- `src/controllers/ismcts_node.py`: ISMCTSNodeクラス
- `src/controllers/ismcts_engine.py`: ISMCTSEngineクラス
- `src/controllers/ismcts_strategy.py`: ISMCTSStrategyクラス
- `tests/test_information_set.py`: InformationSetのテスト
- `tests/test_ismcts_integration.py`: IS-MCTS統合テスト
- `benchmark_ismcts.py`: IS-MCTSベンチマークスクリプト
- `ISMCTS_EVALUATION_REPORT.md`: 評価レポート

### ドキュメント更新

- `README.md`: IS-MCTS戦略の説明追加
- `DEVELOPMENT.md`: ステップ7完了記録

---

## [2025-10-13] - ヒューリスティック戦略の実装

### 追加

- **ヒューリスティック戦略**: 高速かつ実用的な戦略
  - 柔軟性スコアに基づく手の選択
  - 平均7.70枚/ゲーム（ランダム比+19.0%改善）
  - 実行時間: 0.0018秒/ゲーム（MCTS比1000倍以上高速）
  - 説明機能付き（なぜそのカードを選んだか）

### 新規ファイル

- `src/controllers/observable_game_state.py`: ObservableGameStateクラス
- `src/controllers/flexibility_calculator.py`: FlexibilityCalculatorクラス
- `src/controllers/heuristic_strategy.py`: HeuristicStrategyクラス
- `tests/test_observable_game_state.py`: テスト
- `tests/test_flexibility_calculator.py`: テスト
- `tests/test_heuristic_strategy.py`: テスト
- `benchmark_heuristic.py`: ヒューリスティックベンチマーク
- `benchmark_random.py`: ランダムベンチマーク（比較用）
- `PERFORMANCE_EVALUATION.md`: 性能評価レポート

### WebUI更新

- 戦略選択UI（ヒューリスティック/MCTS）
- 戦略の説明表示機能

---

## [2025-10-13] - WebUIリファクタリング（MVCモデル適用）

### 変更

- **app.pyのリファクタリング**: 661行 → 244行（-63%削減）
- **MVCモデルに基づくビュー層の分割**
  - `src/views/components/`: UIコンポーネント（5ファイル）
  - `src/views/dialogs/`: ダイアログ（3ファイル）
  - `src/views/styles/`: スタイル定義（1ファイル）
  - `src/views/utils/`: ユーティリティ（2ファイル）

### 新規ファイル

- `src/views/components/game_state_display.py`
- `src/views/components/hand_display.py`
- `src/views/components/field_display.py`
- `src/views/components/deck_status_display.py`
- `src/views/components/card_selection_table.py`
- `src/views/dialogs/exclude_card_dialog.py`
- `src/views/dialogs/hand_selection_dialog.py`
- `src/views/dialogs/add_card_dialog.py`
- `src/views/styles/card_table_styles.py`
- `src/views/utils/ui_helpers.py`
- `src/views/utils/session_manager.py`
- `tests/test_app_behavior.py`: 動作保証テスト（11テスト）

### テスト結果

- 全126テスト成功 ✅

---

## [2025-10-13] - WebUIアプリケーションの実装（ステップ4完了）

### 追加

- **Streamlit WebUI**: `app.py`
  - ゲーム状態の視覚化
  - 手札・場・山札の表示
  - MCTS最適解分析機能
  - 履歴表示
  - 除外カード・初期手札指定機能
  - 山札状況表示（8×10テーブル）

### 新規ファイル

- `app.py`: WebUIメインファイル
- `WEBUI_GUIDE.md`: WebUI使用方法ドキュメント

---

## [2025-10-13] - MCTS（モンテカルロ木探索）の実装（ステップ3完了）

### 追加

- **MCTS探索アルゴリズム**
  - 平均17.8枚/ゲーム（ランダム比+178%改善）
  - UCB1ベースの選択戦略
  - 評価関数による状態評価

### 新規ファイル

- `src/controllers/evaluator.py`: Evaluatorクラス
- `src/controllers/mcts_node.py`: MCTSNodeクラス
- `src/controllers/mcts_engine.py`: MCTSEngineクラス
- `src/controllers/mcts_strategy.py`: MCTSStrategyクラス
- `tests/test_evaluator.py`: 7テスト
- `tests/test_mcts_node.py`: 14テスト
- `tests/test_mcts_engine.py`: 11テスト
- `tests/test_mcts_strategy.py`: 11テスト
- `benchmark_mcts.py`: MCTSベンチマーク

### テスト結果

- 全114テスト成功 ✅

---

## [2025-10-13] - ゲームロジックの実装（ステップ2完了）

### 追加

- **合法手判定**: MoveValidatorクラス
- **ゲーム状態管理**: GameStateクラス
- **ゲームフロー制御**: Gameクラス
- **ランダムシミュレーション**: 平均6.4枚/ゲーム

### 新規ファイル

- `src/controllers/move_validator.py`: 12テスト
- `src/controllers/game_state.py`: 8テスト
- `src/controllers/game.py`: 10テスト
- `main.py`: シミュレーションデモ

### テスト結果

- 全71テスト成功 ✅

---

## [2025-10-13] - 開発環境の構築（ステップ1完了）

### 追加

- **プロジェクト初期化**
  - uvによる依存関係管理
  - MVCモデルに基づくフォルダ構造
  - 基本クラスの実装とテスト

### 実装済みクラス

- `Suit`: 8種類のスートを表すEnum
- `Card`: カードクラス（スート+数値1-10）
- `Deck`: 山札クラス（80枚→10枚除外→70枚）
- `Hand`: 手札クラス
- `FieldSlot`: スロット（カードの山）クラス
- `Field`: 場クラス（2つのスロット）
- `PointCalculator`: ポイント計算ロジック

### テスト結果

- 全41テスト成功 ✅

---

## プロジェクト概要

**プロジェクト名**: twin-cool-emulator
**目的**: VRChat「MedalGameWorld」ワールドのカードゲームエミュレータ

### 技術スタック

- **言語**: Python 3.13.8
- **パッケージ管理**: uv
- **テスト**: unittest
- **WebUI**: Streamlit
- **開発環境**: Windows 11, PowerShell

### ゲームルール

- 8種類のスート × 10数値 = 80枚
- 初期除外: 10枚 → 山札: 70枚
- 初期手札: 5枚
- 場: 2つのスロット
- 目標: 場に出したカード枚数の最大化
