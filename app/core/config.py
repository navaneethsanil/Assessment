import os

from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API keys
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str
    
    # Database
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = ".env"

settings = Settings()
