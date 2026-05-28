# ☁️ 클라우드 배포 안내 (컴퓨터를 꺼도 예약 발행)

내 컴퓨터가 꺼져 있어도 **예약 발행이 자동으로 돌아가게** 하려면 클라우드 서버에 올립니다.
공개 https 주소가 자동으로 생겨서 **ngrok 없이** 인스타/스레드/틱톡 업로드가 됩니다.

초보자에게 가장 쉬운 곳: **Railway** 또는 **Render**.

---

## Railway 로 배포 (추천)

1. https://railway.app 가입 (GitHub 계정으로 로그인)
2. **New Project → Deploy from GitHub repo → 이 저장소 선택**
3. 루트 디렉터리(Root Directory)를 **`cardnews`** 로 설정
4. 시작 명령(Start Command):
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. **Variables(환경변수)** 에 `.env` 내용을 한 줄씩 입력
   (OPENAI_API_KEY, IG_*, THREADS_*, YOUTUBE_*, TIKTOK_* 등 필요한 것만)
6. 배포되면 생성된 공개 주소(예: `https://xxx.up.railway.app`)를
   **`PUBLIC_BASE_URL`** 환경변수에도 동일하게 넣고 재배포
7. 그 주소로 접속하면 어디서든(폰에서도) 사용 가능

> Railway 무료 크레딧 소진 후에는 소정의 비용이 들 수 있습니다.

---

## Render 로 배포

1. https://render.com 가입
2. **New → Web Service → GitHub 저장소 연결**
3. 설정:
   - Root Directory: `cardnews`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment** 탭에서 `.env` 값들을 입력
5. 배포 후 생긴 주소를 `PUBLIC_BASE_URL` 에도 넣고 재배포

---

## 배포 후 체크리스트

- [ ] `PUBLIC_BASE_URL` 이 배포된 https 주소와 같은가?
- [ ] 필요한 플랫폼 토큰을 환경변수에 모두 넣었는가?
- [ ] 주소로 접속해 `/health` 가 `ok` 인가?
- [ ] 비공개로 1건 테스트 발행이 되는가?

> 토큰 발급 방법은 `GUIDE.md` 를 참고하세요.
