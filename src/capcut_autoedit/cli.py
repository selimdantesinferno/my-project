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
@click.argument("source", required=False)
@click.option("--out", "out_dir", required=True, help="출력 폴더 경로")
@click.option(
    "--style",
    "subtitle_style",
    type=click.Choice(["plain", "shorts-ko"]),
    default="plain",
    show_default=True,
    help="자막 스타일. shorts-ko는 한국어 Shorts 내레이션 어미/구두점 규칙 적용",
)
@click.option(
    "--fast",
    is_flag=True,
    default=False,
    help="ffmpeg 스트림 카피로 빠르게 자르기(키프레임에 스냅됨). 기본은 정밀 재인코딩",
)
@click.option(
    "--from-plan",
    "from_plan",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="기존 edit_plan.json 으로 Gemini 분석을 건너뛰고 export만 실행",
)
def draft(
    source: str | None,
    out_dir: str,
    subtitle_style: str,
    fast: bool,
    from_plan: str | None,
) -> None:
    """[모드 1] 영상에서 컷 클립 + SRT 자막 번들을 생성한다.

    SOURCE 는 로컬 영상 파일 경로 또는 유튜브 링크.
    --from-plan 사용 시 SOURCE 생략 가능 (plan 내 source_path 사용).
    결과 폴더의 clip_*.mp4 와 subtitles.srt 를 CapCut 등 편집기로 드래그해 사용.
    """
    if not source and not from_plan:
        raise click.UsageError("SOURCE 또는 --from-plan 중 하나는 필요합니다")
    out = draft_mode.run(
        source or "",
        out_dir,
        subtitle_style=subtitle_style,
        fast=fast,
        from_plan=from_plan,
    )
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
