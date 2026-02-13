"""香川県未来投資応援補助金 データモデル"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CompanyInfo:
    """企業基本情報"""
    name: str = ""
    corporate_number: str = ""
    representative: str = ""
    representative_title: str = "代表取締役"
    postal_code: str = ""
    address: str = ""
    phone: str = ""
    fax: str = ""
    email: str = ""
    industry: str = ""
    industry_code: str = ""
    business_description: str = ""
    employee_count: int = 0
    capital: int = 0
    established_date: str = ""
    fiscal_month: int = 0
    entity_type: str = ""  # 中小企業/個人事業主/その他法人
    sales_category: str = ""  # 10億円未満 / 10億円以上


@dataclass
class PriceImpact:
    """物価高騰の影響"""
    history: str = ""
    main_business: str = ""
    strengths: str = ""
    customers: str = ""
    achievements: str = ""
    material_name: str = ""
    price_increase_rate: str = ""
    monthly_cost_increase: str = ""
    energy_impact: str = ""
    labor_cost_impact: str = ""
    annual_total_increase: str = ""
    cost_to_sales_ratio: str = ""
    countermeasures: str = ""
    limitations: str = ""


@dataclass
class BusinessPlan:
    """補助事業の内容"""
    project_name: str = ""
    purpose: str = ""
    method: str = ""
    current_field: str = ""
    plan_field: str = ""
    equipment_name: str = ""
    equipment_description: str = ""
    equipment_maker: str = ""
    selection_reason: str = ""
    before_process: str = ""
    after_process: str = ""
    comparison: str = ""
    schedule_order: str = ""
    schedule_delivery: str = ""
    schedule_start: str = ""
    schedule_complete: str = ""


@dataclass
class EffectPlan:
    """補助事業の効果"""
    sales_increase_annual: int = 0
    sales_increase_reason: str = ""
    cost_reduction_annual: int = 0
    cost_reduction_reason: str = ""
    useful_life: str = ""
    maintenance: str = ""
    ease_of_operation: str = ""
    payback_estimate: str = ""
    regional_contribution: str = ""
    reference_for_others: str = ""
    other_notes: str = ""


@dataclass
class WagePlan:
    """賃上げ計画"""
    start_date: str = ""
    target_employees: str = ""
    method: str = ""
    amount: str = ""
    annual_increase: int = 0
    funding_source: str = ""


@dataclass
class FinancialInfo:
    """財務情報"""
    sales: int = 0
    operating_profit: int = 0
    personnel_cost: int = 0
    depreciation: int = 0
    salary_total: int = 0
    employee_count: int = 1


@dataclass
class SubsidyExpenseItem:
    """補助対象経費の項目"""
    category: str = ""
    item_name: str = ""
    amount: int = 0
    has_quote: bool = False
    note: str = ""


@dataclass
class HearingData:
    """ヒアリングデータ全体"""
    company: CompanyInfo = field(default_factory=CompanyInfo)
    price_impact: PriceImpact = field(default_factory=PriceImpact)
    business: BusinessPlan = field(default_factory=BusinessPlan)
    effect: EffectPlan = field(default_factory=EffectPlan)
    wage: WagePlan = field(default_factory=WagePlan)
    financial: FinancialInfo = field(default_factory=FinancialInfo)
    expenses: List[SubsidyExpenseItem] = field(default_factory=list)
    generated_texts: Dict[str, str] = field(default_factory=dict)
