"""香川県未来投資応援補助金 要件検証

補助金の交付要件を満たしているかチェックする。
"""

from .calculate_plan import ThreeYearPlan, SubsidyCalculation


def validate_requirements(
    plan: ThreeYearPlan,
    subsidy: SubsidyCalculation,
) -> dict:
    """全要件を検証してレポートを返す

    Returns:
        dict: {
            "added_value": {"ok": bool, "rate": float, "message": str},
            "salary": {"ok": bool, "rate": float, "message": str},
            "expense_min": {"ok": bool, "amount": int, "message": str},
            "all_met": bool,
        }
    """
    result = {}

    # 付加価値額の増加
    result["added_value"] = {
        "ok": plan.added_value_increasing,
        "rate": plan.added_value_growth_rate,
        "message": (
            f"付加価値額 {plan.added_value_growth_rate:+.1f}%（3年間）"
            if plan.added_value_increasing
            else f"付加価値額が増加していません（{plan.added_value_growth_rate:+.1f}%）"
        ),
    }

    # 給与支給総額の増加
    result["salary"] = {
        "ok": plan.salary_increasing,
        "rate": plan.salary_growth_rate,
        "message": (
            f"給与支給総額 {plan.salary_growth_rate:+.1f}%（3年間）"
            if plan.salary_increasing
            else f"給与支給総額が増加していません（{plan.salary_growth_rate:+.1f}%）"
        ),
    }

    # 補助対象経費25万円以上
    expense_ok = subsidy.total_expense >= 250_000
    result["expense_min"] = {
        "ok": expense_ok,
        "amount": subsidy.total_expense,
        "message": (
            f"補助対象経費 {subsidy.total_expense:,}円（25万円以上）"
            if expense_ok
            else f"補助対象経費が25万円未満です（{subsidy.total_expense:,}円）"
        ),
    }

    result["all_met"] = all([
        result["added_value"]["ok"],
        result["salary"]["ok"],
        result["expense_min"]["ok"],
    ])

    return result
