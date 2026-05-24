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

_PROMPT = """당신은 영상 편집 어시스턴트입니다.
주어진 영상을 분석해 다음을 JSON으로만 출력하세요(설명 금지):

{
  "cuts": [{"start": <초>, "end": <초>}],   // 최종 영상에 '남길' 구간들(원본 기준), 시간순
  "subtitles": [{"start": <초>, "end": <초>, "text": "..."}]  // 컷 적용 후 타임라인 기준 자막
}

규칙:
- 정적이거나 불필요한 구간(긴 침묵, 반복)은 cuts에서 제외해 영상을 압축하세요.
- 자막은 화자의 말을 받아써서 짧은 줄로 나누세요.
- 시간은 초 단위 숫자(소수 허용)."""


def analyze(path: Path, config: Config) -> EditPlan:
    from google import genai

    meta = probe(path)
    client = genai.Client(api_key=config.gemini_api_key)

    uploaded = client.files.upload(file=str(path))
    uploaded = _wait_active(client, uploaded)

    response = client.models.generate_content(
        model=config.gemini_model,
        contents=[uploaded, _PROMPT],
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

    cuts = [
        Cut(seconds_to_us(c["start"]), seconds_to_us(c["end"]))
        for c in data.get("cuts", [])
        if c["end"] > c["start"]
    ]
    # 컷이 비어 있으면 영상 전체를 하나의 컷으로 처리
    if not cuts:
        cuts = [Cut(0, meta["duration_us"])]

    subtitles = [
        Subtitle(seconds_to_us(s["start"]), seconds_to_us(s["end"]), s["text"])
        for s in data.get("subtitles", [])
        if s.get("text") and s["end"] > s["start"]
    ]

    return EditPlan(
        source_path=str(path),
        width=meta["width"],
        height=meta["height"],
        fps=meta["fps"],
        duration_us=meta["duration_us"],
        cuts=cuts,
        subtitles=subtitles,
    )
