# 🔑 실제 발행 설정 가이드 (토큰 + ngrok 단계별)

이 문서대로 따라 하면 **실제로 인스타그램·스레드·유튜브·틱톡에 게시**할 수 있습니다.

> ⚠️ 모든 토큰/키는 **`.env` 파일에만** 넣으세요. 채팅·깃허브·코드에 붙여넣지 마세요.

순서: **0) 설치 → 1) ngrok 공개주소 → 2) 스레드 → 3) 인스타 → 4) 유튜브 → 5) 틱톡 → 6) 실행·테스트**

---

## 0. 설치

```bash
cd cardnews
python3 -m venv .venv
source .venv/bin/activate          # 윈도우: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # 이제 .env 를 편집해 갑니다
```

---

## 1. ngrok — "공개 주소" 만들기 (가장 중요)

인스타/스레드/틱톡 API는 이미지·영상을 **공개 인터넷 주소**에서 가져갑니다.
로컬(`localhost`)은 외부에서 못 봐서, ngrok으로 임시 공개 주소를 만듭니다.

1. https://ngrok.com 가입 → `ngrok` 설치 → 인증토큰 등록
   ```bash
   ngrok config add-authtoken <발급받은_토큰>
   ```
2. (앱 서버는 8000 포트로 띄울 거예요) 새 터미널에서:
   ```bash
   ngrok http 8000
   ```
3. 출력된 `Forwarding  https://xxxx-xx-xx.ngrok-free.app` 주소를 복사
4. `.env` 에 입력 (끝에 `/` 없이):
   ```
   PUBLIC_BASE_URL=https://xxxx-xx-xx.ngrok-free.app
   ```

> ngrok 무료 주소는 재시작할 때마다 바뀝니다. 바뀌면 `PUBLIC_BASE_URL`도 다시 바꾸세요.
> 운영용으로는 클라우드(예: Railway, Render, VPS)에 배포하고 고정 도메인을 쓰는 게 좋습니다.

---

## 2. 스레드(Threads) 토큰

1. https://developers.facebook.com → **내 앱 > 앱 만들기**
2. 유형은 **비즈니스**, 제품에서 **Threads API** 추가
3. **Threads API > 설정**에서 권한 추가: `threads_basic`, `threads_content_publish`
4. 토큰 생성기/Graph API 탐색기로 **액세스 토큰**과 **Threads 사용자 ID** 확보
   - 사용자 ID 조회: `GET https://graph.threads.net/v1.0/me?fields=id,username&access_token=<토큰>`
5. `.env` 에 입력:
   ```
   THREADS_USER_ID=<me 로 조회한 id>
   THREADS_ACCESS_TOKEN=<액세스 토큰>
   ```

> 단기 토큰은 만료됩니다. **장기(long-lived) 토큰**으로 교환해 두면 60일간 유효합니다.

---

## 3. 인스타그램(Instagram Graph API) 토큰

전제: **인스타 프로페셔널(비즈니스/크리에이터) 계정** + 연결된 **페이스북 페이지**.

1. 같은 Meta 앱에 **Instagram** / **Facebook Login** 제품 추가
2. 권한: `instagram_basic`, `instagram_content_publish`, `pages_show_list`
3. **Graph API 탐색기**에서 페이지 토큰 발급 → IG 비즈니스 계정 ID 조회:
   ```
   GET /me/accounts                       → 페이지 id
   GET /<page-id>?fields=instagram_business_account
   ```
4. `.env` 에 입력:
   ```
   IG_USER_ID=<instagram_business_account 의 id>
   IG_ACCESS_TOKEN=<장기 페이지 토큰>
   ```

> 카드뉴스(이미지)·릴스(영상) 모두 이 토큰으로 발행합니다.
> 릴스는 인코딩에 시간이 걸려, 프로그램이 자동으로 완료를 기다린 뒤 발행합니다.

---

## 4. 유튜브(YouTube Data API) — OAuth refresh token

유튜브는 토큰 하나가 아니라 **OAuth 인증**이 필요합니다. 도우미 스크립트로 한 번만 받으면 됩니다.

