"""환경변수 기반 설정."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    gemini_api_key: str
    gemini_model: str

    @classmethod
    def load(cls) -> "Config":
        key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요 (.env.example 참고)."
            )
        return cls(
            gemini_api_key=key,
            gemini_model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip(),
        )
