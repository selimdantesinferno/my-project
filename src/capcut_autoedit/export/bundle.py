"""편집 모드의 최종 출력: 컷 클립 + SRT + 편집계획 + 사용 안내."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..models import EditPlan
from .clips import export_clips
from .srt import to_srt

_README = """# capcut-autoedit 출력물

이 폴더의 내용
  clips/         — 원본을 편집점에 맞춰 잘라낸 비디오 클립
  subtitles.srt  — 표준 SRT 자막
  edit_plan.json — 분석 결과(편집 계획) 원본. 참고용
  README.txt     — 이 파일

## CapCut 데스크톱에서 쓰는 방법
1. CapCut을 열고 새 프로젝트를 만든다
2. clips/ 폴더의 clip_*.mp4 를 전부 선택해 타임라인으로 드래그
   (파일명 순서대로 자동 배치됨)
3. subtitles.srt 를 타임라인의 자막 트랙으로 드래그

## 다른 편집기
프리미어 / DaVinci Resolve / Vrew 등에서도 동일한 방식으로 사용 가능.
"""


def write_bundle(plan: EditPlan, out_dir: str | Path, fast: bool = False) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    export_clips(plan, out / "clips", fast=fast)
    (out / "subtitles.srt").write_text(to_srt(plan.subtitles), encoding="utf-8")
    (out / "edit_plan.json").write_text(
        json.dumps(asdict(plan), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "README.txt").write_text(_README, encoding="utf-8")
    return out
