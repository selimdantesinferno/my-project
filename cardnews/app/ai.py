"""AI로 글감을 카드뉴스 슬라이드 구조로 변환합니다.

ChatGPT(OpenAI) 와 Gemini(Google) 를 모두 지원하며,
설정(AI_PROVIDER) 또는 요청 파라미터로 선택합니다.

반환 형식(JSON):
{
  "slides": [
    {"type": "cover|content|stat", "title": "...", "body": "...", "highlight": "..."},
    ...
  ],
  "caption": "게시물 본문 캡션",
  "hashtags": ["#태그", ...]
}
"""
from __future__ import annotations

import json

from .config import settings

DEFAULT_PROMPT = (
    "핵심 정보를 간결하게 전달하는 카드뉴스를 만들어 주세요. "
    "주제 본문의 핵심 메시지를 추출하여 슬라이드별로 구성하고, "
    "통계 숫자가 있으면 반드시 강조(stat) 슬라이드로 활용하며, "
    "읽기 쉽고 임팩트 있는 짧은 문장을 사용하세요."
)


def _build_instruction(slide_count: int, account: str, user_prompt: str) -> str:
    return f"""당신은 한국어 카드뉴스(인스타그램/스레드 캐러셀) 카피라이터입니다.
아래 글감을 바탕으로 정확히 {slide_count}장의 슬라이드로 구성된 카드뉴스를 작성하세요.

작성 지침:
{user_prompt or DEFAULT_PROMPT}

각 슬라이드 규칙:
- 1번 슬라이드는 반드시 type="cover" (강렬한 후킹 제목).
- 마지막 슬라이드는 행동 유도(CTA)나 핵심 요약.
- 통계/숫자가 핵심이면 type="stat" 으로 만들고 highlight 에 숫자를 넣으세요.
- 그 외는 type="content".
- title 은 한 줄(최대 22자), body 는 1~3문장(최대 90자)로 짧게.
- 계정명 "{account}" 는 본문에 직접 넣지 마세요(디자인에서 자동 표기).

추가로 caption(게시물 본문, 2~4문장)과 hashtags(5~10개, # 포함)를 작성하세요.

반드시 아래 JSON 형식으로만 응답하세요(설명/마크다운 금지):
{{
  "slides": [
    {{"type": "cover", "title": "...", "body": "...", "highlight": ""}}
  ],
  "caption": "...",
  "hashtags": ["#...", "#..."]
}}"""


def _parse(raw: str) -> dict:
    raw = raw.strip()
    # 코드펜스 제거
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1] if raw.count("```") >= 2 else raw.strip("`")
        if raw.lstrip().startswith("json"):
            raw = raw.lstrip()[4:]
    # 첫 { 부터 마지막 } 까지 추출
    start, end = raw.find("{"), raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start : end + 1]
    data = json.loads(raw)
    if not isinstance(data.get("slides"), list) or not data["slides"]:
        raise ValueError("AI 응답에 slides 가 없습니다.")
    data.setdefault("caption", "")
    data.setdefault("hashtags", [])
    return data


async def _generate_openai(source: str, instruction: str) -> str:
    from openai import AsyncOpenAI

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY 가 설정되지 않았습니다.")
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    resp = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f"[글감]\n{source}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    return resp.choices[0].message.content or ""


async def _generate_gemini(source: str, instruction: str) -> str:
    import google.generativeai as genai

    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY 가 설정되지 않았습니다.")
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(
        settings.gemini_model,
        system_instruction=instruction,
        generation_config={"response_mime_type": "application/json"},
    )
    resp = await model.generate_content_async(f"[글감]\n{source}")
    return resp.text or ""


async def generate_slides(
    source: str,
    slide_count: int = 7,
    account: str = "",
    user_prompt: str = "",
    provider: str | None = None,
) -> dict:
    """글감(source)으로부터 카드뉴스 구조를 생성해 반환합니다."""
    provider = (provider or settings.ai_provider).lower()
    instruction = _build_instruction(slide_count, account, user_prompt)

    if provider == "gemini":
        raw = await _generate_gemini(source, instruction)
    else:
        raw = await _generate_openai(source, instruction)

    data = _parse(raw)
    # 슬라이드 수 보정
    data["slides"] = data["slides"][:slide_count]
    return data
