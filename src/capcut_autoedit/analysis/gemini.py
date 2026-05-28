"""Gemini로 영상을 분석해 편집점 + 자막을 EditPlan으로 만든다.

위치: 백엔드. API 키는 환경변수에서만 읽는다(프론트에 노출 금지).

흐름:
  1) 영상 파일을 Gemini File API에 업로드
  2) JSON 형식으로 컷 구간 + 자막을 요청
  3) 응답을 EditPlan으로 정규화
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from ..config import Config
from ..media import probe
from ..models import Cut, EditPlan, Subtitle, seconds_to_us

# 자막 스타일 — Shorts 스타일은 '채널 헌법' 내레이션 가이드에서 핵심 규칙만 추출
SubtitleStyle = str  # "plain" | "shorts-ko"

_BASE_PROMPT = """당신은 영상 편집 어시스턴트이다.
주어진 영상(실측 길이 {duration_s:.3f}초)을 분석해 편집 계획을 JSON으로만 출력하라.

[제0원칙 — 타임코드 무결성 / 절대 진실성]
- 영상 실측 길이({duration_s:.3f}초)를 초과하는 타임코드를 절대 생성하지 마라.
- 영상에 명시적으로 존재하지 않는 사실/대사를 추측하거나 창작하지 마라.
- 불확실한 구간은 cuts에 포함하지 말고 버려라.

[Step 1 — 내부 분석 (출력하지 말 것, 사고만)]
영상을 프레임 단위로 다음 5요소로 해부한다:
  1) 객체/행위  2) 수치/텍스트  3) 시네마틱 정보(카메라/조명)
  4) 청각 정보(대사·소리)  5) 물리적 상호작용
정적·반복·침묵·NG 구간을 식별한다.

[Step 2 — 편집 결정 (이 JSON만 출력)]
{{
  "cuts":      [{{"start": <초>, "end": <초>}}],
  "subtitles": [{{"start": <초>, "end": <초>, "text": "..."}}]
}}

규칙:
- cuts: 원본 기준 '남길' 구간 목록(시간순). 정적/반복/침묵은 제외해 압축한다.
- subtitles: 컷 적용 후 '최종 타임라인 기준'으로 자막을 부여한다(원본 기준 아님).
- 시간은 초 단위 숫자(소수 허용).
- 한 자막 줄은 길어도 약 20자, 길이는 2~4초 권장.
{style_block}"""

_SHORTS_KO_STYLE = """
[자막 스타일 — Shorts 한국어]
- 어미는 '선언(~다/~니다/~합니다)'과 '연결(~데요/~는데요/~죠/~요)'을 교차 사용한다.
- 같은 계열 어미가 2회 연속 나오지 않게 한다.
- 마침표(.), 쉼표(,), 작은따옴표(') 사용 금지. 강조는 느낌표(!)만.
- 금지 어미: ~고요, ~까요, ~네요, ~는요, ~겁니다 (사용 시 해당 자막 폐기 후 재작성)."""

_PLAIN_STYLE = """
[자막 스타일 — 기본]
- 화자의 말을 받아써서 자연스럽게 분할한다."""


def _build_prompt(duration_us: int, style: SubtitleStyle) -> str:
    duration_s = duration_us / 1_000_000
    style_block = _SHORTS_KO_STYLE if style == "shorts-ko" else _PLAIN_STYLE
    return _BASE_PROMPT.format(duration_s=duration_s, style_block=style_block)


def analyze(
    path: Path, config: Config, subtitle_style: SubtitleStyle = "plain"
) -> EditPlan:
    from google import genai

    meta = probe(path)
    client = genai.Client(api_key=config.gemini_api_key)

    uploaded = client.files.upload(file=str(path))
    uploaded = _wait_active(client, uploaded)

    prompt = _build_prompt(meta["duration_us"], subtitle_style)
    response = client.models.generate_content(
        model=config.gemini_model,
        contents=[uploaded, prompt],
        config={"response_mime_type": "application/json"},
    )
    return _to_plan(response.text, path, meta)


def _wait_active(client, file, timeout_s: int = 300):
    """업로드된 파일이 처리(ACTIVE)될 때까지 대기."""
    deadline = time.time() + timeout_s
    while getattr(file.state, "name", file.state) == "PROCESSING":
        if time.time() > deadline:
            raise TimeoutError("Gemini 파일 처리 시간 초과")
        time.sleep(2)
        file = client.files.get(name=file.name)
    if getattr(file.state, "name", file.state) == "FAILED":
        raise RuntimeError("Gemini 파일 처리 실패")
    return file


def _to_plan(raw_json: str, path: Path, meta: dict) -> EditPlan:
    data = json.loads(raw_json)
    duration_us = meta["duration_us"]

    cuts: list[Cut] = []
    for c in data.get("cuts", []):
        start_us = max(0, seconds_to_us(c["start"]))
        end_us = min(duration_us, seconds_to_us(c["end"]))
        if end_us > start_us:
            cuts.append(Cut(start_us, end_us))

    # 컷이 비어 있으면 영상 전체를 하나의 컷으로 처리
    if not cuts:
        cuts = [Cut(0, duration_us)]

    timeline_total = sum(c.duration_us for c in cuts)

    subtitles: list[Subtitle] = []
    for s in data.get("subtitles", []):
        text = (s.get("text") or "").strip()
        if not text:
            continue
        start_us = max(0, seconds_to_us(s["start"]))
        end_us = min(timeline_total, seconds_to_us(s["end"]))
        if end_us > start_us:
            subtitles.append(Subtitle(start_us, end_us, text))

    return EditPlan(
        source_path=str(path),
        width=meta["width"],
        height=meta["height"],
        fps=meta["fps"],
        duration_us=duration_us,
        cuts=cuts,
        subtitles=subtitles,
    )
