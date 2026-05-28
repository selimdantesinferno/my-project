"""커맨드라인 진입점.

두 가지 모드를 지원한다:
  draft     — 영상 → CapCut 편집 가능 프로젝트 (현재)
  autopilot — 영상 → 완성된 새 영상 (예정)
"""

from __future__ import annotations

import sys

import click

from .modes import autopilot as autopilot_mode
from .modes import draft as draft_mode


@click.group()
def main() -> None:
    """영상 → CapCut 편집 프로젝트 / 완성 영상 자동 생성."""


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
def draft(source: str, out_dir: str, subtitle_style: str) -> None:
    """[모드 1] 영상을 CapCut 편집 가능 프로젝트(draft 폴더)로 변환한다.

    SOURCE 는 로컬 영상 파일 경로 또는 유튜브 링크.
    """
    out = draft_mode.run(source, out_dir, subtitle_style=subtitle_style)
    click.echo(f"완료: {out}")


@main.command()
@click.argument("source")
def autopilot(source: str) -> None:
    """[모드 2] 영상에서 완성된 새 영상을 자동 생성한다. (미구현)

    예정 단계: 분석 → 대본 → TTS → BGM → 효과 자막 → 컷 → 썸네일 → (선택) 업로드.
    """
    try:
        autopilot_mode.run(source)
    except NotImplementedError as e:
        click.echo(str(e), err=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
