# 情報セットMCTS (IS-MCTS) 設計ドキュメント

## 📋 概要

不完全情報ゲームに対応した情報セットMCTS (Information Set Monte Carlo Tree Search) の実装設計。

## 🎯 目的

実際のゲームプレイでは**山札の順番が未知**であるため、従来のMCTSでは正確な探索ができない。
ISMCTSは、複数の可能な世界状態（決定化）間で探索木を共有することで、不完全情報下での最適な手を探索する。

## 🧩 主要コンポーネント

### 1. 情報セット (Information Set)

**定義**: プレイヤーから見て区別がつかない状態の集合

**このゲームにおける情報セット**:
- **既知情報**: 現在の手札、場の状態、既に場に出たカード
- **未知情報**: 山札の残りカードの順番、除外された10枚のカード

**同一情報セットの判定基準**:
```python
def is_same_information_set(state1, state2) -> bool:
    return (
        state1.hand == state2.hand and
        state1.field == state2.field and
        state1.played_cards == state2.played_cards
    )
```

### 2. 決定化 (Determinization)

**定義**: 未知情報に対して具体的な値を割り当てたもの

**決定化の生成方法**:
1. **既出カード**を全80枚から除外
2. 残りのカードを**除外10枚**と**山札**にランダム分配
3. 山札をランダムシャッフル

```
全80枚
  ├─ 既出カード（既知）
  └─ 未出カード（未知）
       ├─ 除外10枚（ランダム選択）
       └─ 山札残り（ランダム順序）
```

### 3. ISMCTSアルゴリズム

#### フロー

```
各イテレーション:
  1. 決定化を1つ生成（山札の可能性をサンプリング）
  2. その決定化でMCTS探索を実行
     - Selection: 情報セット単位でUCB1選択
     - Expansion: 新しい手を試す
     - Simulation: ゲーム終了までランダムプレイ
     - Backpropagation: 情報セット単位で統計更新
  3. 全イテレーション終了後、最も訪問回数が多い手を選択
```

#### 重要な違い

| 従来MCTS | IS-MCTS |
|---------|---------|
| 1つの状態 = 1ノード | 1つの情報セット = 1ノード |
| 状態が異なれば別ノード | 情報セットが同じなら同一ノード |
| 木は1つの世界のみ | 木は複数の世界で共有 |

## 🛠️ 実装クラス設計

### InformationSet クラス

```python
class InformationSet:
    """
    情報セットを表すクラス
    プレイヤーから見て区別がつかない状態群を識別
    """
    
    def __init__(self, hand: Hand, field: Field, played_cards: List[Card]):
        self.hand = hand.copy()
        self.field = field.copy()
        self.played_cards = played_cards.copy()
    
    def __hash__(self) -> int:
        """情報セットのハッシュ値（ノード共有のため）"""
        pass
    
    def __eq__(self, other) -> bool:
        """情報セットの同一性判定"""
        pass
```

### ISMCTSNode クラス

```python
class ISMCTSNode:
    """
    IS-MCTSの探索木のノード
    情報セットに対応（複数の決定化で共有）
    """
    
    def __init__(self, info_set: InformationSet, parent=None, move=None):
        self.info_set = info_set
        self.parent = parent
        self.move = move
        
        # 統計情報（全決定化で共有）
        self.visits = 0
        self.total_reward = 0.0
        
        # 子ノード（手 -> ノード）
        self.children: Dict[Tuple[Card, int], ISMCTSNode] = {}
        
        # 未試行の手
        self.untried_moves = self._get_valid_moves()
```

### ISMCTSEngine クラス

