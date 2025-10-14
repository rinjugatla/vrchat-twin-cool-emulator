# IS-MCTS 実装計画

## 📋 実装順序と詳細

### Phase 1: 基盤クラスの実装

#### 1.1 ObservableGameState クラス

**ファイル**: `src/controllers/observable_game_state.py`

**目的**: プレイヤーが実際に知っている情報のみを保持

```python
class ObservableGameState:
    """観測可能なゲーム状態（不完全情報）"""
    
    def __init__(self):
        self.hand: Hand                    # 現在の手札（既知）
        self.field: Field                  # 場の状態（既知）
        self.played_cards: List[Card]      # 既に場に出したカード（既知）
        self.total_points: int             # 累積ポイント（既知）
        self.turn_count: int               # ターン数（既知）
        
        # 推定情報
        self.remaining_deck_size: int      # 山札残り枚数（既知）
        self.excluded_cards_count: int = 10  # 除外カード数（固定）
    
    def get_unplayed_cards(self) -> List[Card]:
        """未出現カードを取得（山札 + 除外10枚）"""
        all_cards = self._get_all_80_cards()
        played_and_hand = self.played_cards + self.hand.get_cards()
        return [c for c in all_cards if c not in played_and_hand]
    
    @staticmethod
    def from_game_state(game_state: GameState, 
                       played_cards: List[Card]) -> 'ObservableGameState':
        """既存のGameStateから観測可能状態を構築"""
        obs = ObservableGameState()
        obs.hand = game_state.get_hand().copy()
        obs.field = game_state.get_field().copy()
        obs.played_cards = played_cards.copy()
        obs.total_points = game_state.get_total_points()
        obs.turn_count = game_state.turn_count
        obs.remaining_deck_size = game_state.get_deck().remaining_count()
        return obs
```

**テスト**: `tests/test_observable_game_state.py`

#### 1.2 InformationSet クラス

**ファイル**: `src/controllers/information_set.py`

**目的**: 情報セットの識別とハッシュ化

```python
class InformationSet:
    """
    情報セット
    プレイヤーから見て区別がつかない状態群
    """
    
    def __init__(self, hand: Hand, field: Field, played_cards: List[Card]):
        self.hand_cards = tuple(sorted(hand.get_cards()))  # ソートして順序無視
        self.field_state = self._encode_field(field)
        self.played_cards = tuple(sorted(played_cards))
    
    def _encode_field(self, field: Field) -> Tuple:
        """場の状態をタプルにエンコード"""
        slot1_top = field.get_top_card(0)
        slot2_top = field.get_top_card(1)
        return (
            slot1_top if slot1_top else None,
            slot2_top if slot2_top else None
        )
    
    def __hash__(self) -> int:
        """ハッシュ値計算（辞書のキーとして使用）"""
        return hash((self.hand_cards, self.field_state, self.played_cards))
    
    def __eq__(self, other: 'InformationSet') -> bool:
        """同一性判定"""
        if not isinstance(other, InformationSet):
            return False
        return (
            self.hand_cards == other.hand_cards and
            self.field_state == other.field_state and
            self.played_cards == other.played_cards
        )
    
    def __repr__(self) -> str:
        return f"InfoSet(hand={len(self.hand_cards)}, played={len(self.played_cards)})"
```

**テスト**: `tests/test_information_set.py`

#### 1.3 決定化生成ロジック

**ファイル**: `src/controllers/determinizer.py`

**目的**: 観測可能状態から完全なゲーム状態をサンプリング

