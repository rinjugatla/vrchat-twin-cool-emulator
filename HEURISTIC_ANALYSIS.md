# ヒューリスティック手法の分析

## 💡 提案されたヒューリスティック

### 基本戦略: 「柔軟性優先選択」

**方針**: 
手札から、残りの山札で**出せる可能性が最も高いカード**（=多くのカードと接続できるカード）を残し、
**出せる可能性が低いカード**を優先的に場に出す。

### 具体的な評価方法

#### 1. 各手札カードの「柔軟性スコア」計算

```python
def calculate_flexibility_score(card: Card, 
                                unknown_cards: List[Card]) -> int:
    """
    カードの柔軟性スコアを計算
    = 未知の山札の中で、このカードから出せるカードの数
    """
    compatible_count = 0
    
    for unknown_card in unknown_cards:
        # 同じスートまたは同じ数値なら接続可能
        if (unknown_card.suit == card.suit or 
            unknown_card.value == card.value):
            compatible_count += 1
    
    return compatible_count
```

#### 2. 選択ロジック

```python
def select_card_to_play(hand: Hand, 
                       field: Field,
                       unknown_cards: List[Card]) -> Tuple[Card, int]:
    """
    ヒューリスティックでカードを選択
    """
    valid_moves = get_valid_moves(hand, field)
    
    # 各有効手の柔軟性スコアを計算
    scores = []
    for card, slot in valid_moves:
        # このカードを出した後の手札の柔軟性を評価
        remaining_hand = hand.copy()
        remaining_hand.remove(card)
        
        # 残った手札全体の柔軟性スコア
        total_flexibility = sum(
            calculate_flexibility_score(c, unknown_cards) 
            for c in remaining_hand.get_cards()
        )
        
        scores.append((card, slot, total_flexibility))
    
    # 柔軟性が最も高くなる手を選択
    # = 柔軟性が低いカードを先に出す
    best_move = min(scores, key=lambda x: x[2])
    return best_move[0], best_move[1]
```

## 📊 ヒューリスティック vs MCTS の比較

### 比較表

| 項目 | ヒューリスティック | 決定論的MCTS | IS-MCTS |
|------|-----------------|-------------|---------|
| **実装複雑度** | ⭐ 非常に簡単 | ⭐⭐⭐ 中程度 | ⭐⭐⭐⭐⭐ 非常に複雑 |
| **実装時間** | 1-2時間 | 1-2日 | 4-7日 |
| **計算速度** | ⭐⭐⭐⭐⭐ 瞬時 | ⭐⭐⭐ 数秒 | ⭐⭐ 数秒〜数十秒 |
| **精度** | ⭐⭐ 局所最適 | ⭐⭐⭐⭐ 良い | ⭐⭐⭐⭐⭐ 最良 |
| **先読み能力** | ❌ なし | ✅ あり（数手先） | ✅ あり（数手先） |
| **デバッグ容易性** | ⭐⭐⭐⭐⭐ 非常に容易 | ⭐⭐⭐ 中程度 | ⭐⭐ 困難 |
| **説明可能性** | ⭐⭐⭐⭐⭐ 明確 | ⭐⭐ 統計的 | ⭐⭐ 統計的 |

## 🔍 ヒューリスティックの長所

### 1. **実装の簡単さ**

```python
# たった50行程度で実装可能
class FlexibilityHeuristic:
    def get_best_move(self, observable_state):
        unknown_cards = self._get_unknown_cards(observable_state)
        valid_moves = self._get_valid_moves(observable_state)
        
        best_move = None
        best_flexibility = -1
        
        for card, slot in valid_moves:
            flexibility = self._evaluate_flexibility(
                card, slot, observable_state, unknown_cards
            )
            if flexibility > best_flexibility:
                best_flexibility = flexibility
                best_move = (card, slot)
        
        return best_move
```

### 2. **計算速度**

- **ヒューリスティック**: O(N × M) - N=手札枚数、M=未知カード数
  - 実時間: < 0.001秒
  
- **決定論的MCTS**: O(S × I × D) - S=サンプル数、I=イテレーション、D=深さ
  - 実時間: 1-10秒

- **IS-MCTS**: O(I × D) - ただし各イテレーションが重い
  - 実時間: 5-30秒

### 3. **説明可能性**

ヒューリスティックの判断理由を明確に説明できる:

