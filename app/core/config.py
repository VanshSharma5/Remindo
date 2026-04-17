from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    CRON_HOUR: int
    CRON_MINUTE: int

    class Config:
        env_file = ".env"

settings = Settings()