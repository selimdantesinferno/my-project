"""명령줄에서 카드뉴스를 생성(+선택적 업로드)하는 헤드리스 도구.

예)
  python cli.py --text "글감..." --slides 7 --template toss --tone blue --account "@me"
  python cli.py --url https://example.com --upload instagram threads
"""
from __future__ import annotations

import argparse
import asyncio

from app import ai, fetch, meta, render
from app.config import OUTPUT_DIR


async def run(args: argparse.Namespace) -> None:
    source = (args.text or "").strip()
    if args.url:
        source = (source + "\n\n" + await fetch.fetch_url_text(args.url)).strip()
    if not source:
        raise SystemExit("글감(--text 또는 --url)을 입력하세요.")

    print("• AI 생성 중...")
    data = await ai.generate_slides(
        source=source, slide_count=args.slides, account=args.account,
        user_prompt=args.prompt or "", provider=args.provider,
    )
    print(f"• 슬라이드 {len(data['slides'])}장, 렌더링 중...")
    images = render.render_deck(data["slides"], args.template, args.tone, args.account)
    for n in images:
        print("   ", OUTPUT_DIR / n)
    print("• 캡션:", data["caption"])
    print("• 해시태그:", " ".join(data["hashtags"]))

    if args.upload:
        print(f"• 업로드: {args.upload}")
        results = await meta.upload(args.upload, images, data["caption"], data["hashtags"])
        for r in results:
            print(f"   {r['platform']}: {r['id']}")


def main() -> None:
    p = argparse.ArgumentParser(description="카드뉴스 자동화 CLI")
    p.add_argument("--text", help="글감 본문")
    p.add_argument("--url", help="글감으로 쓸 링크")
    p.add_argument("--slides", type=int, default=7)
    p.add_argument("--template", default="toss")
    p.add_argument("--tone", default="blue")
    p.add_argument("--account", default="")
    p.add_argument("--prompt", default="")
    p.add_argument("--provider", choices=["openai", "gemini"])
    p.add_argument("--upload", nargs="*", choices=["instagram", "threads"], default=[])
    asyncio.run(run(p.parse_args()))


if __name__ == "__main__":
    main()
