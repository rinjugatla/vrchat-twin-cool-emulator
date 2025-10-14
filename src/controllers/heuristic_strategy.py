"""
ヒューリスティック戦略
柔軟性に基づいてカードを選択
"""

from typing import Optional, Tuple, Dict
from ..models.card import Card
from .observable_game_state import ObservableGameState
from .move_validator import MoveValidator
from .flexibility_calculator import FlexibilityCalculator


class HeuristicStrategy:
    """
    柔軟性ヒューリスティック戦略
    
    戦略:
    - 手札から柔軟性が**低い**カードを優先的に出す
    - 柔軟性が高いカードは手札に残す
    
    理由:
    - 柔軟性が高い = 多くのカードと接続可能 = 後で出しやすい
    - 柔軟性が低い = 接続できるカードが少ない = 今出さないと出せなくなる
    """
    
    def __init__(self, verbose: bool = False):
        """
        ヒューリスティック戦略の初期化
        
        Args:
            verbose: 詳細情報を出力するか
        """
        self.verbose = verbose
        self.last_explanation: Optional[str] = None
    
    def get_best_move(
        self,
        observable_state: ObservableGameState
    ) -> Optional[Tuple[Card, int]]:
        """
        最適な手を取得
        
        Args:
            observable_state: 観測可能なゲーム状態
        
        Returns:
            (カード, スロット番号) または None
        """
        hand = observable_state.get_hand()
        field = observable_state.get_field()
        
        # 有効な手を取得
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        
        if len(valid_moves) == 0:
            self.last_explanation = "出せるカードがありません"
            return None
        
        # 未知のカード（山札候補）を取得
        unknown_cards = observable_state.get_unknown_cards()
        
        # 各手を評価
        move_scores = []
        for card, slot in valid_moves:
            remaining_flex, card_flex = FlexibilityCalculator.evaluate_move_flexibility(
                card, slot, hand, unknown_cards
            )
            
            # スコア = 残った手札の柔軟性の合計
            # このスコアが高いほど良い（柔軟性が低いカードを出している）
            move_scores.append((card, slot, remaining_flex, card_flex))
        
        # 残った手札の柔軟性が最も高くなる手を選択
        # = 柔軟性が低いカードを出す
        best_move = max(move_scores, key=lambda x: x[2])
        best_card, best_slot, remaining_flex, card_flex = best_move
        
        # 説明文を生成
        self._generate_explanation(
            best_card, best_slot, card_flex, remaining_flex, 
            len(valid_moves), unknown_cards
        )
        
        if self.verbose:
            print(self.last_explanation)
        
        return best_card, best_slot
    
    def _generate_explanation(
        self,
        card: Card,
        slot: int,
        card_flex: int,
        remaining_flex: int,
        num_moves: int,
        unknown_cards: list
    ):
        """
        判断理由の説明文を生成
        
        Args:
            card: 選択されたカード
            slot: 選択されたスロット
            card_flex: 選択されたカードの柔軟性
            remaining_flex: 残った手札の柔軟性
            num_moves: 選択肢の数
            unknown_cards: 未知のカード
        """
        # 詳細情報を取得
        details = FlexibilityCalculator.get_card_compatibility_details(
            card, unknown_cards
        )
        
        self.last_explanation = (
            f"【ヒューリスティック判断】\n"
            f"選択: {card} をスロット{slot + 1}に\n"
            f"理由: このカードの柔軟性は {card_flex} (同スート:{details['same_suit']}, "
            f"同数値:{details['same_value']})\n"
            f"      {num_moves}個の選択肢の中で、これを出すと残りの手札の柔軟性が "
            f"{remaining_flex} になり最大\n"
            f"戦略: 柔軟性が低いカードを優先的に出して、柔軟性が高いカードを手札に残す"
        )
    
    def explain(self, move: Optional[Tuple[Card, int]] = None) -> str:
        """
        最後の判断の説明を取得
        
        Args:
            move: 説明する手（Noneの場合は最後の判断）
        
        Returns:
            説明文
        """
        if self.last_explanation is None:
            return "まだ判断を行っていません"
        return self.last_explanation
    
    def get_flexibility_analysis(
        self,
        observable_state: ObservableGameState
    ) -> Dict:
        """
        現在の手札の柔軟性分析を取得（デバッグ・UI表示用）
        
        Args:
            observable_state: 観測可能な状態
        
        Returns:
            {
                'hand_scores': {Card: int},  # 各カードの柔軟性スコア
                'valid_moves': [(Card, int, int, int)],  # (カード, スロット, 残り柔軟性, カード柔軟性)
                'unknown_count': int  # 未知カード数
            }
        """
        hand = observable_state.get_hand()
        field = observable_state.get_field()
        unknown_cards = observable_state.get_unknown_cards()
        
        # 手札全体のスコア
        hand_scores = FlexibilityCalculator.calculate_all_flexibility_scores(
            hand, unknown_cards
        )
        
        # 有効な手の評価
        valid_moves = MoveValidator.get_valid_moves(hand, field)
        move_evaluations = []
        
        for card, slot in valid_moves:
            remaining_flex, card_flex = FlexibilityCalculator.evaluate_move_flexibility(
                card, slot, hand, unknown_cards
            )
            move_evaluations.append((card, slot, remaining_flex, card_flex))
        
        return {
            'hand_scores': hand_scores,
            'valid_moves': move_evaluations,
            'unknown_count': len(unknown_cards)
        }
