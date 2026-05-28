"""영상 파일을 여러 SNS에 업로드합니다.

지원:
  - Instagram 릴스 (Graph API, 공개 video_url)
  - Threads 동영상 (Threads API, 공개 video_url)
  - YouTube (Data API v3, OAuth2 / 파일 바이트 업로드)
  - TikTok  → 현재 미연동 (영상 시연과 동일). 명확한 안내 에러 반환.

Instagram/Threads 는 영상 처리(인코딩) 시간이 필요하므로
컨테이너 상태가 FINISHED 가 될 때까지 폴링 후 발행합니다.
"""
from __future__ import annotations

import asyncio
import io

import httpx

from . import drive
from .config import settings
from .meta import GRAPH, THREADS, UploadError, _post


async def _poll_ready(client: httpx.AsyncClient, base: str, container_id: str,
                      token: str, tries: int = 30, delay: float = 4.0) -> None:
    """미디어 컨테이너가 발행 가능(FINISHED) 상태가 될 때까지 대기."""
    for _ in range(tries):
        r = await client.get(f"{base}/{container_id}",
                             params={"fields": "status_code,status", "access_token": token})
        data = r.json()
        code = data.get("status_code") or data.get("status")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise UploadError(f"영상 처리 실패: {data}")
        await asyncio.sleep(delay)
    raise UploadError("영상 처리 시간이 초과되었습니다.")


# ---------- Instagram 릴스 ----------
async def upload_instagram_reel(video_url: str, caption: str,
                                first_comment: str = "") -> dict:
    if not (settings.ig_user_id and settings.ig_access_token):
        raise UploadError("Instagram 자격정보(IG_USER_ID/IG_ACCESS_TOKEN)가 없습니다.")
    token, uid = settings.ig_access_token, settings.ig_user_id
    src = drive.direct_download_url(video_url)
    async with httpx.AsyncClient(timeout=120.0) as client:
        container = await _post(client, f"{GRAPH}/{uid}/media", {
            "media_type": "REELS", "video_url": src,
            "caption": caption, "access_token": token,
        })
        await _poll_ready(client, GRAPH, container["id"], token)
        result = await _post(client, f"{GRAPH}/{uid}/media_publish", {
            "creation_id": container["id"], "access_token": token,
        })
        media_id = result.get("id")
        comment_id = None
        if first_comment and media_id:
            c = await _post(client, f"{GRAPH}/{media_id}/comments",
                            {"message": first_comment, "access_token": token})
            comment_id = c.get("id")
    return {"platform": "instagram", "id": media_id, "comment_id": comment_id}


# ---------- Threads 동영상 ----------
async def upload_threads_video(video_url: str, text: str,
                               first_comment: str = "") -> dict:
    if not (settings.threads_user_id and settings.threads_access_token):
        raise UploadError("Threads 자격정보가 없습니다.")
    token, uid = settings.threads_access_token, settings.threads_user_id
    src = drive.direct_download_url(video_url)
    async with httpx.AsyncClient(timeout=120.0) as client:
        container = await _post(client, f"{THREADS}/{uid}/threads", {
            "media_type": "VIDEO", "video_url": src,
            "text": text, "access_token": token,
        })
        await _poll_ready(client, THREADS, container["id"], token)
        result = await _post(client, f"{THREADS}/{uid}/threads_publish", {
            "creation_id": container["id"], "access_token": token,
        })
        thread_id = result.get("id")
        comment_id = None
        if first_comment and thread_id:
            reply = await _post(client, f"{THREADS}/{uid}/threads", {
                "media_type": "TEXT", "text": first_comment,
                "reply_to_id": thread_id, "access_token": token,
            })
            await asyncio.sleep(2)
            rp = await _post(client, f"{THREADS}/{uid}/threads_publish",
                             {"creation_id": reply["id"], "access_token": token})
            comment_id = rp.get("id")
    return {"platform": "threads", "id": thread_id, "comment_id": comment_id}


# ---------- YouTube ----------
def _youtube_client():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not (settings.youtube_client_id and settings.youtube_client_secret
            and settings.youtube_refresh_token):
        raise UploadError("YouTube 자격정보(CLIENT_ID/SECRET/REFRESH_TOKEN)가 없습니다.")
    creds = Credentials(
        token=None,
        refresh_token=settings.youtube_refresh_token,
        client_id=settings.youtube_client_id,
        client_secret=settings.youtube_client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def _youtube_upload_sync(video_bytes: bytes, title: str, description: str,
                         privacy: str) -> dict:
    from googleapiclient.http import MediaIoBaseUpload

    youtube = _youtube_client()
    media = MediaIoBaseUpload(io.BytesIO(video_bytes), mimetype="video/*",
                              chunksize=-1, resumable=True)
    body = {
        "snippet": {"title": title or "업로드", "description": description or ""},
        "status": {"privacyStatus": privacy or "private",
                   "selfDeclaredMadeForKids": False},
    }
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    return {"platform": "youtube", "id": resp.get("id")}


async def upload_youtube(video_url: str, title: str, description: str,
                         privacy: str = "private") -> dict:
    """드라이브 영상을 내려받아 YouTube 에 업로드합니다."""
    content, _ = await drive.download(video_url)
    # google-api-client 는 동기이므로 스레드에서 실행
    return await asyncio.to_thread(
        _youtube_upload_sync, content, title, description, privacy)


# ---------- TikTok (미연동) ----------
async def upload_tiktok(*_args, **_kwargs) -> dict:
    raise UploadError("TikTok 은 아직 연동되지 않았습니다. (추후 TikTok Content Posting API 지원 예정)")


# ---------- 통합 ----------
async def upload_video(*, targets: list[str], video_url: str, title: str = "",
                       description: str = "", first_comment: str = "",
                       privacy: str = "private",
                       overrides: dict | None = None) -> list[dict]:
    """대상 플랫폼별로 영상 업로드. overrides[platform] 로 설명 등 개별 지정 가능."""
    overrides = overrides or {}
    results = []
    for t in targets:
        ov = overrides.get(t, {})
        desc = ov.get("description", description)
        if t == "instagram":
            results.append(await upload_instagram_reel(video_url, desc, first_comment))
        elif t == "threads":
            results.append(await upload_threads_video(video_url, desc, first_comment))
        elif t == "youtube":
            results.append(await upload_youtube(
                video_url, ov.get("title", title), desc, ov.get("privacy", privacy)))
        elif t == "tiktok":
            results.append(await upload_tiktok())
    return results