```python
class Determinizer:
    """
    決定化生成器
    不完全情報から完全情報ゲーム状態をサンプリング
    """
    
    @staticmethod
    def create_determinization(
        observable_state: ObservableGameState,
        seed: Optional[int] = None
    ) -> GameState:
        """
        決定化を1つ生成
        
        手順:
        1. 未出現カードを取得
        2. ランダムに10枚を除外
        3. 残りを山札としてシャッフル
        4. GameStateを構築
        """
        if seed is not None:
            random.seed(seed)
        
        # 未出現カード = 全80枚 - 既出カード - 手札
        unplayed_cards = observable_state.get_unplayed_cards()
        
        # ランダムに10枚を除外
        random.shuffle(unplayed_cards)
        excluded_cards = unplayed_cards[:10]
        deck_cards = unplayed_cards[10:]
        
        # 山札をシャッフル
        random.shuffle(deck_cards)
        
        # 完全なGameStateを構築
        game_state = GameState.from_observable_determinization(
            hand=observable_state.hand.copy(),
            field=observable_state.field.copy(),
            deck_cards=deck_cards,
            excluded_cards=excluded_cards,
            total_points=observable_state.total_points,
            turn_count=observable_state.turn_count
        )
        
        return game_state
    
    @staticmethod
    def create_multiple_determinizations(
        observable_state: ObservableGameState,
        count: int
    ) -> List[GameState]:
        """複数の決定化を生成"""
        return [
            Determinizer.create_determinization(observable_state)
            for _ in range(count)
        ]
```

**テスト**: `tests/test_determinizer.py`

---

### Phase 2: ISMCTSコア実装

#### 2.1 ISMCTSNode クラス

**ファイル**: `src/controllers/ismcts_node.py`

**重要な違い**: 従来のMCTSNodeとの差異
- 状態ではなく**情報セット**を保持
- 複数の決定化で統計を共有
- ノードの子は**手**でインデックス

```python
class ISMCTSNode:
    """
    IS-MCTSの探索ノード
    情報セット単位で管理
    """
    
    def __init__(
        self,
        info_set: InformationSet,
        parent: Optional['ISMCTSNode'] = None,
        move: Optional[Tuple[Card, int]] = None
    ):
        self.info_set = info_set
        self.parent = parent
        self.move = move
        
        # 統計情報（全決定化で共有）
        self.visits = 0
        self.total_reward = 0.0
        
        # 子ノード（手 -> ISMCTSNode）
        self.children: Dict[Tuple[Card, int], ISMCTSNode] = {}
        
        # 未試行の手（情報セットから推定）
        self.untried_moves: List[Tuple[Card, int]] = []
        self._initialized_moves = False
    
    def initialize_untried_moves(self, valid_moves: List[Tuple[Card, int]]):
        """有効手を初期化（決定化依存）"""
        if not self._initialized_moves:
            self.untried_moves = valid_moves.copy()
            self._initialized_moves = True
    
    def is_fully_expanded(self) -> bool:
        """全ての手が試されたか"""
        return len(self.untried_moves) == 0
    
    def ucb1_score(self, exploration_weight: float = 1.41) -> float:
        """UCB1スコア計算"""
        if self.visits == 0:
            return float('inf')
        
        if self.parent is None or self.parent.visits == 0:
            return self.total_reward / self.visits
        
        exploitation = self.total_reward / self.visits
        exploration = exploration_weight * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        
        return exploitation + exploration
    
    def select_best_child(self, exploration_weight: float) -> 'ISMCTSNode':
        """UCB1で最良の子を選択"""
        return max(
            self.children.values(),
            key=lambda child: child.ucb1_score(exploration_weight)
        )
    
    def get_best_move(self) -> Optional[Tuple[Card, int]]:
        """最も訪問回数が多い手を返す"""
        if len(self.children) == 0:
            return None
        
        best_child = max(self.children.values(), key=lambda c: c.visits)
        return best_child.move
    
    def update(self, reward: float):
        """統計情報を更新"""
        self.visits += 1
        self.total_reward += reward
```

**テスト**: `tests/test_ismcts_node.py`

#### 2.2 ISMCTSEngine クラス

**ファイル**: `src/controllers/ismcts_engine.py`

**核心**: 情報セットベースの探索ループ

