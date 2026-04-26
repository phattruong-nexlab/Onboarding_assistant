import os
from pydantic_settings import BaseSettings

# Calculate path to the root .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Onboarding Assistant API"
    GEMINI_API_KEY: str

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
