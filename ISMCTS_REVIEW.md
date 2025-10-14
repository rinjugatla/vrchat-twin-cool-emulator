# IS-MCTS 実装検討レビュー

## 📋 目的

ランダムな山札に対して最適な戦略を選択するため、**情報セットMCTS (IS-MCTS)** の実装を検討する。

## 🎯 なぜIS-MCTSが必要か

### 現状の問題点

1. **通常のMCTSの限界**
   - 現在の`MCTSEngine`は**完全情報**を前提としている
   - 山札の順序が既知であると仮定した探索を行う
   - **実際のゲームプレイでは山札の順序は未知**

2. **実際のゲーム状況**
   - プレイヤーが知っているのは：手札、場の状態、既出カード
   - プレイヤーが知らないのは：山札の順序、除外された10枚
   - この**情報の非対称性**を考慮した探索が必要

### IS-MCTSの利点

1. **不完全情報への対応**
   - 複数の可能な山札配置（決定化）を考慮
   - 各決定化で探索木を共有することで効率的に学習

2. **実戦での有効性**
   - 実際のゲームプレイに近い状況で学習
   - より堅牢な戦略を獲得可能

## 📊 既存実装との比較

| 項目 | 通常MCTS | IS-MCTS |
|------|----------|---------|
| **情報前提** | 完全情報 | 不完全情報 |
| **ノード単位** | ゲーム状態 | 情報セット |
| **探索木** | 1つの世界 | 複数の世界で共有 |
| **決定化** | 不要 | 毎イテレーション生成 |
| **適用場面** | テスト・ベンチマーク | 実際のゲームプレイ |

## 🏗️ アーキテクチャ概要

### コンポーネント構成

```
IS-MCTS実装
├── ObservableGameState (既存)
│   └── プレイヤーの観測可能な情報
├── InformationSet (新規)
│   └── 情報セットの識別・ハッシュ化
├── Determinizer (新規)
│   └── 決定化の生成
├── ISMCTSNode (新規)
│   └── 情報セット単位のノード
├── ISMCTSEngine (新規)
│   └── IS-MCTSアルゴリズムの実行
└── ISMCTSStrategy (新規)
    └── 戦略インターフェース
```

### データフロー

```
実際のゲーム状態
    ↓
ObservableGameState（観測可能情報のみ）
    ↓
InformationSet（ハッシュ可能な識別子）
    ↓
ISMCTSEngine.search()
    ├→ Determinizer（山札をサンプリング）
    ├→ MCTS探索（情報セット単位）
    └→ 統計更新（全決定化で共有）
    ↓
最良の手を返す
```

## 🔧 実装計画

### Phase 1: 基盤クラス（情報セット関連）

#### 1.1 InformationSet クラス
**ファイル**: `src/controllers/information_set.py`

**役割**:
- プレイヤーから見て区別がつかない状態群を識別
- ハッシュ化により辞書のキーとして使用可能
- ノードの共有を実現

**重要な設計判断**:
```python
# 情報セットの同一性判定基準
- 手札のカード（順序無視）
- 場のトップカード
- 既出カード（順序無視）

# 山札の順序や残り枚数は含めない
# → 同じ観測可能情報なら同じ情報セット
```

**実装のポイント**:
- `__hash__()`: タプル化してハッシュ値計算
- `__eq__()`: 各要素を比較
- カードのソート: 順序を無視するため

#### 1.2 Determinizer クラス
**ファイル**: `src/controllers/determinizer.py`

**役割**:
- 観測可能状態から完全なゲーム状態をサンプリング
- 未出現カードを山札と除外10枚にランダム分配

**アルゴリズム**:
```python
def create_determinization(observable_state):
    # 1. 未出現カード取得
    unplayed = 全80枚 - 手札 - 既出カード
    
    # 2. ランダムに10枚除外
    shuffle(unplayed)
    excluded = unplayed[:10]
    deck = unplayed[10:]
    
    # 3. 山札シャッフル
    shuffle(deck)
    
    # 4. GameState構築
    return GameState.from_observable_determinization(...)
```

