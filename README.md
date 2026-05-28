# capcut-autoedit

영상에서 출발해 두 가지 결과물 중 하나를 만드는 도구입니다.

## 두 가지 모드

| 모드 | 명령 | 결과물 | 상태 |
|---|---|---|---|
| **1. 편집 모드 (Draft)** | `capcut-autoedit draft` | CapCut 데스크톱에서 바로 여는 **편집 가능한 프로젝트** | ✅ 진행 중 |
| **2. 완전자동 모드 (Autopilot)** | `capcut-autoedit autopilot` | TTS·BGM·효과자막·썸네일까지 들어간 **완성 영상** | 🚧 예정 |

```
[모드 1]  영상 → 분석(편집점+자막) → CapCut draft 폴더  (사용자가 마무리 편집)
[모드 2]  영상/주제 → 분석 → 대본 → TTS → BGM → 효과자막 → 컷 → 썸네일 → 완성 영상
```

먼저 모드 1을 완성한 뒤, 모드 2를 순차적으로 붙여 나갑니다.

## 상태

스캐폴딩 단계입니다. 모드 1의 파이프라인과 핵심 빌더는 동작하지만,
**CapCut draft JSON 스키마는 비공식**이라 실제 CapCut에서 만든 샘플
draft 폴더로 검증/보정해야 합니다 (`docs/CAPCUT_FORMAT.md` 참고).

모드 2는 자리만 잡혀 있고 미구현입니다 — 로드맵은 `src/capcut_autoedit/modes/autopilot.py` 참고.

## 구조

```
src/capcut_autoedit/
  cli.py              # 커맨드라인 진입점 (draft / autopilot)
  config.py           # 환경변수(GEMINI_API_KEY 등)
  models.py           # EditPlan, Cut, Subtitle (분석<->빌더 계약)
  media.py            # ffprobe 메타데이터 추출
  input/loader.py     # 로컬 파일 / 유튜브(yt-dlp) 입력
  analysis/gemini.py  # Gemini 영상 분석 -> EditPlan
  capcut/builder.py   # EditPlan -> draft_content.json (핵심)
  capcut/writer.py    # draft 폴더 출력
  modes/
    draft.py          # 모드 1 파이프라인
    autopilot.py      # 모드 2 자리 (미구현 + 로드맵)
tests/
  test_builder.py
```

## 설치

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # GEMINI_API_KEY 입력
```

## 사용

```bash
# 모드 1 — 편집 모드 (로컬 파일)
capcut-autoedit draft input.mp4 --out ./MyProject

# 모드 1 — 편집 모드 (유튜브)
capcut-autoedit draft "https://youtu.be/xxxx" --out ./MyProject

# 모드 1 — Shorts 한국어 자막 스타일
capcut-autoedit draft input.mp4 --out ./MyProject --style shorts-ko

# 모드 2 — 완전자동 (현재는 미구현 안내 출력)
capcut-autoedit autopilot input.mp4
```

## 우선순위 로드맵

**단기 (모드 1 완성)**
1. CapCut 데스크톱에서 "컷 1개 + 자막 1개" 프로젝트를 만들어 draft 폴더 확보
2. `capcut/builder.py` 스키마를 그 샘플에 맞춰 보정 → CapCut에서 실제로 열리는지 확인
3. Gemini 응답 파싱/오류 처리 안정화

**중기 (모드 2 단계적 추가)**
4. 대본 4종 변주 생성 (욕망/본능/감동/분노)
5. TTS 어댑터 (ElevenLabs / TypeCast)
6. BGM 선택·믹싱 + 효과 자막
7. 썸네일 자동 생성
8. ffmpeg 최종 렌더링
9. (선택) YouTube 자동 업로드

**장기**
10. Electron+React GUI — 두 모드 모두 GUI에서 선택
