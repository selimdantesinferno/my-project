# capcut-autoedit

영상에서 출발해 두 가지 결과물 중 하나를 만드는 도구입니다.

## 두 가지 모드

| 모드 | 명령 | 결과물 | 상태 |
|---|---|---|---|
| **1. 편집 모드 (Draft)** | `capcut-autoedit draft` | **컷 클립 + SRT 자막 번들** (CapCut 등으로 드래그) | ✅ 진행 중 |
| **2. 완전자동 모드 (Autopilot)** | `capcut-autoedit autopilot` | TTS·BGM·효과자막·썸네일까지 들어간 **완성 영상** | 🚧 예정 |

```
[모드 1]  영상 → 분석(편집점+자막) → clip_*.mp4 + subtitles.srt 번들  (편집기로 드래그)
[모드 2]  영상/주제 → 분석 → 대본 → TTS → BGM → 효과자막 → 컷 → 썸네일 → 완성 영상
```

## 왜 CapCut 프로젝트 파일을 직접 만들지 않나

최신 CapCut 데스크톱은 `template` (옛 `draft_content.json`) **파일을 암호화해 저장**합니다.
비공식 도구로 직접 쓰는 건 매 업데이트마다 깨질 위험이 크기 때문에, **편집기 종류에 의존하지 않는 안정적인 워크플로우**로 갔습니다:

- 영상은 컷 단위로 미리 잘려 `clips/clip_*.mp4` 로 나옴
- 자막은 표준 `subtitles.srt`
- CapCut 새 프로젝트에 둘 다 드래그하면 끝 (다른 편집기도 동일)

작업 기록은 `docs/CAPCUT_FORMAT.md` 참고.

## 구조

```
src/capcut_autoedit/
  cli.py              # 커맨드라인 진입점 (draft / autopilot)
  config.py           # 환경변수(GEMINI_API_KEY 등)
  models.py           # EditPlan / Cut / Subtitle (분석↔출력 계약)
  media.py            # ffprobe 메타데이터
  input/loader.py     # 로컬 파일 / 유튜브(yt-dlp)
  analysis/gemini.py  # Gemini 영상 분석 → EditPlan
  export/
    clips.py          # ffmpeg 컷별 mp4 분할
    srt.py            # SRT 자막 생성
    bundle.py         # 번들 폴더 출력 (clips + srt + json + README)
  modes/
    draft.py          # 모드 1 파이프라인
    autopilot.py      # 모드 2 자리 (미구현 + 로드맵)
tests/
  test_srt.py
```

## 설치

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # GEMINI_API_KEY 입력
# ffmpeg / ffprobe 가 PATH 에 있어야 함
```

## 사용

```bash
# 모드 1 — 로컬 파일
capcut-autoedit draft input.mp4 --out ./out

# 모드 1 — 유튜브 링크
capcut-autoedit draft "https://youtu.be/xxxx" --out ./out

# 모드 1 — Shorts 한국어 자막 스타일
capcut-autoedit draft input.mp4 --out ./out --style shorts-ko

# 모드 1 — 빠른 컷(스트림 카피, 키프레임에 스냅)
capcut-autoedit draft input.mp4 --out ./out --fast

# 모드 2 — 완전자동 (현재는 미구현 안내)
capcut-autoedit autopilot input.mp4
```

생성된 `./out/` 에서 `clip_*.mp4` 전체와 `subtitles.srt` 를 CapCut 타임라인으로 드래그.

## 우선순위 로드맵

**단기 (모드 1 완성)**
1. 실영상 + 실 Gemini 키로 end-to-end 테스트
2. ffmpeg 컷 정확도/속도 트레이드오프 튜닝
3. 자막 스타일 옵션 확장

**중기 (모드 2 단계적 추가)**
4. 대본 4종 변주 생성 (욕망/본능/감동/분노)
5. TTS 어댑터 (ElevenLabs / TypeCast)
6. BGM 선택·믹싱 + 효과 자막
7. 썸네일 자동 생성
8. ffmpeg 최종 렌더링
9. (선택) YouTube 자동 업로드

**장기**
10. Electron+React GUI — 두 모드 모두 GUI에서 선택
