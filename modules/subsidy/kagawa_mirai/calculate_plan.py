"""香川県未来投資応援補助金 3年間収支計算エンジン

【省力化補助金との違い】
- 計画年数: 5年 → 3年
- 付加価値額要件: 年平均4%以上 → 増加すればOK（率の規定なし）
- 賃上げ要件: 年平均6%以上等 → 増加すればOK（率の規定なし）
- 補助率: 3/4
- 上限: 100万円（売上10億以上は500万円）
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class FinancialData:
    """財務データ（直近期末の実績）"""
    sales: int = 0
    operating_profit: int = 0
    depreciation: int = 0
    personnel_cost: int = 0
    salary_total: int = 0
    employee_count: int = 1

    @property
    def added_value(self) -> int:
        return self.operating_profit + self.personnel_cost + self.depreciation

    @property
    def added_value_rate(self) -> float:
        if self.sales > 0:
            return self.added_value / self.sales * 100
        return 0.0


@dataclass
class SubsidyExpense:
    """補助対象経費"""
    category: str = ""
    item_name: str = ""
    amount: int = 0
    has_quote: bool = False


@dataclass
class SubsidyCalculation:
    """補助金額の計算結果"""
    total_expense: int = 0
    subsidy_rate: float = 0.75
    upper_limit: int = 1_000_000
    subsidy_amount: int = 0
    self_payment: int = 0

    @property
    def is_over_500k(self) -> bool:
        return self.total_expense >= 500_000


@dataclass
class ThreeYearPlan:
    """3年間の収支計画"""
    years: List[Dict] = None
    added_value_increasing: bool = False
    salary_increasing: bool = False
    all_requirements_met: bool = False
    added_value_growth_rate: float = 0.0
    salary_growth_rate: float = 0.0

    def __post_init__(self):
        if self.years is None:
            self.years = []


def calculate_subsidy(
    expenses: List[SubsidyExpense],
    sales_over_1billion: bool = False,
) -> SubsidyCalculation:
    """補助金額を計算"""
    calc = SubsidyCalculation()
    calc.total_expense = sum(e.amount for e in expenses)
    calc.subsidy_rate = 0.75
    calc.upper_limit = 5_000_000 if sales_over_1billion else 1_000_000
    raw_subsidy = int(calc.total_expense * calc.subsidy_rate)
    calc.subsidy_amount = min(raw_subsidy, calc.upper_limit)
    calc.self_payment = calc.total_expense - calc.subsidy_amount
    return calc


def calculate_3year_plan(
    financial: FinancialData,
    sales_increase_annual: int = 0,
    cost_reduction_annual: int = 0,
    wage_increase_annual: int = 0,
    new_depreciation: int = 0,
    employee_change: int = 0,
    growth_start_year: int = 1,
) -> ThreeYearPlan:
    """3年間の収支計画を自動計算"""
    plan = ThreeYearPlan()

    base = {
        "year": 0, "label": "基準年度",
        "sales": financial.sales,
        "operating_profit": financial.operating_profit,
        "depreciation": financial.depreciation,
        "personnel_cost": financial.personnel_cost,
        "salary_total": financial.salary_total,
        "employee_count": financial.employee_count,
        "added_value": financial.added_value,
    }
    plan.years.append(base)

    for year in range(1, 4):
        if growth_start_year == 1:
            effect_ratio = 0.5 if year == 1 else 1.0
        else:
            if year == 1:
                effect_ratio = 0.0
            elif year == 2:
                effect_ratio = 0.7
            else:
                effect_ratio = 1.0

        sales = financial.sales + int(sales_increase_annual * effect_ratio)
        cost_saving = int(cost_reduction_annual * effect_ratio)
        wage_cumulative = wage_increase_annual * year
        personnel_cost = financial.personnel_cost + wage_cumulative
        salary_total = financial.salary_total + wage_cumulative
        depreciation = financial.depreciation + new_depreciation

        emp_ratio = year / 3
        employee_count = financial.employee_count + int(employee_change * emp_ratio)
        if employee_count < 1:
            employee_count = 1

        if financial.sales > 0:
            gross_margin = min(
                (financial.operating_profit + financial.personnel_cost) / financial.sales,
                0.5,
            )
        else:
            gross_margin = 0.3

        profit_from_sales = int((sales - financial.sales) * gross_margin)
        operating_profit = financial.operating_profit + profit_from_sales + cost_saving - wage_cumulative
        added_value = operating_profit + personnel_cost + depreciation

        plan.years.append({
            "year": year, "label": f"{year}年目",
            "sales": sales,
            "operating_profit": operating_profit,
            "depreciation": depreciation,
            "personnel_cost": personnel_cost,
            "salary_total": salary_total,
            "employee_count": employee_count,
            "added_value": added_value,
        })

    base_av = plan.years[0]["added_value"]
    final_av = plan.years[3]["added_value"]
    base_sal = plan.years[0]["salary_total"]
    final_sal = plan.years[3]["salary_total"]

    plan.added_value_increasing = final_av > base_av
    plan.salary_increasing = final_sal > base_sal
    plan.all_requirements_met = plan.added_value_increasing and plan.salary_increasing

    if base_av > 0:
        plan.added_value_growth_rate = (final_av - base_av) / base_av * 100
    if base_sal > 0:
        plan.salary_growth_rate = (final_sal - base_sal) / base_sal * 100

    return plan


def estimate_depreciation(equipment_cost: int, useful_life: int = 5) -> int:
    """設備の年間減価償却費を概算（定額法）"""
    return int(equipment_cost / useful_life)


def calculate_investment_payback(
    subsidy: SubsidyCalculation,
    annual_effect: int,
) -> float:
    """投資回収期間を計算（年）"""
    if annual_effect <= 0:
        return float("inf")
    return round(subsidy.self_payment / annual_effect, 1)
