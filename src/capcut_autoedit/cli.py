"""커맨드라인 진입점."""

from __future__ import annotations

import click

from .pipeline import run


@click.group()
def main() -> None:
    """영상 -> CapCut 편집 프로젝트 자동 생성."""


@main.command()
@click.argument("source")
@click.option("--out", "out_dir", required=True, help="출력할 draft 폴더 경로")
@click.option(
    "--style",
    "subtitle_style",
    type=click.Choice(["plain", "shorts-ko"]),
    default="plain",
    show_default=True,
    help="자막 스타일. shorts-ko는 한국어 Shorts 내레이션 어미/구두점 규칙 적용",
)
def build(source: str, out_dir: str, subtitle_style: str) -> None:
    """SOURCE(로컬 영상 파일 또는 유튜브 링크)로 CapCut draft 폴더를 만든다."""
    draft = run(source, out_dir, subtitle_style=subtitle_style)
    click.echo(f"완료: {draft}")


if __name__ == "__main__":
    main()
