# ドキュメント索引

**vrchat-twin-cool-emulator** プロジェクトの全ドキュメント一覧

---

## 📚 主要ドキュメント

### プロジェクト概要

| ドキュメント | 説明 |
|------------|------|
| [README.md](README.md) | プロジェクトの概要、セットアップ方法、使い方 |
| [SUMMARY.md](SUMMARY.md) | プロジェクト完成サマリー、全体像の把握 |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | ファイル構造とクラス一覧の詳細 |

### 開発・設計ドキュメント

| ドキュメント | 説明 |
|------------|------|
| [DEVELOPMENT.md](DEVELOPMENT.md) | 開発履歴、進捗状況、技術的決定事項 |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | AI開発プロンプト、開発方針 |

### WebUI関連

| ドキュメント | 説明 |
|------------|------|
| [WEBUI_GUIDE.md](WEBUI_GUIDE.md) | WebUIの使用方法、機能説明 |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) | WebUIリファクタリングレビュー |

### 性能評価・ベンチマーク

| ドキュメント | 説明 |
|------------|------|
| [PERFORMANCE_EVALUATION.md](PERFORMANCE_EVALUATION.md) | ヒューリスティック戦略の性能評価 |
| [HEURISTIC_ANALYSIS.md](HEURISTIC_ANALYSIS.md) | ヒューリスティック戦略の詳細分析 |
| [APPROACH_COMPARISON.md](APPROACH_COMPARISON.md) | 戦略アプローチの比較 |

### IS-MCTS（不完全情報対応）関連

| ドキュメント | 説明 |
|------------|------|
| [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) | **IS-MCTS実装・評価レポート（最新）** |
| [ISMCTS_DESIGN.md](ISMCTS_DESIGN.md) | IS-MCTSの設計ドキュメント |
| [ISMCTS_IMPLEMENTATION_PLAN.md](ISMCTS_IMPLEMENTATION_PLAN.md) | IS-MCTS実装計画 |
| [ISMCTS_DESIGN_REVIEW.md](ISMCTS_DESIGN_REVIEW.md) | IS-MCTS設計レビュー |
| [ISMCTS_REVIEW.md](ISMCTS_REVIEW.md) | IS-MCTS実装検討 |

### その他

| ドキュメント | 説明 |
|------------|------|
| [IMPLEMENTATION_REVIEW.md](IMPLEMENTATION_REVIEW.md) | 実装レビュー（履歴） |

---

## 🧪 ベンチマーク・テスト実行ファイル

### ベンチマークスクリプト

| ファイル | 説明 | 実行方法 |
|---------|------|---------|
| `benchmark_random.py` | ランダム戦略ベンチマーク（100ゲーム） | `uv run python benchmark_random.py` |
| `benchmark_heuristic.py` | ヒューリスティック戦略ベンチマーク（100ゲーム） | `uv run python benchmark_heuristic.py` |
| `benchmark_mcts.py` | MCTS vs ランダム比較（20ゲーム） | `uv run python benchmark_mcts.py` |
| `benchmark_ismcts.py` | **IS-MCTS vs 各種戦略比較（10ゲーム）** | `uv run python benchmark_ismcts.py` |

### ベンチマーク結果ファイル

| ファイル | 説明 |
|---------|------|
| `random_benchmark_results.txt` | ランダム戦略の詳細結果 |
| `heuristic_benchmark_results.txt` | ヒューリスティック戦略の詳細結果 |

### メインプログラム

| ファイル | 説明 | 実行方法 |
|---------|------|---------|
| `main.py` | ゲームシミュレーションデモ | `uv run python main.py` |
| `app.py` | Streamlit WebUIアプリケーション | `uv run streamlit run app.py` |

---

## 🎯 戦略の性能まとめ

### 200イテレーション時の性能

| 戦略 | 平均カード数 | 実行時間 | 改善率 | ドキュメント |
|------|-------------|---------|--------|------------|
| **ランダム** | 6.9枚 | <0.001秒 | - | - |
| **ヒューリスティック** | 7.7枚 | 0.002秒 | +11.6% | [HEURISTIC_ANALYSIS.md](HEURISTIC_ANALYSIS.md) |
| **IS-MCTS** | 9.9枚 | 2.1秒 | +43.5% | [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) |
| **MCTS（完全情報）** | 25.3枚 | 1.9秒 | +266.7% | [PERFORMANCE_EVALUATION.md](PERFORMANCE_EVALUATION.md) |

### 戦略の特徴と用途

| 戦略 | 特徴 | 推奨用途 |
|------|------|---------|
| **ランダム** | 合法手からランダム選択 | ベースライン比較 |
| **ヒューリスティック** | 柔軟性スコアに基づく高速戦略 | 実用的なプレイ（推奨） |
| **IS-MCTS** | 不完全情報を正しく扱う | 実戦・研究・アルゴリズム検証 |
| **MCTS** | 山札を知っている状態で探索 | 練習・理論上の最高性能確認 |

---

## 📖 読む順序の推奨

### 初めての方

1. [README.md](README.md) - プロジェクト概要を把握
2. [SUMMARY.md](SUMMARY.md) - 全体像と成果を理解
3. [WEBUI_GUIDE.md](WEBUI_GUIDE.md) - WebUIを使ってみる

### 開発者・技術者

1. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - ファイル構造を理解
2. [DEVELOPMENT.md](DEVELOPMENT.md) - 開発履歴を把握
3. [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) - 最新の実装と評価を確認
4. [PERFORMANCE_EVALUATION.md](PERFORMANCE_EVALUATION.md) - 性能詳細を分析

### 研究者・アルゴリズム志向

1. [APPROACH_COMPARISON.md](APPROACH_COMPARISON.md) - 戦略アプローチの比較
2. [ISMCTS_DESIGN.md](ISMCTS_DESIGN.md) - IS-MCTSの設計を理解
3. [ISMCTS_EVALUATION_REPORT.md](ISMCTS_EVALUATION_REPORT.md) - 実装と評価結果を分析
4. [HEURISTIC_ANALYSIS.md](HEURISTIC_ANALYSIS.md) - ヒューリスティック戦略の詳細

---

## 🔧 テスト実行

### 全テスト実行（164テスト）

```powershell
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

### 個別テスト実行

```powershell
# Models層のテスト
uv run python -m unittest tests.test_card -v
uv run python -m unittest tests.test_deck -v

# Controllers層のテスト
uv run python -m unittest tests.test_game -v
uv run python -m unittest tests.test_mcts_engine -v

# IS-MCTS関連のテスト
uv run python -m unittest tests.test_information_set -v
uv run python -m unittest tests.test_ismcts_integration -v

# ヒューリスティック戦略のテスト
uv run python -m unittest tests.test_heuristic_strategy -v
```

### WebUI動作保証テスト

```powershell
uv run python tests/test_app_behavior.py
```

---

## 📝 最終更新

- **更新日**: 2025年10月14日
- **プロジェクトステータス**: 全7ステップ完了 ✅
- **総テスト数**: 164テスト / 全て通過 ✅
- **実装クラス数**: 24クラス
- **戦略数**: 4種類(ランダム、ヒューリスティック、IS-MCTS、MCTS)

---

**vrchat-twin-cool-emulator** - VRChat「MedalGameWorld」ワールドのカードゲームエミュレータ  
プロジェクト完成
