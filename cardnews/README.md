# 🏭 카드뉴스 자동화 공장

링크·본문 글감을 입력하면 **AI(ChatGPT / Gemini)가 카드뉴스 슬라이드를 생성**하고,
**인스타그램·스레드 캐러셀로 자동 업로드**하는 프로그램입니다.

> 흐름: 글감 입력 → 템플릿/슬라이드수/색상 설정 → AI 생성 → 미리보기 → 인스타·스레드 자동 발행

## 구성

- **Python + FastAPI** 백엔드 (AI 생성 / 이미지 렌더링 / Meta 업로드)
- **웹 UI** (브라우저에서 입력·미리보기·업로드)
- **CLI** (`cli.py`, 헤드리스 자동 발행용)

이미지는 1080×1080 PNG로 렌더링되며, 한국어 폰트(Noto Sans KR)를 사용합니다.

## 설치

```bash
cd cardnews
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 키 입력
```

## 실행 (웹)

```bash
uvicorn app.main:app --reload --port 8000
# 브라우저: http://localhost:8000
```

## 실행 (CLI)

```bash
python cli.py --text "글감..." --slides 7 --template toss --tone blue --account "@me"
python cli.py --url https://example.com --upload instagram threads
```

## 설정 (.env)

| 항목 | 설명 |
|------|------|
| `AI_PROVIDER` | `openai` 또는 `gemini` |
| `OPENAI_API_KEY` / `OPENAI_MODEL` | ChatGPT 사용 시 |
| `GEMINI_API_KEY` / `GEMINI_MODEL` | Gemini 사용 시 |
| `PUBLIC_BASE_URL` | **중요** — Meta API가 이미지를 가져갈 공개 https 주소 |
| `IG_USER_ID` / `IG_ACCESS_TOKEN` | 인스타그램 Graph API |
| `THREADS_USER_ID` / `THREADS_ACCESS_TOKEN` | 스레드 API |

### ⚠️ 공개 URL이 필요한 이유

인스타그램 Graph API와 스레드 API는 업로드할 이미지를 **공개적으로 접근 가능한 URL**로 받습니다.
로컬 파일을 직접 올릴 수 없습니다. 따라서:

- **운영**: 서버를 공개 도메인(https)에 배포하고 `PUBLIC_BASE_URL`을 그 주소로 설정
- **로컬 테스트**: `ngrok http 8000` 등으로 터널링한 https 주소를 `PUBLIC_BASE_URL`에 입력

## 템플릿 & 색상

- 템플릿: `toss`(여백·굵은 한 문장), `magazine`(라벨 바·큰 제목)
- 색상 톤: `blue`, `light`, `dark`, `warm`
- 통계 숫자는 자동으로 강조(stat) 슬라이드로 구성됩니다.

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 웹 UI |
| GET | `/api/options` | 템플릿/톤/제공자 목록 |
| POST | `/api/generate` | 글감 → 슬라이드 생성·렌더 |
| POST | `/api/upload` | 인스타/스레드 업로드 |
| GET | `/output/<file>` | 생성된 이미지 (공개 제공) |
