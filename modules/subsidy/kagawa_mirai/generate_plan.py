"""香川県未来投資応援補助金 事業計画書プロンプトテンプレート

ヒアリング情報から事業計画書（別紙1）の各セクション文章を生成する。
"""

SYSTEM_PROMPT = """あなたは補助金申請の専門家です。
香川県未来投資応援補助金の事業計画書を作成してください。

【審査のポイント】（書面審査のみ）
1. 付加価値額の増加が具体的に計画されているか
2. 賃上げの取組みが具体的かつ実現可能か
3. 補助事業終了後も効果が持続するか
4. 費用対効果が高く具体的な成果が見込めるか
5. 他事業者や地域への波及効果があるか

【最重要: 文章のトーン】
- 経営者が自ら書いた文章に見せる（AI臭を出さない）
- 「〜に取り組む」「〜と考えている」等の簡潔な文末
- 1文1意の原則（1つの文に1つのメッセージ）
- 数字は具体的だが誇張しない
- 補助金の規模感（上限100万円）に合った記述
- 専門用語を避け平易な言葉で
- 1文は60字以内が目安

【絶対に使わない表現】
- 「推進してまいります」「寄与するものと確信」
- 「革新的」「画期的」「飛躍的」
- 「総合的」「包括的」「戦略的」
- 「シナジー効果」「パラダイムシフト」
- 動詞の連鎖（「〜し、〜を実現し、〜に貢献する」）

【推奨する表現】
- 「〜である。」「〜と考えている。」
- 「〜に取り組む。」「〜を計画している。」
- 業界固有の言い回し
- たまに短い文を入れる「これが課題である。」
"""

FULL_PLAN_PROMPT = """
以下の企業情報・ヒアリングデータを基に、香川県未来投資応援補助金の事業計画書（別紙1）の
セクション2〜4の全文を一括で生成してください。

セクション5（収支計画）とセクション6（経費一覧）は自動計算するため不要です。

### 企業・事業情報
{all_data}

### 出力形式
以下のJSON形式で出力してください：

```json
{{
  "section_2_1": "会社の沿革やこれまでの既存事業の内容（400字程度）",
  "section_2_2": "物価高騰による経営面等への影響（400字程度）",
  "section_3_1": "事業の内容（500字程度）",
  "section_3_2": "賃上げの具体的な計画（200字程度）",
  "section_4_1": "付加価値額の増加（300字程度）",
  "section_4_2": "賃上げの内容（100字程度）",
  "section_4_3": "持続性（150字程度）",
  "section_4_4": "有効性（150字程度）",
  "section_4_5": "波及性（150字程度）",
  "section_4_6": "その他特筆すべき事項（100字程度、なければ空文字）"
}}
```

### 文字数の目標合計: 2,500〜3,500字

{system_prompt}
"""


def format_company_info(data: dict) -> str:
    lines = []
    mapping = {
        "company_name": "会社名", "industry": "業種",
        "business_description": "事業内容", "employee_count": "従業員数",
        "established_date": "設立年月日", "capital": "資本金",
        "history": "創業からの経緯", "strengths": "特徴・強み",
        "customers": "主な顧客・取引先", "achievements": "実績・評価",
    }
    for key, label in mapping.items():
        if key in data and data[key]:
            lines.append(f"- {label}: {data[key]}")
    return "\n".join(lines)


def format_price_impact(data: dict) -> str:
    lines = []
    mapping = {
        "material_name": "影響が大きい原材料名",
        "price_increase_rate": "価格上昇率",
        "monthly_cost_increase": "月額コスト増",
        "energy_impact": "エネルギーコストの影響",
        "labor_cost_impact": "人件費の上昇影響",
        "annual_total_increase": "年間合計コスト増",
        "cost_to_sales_ratio": "売上高に対する割合",
        "countermeasures": "これまでの対策",
        "limitations": "対策の限界",
    }
    for key, label in mapping.items():
        if key in data and data[key]:
            lines.append(f"- {label}: {data[key]}")
    return "\n".join(lines)


def format_business_content(data: dict) -> str:
    lines = []
    mapping = {
        "project_name": "事業名", "purpose": "目的", "method": "手法",
        "equipment_name": "設備名称", "equipment_description": "設備の概要・特徴",
        "selection_reason": "選定理由",
        "before_process": "現在の作業方法（Before）",
        "after_process": "導入後の変化（After）",
        "schedule_order": "発注予定日", "schedule_delivery": "納品・設置予定日",
        "schedule_start": "稼働開始予定日", "schedule_complete": "事業完了予定日",
    }
    for key, label in mapping.items():
        if key in data and data[key]:
            lines.append(f"- {label}: {data[key]}")
    return "\n".join(lines)


def format_effect_info(data: dict) -> str:
    lines = []
    mapping = {
        "sales_increase_annual": "年間売上増加見込み",
        "sales_increase_reason": "売上増加の根拠",
        "cost_reduction_annual": "年間コスト削減見込み",
        "cost_reduction_reason": "コスト削減の根拠",
        "useful_life": "設備の耐用年数", "maintenance": "メンテナンス体制",
        "ease_of_operation": "操作の容易さ", "payback_period": "投資回収の見込み",
        "regional_contribution": "地域への貢献",
        "reference_for_others": "他事業者への参考",
        "other_notes": "その他特筆すべき事項",
    }
    for key, label in mapping.items():
        if key in data and data[key]:
            lines.append(f"- {label}: {data[key]}")
    return "\n".join(lines)


def format_wage_info(data: dict) -> str:
    lines = []
    mapping = {
        "start_date": "賃上げ開始時期", "target_employees": "対象者",
        "method": "賃上げ方法", "amount": "具体的な金額",
        "annual_increase": "年間給与支給総額増加額",
        "funding_source": "賃上げの原資",
    }
    for key, label in mapping.items():
        if key in data and data[key]:
            lines.append(f"- {label}: {data[key]}")
    return "\n".join(lines)


def build_full_prompt(hearing_data: dict) -> str:
    """全データからフルプロンプトを構築"""
    sections = []
    sections.append("## 企業基本情報")
    sections.append(format_company_info(hearing_data.get("company", {})))
    sections.append("\n## 物価高騰の影響")
    sections.append(format_price_impact(hearing_data.get("price_impact", {})))
    sections.append("\n## 補助事業の内容")
    sections.append(format_business_content(hearing_data.get("business", {})))
    sections.append("\n## 補助事業の効果")
    sections.append(format_effect_info(hearing_data.get("effect", {})))
    sections.append("\n## 賃上げ計画")
    sections.append(format_wage_info(hearing_data.get("wage", {})))
    all_data = "\n".join(sections)
    return FULL_PLAN_PROMPT.format(all_data=all_data, system_prompt=SYSTEM_PROMPT)
