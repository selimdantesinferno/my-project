"""draft 폴더 출력.

CapCut 데스크톱은 프로젝트를 '폴더 하나'로 저장한다:
  <프로젝트>/
    draft_content.json     <- 트랙/세그먼트/소재
    draft_meta_info.json   <- 메타데이터

[참고] CapCut이 이 폴더를 인식하려면 보통 CapCut의 Drafts 디렉터리 안에
있어야 한다. 위치는 OS/버전마다 다르므로 출력 경로는 사용자가 지정한다.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from ..models import EditPlan
from .builder import build_draft_content


def write_draft(plan: EditPlan, out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    content = build_draft_content(plan)
    _dump(out / "draft_content.json", content)
    _dump(out / "draft_meta_info.json", _meta_info(plan, out.name))
    return out


def _meta_info(plan: EditPlan, name: str) -> dict:
    now_us = int(time.time() * 1_000_000)
    return {
        "draft_name": name,
        "draft_fold_path": "",
        "tm_draft_create": now_us,
        "tm_draft_modified": now_us,
        "draft_duration": plan.total_timeline_us(),
    }


def _dump(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
