"""記事下書き生成アプリ - Phase 2 で本実装予定"""

import streamlit as st
from lib.auth import check_auth
from lib.styles import apply_styles, page_header, footer

st.set_page_config(
    page_title="記事下書き",
    page_icon=":pencil:",
    layout="wide",
)

apply_styles()

if not check_auth():
    st.stop()

page_header(
    ":pencil: 記事下書き",
    "テーマを入力するだけでSEO対応の記事を生成します",
)

st.divider()

# --- Placeholder UI ---
st.info(":construction: このアプリは現在開発中です。以下の機能を実装予定です。")

st.markdown("""
### 実装予定の機能

1. **入力フォーム**
   - 記事テーマ
   - ターゲット読者（中小企業経営者 / IT担当者 / 一般ビジネス層）
   - カテゴリ（補助金解説 / AI事例 / DXガイド / 業界トレンド）
   - トーン・文字数の設定

2. **構成提案**
   - AIが記事の見出し構成を提案
   - 編集可能なアウトラインエディタ
   - 承認後に本文生成へ

3. **ストリーミング生成**
   - セクションごとにリアルタイム表示
   - 生成中の進捗バー

4. **品質チェック**
   - AI臭スコア表示
   - 文字数カウント
   - 「人間らしく書き直す」ボタン

5. **出力**
   - Markdownファイルダウンロード
   - クリップボードコピー
""")

footer()
