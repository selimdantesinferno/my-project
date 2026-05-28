"""모드 1 — 편집 모드 (Draft Mode).

영상(파일 또는 유튜브 링크) → Gemini 분석 → CapCut 편집 가능 프로젝트 폴더.

원본 오디오를 보존하고, 컷·자막만 자동화한다. 결과물은 '완성품'이 아니라
CapCut에서 사용자가 직접 손볼 수 있는 '편집 가능한 프로젝트'다.
"""

from __future__ import annotations

from pathlib import Path

from ..analysis.gemini import analyze
from ..capcut.writer import write_draft
from ..config import Config
from ..input.loader import resolve_input


def run(source: str, out_dir: str, subtitle_style: str = "plain") -> Path:
    """편집 모드 파이프라인 실행. 생성된 draft 폴더 경로를 반환한다."""
    config = Config.load()
    video_path = resolve_input(source)
    plan = analyze(video_path, config, subtitle_style=subtitle_style)
    return write_draft(plan, out_dir)
