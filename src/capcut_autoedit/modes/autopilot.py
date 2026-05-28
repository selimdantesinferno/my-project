"""모드 2 — 완전자동 모드 (Autopilot Mode). [미구현]

영상(또는 주제) → 분석 → 대본 → TTS 내레이션 → BGM → 효과 자막
→ 컷 편집 → 썸네일 → (선택) 자동 업로드 → '완성된 새 영상'.

편집 모드와 달리 결과물은 '편집 가능한 프로젝트'가 아니라 '바로 업로드
가능한 완성 영상'을 지향한다.

[로드맵 — 각 단계가 독립 서브 프로젝트라 순차적으로 붙인다]
  1) 대본 4종 변주 생성 (욕망/본능/감동/분노)            : LLM 프롬프트 확장
  2) TTS 내레이션 (ElevenLabs / TypeCast 등)             : 외부 API 어댑터
  3) BGM 자동 선택 / 믹싱                                : 라이선스 안전 소스 풀
  4) 효과 자막(감정 강조) + SRT 출력                     : 자막 스타일 엔진
  5) 썸네일 자동 생성                                    : 이미지 생성 + 텍스트 합성
  6) 최종 렌더링 (ffmpeg)                                : 컷 + 음성 + BGM + 자막
  7) (선택) 자동 업로드                                  : YouTube Data API

[현재 상태]
편집 모드(`draft`)의 빌더가 실제 CapCut 샘플로 검증된 뒤 1단계부터 착수한다.
"""

from __future__ import annotations


def run(*args, **kwargs):
    raise NotImplementedError(
        "완전자동 모드는 아직 구현되지 않았습니다. "
        "현재는 편집 모드(`capcut-autoedit draft`)만 사용 가능합니다. "
        "로드맵은 src/capcut_autoedit/modes/autopilot.py 의 docstring 참고."
    )
