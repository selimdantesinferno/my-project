"""원본 영상에서 컷 구간들을 잘라 개별 mp4로 출력 (ffmpeg)."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..models import EditPlan


def export_clips(plan: EditPlan, out_dir: Path, fast: bool = False) -> list[Path]:
    """각 컷을 clip_NNN.mp4 로 저장하고 경로 목록을 반환한다.

    fast=True 면 스트림 카피(빠르지만 키프레임에 스냅), False(기본)면 정밀 재인코딩.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pad = max(3, len(str(len(plan.cuts))))
    paths: list[Path] = []
    for i, cut in enumerate(plan.cuts, start=1):
        out_path = out_dir / f"clip_{i:0{pad}d}.mp4"
        _ffmpeg_cut(
            plan.source_path, cut.source_start_us, cut.source_end_us, out_path, fast
        )
        paths.append(out_path)
    return paths


def _ffmpeg_cut(src: str, start_us: int, end_us: int, out: Path, fast: bool) -> None:
    start_s = start_us / 1_000_000
    end_s = end_us / 1_000_000
    base = ["ffmpeg", "-y", "-ss", f"{start_s:.3f}", "-to", f"{end_s:.3f}", "-i", src]
    codec = ["-c", "copy"] if fast else ["-c:v", "libx264", "-c:a", "aac"]
    subprocess.run(base + codec + [str(out)], check=True, capture_output=True)
