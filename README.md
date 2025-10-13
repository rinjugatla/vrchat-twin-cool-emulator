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

```powershell
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

## プロジェクト構造

```
twin-cool-emulator/
├── src/                           # ソースコード
│   ├── models/                    # データモデル層（MVC）
│   │   ├── __init__.py
│   │   ├── card.py               # Card, Suitクラス
│   │   ├── deck.py               # Deckクラス（山札）
│   │   ├── hand.py               # Handクラス（手札）
│   │   ├── field.py              # Field, Slotクラス（場）
│   │   └── point_calculator.py   # PointCalculatorクラス
│   ├── controllers/               # ゲームロジック層（MVC）
│   │   ├── __init__.py
│   │   └── game.py               # Gameクラス（今後追加）
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
├── pyproject.toml                # プロジェクト設定
└── README.md                     # このファイル
```

## 開発ステップ

- [x] **ステップ 1**: 開発環境の構築
- [ ] **ステップ 2**: ゲームロジックの実装
- [ ] **ステップ 3**: 最適解探索アルゴリズムの実装
- [ ] **ステップ 4**: WebUIアプリケーションの実装

## ライセンス

MIT License
