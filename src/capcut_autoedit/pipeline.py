"""입력 -> 분석 -> 빌드 오케스트레이션."""

from __future__ import annotations

from pathlib import Path

from .analysis.gemini import analyze
from .capcut.writer import write_draft
from .config import Config
from .input.loader import resolve_input


def run(source: str, out_dir: str) -> Path:
    """전체 파이프라인 실행. 생성된 draft 폴더 경로를 반환한다."""
    config = Config.load()
    video_path = resolve_input(source)
    plan = analyze(video_path, config)
    return write_draft(plan, out_dir)
