"""香川県未来投資応援補助金 申請書類生成アプリ

ヒアリングシート（Excel）から申請書類4種を自動生成する。
"""

import io
import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from lib.auth import check_auth
from lib.styles import apply_styles, page_header, footer
from lib.anthropic_client import generate_text

from modules.subsidy.kagawa_mirai import (
    read_hearing_sheet,
    HearingData,
    FinancialData,
    SubsidyExpense,
    calculate_subsidy,
    calculate_3year_plan,
    estimate_depreciation,
    calculate_investment_payback,
    generate_all_documents,
    generate_texts,
    validate_requirements,
    SECTION_KEYS,
    SECTION_LABELS,
    SECTION_TARGET_CHARS,
)

# ---------------------------------------------------------------------------
# ページ設定
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="香川県補助金申請書類生成",
    page_icon=":clipboard:",
    layout="wide",
)

apply_styles()

if not check_auth():
    st.stop()

page_header(
    ":clipboard: 香川県未来投資応援補助金 申請書類生成",
    "ヒアリングシートをアップロードするだけで、申請書類4種を自動生成します",
)

st.divider()

TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "kagawa_mirai"
ASSET_DIR = Path(__file__).parent.parent / "assets" / "kagawa_mirai"

# ---------------------------------------------------------------------------
# セクション1: ファイルアップロード
# ---------------------------------------------------------------------------
st.subheader("1. ヒアリングシートのアップロード")

col_upload, col_sample = st.columns([3, 1])

with col_upload:
    uploaded = st.file_uploader(
        "ヒアリングシート（.xlsx）",
        type=["xlsx"],
        help="7シート構成のヒアリングシートExcelをアップロードしてください",
    )