```python
class ISMCTSEngine:
    """
    情報セットMCTS探索エンジン
    """
    
    def __init__(
        self,
        exploration_weight: float = 1.41,
        verbose: bool = False
    ):
        self.exploration_weight = exploration_weight
        self.verbose = verbose
        
        # 情報セット -> ノード のマッピング（木の共有）
        self.info_set_tree: Dict[InformationSet, ISMCTSNode] = {}
    
    def search(
        self,
        observable_state: ObservableGameState,
        num_iterations: int = 1000
    ) -> Tuple[Optional[Tuple[Card, int]], Dict]:
        """
        IS-MCTS探索を実行
        
        各イテレーションで:
        1. 決定化を1つ生成
        2. その決定化でMCTS 1回実行（情報セットノード共有）
        3. 統計を更新
        
        Returns:
            (最良の手, 統計情報)
        """
        # ルート情報セットを取得
        root_info_set = self._get_information_set_from_observable(observable_state)
        root_node = self._get_or_create_node(root_info_set)
        
        for iteration in range(num_iterations):
            # 1. 決定化を生成
            determinized_state = Determinizer.create_determinization(
                observable_state
            )
            
            # 2. この決定化でMCTS 1イテレーション
            self._run_one_iteration(root_node, determinized_state)
            
            if self.verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}/{num_iterations}")
        
        # 最良の手を返す
        best_move = root_node.get_best_move()
        stats = self._get_statistics(root_node)
        
        return best_move, stats
    
    def _run_one_iteration(
        self,
        root_node: ISMCTSNode,
        determinized_state: GameState
    ):
        """決定化1つでMCTSイテレーション1回実行"""
        
        # Selection
        node, state = self._select(root_node, determinized_state)
        
        # Expansion
        if not self._is_terminal(state) and not node.is_fully_expanded():
            node, state = self._expand(node, state)
        
        # Simulation
        reward = self._simulate(state)
        
        # Backpropagation
        self._backpropagate(node, reward)
    
    def _select(
        self,
        node: ISMCTSNode,
        state: GameState
    ) -> Tuple[ISMCTSNode, GameState]:
        """Selection フェーズ"""
        current_state = copy.deepcopy(state)
        current_node = node
        
        while not self._is_terminal(current_state):
            # 有効手を取得
            valid_moves = MoveValidator.get_valid_moves(
                current_state.get_hand(),
                current_state.get_field()
            )
            
            # 未試行の手を初期化
            if not current_node._initialized_moves:
                current_node.initialize_untried_moves(valid_moves)
            
            if not current_node.is_fully_expanded():
                return current_node, current_state
            
            # UCB1で最良の子を選択
            current_node = current_node.select_best_child(self.exploration_weight)
            
            # 状態を進める
            card, slot = current_node.move
            current_state.play_card(card, slot)
        
        return current_node, current_state
    
    def _expand(
        self,
        node: ISMCTSNode,
        state: GameState
    ) -> Tuple[ISMCTSNode, GameState]:
        """Expansion フェーズ"""
        # 未試行の手を1つ選択
        move = node.untried_moves.pop()
        card, slot = move
        
        # 状態を進める
        new_state = copy.deepcopy(state)
        new_state.play_card(card, slot)
        
        # 新しい情報セットとノードを作成
        new_info_set = self._get_information_set(new_state)
        new_node = self._get_or_create_node(new_info_set, parent=node, move=move)
        
        # 親の子として登録
        node.children[move] = new_node
        
        return new_node, new_state
    
    def _simulate(self, state: GameState) -> float:
        """Simulation フェーズ（従来と同じ）"""
        sim_state = copy.deepcopy(state)
        
        while MoveValidator.has_valid_move(
            sim_state.get_hand(),
            sim_state.get_field()
        ):
            valid_moves = MoveValidator.get_valid_moves(
                sim_state.get_hand(),
                sim_state.get_field()
            )
            
            if len(valid_moves) == 0:
                break
            
            card, slot = random.choice(valid_moves)
            sim_state.play_card(card, slot)
        
        result = {
            'cards_played': sim_state.get_cards_played_count(),
            'total_points': sim_state.get_total_points()
        }
        
        return Evaluator.evaluate(result)
    
    def _backpropagate(self, node: ISMCTSNode, reward: float):
        """Backpropagation フェーズ"""
        current = node
        while current is not None:
            current.update(reward)
            current = current.parent
    
    def _get_or_create_node(
        self,
        info_set: InformationSet,
        parent: Optional[ISMCTSNode] = None,
        move: Optional[Tuple[Card, int]] = None
    ) -> ISMCTSNode:
        """情報セットに対応するノードを取得または作成（キャッシュ）"""
        if info_set not in self.info_set_tree:
            self.info_set_tree[info_set] = ISMCTSNode(
                info_set,
                parent=parent,
                move=move
            )
        return self.info_set_tree[info_set]
    
    def _get_information_set(self, state: GameState) -> InformationSet:
        """GameStateから情報セットを抽出"""
        # TODO: played_cardsを外部から渡す必要あり
        return InformationSet(
            hand=state.get_hand(),
            field=state.get_field(),
            played_cards=[]  # 要修正
        )
    
    def _get_information_set_from_observable(
        self,
        obs_state: ObservableGameState
    ) -> InformationSet:
        """ObservableGameStateから情報セットを抽出"""
        return InformationSet(
            hand=obs_state.hand,
            field=obs_state.field,
            played_cards=obs_state.played_cards
        )
    
    def _is_terminal(self, state: GameState) -> bool:
        """終端状態判定"""
        return not MoveValidator.has_valid_move(
            state.get_hand(),
            state.get_field()
        )
    
    def _get_statistics(self, root: ISMCTSNode) -> dict:
        """統計情報を取得"""
        return {
            'total_visits': root.visits,
            'num_children': len(root.children),
            'best_move': root.get_best_move(),
            'info_set_cache_size': len(self.info_set_tree)
        }
```