1. https://console.cloud.google.com → 프로젝트 생성
2. **API 및 서비스 > 라이브러리**에서 **YouTube Data API v3** 사용 설정
3. **OAuth 동의 화면** 구성 (외부, 테스트 사용자에 본인 구글계정 추가)
4. **사용자 인증 정보 > 사용자 인증 정보 만들기 > OAuth 클라이언트 ID > 데스크톱 앱**
5. 만든 클라이언트의 **JSON 다운로드** → `cardnews/scripts/client_secret.json` 로 저장
6. refresh token 발급:
   ```bash
   python scripts/get_youtube_token.py
   ```
   브라우저가 열리면 로그인·허용 → 터미널에 출력되는 3줄을 `.env` 에 붙여넣기:
   ```
   YOUTUBE_CLIENT_ID=...
   YOUTUBE_CLIENT_SECRET=...
   YOUTUBE_REFRESH_TOKEN=...
   ```

> 테스트 단계 앱은 refresh token이 만료될 수 있습니다. 만료되면 6번을 다시 실행하세요.

---

## 5. 틱톡(TikTok Content Posting API)

1. https://developers.tiktok.com → 앱 생성
2. **Content Posting API** 권한 신청, 스코프 `video.publish` 추가
3. OAuth 인증으로 **액세스 토큰** 발급 → `.env`:
   ```
   TIKTOK_ACCESS_TOKEN=<액세스 토큰>
   ```

> ⚠️ **앱 심사(audit) 전에는 비공개(SELF_ONLY)로만 게시**됩니다. 본인 계정 드래프트/비공개로는 바로 테스트 가능하고,
> 공개 게시는 틱톡 앱 심사 통과 후 가능합니다. 이 프로그램은 FILE_UPLOAD 방식이라 도메인 인증은 필요 없습니다.

---

## 6. 영상 파일 준비 (구글 드라이브)

영상 업로드는 구글 드라이브 링크로 합니다.

1. 드라이브에 영상 업로드 → 우클릭 **공유**
2. 일반 액세스를 **"링크가 있는 모든 사용자"**로 변경 (영상 시연과 동일!)
3. 링크 복사 → 웹 UI 🎬 영상 탭의 "드라이브 링크"에 붙여넣기

> "제한됨" 상태면 API가 접근 못 해 **발행 실패**합니다. 꼭 "링크가 있는 모든 사용자"로!

---

## 7. 실행 & 연결 테스트

```bash
# 터미널 1: ngrok (1번에서 이미 실행 중)
# 터미널 2:
source .venv/bin/activate
uvicorn app.main:app --port 8000
```

- 브라우저에서 `PUBLIC_BASE_URL`(ngrok 주소) 또는 `http://localhost:8000` 접속
- **연결 확인**: `GET /health` 가 `{"status":"ok", ...}` 면 서버 정상
- 카드뉴스: 글감 입력 → 생성 → **즉시 발행**으로 1건 테스트
- 영상: 드라이브 링크 → **비공개/SELF_ONLY**로 먼저 1건 테스트 권장

### 발행이 실패하면?

| 증상 | 원인 / 해결 |
|------|------|
| 이미지/영상 접근 실패 | `PUBLIC_BASE_URL`이 ngrok https 주소인지, 드라이브가 "모든 사용자" 공유인지 확인 |
| `자격정보가 없습니다` | 해당 플랫폼 토큰이 `.env`에 비어있음 |
| 토큰 만료/권한 오류 | 장기 토큰으로 교환, 필요한 권한(스코프) 추가 |
| 릴스/영상 처리 시간초과 | 영상 용량/형식 확인(mp4 권장), 잠시 후 재시도 |
| 틱톡이 비공개로만 올라감 | 정상 — 앱 심사 전 제한. 심사 후 공개 게시 가능 |

---

## 최종 .env 예시 (값은 본인 것으로)

```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
PUBLIC_BASE_URL=https://xxxx.ngrok-free.app
TIMEZONE=Asia/Seoul

THREADS_USER_ID=...
THREADS_ACCESS_TOKEN=...
IG_USER_ID=...
IG_ACCESS_TOKEN=...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
TIKTOK_ACCESS_TOKEN=...
```

필요한 플랫폼의 값만 채워도 됩니다. (예: 스레드만 쓰면 스레드 값만)