with col_sample:
    sample_path = ASSET_DIR / "hearing_sheet.xlsx"
    if sample_path.exists():
        with open(sample_path, "rb") as f:
            st.download_button(
                label="サンプルDL",
                data=f.read(),
                file_name="hearing_sheet_sample.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

if not uploaded:
    st.info("ヒアリングシート（.xlsx）をアップロードしてください。")
    footer()
    st.stop()

# ---------------------------------------------------------------------------
# セクション2: データプレビュー
# ---------------------------------------------------------------------------
st.divider()
st.subheader("2. データプレビュー")

# ヒアリングシート読み込み（キャッシュ）
if "km_hearing_data" not in st.session_state or st.session_state.get("km_uploaded_name") != uploaded.name:
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    try:
        data = read_hearing_sheet(tmp_path)
        st.session_state["km_hearing_data"] = data
        st.session_state["km_uploaded_name"] = uploaded.name
        # リセット
        st.session_state.pop("km_generated_texts", None)
        st.session_state.pop("km_documents", None)
    except Exception as e:
        st.error(f"ヒアリングシートの読み込みに失敗しました: {e}")
        footer()
        st.stop()
    finally:
        os.unlink(tmp_path)

data: HearingData = st.session_state["km_hearing_data"]

# 企業概要
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("企業名", data.company.name or "未入力")
with col2:
    st.metric("業種", data.company.industry or "未入力")
with col3:
    st.metric("従業員数", f"{data.company.employee_count}名")
with col4:
    st.metric("経費項目数", f"{len(data.expenses)}件")

with st.expander("企業基本情報", expanded=False):
    info_items = {
        "法人番号": data.company.corporate_number,
        "代表者": f"{data.company.representative_title} {data.company.representative}",
        "住所": f"〒{data.company.postal_code} {data.company.address}",
        "電話": data.company.phone,
        "FAX": data.company.fax,
        "Email": data.company.email,
        "資本金": f"{data.company.capital:,}千円" if data.company.capital else "未入力",
        "設立年月日": data.company.established_date,
        "決算月": f"{data.company.fiscal_month}月" if data.company.fiscal_month else "未入力",
        "事業者区分": data.company.entity_type,
        "売上高区分": data.company.sales_category,
    }
    for label, value in info_items.items():
        st.write(f"**{label}:** {value}")

with st.expander("財務情報（千円単位）", expanded=False):
    fin_col1, fin_col2, fin_col3 = st.columns(3)
    with fin_col1:
        st.metric("売上高", f"{data.financial.sales:,}")
        st.metric("営業利益", f"{data.financial.operating_profit:,}")
    with fin_col2:
        st.metric("人件費", f"{data.financial.personnel_cost:,}")
        st.metric("減価償却費", f"{data.financial.depreciation:,}")
    with fin_col3:
        st.metric("給与支給総額", f"{data.financial.salary_total:,}")
        added_value = data.financial.operating_profit + data.financial.personnel_cost + data.financial.depreciation
        st.metric("付加価値額", f"{added_value:,}")

with st.expander("補助対象経費", expanded=False):
    if data.expenses:
        expense_rows = []
        for e in data.expenses:
            expense_rows.append({
                "分類": e.category,
                "品目名": e.item_name,
                "金額（税抜）": f"{e.amount:,}円",
                "見積書": "あり" if e.has_quote else "なし",
            })
        st.dataframe(expense_rows, use_container_width=True)
        total = sum(e.amount for e in data.expenses)
        st.write(f"**合計: {total:,}円**")
    else:
        st.warning("経費データがありません")

# ---------------------------------------------------------------------------
# 収支計算（自動）
# ---------------------------------------------------------------------------
financial = FinancialData(
    sales=data.financial.sales * 1000,
    operating_profit=data.financial.operating_profit * 1000,
    depreciation=data.financial.depreciation * 1000,
    personnel_cost=data.financial.personnel_cost * 1000,
    salary_total=data.financial.salary_total * 1000,
    employee_count=data.financial.employee_count,
)

expenses = [
    SubsidyExpense(
        category=e.category, item_name=e.item_name,
        amount=e.amount, has_quote=e.has_quote,
    )
    for e in data.expenses
]

is_over_1b = "10億" in data.company.sales_category and "以上" in data.company.sales_category
subsidy = calculate_subsidy(expenses, sales_over_1billion=is_over_1b)

useful_life_str = data.effect.useful_life.replace("年", "") if data.effect.useful_life else "5"
try:
    useful_life = int(useful_life_str)
except ValueError:
    useful_life = 5
new_dep = estimate_depreciation(sum(e.amount for e in data.expenses), useful_life=useful_life)

plan = calculate_3year_plan(
    financial=financial,
    sales_increase_annual=data.effect.sales_increase_annual,
    cost_reduction_annual=data.effect.cost_reduction_annual,
    wage_increase_annual=data.wage.annual_increase,
    new_depreciation=new_dep,
    growth_start_year=1,
)

annual_effect = data.effect.sales_increase_annual + data.effect.cost_reduction_annual
payback = calculate_investment_payback(subsidy, annual_effect)

# ---------------------------------------------------------------------------
# セクション3: AI文章生成
# ---------------------------------------------------------------------------
st.divider()
st.subheader("3. AI文章生成（Claude API）")

st.caption("事業計画書のセクション2〜4（10セクション分）の文章をClaude APIで自動生成します。")

if "km_generated_texts" not in st.session_state:
    if st.button("文章を生成する", type="primary"):
        with st.status("事業計画書の文章を生成中...", expanded=True) as status:
            try:
                texts = generate_texts(data, generate_text)
                if texts:
                    st.session_state["km_generated_texts"] = texts
                    data.generated_texts = texts
                    st.session_state["km_hearing_data"] = data
                    total_chars = sum(len(v) for v in texts.values())
                    st.write(f"生成完了: {len(texts)}セクション / {total_chars:,}字")
                    status.update(label=f"文章生成完了（{total_chars:,}字）", state="complete")
                else:
                    status.update(label="文章生成エラー", state="error")
                    st.error("JSONの解析に失敗しました。再度お試しください。")
            except Exception as e:
                status.update(label="文章生成エラー", state="error")
                st.error(f"文章生成に失敗しました: {e}")
else:
    st.success("文章生成済み")

# ---------------------------------------------------------------------------
# セクション4: 文章プレビュー・編集
# ---------------------------------------------------------------------------
if "km_generated_texts" in st.session_state:
    st.divider()
    st.subheader("4. 文章プレビュー・編集")
    st.caption("生成された文章を確認・修正できます。修正後、そのまま書類生成に進みます。")

    texts = st.session_state["km_generated_texts"]
    edited_texts = {}
    total_chars = 0

    for key in SECTION_KEYS:
        label = SECTION_LABELS.get(key, key)
        target = SECTION_TARGET_CHARS.get(key, 200)
        current_text = texts.get(key, "")
        char_count = len(current_text)
        total_chars += char_count

        with st.expander(f"{label}（{char_count}字 / 目標{target}字）", expanded=False):
            edited = st.text_area(
                f"{label}",
                value=current_text,
                height=150,
                key=f"text_{key}",
                label_visibility="collapsed",
            )
            edited_texts[key] = edited

    st.metric("合計文字数", f"{total_chars:,}字（目標: 2,500〜3,500字）")

    # 編集結果をセッションに反映
    if edited_texts != texts:
        st.session_state["km_generated_texts"] = edited_texts
        data.generated_texts = edited_texts
        st.session_state["km_hearing_data"] = data

    # ---------------------------------------------------------------------------
    # セクション5: 書類生成
    # ---------------------------------------------------------------------------
    st.divider()
    st.subheader("5. 書類生成")

    if "km_documents" not in st.session_state:
        if st.button("申請書類を生成する", type="primary"):
            # 最新の編集テキストを反映
            data.generated_texts = st.session_state["km_generated_texts"]

            if not TEMPLATE_DIR.exists():
                st.error("テンプレートディレクトリが見つかりません。")
                st.stop()

            with tempfile.TemporaryDirectory() as tmpdir:
                output_dir = os.path.join(tmpdir, "output")
                os.makedirs(output_dir, exist_ok=True)

                progress = st.progress(0, text="書類を生成中...")

                def on_progress(step, total, label):
                    pct = int(step / total * 100)
                    progress.progress(pct, text=f"{label}を生成中... ({step}/{total})")

                try:
                    results = generate_all_documents(
                        data=data,
                        output_dir=output_dir,
                        template_dir=TEMPLATE_DIR,
                        subsidy=subsidy,
                        plan=plan,
                        on_progress=on_progress,
                    )
                    progress.progress(100, text="書類生成完了")

                    # ZIPにまとめる
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        for root, dirs, files in os.walk(output_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, output_dir)
                                zf.write(file_path, arcname)
                    zip_buffer.seek(0)

                    st.session_state["km_documents"] = {
                        "results": results,
                        "zip_bytes": zip_buffer.getvalue(),
                    }

                except Exception as e:
                    progress.progress(100, text="エラー")
                    st.error(f"書類生成エラー: {e}")
    else:
        st.success("書類生成済み")

    # ---------------------------------------------------------------------------
    # セクション6: 検証結果
    # ---------------------------------------------------------------------------
    if "km_documents" in st.session_state:
        st.divider()
        st.subheader("6. 検証結果")

        validation = validate_requirements(plan, subsidy)

        # 全要件判定
        if validation["all_met"]:
            st.success("全要件をクリアしています")
        else:
            st.error("一部の要件を満たしていません")

        # 個別表示
        for key in ["added_value", "salary", "expense_min"]:
            item = validation[key]
            if item["ok"]:
                st.success(item["message"])
            else:
                st.error(item["message"])

        # 補助金サマリー
        st.info(
            f"補助対象経費: {subsidy.total_expense:,}円　|　"
            f"交付申請額: {subsidy.subsidy_amount:,}円　|　"
            f"自己負担: {subsidy.self_payment:,}円　|　"
            f"投資回収: {payback}年"
        )

        # 収支計画テーブル
        with st.expander("3年間の収支計画（千円単位）", expanded=False):
            headers = ["項目", "基準年度", "1年目", "2年目", "3年目"]
            rows = [
                ("売上高", "sales"),
                ("営業利益", "operating_profit"),
                ("人件費", "personnel_cost"),
                ("減価償却費", "depreciation"),
                ("付加価値額", "added_value"),
                ("給与支給総額", "salary_total"),
                ("従業員数", "employee_count"),
            ]
            table_data = []
            for label, key in rows:
                row_data = {"項目": label}
                for i, year_data in enumerate(plan.years):
                    col_name = headers[i + 1]
                    val = year_data.get(key, 0)
                    if key == "employee_count":
                        row_data[col_name] = f"{val}名"
                    else:
                        row_data[col_name] = f"{val // 1000:,}"
                table_data.append(row_data)
            st.dataframe(table_data, use_container_width=True)

        # 書類生成結果
        doc_results = st.session_state["km_documents"]["results"]
        with st.expander("生成書類一覧", expanded=False):
            for name, path in doc_results.items():
                if path:
                    st.write(f"- {name}: {Path(path).name}")
                else:
                    st.warning(f"- {name}: 生成失敗")

        # ---------------------------------------------------------------------------
        # セクション7: ZIPダウンロード
        # ---------------------------------------------------------------------------
        st.divider()
        st.subheader("7. ダウンロード")

        company_name = data.company.name or "output"
        st.download_button(
            label="全書類をZIPでダウンロード",
            data=st.session_state["km_documents"]["zip_bytes"],
            file_name=f"香川県補助金_{company_name}_申請書類.zip",
            mime="application/zip",
            type="primary",
        )

        st.caption(
            "**注意:** 誓約書は自署が必要です。印刷して自署してください。\n\n"
            "交付申請書のフリガナ、チェックボックスの最終確認も忘れずに行ってください。"
        )

footer()
