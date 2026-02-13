"""香川県未来投資応援補助金 AI文章生成

Claude APIを使って事業計画書のセクション2〜4の文章を生成する。
"""

import json
import re

from .data_models import HearingData
from .hearing_reader import hearing_to_prompt_data
from .generate_plan import build_full_prompt, SYSTEM_PROMPT

SECTION_KEYS = [
    "section_2_1", "section_2_2",
    "section_3_1", "section_3_2",
    "section_4_1", "section_4_2",
    "section_4_3", "section_4_4",
    "section_4_5", "section_4_6",
]

SECTION_LABELS = {
    "section_2_1": "会社の沿革・既存事業",
    "section_2_2": "物価高騰の影響",
    "section_3_1": "事業の内容",
    "section_3_2": "賃上げ計画",
    "section_4_1": "付加価値額の増加",
    "section_4_2": "賃上げの内容",
    "section_4_3": "持続性",
    "section_4_4": "有効性",
    "section_4_5": "波及性",
    "section_4_6": "その他",
}

SECTION_TARGET_CHARS = {
    "section_2_1": 400,
    "section_2_2": 400,
    "section_3_1": 500,
    "section_3_2": 200,
    "section_4_1": 300,
    "section_4_2": 100,
    "section_4_3": 150,
    "section_4_4": 150,
    "section_4_5": 150,
    "section_4_6": 100,
}


def generate_texts(data: HearingData, generate_text_fn) -> dict[str, str]:
    """Claude APIで10セクションの文章を一括生成

    Args:
        data: ヒアリングデータ
        generate_text_fn: テキスト生成関数 (system_prompt, user_message) -> str

    Returns:
        dict: セクションキー → 生成テキスト
    """
    prompt_data = hearing_to_prompt_data(data)
    full_prompt = build_full_prompt(prompt_data)

    response = generate_text_fn(
        system_prompt=SYSTEM_PROMPT,
        user_message=full_prompt,
    )

    return _parse_json_response(response)


def _parse_json_response(response: str) -> dict[str, str]:
    """Claude APIのレスポンスからJSONを抽出"""
    # ```json ... ``` ブロックを探す
    json_match = re.search(r"```json\s*\n?(.*?)\n?\s*```", response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # JSON部分を直接探す
        json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            return {}

    try:
        result = json.loads(json_str)
        # 期待するキーのみ抽出
        return {k: v for k, v in result.items() if k in SECTION_KEYS}
    except json.JSONDecodeError:
        return {}
