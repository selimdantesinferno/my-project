"""슬라이드 데이터를 1080x1080 PNG 카드 이미지로 렌더링합니다.

템플릿(magazine/toss) × 색상 톤(palette) 조합으로 디자인이 결정됩니다.
한국어 줄바꿈을 픽셀 폭 기준으로 처리합니다.
"""
from __future__ import annotations

import uuid
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import FONTS_DIR, OUTPUT_DIR
from .templates import Palette, get_palette, get_template

SIZE = 1080  # 인스타/스레드 정사각 권장
MARGIN = 96

_REGULAR = FONTS_DIR / "NotoSansKR-Regular.ttf"
_BOLD = FONTS_DIR / "NotoSansKR-Bold.ttf"
_BLACK = FONTS_DIR / "NotoSansKR-Black.ttf"


def _font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    """픽셀 폭 기준 줄바꿈. 한국어는 어절 단위, 길면 글자 단위로 쪼갭니다."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split(" ")
        cur = ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=font) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # 단어 자체가 너무 길면 글자 단위로 분할
                if draw.textlength(word, font=font) > max_width:
                    piece = ""
                    for ch in word:
                        if draw.textlength(piece + ch, font=font) <= max_width:
                            piece += ch
                        else:
                            lines.append(piece)
                            piece = ch
                    cur = piece
                else:
                    cur = word
        if cur:
            lines.append(cur)
    return lines


def _draw_block(
    draw: ImageDraw.ImageDraw, text: str, font, fill, x: int, y: int,
    max_width: int, line_gap: float = 1.35, align: str = "left",
) -> int:
    """여러 줄 텍스트를 그리고 다음 y 좌표를 반환합니다."""
    lines = _wrap(draw, text, font, max_width)
    ascent, descent = font.getmetrics()
    line_h = int((ascent + descent) * line_gap)
    for line in lines:
        if line:
            if align == "center":
                w = draw.textlength(line, font=font)
                draw.text(((SIZE - w) / 2, y), line, font=font, fill=fill)
            else:
                draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def _footer(draw: ImageDraw.ImageDraw, account: str, pal: Palette,
            index: int, total: int) -> None:
    """하단에 계정명과 페이지 표시."""
    f = _font(_REGULAR, 30)
    if account:
        draw.text((MARGIN, SIZE - MARGIN + 4), account, font=f, fill=pal.sub)
    page = f"{index + 1} / {total}"
    w = draw.textlength(page, font=f)
    draw.text((SIZE - MARGIN - w, SIZE - MARGIN + 4), page, font=f, fill=pal.sub)


def _render_toss(slide: dict, pal: Palette, account: str,
                 index: int, total: int) -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), pal.bg)
    draw = ImageDraw.Draw(img)
    stype = slide.get("type", "content")
    title = slide.get("title", "")
    body = slide.get("body", "")
    highlight = slide.get("highlight", "")
    max_w = SIZE - MARGIN * 2

    if stype == "stat" and highlight:
        # 큰 숫자 강조
        big = _font(_BLACK, 200)
        bw = draw.textlength(highlight, font=big)
        draw.text(((SIZE - bw) / 2, 300), highlight, font=big, fill=pal.accent)
        y = _draw_block(draw, title, _font(_BOLD, 56), pal.fg,
                        MARGIN, 560, max_w, align="center")
        if body:
            _draw_block(draw, body, _font(_REGULAR, 38), pal.sub,
                        MARGIN, y + 20, max_w, align="center")
    elif stype == "cover":
        # 상단 강조 점 + 큰 제목
        draw.rectangle([MARGIN, 300, MARGIN + 70, 314], fill=pal.accent)
        y = _draw_block(draw, title, _font(_BLACK, 84), pal.fg,
                        MARGIN, 360, max_w, line_gap=1.2)
        if body:
            _draw_block(draw, body, _font(_REGULAR, 40), pal.sub,
                        MARGIN, y + 30, max_w)
    else:
        y = _draw_block(draw, title, _font(_BOLD, 64), pal.fg,
                        MARGIN, 320, max_w, line_gap=1.25)
        if body:
            _draw_block(draw, body, _font(_REGULAR, 42), pal.sub,
                        MARGIN, y + 30, max_w)

    _footer(draw, account, pal, index, total)
    return img


def _render_magazine(slide: dict, pal: Palette, account: str,
                     index: int, total: int) -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), pal.bg)
    draw = ImageDraw.Draw(img)
    stype = slide.get("type", "content")
    title = slide.get("title", "")
    body = slide.get("body", "")
    highlight = slide.get("highlight", "")
    max_w = SIZE - MARGIN * 2

    # 상단 라벨 바
    label = {"cover": "CARD NEWS", "stat": "KEY DATA"}.get(stype, "INSIGHT")
    lf = _font(_BOLD, 30)
    lw = draw.textlength(label, font=lf)
    draw.rectangle([MARGIN, 140, MARGIN + lw + 40, 200], fill=pal.accent)
    draw.text((MARGIN + 20, 150), label, font=lf, fill=pal.accent_fg)

    if stype == "stat" and highlight:
        big = _font(_BLACK, 180)
        draw.text((MARGIN, 320), highlight, font=big, fill=pal.accent)
        y = _draw_block(draw, title, _font(_BOLD, 60), pal.fg, MARGIN, 560, max_w)
        if body:
            _draw_block(draw, body, _font(_REGULAR, 38), pal.sub, MARGIN, y + 20, max_w)
    else:
        size = 80 if stype == "cover" else 60
        y = _draw_block(draw, title, _font(_BLACK if stype == "cover" else _BOLD, size),
                        pal.fg, MARGIN, 300, max_w, line_gap=1.2)
        # 구분선
        draw.rectangle([MARGIN, y + 24, MARGIN + 120, y + 30], fill=pal.accent)
        if body:
            _draw_block(draw, body, _font(_REGULAR, 40), pal.sub, MARGIN, y + 64, max_w)

    _footer(draw, account, pal, index, total)
    return img


_RENDERERS = {"toss": _render_toss, "magazine": _render_magazine}


def render_card(slide: dict, template: str, tone: str, account: str,
                index: int, total: int) -> Image.Image:
    pal = get_palette(tone)
    style = get_template(template)["style"]
    renderer = _RENDERERS.get(style, _render_toss)
    return renderer(slide, pal, account, index, total)


def render_deck(slides: list[dict], template: str, tone: str,
                account: str) -> list[str]:
    """슬라이드 전체를 렌더링하고 저장된 파일 경로 목록을 반환합니다."""
    batch = uuid.uuid4().hex[:10]
    total = len(slides)
    paths: list[str] = []
    for i, slide in enumerate(slides):
        img = render_card(slide, template, tone, account, i, total)
        fname = f"{batch}_{i:02d}.png"
        fpath = OUTPUT_DIR / fname
        img.save(fpath, "PNG")
        paths.append(fname)
    return paths
