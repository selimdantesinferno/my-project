"""분석 단계와 빌더 단계 사이의 데이터 계약.

CapCut은 시간을 마이크로초(1초 = 1_000_000) 단위로 다룬다.
이 모듈의 모든 시간 값도 마이크로초로 통일한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

US_PER_SECOND = 1_000_000


def seconds_to_us(seconds: float) -> int:
    return round(seconds * US_PER_SECOND)


@dataclass
class Cut:
    """원본 영상에서 '남길' 구간 하나.

    source_start_us..source_end_us 는 원본 기준 구간이며,
    타임라인 상의 위치(target)는 빌더가 컷들을 순서대로 이어붙여 계산한다.
    """

    source_start_us: int
    source_end_us: int

    @property
    def duration_us(self) -> int:
        return self.source_end_us - self.source_start_us

    def __post_init__(self) -> None:
        if self.duration_us <= 0:
            raise ValueError(
                f"컷 길이가 0 이하입니다: start={self.source_start_us}, end={self.source_end_us}"
            )


@dataclass
class Subtitle:
    """타임라인 기준(컷이 적용된 최종 결과 기준) 자막 한 줄."""

    start_us: int
    end_us: int
    text: str

    @property
    def duration_us(self) -> int:
        return self.end_us - self.start_us


@dataclass
class EditPlan:
    """Gemini 분석 결과를 정규화한 편집 계획. 빌더의 입력."""

    source_path: str
    width: int
    height: int
    fps: float
    duration_us: int
    cuts: list[Cut] = field(default_factory=list)
    subtitles: list[Subtitle] = field(default_factory=list)

    def total_timeline_us(self) -> int:
        """컷들을 이어붙였을 때의 최종 타임라인 길이."""
        return sum(c.duration_us for c in self.cuts)
