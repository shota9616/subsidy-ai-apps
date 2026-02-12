"""戦略分析アプリ - Phase 3 で本実装予定"""

import streamlit as st
from lib.auth import check_auth
from lib.styles import apply_styles, page_header, footer

st.set_page_config(
    page_title="戦略分析",
    page_icon=":bar_chart:",
    layout="wide",
)

apply_styles()

if not check_auth():
    st.stop()

page_header(
    ":bar_chart: 戦略分析",
    "5つのAIエージェントが多角的に事業戦略を分析します",
)

st.divider()

# --- Placeholder UI ---
st.info(":construction: このアプリは現在開発中です。以下の機能を実装予定です。")

st.markdown("""
### 実装予定の機能

1. **入力フォーム**
   - 分析テーマ
   - 背景・コンテキスト
   - 財務データのアップロード（任意）
   - 分析深度（クイック / 標準 / 詳細）

2. **5エージェント分析パイプライン**
   ```
   [1] 質問設計者       → 分析の論点を構造化
   [2a] 市場リサーチャー → 市場規模・トレンド・競合分析
   [2b] 定量アナリスト   → 財務指標・KPI・ROI試算
   [3] 戦略デザイナー   → SWOT分析・3つの戦略オプション
   [4] 批判的レビュアー → リスク検知・盲点発見
   ```

3. **リアルタイム進捗表示**
   - 各エージェントの実行状況
   - 完了済みエージェントの出力を展開可能

4. **出力**
   - 統合戦略レポート
   - Markdown / PDF ダウンロード
   - 各エージェントの個別出力
""")

footer()
