"""
カードテーブル用CSSスタイル定義
"""


def get_card_table_styles() -> str:
    """
    カード選択テーブル用のCSSスタイルを取得
    
    Returns:
        CSSスタイル文字列
    """
    return """
    <style>
    /* カード選択テーブル全体のスタイル */
    div[class*="st-key-card-selection-table"] {
        gap: 0 !important;
    }

    div[class*="st-key-card-selection-table"] div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        column-gap: 0 !important;
        row-gap: 0 !important;
    }
    
    /* カラムのスタイル */
    div[class*="st-key-card-selection-table"] div[data-testid="stColumn"] {
        padding: 0 !important;
        gap: 0 !important;
    }
    
    /* 垂直ブロックのスタイル */
    div[class*="st-key-card-selection-table"] div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        row-gap: 0 !important;
        column-gap: 0 !important;
    }
    
    /* 要素コンテナのスタイル */
    div[class*="st-key-card-selection-table"] div[data-testid="stElementContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ボタンコンテナのスタイル */
    div[class*="st-key-card-selection-table"] div[data-testid="stButton"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ボタン自体のスタイル */
    div[class*="st-key-card-selection-table"] div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 50px !important;
        border: 1px solid #ddd !important;
        border-radius: 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* ボタン内のマークダウンコンテナ */
    div[class*="st-key-card-selection-table"] div[data-testid="stButton"] > button > div[data-testid="stMarkdownContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ボタン内の段落 */
    div[class*="st-key-card-selection-table"] div[data-testid="stButton"] > button > div[data-testid="stMarkdownContainer"] > p {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* マークダウンコンテナ（スート列用） */
    div[class*="st-key-card-selection-table"] div[data-testid="stMarkdown"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[class*="st-key-card-selection-table"] div[data-testid="stMarkdownContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
    """