```
なぜこのカードを出したか？
→ このカードは柔軟性スコアが3しかない
→ 手札に残しても次に出せる確率が低い
→ 今出しておくべき
```

MCTSの場合:
```
なぜこのカードを出したか？
→ 1000回シミュレーションした結果、統計的に最良だった
→ （具体的な理由は不明瞭）
```

### 4. **メモリ効率**

- ヒューリスティック: ほぼゼロ（状態コピー不要）
- MCTS: 探索木のため大量のメモリ使用

## ⚠️ ヒューリスティックの短所

### 1. **先読みの欠如**

**例**: 短期的には良いが、長期的には悪い手

```
状況:
手札: [♠3, ♥5, ♦7, ♣2, ♠9]
場: 空
山札未知: 60枚

ヒューリスティックの判断:
→ ♠3を出す（柔軟性低い）

実際の最適解:
→ ♥5を出す
  理由: 2手後に♠3と♠9の連鎖が期待できる
  
ヒューリスティックは「2手後の連鎖」を予測できない
```

### 2. **ポイント獲得の最適化**

ヒューリスティックは「柔軟性」のみ考慮し、**特別なポイント**を考慮しにくい:

```
状況:
手札: [♠3, ♠4, ♠5, ♠6, ♥7]

ヒューリスティック:
→ ♥7を出す（異なるスート）

最適解:
→ 手札を維持してストレートフラッシュ（50pt）を狙う
→ 山札から♠2か♠7が来る可能性に賭ける

ヒューリスティックは「待つ価値」を評価できない
```

### 3. **複雑な状況での限界**

**例**: 2つのスロットの相互作用

```
状況:
スロット1: ♠5 (トップ)
スロット2: ♥7 (トップ)
手札: [♠3, ♥3, ♦8]

選択肢:
A) ♠3をスロット1に → スロット1が♠に固定
B) ♥3をスロット2に → スロット2が♥に固定
C) ♦8を出す → 両方に出せない

ヒューリスティック:
→ 単純な柔軟性だけでは最適解が出ない

MCTS:
→ 数手先をシミュレーションして最適解を発見
```

### 4. **局所最適に陥る**

貪欲法の典型的問題:

```
各ターンで最良の手を選んでも、
ゲーム全体では最適にならない

例: ナップサック問題と同様の構造
```

## 🧪 実験: 性能比較予測

### シミュレーション結果の予測

| 手法 | 平均カード枚数 | 平均ポイント | 実行時間 |
|------|--------------|------------|---------|
| **ランダム** | 15枚 | 2pt | < 0.001秒 |
| **ヒューリスティック** | 22枚 | 5pt | < 0.001秒 |
| **決定論的MCTS (10サンプル)** | 28枚 | 12pt | 1秒 |
| **決定論的MCTS (100サンプル)** | 30枚 | 15pt | 10秒 |
| **IS-MCTS (1000イテレーション)** | 32枚 | 18pt | 20秒 |

### 性能/コスト比

```
性能改善率 / 計算時間 = 効率

ランダム → ヒューリスティック:
  (22-15) / 0.001 = 7000 改善/秒 ⭐⭐⭐⭐⭐

ヒューリスティック → 決定論的MCTS:
  (28-22) / 1 = 6 改善/秒 ⭐⭐⭐

決定論的MCTS → IS-MCTS:
  (32-30) / 20 = 0.1 改善/秒 ⭐
```

**結論**: ヒューリスティックの**コストパフォーマンスが圧倒的**

## 🎯 ハイブリッドアプローチの提案

### アプローチ4: ヒューリスティック + MCTS

#### 戦略1: ヒューリスティックでフィルタリング

```python
def hybrid_search(observable_state):
    # 1. ヒューリスティックで候補を絞る
    valid_moves = get_valid_moves(observable_state)
    
    # 柔軟性スコアでソート
    sorted_moves = sort_by_flexibility(valid_moves)
    
    # 上位3つだけMCTSで評価
    top_candidates = sorted_moves[:3]
    
    # 2. 候補に対してMCTS
    best_move = None
    best_score = -inf
    
    for move in top_candidates:
        score = mcts_evaluate(move, iterations=100)
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move
```

**メリット**:
- 探索空間を削減（高速化）
- ヒューリスティックの知識を活用
- MCTSの精度を保持

#### 戦略2: 局面に応じた切り替え

