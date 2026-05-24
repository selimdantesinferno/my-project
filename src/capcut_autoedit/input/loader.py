"""입력 처리: 로컬 영상 파일 또는 유튜브 링크 -> 로컬 파일 경로.

위치: 백엔드. 유튜브 링크면 yt-dlp 로 내려받아 로컬 경로를 돌려준다.
"""

from __future__ import annotations

import re
from pathlib import Path

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def is_url(source: str) -> bool:
    return bool(_URL_RE.match(source.strip()))


def resolve_input(source: str, download_dir: str = "downloads") -> Path:
    """입력 소스를 로컬 파일 경로로 정규화한다.

    - 로컬 경로면 존재 확인 후 그대로 반환
    - URL이면 yt-dlp로 다운로드 후 받은 파일 경로 반환
    """
    if is_url(source):
        return _download(source, download_dir)

    path = Path(source).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {source}")
    return path


def _download(url: str, download_dir: str) -> Path:
    # 무거운 의존성이라 사용 시점에만 import
    from yt_dlp import YoutubeDL

    out_dir = Path(download_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best",
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info))
