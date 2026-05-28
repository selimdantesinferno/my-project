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

## 주요 기능

- **카드뉴스 자동 생성·발행** — 링크/본문 → AI 슬라이드 → 인스타·스레드 캐러셀
- **영상 업로드** — 구글 드라이브 영상 → 유튜브 / 인스타 릴스 / 스레드 동영상 (틱톡은 미연동)
- **즉시 발행** — 생성 후 선택한 플랫폼에 바로 업로드
- **고정(첫) 댓글** — 발행 직후 첫 댓글 자동 등록 (예: "프로필 링크 확인")
- **예약 발행** — 날짜·시간 지정(설정 시간대 기준), 백그라운드 스케줄러가 발행
- **엑셀/CSV 대량 업로드** — 카드뉴스/영상 행을 섞어 등록 가능 (샘플 양식 제공)

## 영상 업로드 (구글 드라이브 연동)

1. 드라이브에서 영상 공유를 **"링크가 있는 모든 사용자"**로 변경 (영상 시연과 동일)
2. 웹 UI **🎬 영상 업로드** 탭에서 드라이브 링크·제목·설명·플랫폼·공개상태 입력
3. 즉시 발행 또는 예약

- **인스타 릴스 / 스레드 동영상**: 드라이브 링크를 직접 다운로드 URL로 변환해 전달, 인코딩 완료까지 폴링 후 발행
- **유튜브**: Data API v3로 파일을 내려받아 업로드 (OAuth2 — `YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN` 필요)
- **틱톡**: 현재 미연동 (선택 시 안내 메시지 반환, 추후 TikTok Content Posting API 지원 예정)

영상 대량 업로드 열: `type, video_url, title, description, targets, first_comment, privacy, scheduled_at`
(`type=video` 또는 `video_url` 이 있으면 영상 잡으로 등록. 양식: `GET /api/bulk/sample?kind=video`)

### 대량 업로드 양식 (열)

`url, text, slide_count, template, tone, account, prompt, targets, first_comment, scheduled_at, provider`

- `targets`: `instagram,threads` 처럼 콤마 구분
- `scheduled_at`: `YYYY-MM-DD HH:MM` (`TIMEZONE` 기준). 비우면 즉시 발행
- 웹 UI의 "샘플 양식" 버튼 또는 `GET /api/bulk/sample` 로 양식 받기

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 웹 UI |
| GET | `/api/options` | 템플릿/톤/제공자 목록 |
| POST | `/api/generate` | 글감 → 슬라이드 생성·렌더 |
| POST | `/api/upload` | 카드뉴스 즉시 발행 (고정 댓글 포함) |
| POST | `/api/video` | 영상 업로드 (즉시/예약, 다중 플랫폼) |
| POST | `/api/schedule` | 카드뉴스 예약 발행 잡 등록 |
| GET | `/api/jobs` | 예약 잡 목록 |
| POST | `/api/jobs/{id}/cancel` | 예약 취소 |
| POST | `/api/bulk` | 엑셀/CSV 대량 등록 |
| GET | `/api/bulk/sample` | 대량 업로드 샘플 CSV |
| GET | `/output/<file>` | 생성된 이미지 (공개 제공) |
