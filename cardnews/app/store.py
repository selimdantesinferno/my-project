"""예약 발행 잡(job) 저장소. JSON 파일 기반의 단순 저장소입니다."""
from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import BASE_DIR

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
JOBS_FILE = DATA_DIR / "jobs.json"

_lock = asyncio.Lock()


def _read() -> list[dict]:
    if not JOBS_FILE.exists():
        return []
    try:
        return json.loads(JOBS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _write(jobs: list[dict]) -> None:
    JOBS_FILE.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def add_job(*, scheduled_at: str, targets: list[str], images: list[str],
                  caption: str, hashtags: list[str], first_comment: str = "",
                  label: str = "") -> dict:
    """예약 잡 추가. scheduled_at 은 ISO8601(UTC) 문자열."""
    job = {
        "id": uuid.uuid4().hex[:12],
        "status": "scheduled",
        "label": label,
        "scheduled_at": scheduled_at,
        "targets": targets,
        "images": images,
        "caption": caption,
        "hashtags": hashtags,
        "first_comment": first_comment,
        "created_at": _now_iso(),
        "result": None,
        "error": None,
    }
    async with _lock:
        jobs = _read()
        jobs.append(job)
        _write(jobs)
    return job


async def list_jobs() -> list[dict]:
    async with _lock:
        return sorted(_read(), key=lambda j: j.get("scheduled_at", ""))


async def update_job(job_id: str, **fields) -> dict | None:
    async with _lock:
        jobs = _read()
        for job in jobs:
            if job["id"] == job_id:
                job.update(fields)
                _write(jobs)
                return job
    return None


async def cancel_job(job_id: str) -> bool:
    job = await update_job(job_id, status="canceled")
    return job is not None and job["status"] == "canceled"


async def due_jobs() -> list[dict]:
    """발행 시각이 지난 'scheduled' 잡들을 반환합니다."""
    now = datetime.now(timezone.utc)
    out = []
    for job in await list_jobs():
        if job["status"] != "scheduled":
            continue
        try:
            sched = datetime.fromisoformat(job["scheduled_at"])
        except (ValueError, KeyError):
            continue
        if sched.tzinfo is None:
            sched = sched.replace(tzinfo=timezone.utc)
        if sched <= now:
            out.append(job)
    return out