```python
def adaptive_strategy(observable_state):
    # ゲーム序盤: ヒューリスティック（速度重視）
    if observable_state.turn_count < 10:
        return heuristic_move(observable_state)
    
    # ゲーム中盤: 軽量MCTS
    elif observable_state.turn_count < 30:
        return mcts_move(observable_state, iterations=100)
    
    # ゲーム終盤: 重量MCTS（精度重視）
    else:
        return mcts_move(observable_state, iterations=1000)
```

#### 戦略3: ヒューリスティックをシミュレーションポリシーに

```python
class HeuristicGuidedMCTS:
    def _simulate(self, state):
        """
        ランダムではなく、ヒューリスティックでプレイアウト
        """
        while not is_terminal(state):
            valid_moves = get_valid_moves(state)
            
            # ヒューリスティックで選択（ランダムより賢い）
            move = select_by_heuristic(valid_moves, state)
            state.apply(move)
        
        return evaluate(state)
```

**効果**: シミュレーションの質が向上 → 少ないイテレーションで高精度

## 📊 推奨実装順序（改訂版）

### レベル0: ランダム（現状のfallback）
- 実装済み
- ベースライン

### **レベル1: ヒューリスティック（NEW!）**
- ✅ **実装時間**: 2-3時間
- ✅ **効果**: 大幅改善（予想: 15枚→22枚）
- ✅ **コスト**: 実質ゼロ（瞬時）
- ✅ **説明可能**: ユーザーに判断理由を提示可能

**実装内容**:
1. `FlexibilityCalculator` クラス
2. `HeuristicStrategy` クラス
3. WebUIで選択可能に

### レベル2: ハイブリッド（ヒューリスティック + 軽量MCTS）
- 実装時間: 1日
- 候補絞り込み + MCTS評価
- バランス型

### レベル3: 決定論的MCTS（完全版）
- 実装時間: 2日
- 精度重視

### レベル4: IS-MCTS（研究版）
- 実装時間: 5-7日
- 理論的完璧性

## 🎖️ 最終推奨

### **まずヒューリスティックを実装！**

**理由**:
1. ✅ **即効性**: 今日中に完成
2. ✅ **大幅改善**: ランダムから劇的に向上
3. ✅ **リスクゼロ**: 実装簡単、バグも少ない
4. ✅ **ユーザー体験**: 判断理由を表示できる
5. ✅ **基盤**: MCTS実装の前段階として有用

**実装後の選択肢**:
- ヒューリスティックで満足 → 完成！
- さらに精度が欲しい → MCTS追加
- 学術的追求 → IS-MCTS実装

## 📝 具体的な実装提案

### ファイル構成

```
src/controllers/
  ├─ heuristic_calculator.py    # 柔軟性スコア計算
  ├─ heuristic_strategy.py      # ヒューリスティック戦略
  └─ strategy_selector.py       # 戦略切り替え
```

### インターフェース統一

```python
# 全ての戦略が同じインターフェース
class Strategy(ABC):
    @abstractmethod
    def get_best_move(self, observable_state) -> Tuple[Card, int]:
        pass

class HeuristicStrategy(Strategy):
    def get_best_move(self, observable_state):
        # ヒューリスティック実装
        pass

class MCTSStrategy(Strategy):
    def get_best_move(self, observable_state):
        # MCTS実装
        pass

class ISMCTSStrategy(Strategy):
    def get_best_move(self, observable_state):
        # IS-MCTS実装
        pass
```

### WebUI統合

```python
strategy_type = st.sidebar.selectbox(
    "戦略選択",
    ["ヒューリスティック（高速）", 
     "MCTS（バランス）", 
     "IS-MCTS（精密）"]
)

if strategy_type == "ヒューリスティック（高速）":
    strategy = HeuristicStrategy()
elif strategy_type == "MCTS（バランス）":
    strategy = MCTSStrategy(iterations=500)
else:
    strategy = ISMCTSStrategy(iterations=1000)

best_move = strategy.get_best_move(observable_state)

# 判断理由を表示
if hasattr(strategy, 'explain'):
    st.info(strategy.explain(best_move))
```

## 🚀 次のステップ

**提案**: ヒューリスティック戦略を実装しますか？

実装する場合:
1. `ObservableGameState` クラス（既出カード管理）
2. `FlexibilityCalculator` クラス（柔軟性計算）
3. `HeuristicStrategy` クラス（戦略本体）
4. テストコード
5. WebUI統合

**推定時間**: 2-3時間で完成し、即座に効果を実感できます。

実装を進めますか？
