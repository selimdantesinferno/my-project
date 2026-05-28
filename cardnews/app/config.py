"""환경설정 로드. .env 파일 또는 환경변수에서 값을 읽습니다."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
FONTS_DIR = BASE_DIR / "assets" / "fonts"
WEB_DIR = BASE_DIR / "web"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # AI
    ai_provider: str = "openai"  # openai | gemini
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # 서버 공개 주소 (Meta API가 이미지를 가져갈 URL)
    public_base_url: str = "http://localhost:8000"

    # 예약 시각 입력의 기준 시간대 (naive 시각 해석용)
    timezone: str = "Asia/Seoul"

    # Threads
    threads_user_id: str = ""
    threads_access_token: str = ""

    # Instagram
    ig_user_id: str = ""
    ig_access_token: str = ""

    # YouTube Data API (OAuth2) - 영상 업로드용
    youtube_client_id: str = ""
    youtube_client_secret: str = ""
    youtube_refresh_token: str = ""

    # TikTok Content Posting API
    tiktok_access_token: str = ""

    @property
    def base_url(self) -> str:
        return self.public_base_url.rstrip("/")


settings = Settings()
