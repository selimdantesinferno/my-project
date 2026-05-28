"""링크에서 본문 텍스트를 추출합니다.

글감으로 URL만 주어졌을 때, 페이지의 핵심 텍스트를 긁어와
AI 프롬프트의 재료로 사용합니다.
"""
from __future__ import annotations

import httpx
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    )
}


async def fetch_url_text(url: str, max_chars: int = 8000) -> str:
    """주어진 URL의 본문 텍스트를 추출해 반환합니다."""
    async with httpx.AsyncClient(
        headers=_HEADERS, follow_redirects=True, timeout=20.0
    ) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        html = resp.text

    soup = BeautifulSoup(html, "html.parser")

    # 불필요한 태그 제거
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    # 본문 후보: article > main > body 순
    container = soup.find("article") or soup.find("main") or soup.body or soup
    text = container.get_text(separator="\n", strip=True)

    # 빈 줄 정리
    lines = [ln for ln in (l.strip() for l in text.splitlines()) if ln]
    body = "\n".join(lines)

    combined = (f"[제목] {title}\n\n{body}" if title else body)
    return combined[:max_chars]
