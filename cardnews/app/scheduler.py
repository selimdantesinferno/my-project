"""예약 발행 백그라운드 스케줄러.

앱 시작 시 루프를 돌며, 발행 시각이 된 잡을 찾아 인스타/스레드에 발행합니다.
"""
from __future__ import annotations

import asyncio
import logging

from . import meta, store, video

log = logging.getLogger("scheduler")

_CHECK_INTERVAL = 20  # 초


async def _publish_job(job: dict) -> None:
    await store.update_job(job["id"], status="publishing")
    try:
        if job.get("kind") == "video":
            results = await video.upload_video(
                targets=job["targets"],
                video_url=job["video_url"],
                title=job.get("title", ""),
                description=job.get("description", ""),
                first_comment=job.get("first_comment", ""),
                privacy=job.get("privacy", "private"),
                overrides=job.get("overrides", {}),
            )
        else:
            results = await meta.upload(
                targets=job["targets"],
                filenames=job["images"],
                caption=job["caption"],
                hashtags=job.get("hashtags", []),
                first_comment=job.get("first_comment", ""),
            )
        await store.update_job(job["id"], status="done", result=results, error=None)
        log.info("발행 완료: %s", job["id"])
    except Exception as e:  # noqa: BLE001 - 잡 단위 격리
        await store.update_job(job["id"], status="failed", error=str(e))
        log.warning("발행 실패: %s (%s)", job["id"], e)


async def _loop() -> None:
    log.info("예약 발행 스케줄러 시작")
    while True:
        try:
            for job in await store.due_jobs():
                await _publish_job(job)
        except Exception as e:  # noqa: BLE001
            log.error("스케줄러 루프 오류: %s", e)
        await asyncio.sleep(_CHECK_INTERVAL)


_task: asyncio.Task | None = None


def start() -> None:
    global _task
    if _task is None or _task.done():
        _task = asyncio.create_task(_loop())


def stop() -> None:
    if _task and not _task.done():
        _task.cancel()
