# vrchat-twin-cool-emulator

VRChat内の「MedalGameWorld」ワールドに実装されたカードゲームのシミュレーションとWebUIアプリケーション

## プロジェクト概要

このプロジェクトは、VRChat内の「MedalGameWorld」ワールドで遊べるカードゲームをシミュレートし、探索アルゴリズム（MCTS、IS-MCTS、ヒューリスティック）を用いて最適な戦略を探索するプログラムです。最終的には、プレイヤーが次に取るべき最適な手をWebUIで提示します。

## 開発環境

- **OS**: Windows 11
- **Python**: 3.13.8
- **パッケージ管理**: uv
- **テスト**: unittest (Python標準ライブラリ)
- **WebUI**: Streamlit

## セットアップ

### 1. 依存関係のインストール

```powershell
uv sync
```

### 2. テストの実行

全テスト（126個）を実行：

```powershell
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

WebUIリファクタリング前後の動作保証テスト：

```powershell
uv run python tests/test_app_behavior.py
```

### 3. ゲームシミュレーションの実行

ランダム戦略とMCTS戦略のデモ：

```powershell
uv run python main.py
```

### 4. パフォーマンスベンチマーク

ヒューリスティック戦略のベンチマーク（100ゲーム）：

```powershell
uv run python benchmark_heuristic.py
```

ランダム戦略のベンチマーク（100ゲーム、比較用）：

```powershell
uv run python benchmark_random.py
```

MCTS vs ランダムの詳細な比較（20ゲーム）：

```powershell
uv run python benchmark_mcts.py
```

IS-MCTS（不完全情報対応）vs 各種戦略の比較（10ゲーム）：

```powershell
uv run python benchmark_ismcts.py
```

## プロジェクト構造

```
vrchat-twin-cool-emulator/
├── src/                           # ソースコード
│   ├── models/                    # データモデル層（MVC）
│   │   ├── __init__.py
│   │   ├── suit.py               # Suitクラス（Enum）
│   │   ├── card.py               # Cardクラス
│   │   ├── deck.py               # Deckクラス（山札）
│   │   ├── hand.py               # Handクラス（手札）
│   │   ├── field_slot.py         # FieldSlotクラス（スロット）
│   │   ├── field.py              # Fieldクラス（場）
│   │   └── point_calculator.py   # PointCalculatorクラス
│   ├── controllers/               # ゲームロジック層（MVC）
│   │   ├── __init__.py
│   │   ├── move_validator.py     # MoveValidatorクラス
│   │   ├── game_state.py         # GameStateクラス
│   │   ├── game.py               # Gameクラス
│   │   ├── evaluator.py          # Evaluatorクラス（評価関数）
│   │   ├── mcts_node.py          # MCTSNodeクラス（MCTS木）
│   │   ├── mcts_engine.py        # MCTSEngineクラス（探索）
│   │   ├── mcts_strategy.py      # MCTSStrategyクラス（戦略API）
│   │   ├── observable_game_state.py  # ObservableGameStateクラス（不完全情報）
│   │   ├── flexibility_calculator.py # FlexibilityCalculatorクラス
│   │   ├── heuristic_strategy.py     # HeuristicStrategyクラス（高速戦略）
│   │   ├── information_set.py        # InformationSetクラス（IS-MCTS用）
│   │   ├── determinizer.py           # Determinizerクラス（決定化生成）
│   │   ├── ismcts_node.py            # ISMCTSNodeクラス（IS-MCTSノード）
│   │   ├── ismcts_engine.py          # ISMCTSEngineクラス（IS-MCTS探索）
│   │   └── ismcts_strategy.py        # ISMCTSStrategyクラス（IS-MCTS戦略）
│   ├── views/                     # ユーザーインターフェース層（MVC）✅
│   │   ├── __init__.py
│   │   ├── components/           # UIコンポーネント
│   │   ├── dialogs/              # ダイアログ
│   │   ├── styles/               # スタイル定義
│   │   └── utils/                # ユーティリティ
│   └── __init__.py
├── tests/                         # テストコード
│   ├── __init__.py
│   ├── test_card.py
│   ├── test_deck.py
│   ├── test_hand.py
│   ├── test_field.py
│   └── test_point_calculator.py
├── app.py                         # Streamlit WebUIアプリ（今後追加）
├── main.py                        # メインエントリーポイント
├── benchmark_mcts.py             # MCTSパフォーマンスベンチマーク
├── pyproject.toml                # プロジェクト設定
└── README.md                     # このファイル
```

## 開発ステップ

- [x] **ステップ 1**: 開発環境の構築 ✅
- [x] **ステップ 2**: ゲームロジックの実装 ✅
- [x] **ステップ 3**: MCTS最適解探索の実装 ✅
- [x] **ステップ 4**: WebUIアプリケーションの実装 ✅
- [x] **ステップ 5**: WebUIリファクタリング ✅（661行→244行、-63%削減）
- [x] **ステップ 6**: ヒューリスティック戦略の実装 ✅
- [x] **ステップ 7**: IS-MCTS（不完全情報対応）の実装 ✅

## 🎮 WebUIの起動

```powershell
uv run streamlit run app.py
```

ブラウザで http://localhost:8501 にアクセスして、インタラクティブにゲームをプレイできます！

### WebUIの主な機能

#### 基本機能

- **ゲーム状態の可視化**: ターン数、場に出したカード枚数、獲得ポイントなど
- **手札表示**: スートごとに色分けされたカード表示
- **場のスロット表示**: 2つのスロットのトップカードを表示
- **📊 山札状況表示**: 全80枚のカードを表形式で視覚的に表示
  - 🟥 赤色: 推奨カード（次に使うべきカード）
  - 🟨 黄色: 手札のカード
  - 薄い数値: 使用済みカード（場に出したカード）
  - 空欄: 山札に含まれないカード（初期の10枚除外）
  - 通常: 山札に残っているカード
- **🎯 除外カード・初期手札指定機能**: 山札から除外する10枚と初期手札5枚を手動で選択可能
  - ランダムゲーム開始と完全指定ゲーム開始の両方に対応
  - 2ステップで設定: ①除外カード10枚 → ②初期手札5枚
  - 特定のシナリオをテストしたり、戦略を検証できる
- **履歴表示**: プレイ履歴の確認（スート絵文字付き）

#### 戦略選択

- **🎲 戦略選択**: 2つの戦略から選択可能
  - **ヒューリスティック戦略（高速）**: 即座に結果表示（推奨）
  - **MCTS戦略（精密）**: より精密な解を探索（時間がかかる）
- **📝 戦略の説明**: ヒューリスティック戦略では、なぜそのカードを選んだかの詳細な説明を表示

#### 🎯 自動計算機能（2025-10-14追加）

- **手札更新時の自動計算**: 手札を場に出し、山札からカードを追加すると、自動的に次の最適解を計算
- **戦略変更時の即座再計算**: 戦略を変更（ヒューリスティック⇔MCTS、または探索回数変更）すると、即座に最適解を再計算
- **スムーズなプレイ体験**: 毎回「最適解を分析」ボタンを押す必要がなく、自動的に次の手が提示される

詳細は [WEBUI_GUIDE.md](WEBUI_GUIDE.md) を参照してください。

## パフォーマンス

詳細な評価結果は [PERFORMANCE_EVALUATION.md](PERFORMANCE_EVALUATION.md) を参照してください。

### ランダム戦略（ベースライン）

- 平均カード枚数: **6.47枚** / 70枚
- 平均ポイント: 0.00pt
- 実行時間: <0.001秒/ゲーム

### ヒューリスティック戦略（推奨）⚡

- 平均カード枚数: **7.70枚** / 70枚 (**+19.0%改善** 🎯)
- 最大カード枚数: **48枚**
- 平均ポイント: 0.04pt
- 実行時間: 0.0018秒/ゲーム（**MCTS戦略の1000倍以上高速**）

### MCTS戦略（完全情報）

- 平均カード枚数: **25.3枚** / 70枚 (**+291%改善** 🎉)
- 最大カード枚数: **50枚**
- 平均ポイント: 0.0pt
- 実行時間: 1.9秒/ゲーム（200反復）
- **注意**: 山札の順序を完全に知っている状態で探索（実戦では使用不可）

### IS-MCTS戦略（不完全情報）

- 平均カード枚数: **9.9枚** / 70枚 (**+43.5%改善** 📊)
- 最大カード枚数: 未測定
- 平均ポイント: 0.0pt
- 実行時間: 2.1秒/ゲーム（200反復）
- **特徴**: 山札の順序を未知として扱う実戦的な戦略
- **用途**: 研究・実験、不完全情報ゲームの探索アルゴリズム検証

## 戦略の比較と選択

| 戦略 | 平均カード数 | 速度 | 用途 | 推奨度 |
|------|-------------|------|------|--------|
| **ランダム** | 6.9枚 | ⚡⚡⚡ | ベースライン比較 | - |
| **ヒューリスティック** | 7.7枚 | ⚡⚡⚡ | 実用的なプレイ | ⭐⭐⭐ |
| **IS-MCTS** | 9.9枚 | ⚡ | 実戦・研究 | ⭐⭐ |
| **MCTS（完全情報）** | 25.3枚 | ⚡ | 練習・最高性能確認 | ⭐ |

### 各戦略の詳細

**ヒューリスティック戦略（推奨）**:
- **長所**: 即座に結果表示、実用的な性能、説明付き
- **短所**: 複雑な局面では最適解を見逃す可能性
- **最適な用途**: WebUIでのリアルタイムプレイ

**IS-MCTS戦略（実戦モード）**:
- **長所**: 不完全情報を正しく扱う、理論的に正しい実装
- **短所**: ヒューリスティックと同程度の性能、実行時間が長い
- **最適な用途**: 不完全情報ゲームの研究、アルゴリズム検証

**MCTS戦略（練習モード）**:
- **長所**: 最高の性能、最適解に近い手を探索
- **短所**: 山札を見る「チート」状態、実戦では使用不可
- **最適な用途**: 理論上の最高性能確認、戦略研究

詳細は [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) を参照してください。

**推奨事項**: 
- **実用プレイ**: ヒューリスティック戦略（高速・実用的）
- **研究・実験**: IS-MCTS戦略（不完全情報対応）
- **性能確認**: MCTS戦略（理論上の最高性能）

## ライセンス

MIT License
