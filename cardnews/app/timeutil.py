"""예약 시각 파싱 유틸. 입력은 설정된 시간대 기준, 저장은 UTC ISO."""
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from .config import settings


def _local_tz() -> ZoneInfo:
    try:
        return ZoneInfo(settings.timezone)
    except Exception:
        return ZoneInfo("UTC")


def to_utc_iso(value: str | None) -> str:
    """'YYYY-MM-DD HH:MM' 또는 ISO 문자열 → UTC ISO. 비어있으면 지금(UTC)."""
    if not value or not value.strip():
        return datetime.now(timezone.utc).isoformat()

    text = value.strip().replace("T", " ")
    dt = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S%z"):
        try:
            dt = datetime.strptime(text, fmt)
            break
        except ValueError:
            continue
    if dt is None:
        try:
            dt = datetime.fromisoformat(value.strip())
        except ValueError as e:
            raise ValueError(f"예약 시각 형식 오류: {value!r} (예: 2026-05-28 14:30)") from e

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_local_tz())
    return dt.astimezone(timezone.utc).isoformat()