**注意点**:
- 毎回異なる決定化を生成（乱数シード管理）
- 既知情報（手札、場）は保持
- `GameState.from_observable_determinization()` メソッドが必要

### Phase 2: IS-MCTSコア実装

#### 2.1 ISMCTSNode クラス
**ファイル**: `src/controllers/ismcts_node.py`

**従来のMCTSNodeとの差異**:

| 項目 | MCTSNode | ISMCTSNode |
|------|----------|------------|
| ノード識別 | GameState | InformationSet |
| 親子関係 | 状態遷移 | 手（move）によるインデックス |
| 統計共有 | 単一状態のみ | 全決定化で共有 |

**データ構造**:
```python
class ISMCTSNode:
    info_set: InformationSet      # 情報セット
    visits: int                   # 訪問回数（全決定化共有）
    total_reward: float           # 累積報酬（全決定化共有）
    children: Dict[Move, ISMCTSNode]  # 子ノード
    untried_moves: List[Move]     # 未試行の手
```

**重要メソッド**:
- `ucb1_score()`: UCB1計算（探索と活用のバランス）
- `select_best_child()`: UCB1で最良の子を選択
- `get_best_move()`: 最も訪問された手を返す

#### 2.2 ISMCTSEngine クラス
**ファイル**: `src/controllers/ismcts_engine.py`

**IS-MCTSの核心アルゴリズム**:

```python
def search(observable_state, num_iterations):
    root_info_set = 情報セット抽出(observable_state)
    root_node = ノード取得または作成(root_info_set)
    
    for i in range(num_iterations):
        # 1. 決定化生成
        determinized_state = Determinizer.create_determinization(observable_state)
        
        # 2. MCTS 1イテレーション
        #    - Selection: UCB1で選択
        #    - Expansion: 新しい手を試す
        #    - Simulation: ランダムプレイアウト
        #    - Backpropagation: 情報セット単位で更新
        run_one_iteration(root_node, determinized_state)
    
    return root_node.get_best_move()
```

**キーポイント**:
1. **情報セットツリーのキャッシュ**: `info_set_tree: Dict[InformationSet, ISMCTSNode]`
2. **ノードの共有**: 同じ情報セットなら同じノードを使用
3. **決定化ごとの探索**: 毎回異なる山札で探索するが、統計は共有

### Phase 3: GameState拡張

**ファイル**: `src/controllers/game_state.py` (既存)

**追加が必要なメソッド**:

```python
@staticmethod
def from_observable_determinization(
    hand, field, deck_cards, excluded_cards,
    total_points, turn_count
) -> GameState:
    """決定化から完全なGameStateを構築"""
    # Deckの内部状態を直接設定
    # 順序を保持したまま復元
```

**設計上の課題**:
- `Deck`クラスの内部状態（`_cards`）へのアクセス
- カプセル化を維持しつつ柔軟な初期化を実現

**解決策**:
1. `Deck`に`from_cards_list()`コンストラクタを追加
2. または`GameState`でのみ特殊な初期化を許可

### Phase 4: 戦略インターフェース

#### ISMCTSStrategy クラス
**ファイル**: `src/controllers/ismcts_strategy.py`

**役割**:
- 既存の`MCTSStrategy`と同じインターフェースを提供
- WebUIから簡単に利用可能
- ゲームループとの統合

**インターフェース**:
```python
class ISMCTSStrategy:
    def get_best_move(
        self,
        observable_state: ObservableGameState
    ) -> Optional[Tuple[Card, int]]:
        """最良の手を返す"""
        best_move, stats = self.engine.search(
            observable_state,
            self.num_iterations
        )
        return best_move
```

## 🧪 テスト戦略

### 各クラスのユニットテスト

