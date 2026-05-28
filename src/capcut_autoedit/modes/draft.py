"""모드 1 — 편집 모드 (Draft Mode).

영상(파일 또는 유튜브 링크) → Gemini 분석 → 편집 가능 번들 폴더 출력
(컷별 클립 + SRT 자막 + 편집계획 JSON + 사용 안내).

CapCut 데스크톱 최신 버전이 draft 파일을 암호화해 직접 쓰는 게 불가능해진 뒤,
원래의 "자동으로 캡컷 프로젝트 파일 생성" 방식 대신 어느 편집기에서도 통하는
'드래그 한 번으로 들어가는' 번들을 만든다.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..analysis.gemini import analyze
from ..config import Config
from ..export.bundle import write_bundle
from ..input.loader import resolve_input
from ..models import EditPlan


def run(
    source: str,
    out_dir: str,
    subtitle_style: str = "plain",
    fast: bool = False,
    from_plan: str | None = None,
) -> Path:
    """편집 모드 파이프라인 실행. 생성된 번들 폴더 경로를 반환한다.

    from_plan 이 주어지면 Gemini 분석을 건너뛰고 해당 JSON 의 EditPlan 을
    그대로 사용해 export 만 실행한다 (재실행 / 수동 편집 / 키 없이 테스트).
    """
    if from_plan:
        plan = EditPlan.from_dict(json.loads(Path(from_plan).read_text(encoding="utf-8")))
        if source:
            # 사용자가 source 를 명시했다면 plan 의 source_path 를 덮어쓴다
            plan.source_path = str(resolve_input(source))
    else:
        config = Config.load()
        video_path = resolve_input(source)
        plan = analyze(video_path, config, subtitle_style=subtitle_style)

    return write_bundle(plan, out_dir, fast=fast)
