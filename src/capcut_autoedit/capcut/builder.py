"""EditPlan -> CapCut draft_content.json (dict).

이 파일이 프로젝트의 심장이다.

[중요] CapCut draft 스키마는 비공식이며 버전마다 필드가 다르다.
여기 구조는 리버스 엔지니어링에 기반한 '근사치'이므로, 실제 CapCut
데스크톱에서 만든 샘플 draft_content.json 으로 반드시 검증/보정해야 한다.
(docs/CAPCUT_FORMAT.md 참고)

핵심 개념:
  - materials: 소재 풀(videos / texts ...). 각 소재는 고유 id를 가진다.
  - tracks: 트랙 목록. 각 트랙의 segment가 material_id로 소재를 참조한다.
  - target_timerange: 타임라인 상의 위치/길이 (마이크로초)
  - source_timerange: 원본 소재에서 잘라 쓸 구간 (마이크로초)
"""

from __future__ import annotations

import uuid

from ..models import EditPlan


def _uid() -> str:
    return str(uuid.uuid4()).upper()


def _timerange(start: int, duration: int) -> dict:
    return {"start": int(start), "duration": int(duration)}


def build_draft_content(plan: EditPlan) -> dict:
    """EditPlan을 draft_content.json 구조(dict)로 변환한다."""
    video_material = _video_material(plan)
    video_segments, timeline_len = _video_segments(plan, video_material["id"])

    text_materials, text_segments = _text_track(plan)

    canvas = {"id": _uid(), "type": "canvas_color", "color": "#000000"}

    return {
        "id": _uid(),
        "canvas_config": {
            "width": plan.width,
            "height": plan.height,
            "ratio": "original",
        },
        "fps": plan.fps,
        "duration": timeline_len,
        "materials": {
            "videos": [video_material],
            "texts": text_materials,
            "canvases": [canvas],
            "audios": [],
            "stickers": [],
        },
        "tracks": [
            {
                "id": _uid(),
                "type": "video",
                "attribute": 0,
                "segments": video_segments,
            },
            {
                "id": _uid(),
                "type": "text",
                "attribute": 0,
                "segments": text_segments,
            },
        ],
        "platform": "capcut-autoedit",
        "version": "0.1.0",
    }


def _video_material(plan: EditPlan) -> dict:
    return {
        "id": _uid(),
        "type": "video",
        "path": plan.source_path,
        "width": plan.width,
        "height": plan.height,
        "duration": plan.duration_us,
        "has_audio": True,
    }


def _video_segments(plan: EditPlan, material_id: str) -> tuple[list[dict], int]:
    """컷들을 타임라인에 순서대로 이어붙인다.

    각 컷은 원본의 [source_start, source_end] 구간을 가져와(source_timerange),
    타임라인에서는 직전 컷 끝에 바로 이어 붙인다(target_timerange).
    """
    segments: list[dict] = []
    cursor = 0
    for cut in plan.cuts:
        segments.append(
            {
                "id": _uid(),
                "material_id": material_id,
                "target_timerange": _timerange(cursor, cut.duration_us),
                "source_timerange": _timerange(cut.source_start_us, cut.duration_us),
                "speed": 1.0,
                "volume": 1.0,
                "visible": True,
            }
        )
        cursor += cut.duration_us
    return segments, cursor


def _text_track(plan: EditPlan) -> tuple[list[dict], list[dict]]:
    """자막마다 text 소재 1개 + 세그먼트 1개."""
    materials: list[dict] = []
    segments: list[dict] = []
    for sub in plan.subtitles:
        mat_id = _uid()
        materials.append(
            {
                "id": mat_id,
                "type": "text",
                "content": sub.text,
                "font_size": 8.0,
                "text_color": "#FFFFFF",
            }
        )
        segments.append(
            {
                "id": _uid(),
                "material_id": mat_id,
                "target_timerange": _timerange(sub.start_us, sub.duration_us),
                "visible": True,
            }
        )
    return materials, segments