**テスト**: `tests/test_ismcts_engine.py`

---

### Phase 3: GameState拡張

**ファイル**: `src/controllers/game_state.py` (既存ファイルに追加)

**追加メソッド**:

```python
class GameState:
    # ... 既存コード ...
    
    @staticmethod
    def from_observable_determinization(
        hand: Hand,
        field: Field,
        deck_cards: List[Card],
        excluded_cards: List[Card],
        total_points: int,
        turn_count: int
    ) -> 'GameState':
        """
        観測可能状態と決定化から完全なGameStateを構築
        
        Args:
            hand: 手札
            field: 場
            deck_cards: 山札のカード（順序付き）
            excluded_cards: 除外カード10枚
            total_points: 累積ポイント
            turn_count: ターン数
        
        Returns:
            完全なGameState
        """
        # Deckを構築
        state = GameState.__new__(GameState)
        state.deck = Deck(excluded_cards=excluded_cards)
        state.deck._cards = deck_cards.copy()  # 順序を保持
        
        state.hand = hand.copy()
        state.field = field.copy()
        state.total_points = total_points
        state.turn_count = turn_count
        
        return state
    
    def get_cards_played_count(self) -> int:
        """場に出したカードの枚数を取得"""
        return self.field.get_total_cards_count()
```

---

### Phase 4: 戦略インターフェース統合

**ファイル**: `src/controllers/ismcts_strategy.py`

**目的**: 既存のMCTSStrategyと同じインターフェース

```python
class ISMCTSStrategy:
    """
    IS-MCTS戦略（不完全情報対応）
    """
    
    def __init__(self, num_iterations: int = 1000, verbose: bool = False):
        self.num_iterations = num_iterations
        self.verbose = verbose
        self.engine = ISMCTSEngine(verbose=verbose)
    
    def get_best_move(
        self,
        observable_state: ObservableGameState
    ) -> Optional[Tuple[Card, int]]:
        """
        最適な手を取得
        
        Args:
            observable_state: 観測可能なゲーム状態
        
        Returns:
            最良の手（カード、スロット番号）
        """
        best_move, stats = self.engine.search(
            observable_state,
            num_iterations=self.num_iterations
        )
        
        if self.verbose:
            print(f"\n=== IS-MCTS Statistics ===")
            print(f"Total visits: {stats['total_visits']}")
            print(f"Children: {stats['num_children']}")
            print(f"Cache size: {stats['info_set_cache_size']}")
            print(f"Best move: {stats['best_move']}")
        
        return best_move
```

