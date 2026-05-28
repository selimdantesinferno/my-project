"""자막을 표준 SRT 텍스트로 변환."""

from __future__ import annotations

from ..models import Subtitle


def to_srt(subtitles: list[Subtitle]) -> str:
    """SRT(SubRip) 포맷 문자열 생성."""
    blocks: list[str] = []
    for i, s in enumerate(subtitles, start=1):
        blocks.append(
            f"{i}\n{_ts(s.start_us)} --> {_ts(s.end_us)}\n{s.text}\n"
        )
    return "\n".join(blocks)


def _ts(us: int) -> str:
    """마이크로초 → 'HH:MM:SS,mmm' (SRT 시간 표기)."""
    if us < 0:
        us = 0
    ms_total = us // 1000
    h, ms_total = divmod(ms_total, 3_600_000)
    m, ms_total = divmod(ms_total, 60_000)
    s, ms = divmod(ms_total, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
