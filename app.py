"""AI経営管理ポータル - ホームページ"""

import streamlit as st
from lib.auth import check_auth, logout
from lib.styles import apply_styles, footer

st.set_page_config(
    page_title="AI経営管理ポータル",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

# --- Authentication ---
if not check_auth():
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.markdown("### AI経営管理ポータル")
    st.caption("制度とテクノロジーで中小企業の成果を作る")
    st.divider()
    if st.button("ログアウト"):
        logout()

# --- Main Content ---
st.markdown("# :briefcase: AI経営管理ポータル")
st.markdown("ワークフローをWebアプリとして利用できます。左のサイドバーからツールを選択してください。")

st.divider()

# --- App Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### :clipboard: 香川県補助金申請書類生成")
    st.markdown("ヒアリングシートをアップロードするだけで、香川県未来投資応援補助金の申請書類4種を自動生成します。")
    st.caption(":green_circle: 稼働中")

with col2:
    st.markdown("### :pencil: 記事下書き")
    st.markdown("テーマと読者を指定するだけで、SEO対応の記事下書きをAIがストリーミング生成します。")
    st.caption(":yellow_circle: 開発中")

with col3:
    st.markdown("### :bar_chart: 戦略分析")
    st.markdown("5つのAIエージェントが多角的に事業戦略を分析。市場調査から批判的レビューまで一気通貫。")
    st.caption(":yellow_circle: 開発中")

st.divider()

# --- Status ---
st.markdown("### :gear: システム状況")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.metric("登録アプリ", "3")

with status_col2:
    st.metric("稼働中", "1")

with status_col3:
    st.metric("開発中", "2")

footer()
