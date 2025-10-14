# プロジェクト構造サマリー

## 更新日: 2025-10-14

### ✅ 完了した修正内容

1. **MVCモデルに基づくフォルダ構造の実装**
   - `src/models/` - データモデルとビジネスロジック（7クラス）
   - `src/controllers/` - ゲームフロー制御（13クラス）
   - `src/views/` - UI層（11ファイル）

2. **4つの戦略実装**
   - ランダム戦略（ベースライン）
   - ヒューリスティック戦略（実用推奨）
   - IS-MCTS戦略（不完全情報対応）
   - MCTS戦略（完全情報、練習用）

3. **全テスト通過**
   - 全164テスト通過を確認 ✅

4. **ドキュメント整備**
   - `README.md` - プロジェクト概要とセットアップ手順
   - `DEVELOPMENT.md` - 開発状況とコーディング規約
   - `ISMCTS_EVALUATION_REPORT.md` - IS-MCTS実装・評価レポート
   - このファイル（PROJECT_STRUCTURE.md）

### 📁 現在のディレクトリ構造

```
twin-cool-emulator/
├── .git/                          # Gitリポジトリ
├── .github/                       # GitHub設定
│   └── copilot-instructions.md   # 開発プロンプト
├── .venv/                         # Python仮想環境（uvが管理）
├── src/                           # ソースコード
│   ├── models/                    # ✅ データモデル層
│   │   ├── __init__.py
│   │   ├── suit.py               # Suit
│   │   ├── card.py               # Card
│   │   ├── deck.py               # Deck
│   │   ├── hand.py               # Hand
│   │   ├── field_slot.py         # FieldSlot
│   │   ├── field.py              # Field
│   │   └── point_calculator.py   # PointCalculator
│   ├── controllers/               # ✅ コントローラー層
│   │   ├── __init__.py
│   │   ├── move_validator.py     # MoveValidator
│   │   ├── game_state.py         # GameState
│   │   ├── game.py               # Game
│   │   ├── evaluator.py          # Evaluator
│   │   ├── mcts_node.py          # MCTSNode
│   │   ├── mcts_engine.py        # MCTSEngine
│   │   ├── mcts_strategy.py      # MCTSStrategy
│   │   ├── observable_game_state.py  # ObservableGameState
│   │   ├── flexibility_calculator.py # FlexibilityCalculator
│   │   ├── heuristic_strategy.py     # HeuristicStrategy
│   │   ├── information_set.py        # InformationSet
│   │   ├── determinizer.py           # Determinizer
│   │   ├── ismcts_node.py            # ISMCTSNode
│   │   ├── ismcts_engine.py          # ISMCTSEngine
│   │   └── ismcts_strategy.py        # ISMCTSStrategy
│   ├── views/                     # ✅ ビュー層（リファクタリング完了）
│   │   ├── __init__.py
│   │   ├── components/           # UIコンポーネント
│   │   │   ├── __init__.py
│   │   │   ├── game_state_display.py     # ゲーム状態表示
│   │   │   ├── hand_display.py           # 手札表示
│   │   │   ├── field_display.py          # 場表示
│   │   │   ├── deck_status_display.py    # 山札状況表示
│   │   │   └── card_selection_table.py   # カード選択テーブル
│   │   ├── dialogs/              # ダイアログ
│   │   │   ├── __init__.py
│   │   │   ├── exclude_card_dialog.py    # 除外カード選択
│   │   │   └── hand_selection_dialog.py  # 初期手札選択
│   │   ├── styles/               # スタイル定義
│   │   │   ├── __init__.py
│   │   │   └── card_table_styles.py      # CSSスタイル
│   │   └── utils/                # ユーティリティ
│   │       ├── __init__.py
│   │       ├── ui_helpers.py             # UI補助関数
│   │       └── session_manager.py        # セッション管理
│   └── __init__.py
├── tests/                         # ✅ テストコード
│   ├── __init__.py
│   ├── test_card.py              # 7テスト
│   ├── test_deck.py              # 6テスト
│   ├── test_hand.py              # 7テスト
│   ├── test_field.py             # 10テスト
│   └── test_point_calculator.py  # 11テスト
├── .gitignore                     # Git除外設定
├── .python-version                # Python バージョン指定
├── main.py                        # ✅ メインエントリーポイント
├── pyproject.toml                # ✅ プロジェクト設定
├── uv.lock                        # uvロックファイル
├── README.md                      # ✅ プロジェクト概要
├── DEVELOPMENT.md                 # ✅ 開発ドキュメント
└── PROJECT_STRUCTURE.md          # ✅ このファイル
```

### 📊 実装状況

#### ✅ 完了 (ステップ1)

| クラス | ファイルパス | 役割 | テスト数 |
|--------|-------------|------|---------|
| `Suit` | `src/models/suit.py` | 8種類のスートEnum | - |
| `Card` | `src/models/card.py` | カードクラス | 7 |
| `Deck` | `src/models/deck.py` | 山札（70枚） | 6 |
| `Hand` | `src/models/hand.py` | 手札管理 | 7 |
| `FieldSlot` | `src/models/field_slot.py` | カードの山 | 4 |
| `Field` | `src/models/field.py` | 場（2スロット） | 6 |
| `PointCalculator` | `src/models/point_calculator.py` | ポイント計算 | 11 |

