"""FastAPI 앱: 웹 UI 제공 + 카드뉴스 생성/렌더/업로드 API."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import ai, fetch, meta, render
from .config import OUTPUT_DIR, WEB_DIR, settings
from .templates import TEMPLATES, TONES

app = FastAPI(title="카드뉴스 자동화 공장")

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
        results = await meta.upload(req.targets, req.images, req.caption, req.hashtags)
    except meta.UploadError as e:
        raise HTTPException(502, str(e))
    return {"results": results}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "base_url": settings.base_url}
