"""YouTube 업로드용 OAuth2 refresh token 발급 도우미.

사용법:
  1) Google Cloud Console 에서 OAuth 클라이언트(데스크톱 앱) 만들고
     client_secret.json 을 내려받아 이 스크립트와 같은 폴더에 둡니다.
  2) python scripts/get_youtube_token.py
  3) 브라우저가 열리면 구글 로그인 → 권한 허용
  4) 출력된 refresh_token 을 .env 의 YOUTUBE_REFRESH_TOKEN 에 붙여넣기
     (CLIENT_ID / CLIENT_SECRET 도 client_secret.json 값으로 채우기)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
HERE = Path(__file__).resolve().parent


def main() -> None:
    secret = HERE / "client_secret.json"
    if not secret.exists():
        sys.exit(f"client_secret.json 이 없습니다: {secret}\n"
                 "Google Cloud Console > 사용자 인증 정보 > 데스크톱 앱에서 받으세요.")

    flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")

    info = json.loads(secret.read_text())
    block = info.get("installed") or info.get("web") or {}
    print("\n===== .env 에 아래 값을 넣으세요 =====")
    print("YOUTUBE_CLIENT_ID=", block.get("client_id", ""), sep="")
    print("YOUTUBE_CLIENT_SECRET=", block.get("client_secret", ""), sep="")
    print("YOUTUBE_REFRESH_TOKEN=", creds.refresh_token, sep="")


if __name__ == "__main__":
    main()