**ステップ1 (Models) テスト数**: 41テスト
**ステップ2 (Game Logic) テスト数**: 30テスト
**ステップ3 (MCTS) テスト数**: 43テスト
**ステップ4 (WebUI) テスト数**: 1テスト
**ステップ5 (Refactoring) テスト数**: 11テスト
**ステップ6 (Heuristic) テスト数**: 26テスト
**ステップ7 (IS-MCTS) テスト数**: 12テスト
**総テスト数**: 164テスト / 全て通過 ✅

#### ✅ 完了 (ステップ2 & 3)

| クラス | ファイルパス | 役割 | テスト数 |
|--------|-------------|------|---------|
| `MoveValidator` | `src/controllers/move_validator.py` | 合法手判定 | 12 |
| `GameState` | `src/controllers/game_state.py` | ゲーム状態管理 | 8 |
| `Game` | `src/controllers/game.py` | ゲーム全体制御 | 10 |
| `Evaluator` | `src/controllers/evaluator.py` | 評価関数 | 6 |
| `MCTSNode` | `src/controllers/mcts_node.py` | MCTS木ノード | 9 |
| `MCTSEngine` | `src/controllers/mcts_engine.py` | MCTS探索エンジン | 12 |
| `MCTSStrategy` | `src/controllers/mcts_strategy.py` | MCTS戦略API | 16 |
| `ObservableGameState` | `src/controllers/observable_game_state.py` | 不完全情報状態 | 6 |
| `FlexibilityCalculator` | `src/controllers/flexibility_calculator.py` | 柔軟性計算 | 4 |
| `HeuristicStrategy` | `src/controllers/heuristic_strategy.py` | ヒューリスティック戦略 | 16 |
| `InformationSet` | `src/controllers/information_set.py` | 情報セット | 6 |
| `Determinizer` | `src/controllers/determinizer.py` | 決定化生成 | - |
| `ISMCTSNode` | `src/controllers/ismcts_node.py` | IS-MCTSノード | - |
| `ISMCTSEngine` | `src/controllers/ismcts_engine.py` | IS-MCTS探索エンジン | - |
| `ISMCTSStrategy` | `src/controllers/ismcts_strategy.py` | IS-MCTS戦略API | 6 |

#### 🎨 WebUIアプリケーション (ステップ4) ✅

| ファイル | 説明 | 行数 |
|---------|------|------|
| `app.py` | Streamlit WebUIアプリケーション（リファクタリング後） | 244行 |
| `app_old.py` | 元のapp.py（バックアップ） | 661行 |
| `WEBUI_GUIDE.md` | WebUI使用方法ドキュメント | - |

**WebUI主要機能**:

- ゲーム状態の視覚化（スート絵文字付き）
- 📊 山札状況表示（8スート×10数値の表形式）
- リアルタイムMCTS最適解分析
- 履歴管理（スート絵文字付き）
- 除外カード指定機能
- 初期手札指定機能
- 🎯 **自動計算機能**（2025-10-14追加）
  - 手札更新時の自動最適解計算
  - 戦略変更時の即座再計算
  - ボタン操作不要のスムーズなプレイ体験

#### 📋 全ステップ完了 ✅

- ✅ ステップ1: 開発環境構築
- ✅ ステップ2: ゲームロジック実装
- ✅ ステップ3: モンテカルロ木探索（MCTS）実装
- ✅ ステップ4: Streamlit WebUI実装
- ✅ ステップ5: WebUIのリファクタリング（MVCモデル適用）
- ✅ ステップ6: ヒューリスティック戦略実装
- ✅ ステップ7: IS-MCTS（不完全情報対応）実装

#### ✅ WebUIリファクタリング完了

**リファクタリング成果**:
- **コードサイズ削減**: `app.py` 661行 → 244行（**-63%削減**）
- **モジュール分割**: 1ファイル → 11ファイル（components, dialogs, styles, utils）
- **保守性向上**: 各機能が独立したファイルに分離
- **テスト保証**: 11/11テスト成功（リファクタリング前後で同じ動作を保証）

**新しいビュー層の構造**:
- `components/`: 再利用可能なUIコンポーネント（5ファイル）
- `dialogs/`: ダイアログ画面（2ファイル）
- `styles/`: CSSスタイル定義（1ファイル）
- `utils/`: ユーティリティ関数（2ファイル）

### 🔧 コーディング規約の遵守状況

- ✅ 1クラス1ファイルの原則
- ✅ ファイル名はスネークケース
- ✅ クラス名はパスカルケース
- ✅ ファイル名とクラス名の一致
- ✅ MVCモデルに基づくフォルダ構造
- ✅ 関数ごとのテストコード作成
- ✅ PEP8準拠

### 🎉 全ステップ完了

**twin-cool-emulator プロジェクト完成！**

実装した機能：
- ✅ 完全なゲームエンジン（8スート×10数値、70枚）
- ✅ 4つの戦略実装
  - ランダム戦略（ベースライン）
  - ヒューリスティック戦略（実用推奨）
  - IS-MCTS戦略（不完全情報対応）
  - MCTS戦略（完全情報、練習用）
- ✅ WebUIアプリケーション（Streamlit）
- ✅ 164個の包括的なテスト
- ✅ 詳細な性能評価とドキュメント

### � 戦略の性能比較（200イテレーション）

| 戦略 | 平均カード数 | 速度 | 用途 |
|------|-------------|------|------|
| ランダム | 6.9枚 | ⚡⚡⚡ | ベースライン |
| ヒューリスティック | 7.7枚 | ⚡⚡⚡ | 実用プレイ（推奨） |
| IS-MCTS | 9.9枚 | ⚡ | 実戦・研究 |
| MCTS（完全情報） | 25.3枚 | ⚡ | 練習・性能確認 |

詳細は [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) を参照してください。
