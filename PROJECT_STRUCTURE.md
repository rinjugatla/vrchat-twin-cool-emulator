# プロジェクト構造サマリー

## 更新日: 2025-10-13

### ✅ 完了した修正内容

1. **MVCモデルに基づくフォルダ構造の実装**
   - `src/models/` - データモデルとビジネスロジック
   - `src/controllers/` - ゲームフロー制御（今後実装）
   - `src/views/` - UI層（今後実装）

2. **ファイル名とクラス名の一致**
   - `points.py` → `point_calculator.py` にリネーム
   - `PointCalculator`クラスと一致

3. **全テストのインポートパス更新**
   - `from src.card import Card` → `from src.models.card import Card`
   - 全40テスト通過を確認 ✅

4. **ドキュメント整備**
   - `README.md` - プロジェクト概要とセットアップ手順
   - `DEVELOPMENT.md` - 開発状況とコーディング規約
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
│   │   └── mcts_strategy.py      # MCTSStrategy
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

**ステップ1 テスト数**: 41テスト
**ステップ2 テスト数**: 30テスト
**WebUIリファクタリングテスト**: 11テスト
**総テスト数**: 82テスト / 全て通過 ✅

#### ✅ 完了 (ステップ2)

| クラス | ファイルパス | 役割 | テスト数 |
|--------|-------------|------|---------|
| `MoveValidator` | `src/controllers/move_validator.py` | 合法手判定 | 12 |
| `GameState` | `src/controllers/game_state.py` | ゲーム状態管理 | 8 |
| `Game` | `src/controllers/game.py` | ゲーム全体制御 | 10 |
| `Evaluator` | `src/controllers/evaluator.py` | 評価関数 | 6 |
| `MCTSNode` | `src/controllers/mcts_node.py` | MCTS木ノード | 9 |
| `MCTSEngine` | `src/controllers/mcts_engine.py` | MCTS探索エンジン | 12 |
| `MCTSStrategy` | `src/controllers/mcts_strategy.py` | MCTS戦略API | 16 |

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

#### 📋 全ステップ完了 ✅

- ✅ ステップ1: 開発環境構築
- ✅ ステップ2: ゲームロジック実装
- ✅ ステップ3: モンテカルロ木探索（MCTS）実装
- ✅ ステップ4: Streamlit WebUI実装
- ✅ ステップ5: WebUIのリファクタリング（MVCモデル適用）

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

### 🎉 ステップ2完了

**ステップ 2: ゲームロジックの実装**が完了しました！

実装した機能：
- ✅ 合法手判定（同じスート or 同じ数値）
- ✅ ゲーム状態管理（手札、場、山札、ポイント）
- ✅ ランダムシミュレーション（ゲーム終了まで自動プレイ）
- ✅ 統計情報収集（100回シミュレーション）

### 🚀 次のステップ

**ステップ 3: 最適解探索アルゴリズムの実装**

実装予定：
1. モンテカルロ木探索（MCTS）の実装
2. 状態評価関数の設計
3. より高いスコアを達成する戦略の学習
