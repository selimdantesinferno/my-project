"""FastAPI 앱: 웹 UI 제공 + 카드뉴스 생성/렌더/업로드 API."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import ai, bulk, fetch, meta, render, scheduler, store, timeutil, video
from .config import OUTPUT_DIR, WEB_DIR, settings
from .templates import TEMPLATES, TONES


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.stop()


app = FastAPI(title="카드뉴스 자동화 공장", lifespan=lifespan)

# 생성된 이미지를 공개 URL로 제공 (Meta API가 가져갈 경로)
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")


class GenerateRequest(BaseModel):
    source_text: str = ""
    url: str = ""
    slide_count: int = 7
    template: str = "toss"
    tone: str = "blue"
    account: str = ""
    prompt: str = ""
    provider: str | None = None  # openai | gemini


class GenerateResponse(BaseModel):
    slides: list[dict]
    caption: str
    hashtags: list[str]
    images: list[str]       # 파일명
    image_urls: list[str]   # 공개 URL


class UploadRequest(BaseModel):
    targets: list[str]      # ["instagram", "threads"]
    images: list[str]       # 파일명
    caption: str = ""
    hashtags: list[str] = []
    first_comment: str = ""


class ScheduleRequest(BaseModel):
    targets: list[str]
    images: list[str]
    caption: str = ""
    hashtags: list[str] = []
    first_comment: str = ""
    scheduled_at: str = ""  # 'YYYY-MM-DD HH:MM' (설정 시간대 기준) 또는 ISO
    label: str = ""


class VideoRequest(BaseModel):
    targets: list[str]      # instagram, threads, youtube, tiktok
    video_url: str          # 구글 드라이브 공유 링크 또는 직접 URL
    title: str = ""
    description: str = ""
    first_comment: str = ""
    privacy: str = "private"           # youtube: public|unlisted|private
    overrides: dict = {}               # 플랫폼별 개별 설정
    scheduled_at: str = ""             # 비우면 즉시 발행
    label: str = ""


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse((WEB_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/api/options")
async def options() -> dict:
    """UI 드롭다운용 템플릿/톤/제공자 목록."""
    return {
        "templates": [{"value": k, "label": v["label"], "description": v["description"]}
                      for k, v in TEMPLATES.items()],
        "tones": list(TONES.keys()),
        "providers": ["openai", "gemini"],
        "default_provider": settings.ai_provider,
        "default_prompt": ai.DEFAULT_PROMPT,
        "video_platforms": ["instagram", "threads", "youtube", "tiktok"],
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:
    # 1) 글감 확보 (직접 입력 본문 + URL 본문)
    source = req.source_text.strip()
    if req.url.strip():
        try:
            fetched = await fetch.fetch_url_text(req.url.strip())
            source = f"{source}\n\n{fetched}".strip() if source else fetched
        except Exception as e:
            raise HTTPException(400, f"링크에서 본문을 가져오지 못했습니다: {e}")
    if not source:
        raise HTTPException(400, "글감(본문 또는 링크)을 입력하세요.")

    # 2) AI 생성
    try:
        data = await ai.generate_slides(
            source=source,
            slide_count=max(2, min(req.slide_count, 12)),
            account=req.account,
            user_prompt=req.prompt,
            provider=req.provider,
        )
    except Exception as e:
        raise HTTPException(502, f"AI 생성 실패: {e}")

    # 3) 렌더링
    try:
        images = render.render_deck(
            slides=data["slides"], template=req.template,
            tone=req.tone, account=req.account,
        )
    except Exception as e:
        raise HTTPException(500, f"이미지 렌더링 실패: {e}")

    return GenerateResponse(
        slides=data["slides"],
        caption=data.get("caption", ""),
        hashtags=data.get("hashtags", []),
        images=images,
        image_urls=[f"{settings.base_url}/output/{n}" for n in images],
    )


@app.post("/api/upload")
async def upload(req: UploadRequest) -> dict:
    if not req.targets:
        raise HTTPException(400, "업로드 대상(targets)을 지정하세요.")
    if not req.images:
        raise HTTPException(400, "업로드할 이미지가 없습니다.")
    try:
        results = await meta.upload(req.targets, req.images, req.caption,
                                    req.hashtags, req.first_comment)
    except meta.UploadError as e:
        raise HTTPException(502, str(e))
    return {"results": results}


@app.post("/api/schedule")
async def schedule(req: ScheduleRequest) -> dict:
    """예약 발행 잡 등록. scheduled_at 이 비면 즉시 발행 대상으로 등록."""
    if not req.targets:
        raise HTTPException(400, "업로드 대상(targets)을 지정하세요.")
    if not req.images:
        raise HTTPException(400, "발행할 이미지가 없습니다.")
    try:
        scheduled_at = timeutil.to_utc_iso(req.scheduled_at)
    except ValueError as e:
        raise HTTPException(400, str(e))
    job = await store.add_job(
        scheduled_at=scheduled_at, targets=req.targets, images=req.images,
        caption=req.caption, hashtags=req.hashtags,
        first_comment=req.first_comment, label=req.label,
    )
    return {"job": job}


@app.post("/api/video")
async def video_upload(req: VideoRequest) -> dict:
    """영상 업로드. scheduled_at 이 있으면 예약, 없으면 즉시 발행."""
    if not req.targets:
        raise HTTPException(400, "업로드 대상(targets)을 지정하세요.")
    if not req.video_url.strip():
        raise HTTPException(400, "영상 URL(구글 드라이브 링크)을 입력하세요.")

    if req.scheduled_at.strip():
        try:
            scheduled_at = timeutil.to_utc_iso(req.scheduled_at)
        except ValueError as e:
            raise HTTPException(400, str(e))
        job = await store.add_video_job(
            scheduled_at=scheduled_at, targets=req.targets, video_url=req.video_url,
            title=req.title, description=req.description,
            first_comment=req.first_comment, privacy=req.privacy,
            overrides=req.overrides, label=req.label or req.title,
        )
        return {"scheduled": True, "job": job}

    try:
        results = await video.upload_video(
            targets=req.targets, video_url=req.video_url, title=req.title,
            description=req.description, first_comment=req.first_comment,
            privacy=req.privacy, overrides=req.overrides,
        )
    except video.UploadError as e:
        raise HTTPException(502, str(e))
    return {"scheduled": False, "results": results}


@app.get("/api/jobs")
async def jobs() -> dict:
    return {"jobs": await store.list_jobs()}


@app.post("/api/jobs/{job_id}/cancel")
async def cancel(job_id: str) -> dict:
    ok = await store.cancel_job(job_id)
    if not ok:
        raise HTTPException(404, "잡을 찾을 수 없습니다.")
    return {"ok": True}


@app.post("/api/bulk")
async def bulk_upload(file: UploadFile = File(...)) -> dict:
    """엑셀(.xlsx)/CSV 대량 업로드: 행마다 생성 후 예약 잡 등록."""
    content = await file.read()
    try:
        return await bulk.process(file.filename or "upload.csv", content)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"대량 업로드 처리 실패: {e}")


@app.get("/api/bulk/sample")
async def bulk_sample(kind: str = "carousel") -> PlainTextResponse:
    if kind == "video":
        body, fname = bulk.video_sample_csv(), "bulk_video_sample.csv"
    else:
        body, fname = bulk.sample_csv(), "bulk_sample.csv"
    return PlainTextResponse(
        body,
        headers={"Content-Disposition": f"attachment; filename={fname}"},
        media_type="text/csv",
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "base_url": settings.base_url,
            "timezone": settings.timezone}