#### test_information_set.py
```python
- 同じ情報セットのハッシュ値が一致
- 異なる情報セットは区別される
- 手札の順序が違っても同じ情報セット
```

#### test_determinizer.py
```python
- 未出現カードから正しく山札を生成
- 除外10枚が含まれない
- 合計70枚（山札 + 手札）になる
```

#### test_ismcts_node.py
```python
- UCB1スコアの計算が正しい
- 最良の手の選択が機能する
- 統計更新が正しい
```

#### test_ismcts_engine.py
```python
- 決定化ごとに異なる山札で探索
- 情報セットツリーの共有が機能
- 最良の手が返される
```

### 統合テスト

#### test_ismcts_integration.py
```python
- 実際のゲーム状況でIS-MCTSを実行
- 通常MCTSと同じインターフェースで動作
- 合理的な手を選択する
```

## 📈 性能評価計画

### ベンチマーク項目

1. **探索効率**
   - イテレーション数ごとのスコア向上
   - 情報セットツリーのサイズ
   - 決定化数と性能の関係

2. **戦略比較**
   ```
   ランダム戦略
   ↓ (改善)
   ヒューリスティック戦略
   ↓ (改善)
   通常MCTS（完全情報）
   ↓ (改善?)
   IS-MCTS（不完全情報）
   ```

3. **実行時間**
   - 1000イテレーションあたりの実行時間
   - 決定化生成のオーバーヘッド
   - ノードキャッシュの効果

### ベンチマークスクリプト

**ファイル**: `benchmark_ismcts.py`

```python
# 100ゲームを実行して統計を取得
results = []
for game in range(100):
    # IS-MCTSで最後までプレイ
    score = play_game_with_ismcts()
    results.append(score)

# 結果を分析
平均スコア
標準偏差
最高・最低スコア
```

## ⚠️ 実装上の課題と対策

### 課題1: 計算コスト

**問題**: 
- 決定化を毎イテレーション生成するため、通常MCTSより遅い
- 情報セットツリーのメモリ消費

**対策**:
1. **効率的な決定化生成**
   - カードリストの再利用
   - 必要な部分のみコピー

2. **ノードキャッシュの最適化**
   - LRUキャッシュの導入
   - 古いノードの削除

3. **並列化**
   - 複数の決定化を並列処理（Phase 5で検討）

### 課題2: 情報セットの粒度

**問題**:
- 情報セットが細かすぎる → ノードが共有されない
- 情報セットが粗すぎる → 異なる状況を区別できない

**対策**:
1. **適切な情報セット定義**
   - 手札、場のトップカード、既出カード
   - ポイント情報は含めない（報酬で評価）

2. **実験的な調整**
   - 場のカード枚数を含めるか？
   - ターン数を含めるか？
   - ベンチマークで最適な粒度を探索

### 課題3: 既存コードとの統合

**問題**:
- `GameState`は完全情報を前提
- `Game`クラスとの整合性
- WebUIでの使用方法

**対策**:
1. **ObservableGameState を中心に設計**
   - 既存の`GameState`は内部で使用
   - 外部インターフェースは`ObservableGameState`

2. **戦略パターンの活用**
   - `Strategy`インターフェースを統一
   - `MCTSStrategy`, `HeuristicStrategy`, `ISMCTSStrategy`

3. **段階的な導入**
   - まず独立したモジュールとして実装
   - テストで動作確認後、WebUIに統合

## 🎯 実装の優先順位

### 優先度: 高

1. ✅ **ObservableGameState** (既に実装済み)
2. 🔴 **InformationSet** - 情報セットの定義が核心
3. 🔴 **Determinizer** - 決定化生成が必須
4. 🔴 **ISMCTSNode** - ノード管理の実装

### 優先度: 中

5. 🟡 **ISMCTSEngine** - メインアルゴリズム
6. 🟡 **ISMCTSStrategy** - インターフェース統合
7. 🟡 **ユニットテスト** - 各クラスのテスト

### 優先度: 低（機能完成後）

