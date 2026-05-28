"""인스타그램 & 스레드 캐러셀 자동 업로드.

두 API 모두 '공개적으로 접근 가능한 이미지 URL'을 요구하므로,
이미지는 PUBLIC_BASE_URL/output/<file> 로 제공되어야 합니다.

업로드 절차(둘 다 3단계):
  1) 각 이미지를 carousel item 컨테이너로 생성
  2) 자식들을 묶어 CAROUSEL 컨테이너 생성
  3) publish
"""
from __future__ import annotations

import asyncio

import httpx

from .config import settings

GRAPH = "https://graph.facebook.com/v21.0"
THREADS = "https://graph.threads.net/v1.0"


class UploadError(RuntimeError):
    pass


def _image_urls(filenames: list[str]) -> list[str]:
    return [f"{settings.base_url}/output/{name}" for name in filenames]


async def _post(client: httpx.AsyncClient, url: str, params: dict) -> dict:
    resp = await client.post(url, params=params)
    data = resp.json() if resp.content else {}
    if resp.status_code >= 400 or "error" in data:
        msg = data.get("error", {}).get("message", resp.text)
        raise UploadError(f"{url} 실패: {msg}")
    return data


# ---------- Instagram ----------
async def upload_instagram(filenames: list[str], caption: str,
                           first_comment: str = "") -> dict:
    if not (settings.ig_user_id and settings.ig_access_token):
        raise UploadError("Instagram 자격정보(IG_USER_ID/IG_ACCESS_TOKEN)가 없습니다.")
    token = settings.ig_access_token
    uid = settings.ig_user_id
    urls = _image_urls(filenames)

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1) 자식 컨테이너
        child_ids = []
        for url in urls:
            data = await _post(client, f"{GRAPH}/{uid}/media", {
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": token,
            })
            child_ids.append(data["id"])

        # 2) 캐러셀 컨테이너
        container = await _post(client, f"{GRAPH}/{uid}/media", {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
            "access_token": token,
        })

        # 3) 발행
        result = await _post(client, f"{GRAPH}/{uid}/media_publish", {
            "creation_id": container["id"],
            "access_token": token,
        })
        media_id = result.get("id")

        # 4) 고정(첫) 댓글
        comment_id = None
        if first_comment and media_id:
            c = await _post(client, f"{GRAPH}/{media_id}/comments", {
                "message": first_comment,
                "access_token": token,
            })
            comment_id = c.get("id")

    return {"platform": "instagram", "id": media_id,
            "children": child_ids, "comment_id": comment_id}


# ---------- Threads ----------
async def upload_threads(filenames: list[str], text: str,
                         first_comment: str = "") -> dict:
    if not (settings.threads_user_id and settings.threads_access_token):
        raise UploadError("Threads 자격정보(THREADS_USER_ID/THREADS_ACCESS_TOKEN)가 없습니다.")
    token = settings.threads_access_token
    uid = settings.threads_user_id
    urls = _image_urls(filenames)

    async with httpx.AsyncClient(timeout=60.0) as client:
        child_ids = []
        for url in urls:
            data = await _post(client, f"{THREADS}/{uid}/threads", {
                "media_type": "IMAGE",
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": token,
            })
            child_ids.append(data["id"])

        container = await _post(client, f"{THREADS}/{uid}/threads", {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "text": text,
            "access_token": token,
        })

        # 스레드는 발행 전 짧은 처리 시간이 필요할 수 있음
        await asyncio.sleep(2)
        result = await _post(client, f"{THREADS}/{uid}/threads_publish", {
            "creation_id": container["id"],
            "access_token": token,
        })
        thread_id = result.get("id")

        # 고정(첫) 댓글 = 본인 글에 대한 답글
        comment_id = None
        if first_comment and thread_id:
            reply_c = await _post(client, f"{THREADS}/{uid}/threads", {
                "media_type": "TEXT",
                "text": first_comment,
                "reply_to_id": thread_id,
                "access_token": token,
            })
            await asyncio.sleep(2)
            rp = await _post(client, f"{THREADS}/{uid}/threads_publish", {
                "creation_id": reply_c["id"],
                "access_token": token,
            })
            comment_id = rp.get("id")

    return {"platform": "threads", "id": thread_id,
            "children": child_ids, "comment_id": comment_id}


async def upload(targets: list[str], filenames: list[str], caption: str,
                 hashtags: list[str], first_comment: str = "") -> list[dict]:
    """대상 플랫폼들에 업로드. targets: ['instagram','threads'] 중 일부."""
    tag_str = " ".join(hashtags)
    full_caption = f"{caption}\n\n{tag_str}".strip()
    results = []
    for t in targets:
        if t == "instagram":
            results.append(await upload_instagram(filenames, full_caption, first_comment))
        elif t == "threads":
            results.append(await upload_threads(filenames, full_caption, first_comment))
    return results
