"""구글 드라이브 영상 연동.

드라이브 공유 링크('링크가 있는 모든 사용자')를 API가 받을 수 있는
직접 다운로드 URL로 변환하고, 필요 시 파일 바이트를 내려받습니다.
"""
from __future__ import annotations

import re

import httpx

_ID_PATTERNS = [
    r"/file/d/([a-zA-Z0-9_-]+)",      # .../file/d/<id>/view
    r"[?&]id=([a-zA-Z0-9_-]+)",        # ...uc?id=<id>
    r"/d/([a-zA-Z0-9_-]+)",            # 단축형
]


def extract_file_id(url: str) -> str | None:
    for pat in _ID_PATTERNS:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def direct_download_url(url: str) -> str:
    """드라이브 공유 링크 → 직접 다운로드 URL. 드라이브가 아니면 원본 반환."""
    fid = extract_file_id(url)
    if fid:
        return f"https://drive.google.com/uc?export=download&id={fid}"
    return url


async def download(url: str, max_bytes: int = 512 * 1024 * 1024) -> tuple[bytes, str]:
    """URL(드라이브 공유 링크 가능)에서 영상 바이트를 내려받습니다.

    드라이브 대용량 파일의 바이러스 검사 확인 페이지를 우회합니다.
    반환: (bytes, content_type)
    """
    dl = direct_download_url(url)
    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        resp = await client.get(dl)
        # 대용량 파일은 확인 토큰이 필요할 수 있음
        if "text/html" in resp.headers.get("content-type", ""):
            m = re.search(r"confirm=([0-9A-Za-z_-]+)", resp.text)
            token = m.group(1) if m else None
            fid = extract_file_id(url)
            if token and fid:
                resp = await client.get(
                    "https://drive.google.com/uc?export=download",
                    params={"id": fid, "confirm": token},
                )
        resp.raise_for_status()
        content = resp.content
        if len(content) > max_bytes:
            raise ValueError("영상 파일이 너무 큽니다.")
        ctype = resp.headers.get("content-type", "video/mp4")
        return content, ctype
