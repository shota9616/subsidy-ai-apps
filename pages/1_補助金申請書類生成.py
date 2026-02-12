"""補助金申請書類生成アプリ - Phase 1 で本実装予定"""

import streamlit as st
from lib.auth import check_auth
from lib.styles import apply_styles, page_header, footer

st.set_page_config(
    page_title="補助金申請書類生成",
    page_icon=":clipboard:",
    layout="wide",
)

apply_styles()

if not check_auth():
    st.stop()

page_header(
    ":clipboard: 補助金申請書類生成",
    "ヒアリングシートから申請書類を自動生成します",
)

st.divider()

# --- Placeholder UI ---
st.info(":construction: このアプリは現在開発中です。以下の機能を実装予定です。")

st.markdown("""
### 実装予定の機能

1. **ヒアリングシートのアップロード** (xlsx)
   - 10タブのデータを自動解析
   - 不足項目のチェック & 警告表示

2. **データプレビュー & 編集**
   - 抽出データの確認・修正フォーム
   - 財務データの手動入力オプション

3. **書類自動生成**
   - 事業計画書（その1〜その3）
   - 賃金引上げ計画書
   - その他申請書類 全11種

4. **図表自動生成** (Gemini API)
   - 企業概要図、SWOT分析、労働力不足図など12枚

5. **品質チェック**
   - AI臭スコア表示
   - NG表現チェック
   - 自動改善ループ

6. **一括ダウンロード**
   - 全書類 + 図表をZIPでダウンロード
""")

footer()
