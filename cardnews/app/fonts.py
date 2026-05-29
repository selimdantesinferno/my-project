"""한국어 폰트(Noto Sans KR) 자동 준비.

레포에 폰트 바이너리를 포함하지 않고, 최초 실행 시 필요한 폰트를
내려받아 assets/fonts 에 저장합니다.
"""
from __future__ import annotations

import urllib.request

from .config import FONTS_DIR

_BASE = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/KR"
_FONTS = {
    "NotoSansKR-Regular.ttf": f"{_BASE}/NotoSansKR-Regular.otf",
    "NotoSansKR-Bold.ttf": f"{_BASE}/NotoSansKR-Bold.otf",
    "NotoSansKR-Black.ttf": f"{_BASE}/NotoSansKR-Black.otf",
}


def ensure_fonts() -> None:
    """필요한 폰트가 없으면 내려받습니다."""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in _FONTS.items():
        dest = FONTS_DIR / name
        if dest.exists() and dest.stat().st_size > 0:
            continue
        try:
            urllib.request.urlretrieve(url, dest)  # noqa: S310
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(
                f"폰트 다운로드 실패({name}). 인터넷 연결을 확인하거나 "
                f"수동으로 {url} 를 받아 {dest} 에 저장하세요."
            ) from e


if __name__ == "__main__":
    ensure_fonts()
    print("폰트 준비 완료:", FONTS_DIR)
