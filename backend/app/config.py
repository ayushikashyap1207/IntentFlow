from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / '.env')


def _default_model_path() -> str:
    return str(PROJECT_ROOT / 'models' / 'tflite' / 'intentflow_lstm.tflite')


class Settings(BaseModel):
    groq_api_key: str = Field(default_factory=lambda: os.getenv('GROQ_API_KEY', ''))
    supabase_url: str = Field(default_factory=lambda: os.getenv('SUPABASE_URL', ''))
    supabase_key: str = Field(default_factory=lambda: os.getenv('SUPABASE_KEY', ''))
    supabase_db_url: str = Field(default_factory=lambda: os.getenv('SUPABASE_DB_URL', ''))
    tflite_model_path: str = Field(default_factory=lambda: os.getenv('TFLITE_MODEL_PATH', _default_model_path()))
    huggingface_token: str = Field(default_factory=lambda: os.getenv('HUGGINGFACE_TOKEN', ''))
    cors_origins: list[str] = Field(default_factory=lambda: ['http://localhost:3000'])
    api_title: str = 'IntentFlow API'
    api_version: str = '1.0.0'


settings = Settings()