```python
class ISMCTSEngine:
    """
    情報セットMCTS探索エンジン
    """
    
    def __init__(self, num_determinizations: int = 100):
        self.num_determinizations = num_determinizations
        self.info_set_tree: Dict[InformationSet, ISMCTSNode] = {}
    
    def search(self, observable_state: ObservableGameState, 
               num_iterations: int) -> Tuple[Card, int]:
        """
        IS-MCTS探索を実行
        
        Args:
            observable_state: 観測可能な状態（手札、場、既出カード）
            num_iterations: 探索回数
        
        Returns:
            最適な手
        """
        
        for _ in range(num_iterations):
            # 1. 決定化を生成（山札をサンプリング）
            determinized_state = self._create_determinization(observable_state)
            
            # 2. この決定化でMCTS探索（情報セットノードを共有）
            root_info_set = self._get_information_set(determinized_state)
            root_node = self._get_or_create_node(root_info_set)
            
            # Selection
            node, state = self._select(root_node, determinized_state)
            
            # Expansion
            if not node.is_terminal():
                node, state = self._expand(node, state)
            
            # Simulation
            reward = self._simulate(state)
            
            # Backpropagation
            self._backpropagate(node, reward)
        
        # 最良の手を返す
        return root_node.get_best_move()
    
    def _create_determinization(self, 
                               observable_state: ObservableGameState) -> GameState:
        """
        決定化を生成（未知情報をサンプリング）
        """
        # 未出現カードを取得
        all_cards = self._get_all_80_cards()
        unplayed_cards = [c for c in all_cards 
                         if c not in observable_state.played_cards
                         and c not in observable_state.hand.get_cards()]
        
        # ランダムに10枚を除外、残りを山札に
        random.shuffle(unplayed_cards)
        excluded = unplayed_cards[:10]
        deck_cards = unplayed_cards[10:]
        random.shuffle(deck_cards)
        
        # 決定化された状態を構築
        return GameState.from_determinization(
            hand=observable_state.hand,
            field=observable_state.field,
            deck_cards=deck_cards,
            excluded=excluded,
            played_cards=observable_state.played_cards
        )
```

## 📊 メモリとパフォーマンス

### メモリ使用量

- **従来MCTS**: O(N) - N は探索ノード数
- **IS-MCTS**: O(N × D) - D は決定化数... ただし、**情報セット共有**により実際はそれより少ない

### 計算時間

- **従来MCTS**: O(I × S) - I はイテレーション数、S はシミュレーション時間
- **IS-MCTS**: ほぼ同じ（決定化生成のオーバーヘッドは小さい）

## 🎮 観測可能状態 (ObservableGameState)

実際のゲームプレイでプレイヤーが知っている情報:

```python
class ObservableGameState:
    """
    プレイヤーから観測可能なゲーム状態
    """
    
    def __init__(self):
        self.hand: Hand  # 現在の手札
        self.field: Field  # 場の状態
        self.played_cards: List[Card]  # 既に場に出したカード
        self.total_points: int  # 累積ポイント
        self.turn_count: int  # ターン数
        
        # 未知情報（推論に使用）
        self.known_excluded_count: int = 10  # 除外カードは10枚（順不明）
        self.known_remaining_count: int  # 山札残り枚数
```

## 🔄 決定論的MCTS (アプローチ1) との比較

| 観点 | 決定論的MCTS | IS-MCTS |
|------|-------------|---------|
| **実装難易度** | ★☆☆☆☆ | ★★★★☆ |
| **理論的正確性** | ★★☆☆☆ | ★★★★★ |
| **実行速度** | ★★★★☆ | ★★★☆☆ |
| **メモリ効率** | ★★★★★ | ★★☆☆☆ |
| **実用性** | ★★★★☆ | ★★★☆☆ |
| **デバッグ容易性** | ★★★★☆ | ★★☆☆☆ |

## 🎯 推奨実装順序

### フェーズ1: 基盤構築
1. `ObservableGameState` クラス実装
2. `InformationSet` クラス実装（ハッシュ化含む）
3. 決定化生成ロジック実装

### フェーズ2: コア実装
4. `ISMCTSNode` クラス実装
5. `ISMCTSEngine` クラス実装
6. 情報セット共有ロジック実装

### フェーズ3: 統合とテスト
7. 既存システムとの統合
8. ユニットテスト作成
9. パフォーマンステスト

### フェーズ4: UI対応
10. WebUIで「既出カード」入力機能追加
11. 実戦モード実装

## 📈 期待される改善

- **より正確な戦略**: 不完全情報を正しく扱うことで、実戦で有効な手を選択
- **リスク管理**: 最悪ケースも考慮した保守的な手を選べる
- **適応性**: ゲームが進むにつれて情報が増え、より精密な判断が可能

## ⚠️ 注意事項

1. **計算コスト**: 従来MCTSより多くの計算が必要
2. **メモリ**: 情報セット共有のため、ハッシュテーブル管理が重要
3. **デバッグ**: 複数の決定化が絡むため、デバッグが複雑
4. **調整**: 決定化数とイテレーション数のバランス調整が必要

## 🚀 次のステップ

1. プロトタイプ実装
2. 簡単なテストケースで動作確認
3. 決定論的MCTSとの性能比較
4. 実ゲームでの検証
