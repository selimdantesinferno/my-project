"""카드뉴스 템플릿 & 색상 팔레트 정의.

영상에서 본 '매거진', '토스' 스타일을 포함합니다.
색상 톤(blue/light/dark/warm)에 따라 팔레트가 달라집니다.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Palette:
    bg: tuple[int, int, int]
    fg: tuple[int, int, int]          # 본문 글자
    accent: tuple[int, int, int]      # 강조 색
    sub: tuple[int, int, int]         # 보조(설명) 글자
    accent_fg: tuple[int, int, int]   # 강조 배경 위 글자


# 색상 톤 → 팔레트
TONES: dict[str, Palette] = {
    "blue": Palette(
        bg=(15, 32, 64), fg=(255, 255, 255), accent=(64, 156, 255),
        sub=(160, 185, 220), accent_fg=(15, 32, 64),
    ),
    "light": Palette(
        bg=(248, 249, 251), fg=(26, 32, 44), accent=(49, 130, 246),
        sub=(113, 128, 150), accent_fg=(255, 255, 255),
    ),
    "dark": Palette(
        bg=(18, 18, 20), fg=(245, 245, 245), accent=(255, 196, 0),
        sub=(150, 150, 155), accent_fg=(18, 18, 20),
    ),
    "warm": Palette(
        bg=(252, 246, 238), fg=(60, 42, 33), accent=(232, 122, 65),
        sub=(150, 120, 100), accent_fg=(255, 255, 255),
    ),
}

DEFAULT_TONE = "blue"


# 템플릿 메타데이터. style 값은 render.py 가 분기에 사용합니다.
TEMPLATES: dict[str, dict] = {
    "magazine": {
        "label": "매거진",
        "style": "magazine",
        "description": "상단 라벨 바 + 큰 제목, 정보성 콘텐츠에 적합",
    },
    "toss": {
        "label": "토스",
        "style": "toss",
        "description": "여백이 넉넉하고 굵은 한 문장, 임팩트 중심",
    },
}

DEFAULT_TEMPLATE = "toss"


def get_palette(tone: str) -> Palette:
    return TONES.get(tone, TONES[DEFAULT_TONE])


def get_template(name: str) -> dict:
    return TEMPLATES.get(name, TEMPLATES[DEFAULT_TEMPLATE])