8. ⚪ **ベンチマーク実装** - 性能評価
9. ⚪ **WebUI統合** - UI対応
10. ⚪ **最適化** - 並列化、キャッシュ改善

## 📝 次のステップ

### ステップ1: InformationSetクラスの実装

**作業内容**:
1. `src/controllers/information_set.py`を作成
2. `__hash__()`, `__eq__()`メソッドの実装
3. `tests/test_information_set.py`でテスト

**期待される動作**:
```python
# 同じ情報セットは同じハッシュ
info1 = InformationSet(hand1, field1, played1)
info2 = InformationSet(hand1, field1, played1)
assert hash(info1) == hash(info2)
assert info1 == info2

# 辞書のキーとして使用可能
node_cache = {info1: node}
assert node_cache[info2] == node
```

### ステップ2: Determinizerクラスの実装

**作業内容**:
1. `src/controllers/determinizer.py`を作成
2. `create_determinization()`メソッドの実装
3. `GameState.from_observable_determinization()`の実装
4. `tests/test_determinizer.py`でテスト

**期待される動作**:
```python
# 決定化生成
det_state = Determinizer.create_determinization(obs_state)

# 手札と場は保持
assert det_state.hand == obs_state.hand
assert det_state.field == obs_state.field

# 山札が生成されている
assert det_state.deck.remaining_count() > 0
```

### ステップ3: ISMCTSNodeとEngineの実装

**作業内容**:
1. `src/controllers/ismcts_node.py`を作成
2. `src/controllers/ismcts_engine.py`を作成
3. 探索アルゴリズムの実装
4. テストで動作確認

### ステップ4: 統合とベンチマーク

**作業内容**:
1. `ISMCTSStrategy`の実装
2. `benchmark_ismcts.py`の作成
3. 性能比較の実施
4. 結果の分析とドキュメント化

## 📊 期待される成果

### 定量的な目標

1. **スコア向上**
   - ランダム戦略比: +200%
   - ヒューリスティック比: +50%
   - 通常MCTS比: 同等以上

2. **実行時間**
   - 1000イテレーション: 5秒以内
   - 実用的な応答速度を維持

3. **安定性**
   - 標準偏差の低減
   - より予測可能な結果

### 定性的な目標

1. **実戦適用可能**
   - 実際のゲームプレイで使用できる
   - WebUIから簡単に利用可能

2. **拡張性**
   - 他の不完全情報ゲームにも応用可能
   - アルゴリズムの改良が容易

3. **理解しやすいコード**
   - 明確な責任分離
   - 十分なドキュメント

## 🔄 イテレーション計画

### イテレーション1: 基盤実装（1-2日）
- InformationSet, Determinizer
- 基本的なテスト
- 動作確認

### イテレーション2: コア実装（2-3日）
- ISMCTSNode, ISMCTSEngine
- 探索アルゴリズム
- 統合テスト

### イテレーション3: 統合とテスト（1-2日）
- ISMCTSStrategy
- ベンチマーク実装
- 性能評価

### イテレーション4: 最適化と改善（1-2日）
- 性能チューニング
- バグ修正
- ドキュメント整備

## 📚 参考資料

### 論文・文献
- **Information Set MCTS (ISMCTS)** - P.I. Cowling et al. (2012)
  - "Information Set Monte Carlo Tree Search"
  - 不完全情報ゲームへのMCTS適用

### 既存実装
- `src/controllers/mcts_engine.py` - 完全情報MCTS
- `src/controllers/observable_game_state.py` - 観測可能状態

### 関連ドキュメント
- `ISMCTS_DESIGN.md` - IS-MCTSの設計詳細
- `ISMCTS_IMPLEMENTATION_PLAN.md` - 詳細な実装計画
- `DEVELOPMENT.md` - 開発履歴

---

**作成日**: 2025年10月14日
**ステータス**: 実装準備完了
**次のアクション**: InformationSetクラスの実装開始
