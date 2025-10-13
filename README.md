# twin-cool-emulator

オリジナルカードゲーム「最適解探索プログラム」のシミュレーションとWebUIアプリケーション

## プロジェクト概要

このプロジェクトは、特定のルールに基づくカードゲームをシミュレートし、機械学習を用いて最適な戦略を探索するプログラムです。最終的には、プレイヤーが次に取るべき最適な手をWebUIで提示します。

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

全テスト（114個）を実行：

```powershell
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

### 3. ゲームシミュレーションの実行

ランダム戦略とMCTS戦略のデモ：

```powershell
uv run python main.py
```

### 4. パフォーマンスベンチマーク

MCTS vs ランダムの詳細な比較（20ゲーム）：

```powershell
uv run python benchmark_mcts.py
```

## プロジェクト構造

```
twin-cool-emulator/
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
│   │   └── mcts_strategy.py      # MCTSStrategyクラス（戦略API）
│   ├── views/                     # ユーザーインターフェース層（MVC）
│   │   └── __init__.py
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

## 🎮 WebUIの起動

```powershell
uv run streamlit run app.py
```

ブラウザで http://localhost:8501 にアクセスして、インタラクティブにゲームをプレイできます！

### WebUIの主な機能

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
- **最適解の分析**: MCTSアルゴリズムによる最適な手の提案
- **履歴表示**: プレイ履歴の確認（スート絵文字付き）

詳細は [WEBUI_GUIDE.md](WEBUI_GUIDE.md) を参照してください。

## パフォーマンス

### ランダム戦略（ベースライン）
- 平均カード枚数: **6.4枚** / 70枚
- 平均ポイント: 0.1pt

### MCTS戦略（500反復/手）
- 平均カード枚数: **17.8枚** / 70枚 (**+178.1%改善** 🎉)
- 最大カード枚数: **50枚**
- 平均ポイント: 0.1pt

MCTSは**ランダム戦略の約3倍**のパフォーマンスを達成しています！

## ライセンス

MIT License
