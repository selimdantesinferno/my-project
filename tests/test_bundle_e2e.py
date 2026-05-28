"""ffmpeg 합성 영상으로 export 파이프라인 전체를 검증.

Gemini 호출 없이 EditPlan 을 손으로 짜서 write_bundle 만 돌린다 —
컷 분할 mp4·SRT·README가 실제로 만들어지는지, 클립 길이가 맞는지 확인.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from capcut_autoedit.export.bundle import write_bundle
from capcut_autoedit.models import Cut, EditPlan, Subtitle, seconds_to_us

pytestmark = pytest.mark.skipif(
    not shutil.which("ffmpeg") or not shutil.which("ffprobe"),
    reason="ffmpeg/ffprobe 가 PATH에 없음",
)


def _make_test_video(path: Path, seconds: int = 6) -> None:
    """6초짜리 테스트 영상 생성 (컬러바 + 사인파 오디오)."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={seconds}:size=320x240:rate=10",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        str(path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def test_bundle_creates_clips_srt_and_readme(tmp_path: Path):
    src = tmp_path / "source.mp4"
    _make_test_video(src, seconds=6)

    plan = EditPlan(
        source_path=str(src),
        width=320,
        height=240,
        fps=10.0,
        duration_us=seconds_to_us(6),
        cuts=[
            Cut(seconds_to_us(0), seconds_to_us(2)),
            Cut(seconds_to_us(3), seconds_to_us(5)),
        ],
        subtitles=[
            Subtitle(seconds_to_us(0), seconds_to_us(1.5), "첫 번째 자막"),
            Subtitle(seconds_to_us(2), seconds_to_us(3.5), "두 번째 자막"),
        ],
    )

    out = write_bundle(plan, tmp_path / "out")

    # 1) 결과 폴더 구성
    assert (out / "clips").is_dir()
    assert (out / "subtitles.srt").is_file()
    assert (out / "edit_plan.json").is_file()
    assert (out / "README.txt").is_file()

    # 2) 클립 개수 및 길이 (≈ 2초, 오차 0.3초 허용 — 인코딩 디테일)
    clips = sorted((out / "clips").glob("clip_*.mp4"))
    assert len(clips) == 2
    for c in clips:
        d = _probe_duration(c)
        assert 1.7 <= d <= 2.3, f"{c.name} 길이 {d}s 가 기대 범위(2s±0.3) 밖"

    # 3) SRT 내용
    srt = (out / "subtitles.srt").read_text(encoding="utf-8")
    assert "1\n00:00:00,000 --> 00:00:01,500\n첫 번째 자막" in srt
    assert "2\n00:00:02,000 --> 00:00:03,500\n두 번째 자막" in srt

    # 4) edit_plan.json 라운드트립
    restored = json.loads((out / "edit_plan.json").read_text(encoding="utf-8"))
    assert restored["duration_us"] == seconds_to_us(6)
    assert len(restored["cuts"]) == 2
    assert len(restored["subtitles"]) == 2


def test_fast_mode_also_produces_clips(tmp_path: Path):
    src = tmp_path / "source.mp4"
    _make_test_video(src, seconds=6)

    plan = EditPlan(
        source_path=str(src),
        width=320, height=240, fps=10.0,
        duration_us=seconds_to_us(6),
        cuts=[Cut(seconds_to_us(0), seconds_to_us(3))],
        subtitles=[],
    )

    out = write_bundle(plan, tmp_path / "out", fast=True)
    clips = sorted((out / "clips").glob("clip_*.mp4"))
    assert len(clips) == 1
    assert clips[0].stat().st_size > 0
