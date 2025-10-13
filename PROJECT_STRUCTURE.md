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
│   │   ├── card.py               # Card, Suit
│   │   ├── deck.py               # Deck
│   │   ├── hand.py               # Hand
│   │   ├── field.py              # Field, Slot
│   │   └── point_calculator.py   # PointCalculator
│   ├── controllers/               # 🚧 コントローラー層（今後実装）
│   │   └── __init__.py
│   ├── views/                     # 📋 ビュー層（今後実装）
│   │   └── __init__.py
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
| `Suit` | `src/models/card.py` | 8種類のスートEnum | - |
| `Card` | `src/models/card.py` | カードクラス | 7 |
| `Deck` | `src/models/deck.py` | 山札（70枚） | 6 |
| `Hand` | `src/models/hand.py` | 手札管理 | 7 |
| `Slot` | `src/models/field.py` | カードの山 | 4 |
| `Field` | `src/models/field.py` | 場（2スロット） | 6 |
| `PointCalculator` | `src/models/point_calculator.py` | ポイント計算 | 11 |

**総テスト数**: 41テスト / 全て通過 ✅

#### 🚧 次の実装予定 (ステップ2)

| クラス | 予定ファイルパス | 役割 |
|--------|----------------|------|
| `MoveValidator` | `src/controllers/move_validator.py` | 合法手判定 |
| `GameState` | `src/controllers/game_state.py` | ゲーム状態管理 |
| `Game` | `src/controllers/game.py` | ゲーム全体制御 |

#### 📋 未着手 (ステップ3-4)

- ステップ3: モンテカルロ木探索（MCTS）実装
- ステップ4: Streamlit WebUI実装

### 🔧 コーディング規約の遵守状況

- ✅ 1クラス1ファイルの原則
- ✅ ファイル名はスネークケース
- ✅ クラス名はパスカルケース
- ✅ ファイル名とクラス名の一致
- ✅ MVCモデルに基づくフォルダ構造
- ✅ 関数ごとのテストコード作成
- ✅ PEP8準拠

### 🚀 次のステップ

**ステップ 2: ゲームロジックの実装**に進む準備が整いました。

次に実装するクラス：
1. `MoveValidator` - 合法手判定ロジック
2. `GameState` - ゲーム状態とポイント累積管理
3. `Game` - ゲーム全体のフロー制御とランダムシミュレーション
