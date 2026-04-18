from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DJANGO_API_URL: str = "https://julianna-unblossomed-zahra.ngrok-free.dev"
    PORT: int = 8001
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()