---

## 🧪 テスト戦略

### 単体テスト

1. **test_information_set.py**: ハッシュと同一性判定
2. **test_determinizer.py**: 決定化生成の正しさ
3. **test_ismcts_node.py**: UCB1計算、子ノード管理
4. **test_ismcts_engine.py**: 統合テスト

### 統合テスト

**ファイル**: `tests/test_ismcts_integration.py`

```python
def test_ismcts_complete_game():
    """IS-MCTSで完全なゲームを実行"""
    # 観測可能状態を構築
    obs_state = ObservableGameState()
    # ... 初期化 ...
    
    strategy = ISMCTSStrategy(num_iterations=100)
    
    turn = 0
    while has_valid_moves(obs_state):
        best_move = strategy.get_best_move(obs_state)
        # 手を適用
        apply_move(obs_state, best_move)
        turn += 1
    
    assert turn > 0
    print(f"Game completed in {turn} turns")
```

---

## 📊 パフォーマンス比較

**ファイル**: `benchmark_ismcts.py`

```python
def compare_mcts_vs_ismcts():
    """従来MCTSとIS-MCTSの比較"""
    
    test_cases = generate_test_scenarios(count=10)
    
    for scenario in test_cases:
        # 従来MCTS
        time_mcts, result_mcts = benchmark_traditional_mcts(scenario)
        
        # IS-MCTS
        time_ismcts, result_ismcts = benchmark_ismcts(scenario)
        
        print(f"Traditional MCTS: {time_mcts:.2f}s, Score: {result_mcts}")
        print(f"IS-MCTS: {time_ismcts:.2f}s, Score: {result_ismcts}")
```

---

## 🎮 WebUI統合

**ファイル**: `app.py` (既存ファイルに追加)

```python
# サイドバーに追加
search_mode = st.sidebar.radio(
    "探索モード",
    ["練習モード（完全情報）", "実戦モード（不完全情報）"],
    help="実戦モードでは山札が未知として扱われます"
)

if search_mode == "実戦モード（不完全情報）":
    # IS-MCTS使用
    strategy = ISMCTSStrategy(num_iterations=num_iterations)
    
    # 観測可能状態を構築
    obs_state = ObservableGameState.from_game_state(
        st.session_state.game_state,
        st.session_state.played_cards
    )
    
    best_move = strategy.get_best_move(obs_state)
else:
    # 従来MCTS使用
    strategy = MCTSStrategy(num_iterations=num_iterations)
    best_move = strategy.get_best_move(st.session_state.game_state)
```

---

## ⚠️ 実装上の注意点

### 1. played_cardsの管理

**問題**: 現在のGameStateにplayed_cardsが含まれていない

**解決策**:
- `GameState`に`played_cards`を追加
- `play_card()`メソッドで自動更新

### 2. 情報セットのハッシュ化

**問題**: CardオブジェクトはハッシュのMust be hashable

**解決策**:
- `Card`クラスに`__hash__`と`__eq__`を実装済みか確認
- なければ実装

### 3. メモリ管理

**問題**: 長時間実行で`info_set_tree`が肥大化

**解決策**:
- 定期的にキャッシュをクリア
- LRUキャッシュの導入

---

## 🚀 実装開始

実装を開始する場合は、以下の順序で進めます:

1. `Card`のハッシュ化確認
2. `GameState`への`played_cards`追加
3. `ObservableGameState`実装
4. `InformationSet`実装
5. `Determinizer`実装
6. `ISMCTSNode`実装
7. `ISMCTSEngine`実装
8. テスト作成と実行
9. WebUI統合

実装を進めますか？
