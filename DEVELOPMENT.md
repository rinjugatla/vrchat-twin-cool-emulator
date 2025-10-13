# 開発ドキュメント

## 開発状況

### ステップ 1: 開発環境の構築 ✅ 完了

- [x] プロジェクト初期化（uv）
- [x] 依存関係の設定（numpy, streamlit）
- [x] MVCモデルに基づくフォルダ構造の構築
- [x] 基本クラスの実装とテスト

#### 実装済みクラス

| クラス | ファイル | 説明 | テスト |
|--------|---------|------|--------|
| `Suit` | `src/models/suit.py` | 8種類のスートを表すEnum | - |
| `Card` | `src/models/card.py` | カードクラス（スート+数値1-10） | ✅ 7テスト |
| `Deck` | `src/models/deck.py` | 山札クラス（80枚→10枚除外→70枚） | ✅ 6テスト |
| `Hand` | `src/models/hand.py` | 手札クラス | ✅ 7テスト |
| `FieldSlot` | `src/models/field_slot.py` | スロット（カードの山）クラス | ✅ 4テスト |
| `Field` | `src/models/field.py` | 場クラス（2つのスロット） | ✅ 6テスト |
| `PointCalculator` | `src/models/point_calculator.py` | ポイント計算ロジック | ✅ 11テスト |

**ステップ1 テスト数**: 41個 / 全て通過 ✅
**ステップ2 テスト数**: 30個 / 全て通過 ✅
**総テスト数**: 71個 / 全て通過 ✅

### ステップ 2: ゲームロジックの実装 ✅ 完了

#### 実装済みクラス

| クラス | ファイル | 説明 | テスト |
|--------|---------|------|--------|
| `MoveValidator` | `src/controllers/move_validator.py` | 合法手判定ロジック | ✅ 12テスト |
| `GameState` | `src/controllers/game_state.py` | ゲーム状態管理 | ✅ 8テスト |
| `Game` | `src/controllers/game.py` | ゲーム全体のフロー制御 | ✅ 10テスト |

**追加テスト数**: 30個 / 全て通過 ✅

#### 実装機能

1. ✅ **合法手判定** - 同じスートまたは同じ数値のカードを出せる
2. ✅ **ゲーム状態管理** - 手札、場、山札、ポイントを管理
3. ✅ **ランダムシミュレーション** - ゲームを自動でプレイ
4. ✅ **ゲーム終了判定** - 出せるカードがなくなったら終了
5. ✅ **統計情報収集** - 複数回のシミュレーション結果を分析

### ステップ 3: 最適解探索アルゴリズムの実装 📋 未着手

- モンテカルロ木探索（MCTS）の実装
- 状態評価関数の設計
- 学習/探索ループの実装

### ステップ 4: WebUIアプリケーションの実装 📋 未着手

- Streamlitによるインターフェース設計
- ユーザー入力処理
- 最適解の可視化

## コーディング規約

### ファイル命名規則

- **ファイル名**: スネークケース（例: `point_calculator.py`）
- **クラス名**: パスカルケース（例: `PointCalculator`）
- **関数/変数名**: スネークケース（例: `calculate_points`）

### プロジェクト構造規則

1. **1クラス1ファイル**の原則を守る
2. **ファイル名とクラス名を一致**させる
   - 例: `PointCalculator`クラス → `point_calculator.py`
3. **MVCモデル**に基づく配置
   - Models: `src/models/` - データとビジネスロジック
   - Controllers: `src/controllers/` - ゲームフロー制御
   - Views: `src/views/` - UI層（Streamlit）

### テスト規約

- **関数ごと**にテストケースを作成
- テストファイル名: `test_<モジュール名>.py`
- テストクラス名: `Test<クラス名>`
- テストメソッド名: `test_<機能説明>`

## テスト実行コマンド

### 全テスト実行

```powershell
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

### 特定のテストファイル実行

```powershell
uv run python -m unittest tests.test_card -v
```

### 特定のテストクラス実行

```powershell
uv run python -m unittest tests.test_card.TestCard -v
```

### 特定のテストメソッド実行

```powershell
uv run python -m unittest tests.test_card.TestCard.test_card_creation_valid -v
```

## 開発フロー

1. **機能設計** - 実装するクラス/メソッドを設計
2. **テストコード作成** - テストケースを先に作成（TDD）
3. **実装** - 機能を実装
4. **テスト実行** - テストが通ることを確認
5. **リファクタリング** - コードを最適化
6. **ドキュメント更新** - このファイルとREADMEを更新

## 変更履歴

### 2025-10-13

#### ステップ1完了
- 開発環境構築、基本クラス実装
- MVCモデルに基づくフォルダ構造に変更
- `points.py` → `point_calculator.py`にリネーム
- 全41テスト通過確認
- ドキュメント整備

#### ステップ2完了
- ゲームロジック層の実装（MoveValidator, GameState, Game）
- 合法手判定機能の実装
- ランダムシミュレーション機能の実装
- 全30テスト追加・通過確認（総計71テスト）
- main.pyにシミュレーションデモ追加
- ドキュメント更新

#### リファクタリング: 1クラス1ファイル原則の徹底
- `card.py`から`Suit`を分離 → `suit.py`作成
- `field.py`から`Slot`を分離 → `field_slot.py`作成、`FieldSlot`にリネーム
- 全テストのインポートパス更新
- 全70テスト通過確認
