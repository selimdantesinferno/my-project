# capcut-autoedit

영상(파일 또는 유튜브 링크)을 넣으면 **CapCut 데스크톱에서 바로 열리는 편집 프로젝트**를
자동으로 만들어 주는 도구입니다.

```
입력(영상/유튜브)  ->  Gemini 분석(편집점 + 자막)  ->  CapCut draft 폴더 생성
```

## 상태

스캐폴딩 단계입니다. 파이프라인의 뼈대와 핵심 빌더는 동작하지만,
**CapCut draft JSON 스키마는 비공식**이라 실제 CapCut 버전에서 만든 샘플
draft 폴더로 검증/보정해야 합니다 (`docs/CAPCUT_FORMAT.md` 참고).

## 구조

```
src/capcut_autoedit/
  cli.py            # 커맨드라인 진입점
  pipeline.py       # 입력 -> 분석 -> 빌드 오케스트레이션
  config.py         # 설정 / 환경변수(GEMINI_API_KEY 등)
  models.py         # EditPlan, Cut, Subtitle  (분석<->빌더 계약)
  input/loader.py   # 로컬 파일 / 유튜브(yt-dlp) 입력 처리
  analysis/gemini.py# Gemini로 영상 분석 -> EditPlan
  capcut/builder.py # EditPlan -> draft_content.json  (핵심)
  capcut/writer.py  # draft 폴더로 출력
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
# 로컬 파일
capcut-autoedit build input.mp4 --out ./MyProject

# 유튜브 링크
capcut-autoedit build "https://youtu.be/xxxx" --out ./MyProject
```

## 다음 작업 (우선순위)

1. CapCut 데스크톱에서 "빈 컷 1개 + 자막 1개" 프로젝트를 만들어 draft 폴더 확보
2. `capcut/builder.py` 의 스키마를 그 샘플에 맞게 보정 → CapCut에서 실제로 열리는지 확인
3. Gemini 연동 실제 응답 파싱 안정화
4. (선택) Electron+React GUI

> GUI는 2번이 검증된 뒤에 작업하는 것을 권장합니다.
