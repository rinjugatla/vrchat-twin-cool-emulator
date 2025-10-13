"""
twin-cool-emulator メインエントリーポイント
オリジナルカードゲーム「最適解探索プログラム」
"""

from src.models import Card, Suit, Deck, Hand, Field, PointCalculator


def main():
    """メイン関数"""
    print("=" * 60)
    print("twin-cool-emulator - オリジナルカードゲーム最適解探索")
    print("=" * 60)
    print()
    
    # 簡単な動作確認
    print("【基本動作テスト】")
    print()
    
    # デッキの初期化
    deck = Deck(seed=42)
    print(f"✓ デッキ初期化完了: {deck.remaining_count()}枚")
    
    # 手札の初期化
    hand = Hand()
    for _ in range(5):
        card = deck.draw()
        if card:
            hand.add_card(card)
    print(f"✓ 初期手札配布完了: {hand.count()}枚")
    print(f"  手札: {hand}")
    
    # 場の初期化
    field = Field()
    print(f"✓ 場の初期化完了: {field}")
    
    # ポイント計算テスト
    points = PointCalculator.calculate_points(hand.get_cards())
    print(f"✓ 初期手札のポイント: {points}ポイント")
    
    print()
    print("=" * 60)
    print("基本クラスの動作確認が完了しました！")
    print("次のステップ: ゲームロジックの実装")
    print("=" * 60)


if __name__ == "__main__":
    main()
