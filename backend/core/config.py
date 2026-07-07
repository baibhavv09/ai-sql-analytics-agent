from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    APP_NAME: str = "AI SQL Analytics Agent"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    SECRET_KEY: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str

    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_MAX_TOKENS: int = 1000

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    MAX_QUERY_ROWS: int = 1000
    QUERY_TIMEOUT: int = 30
    ALGORITHM: str = "HS256"
    DATABASE_SECRET_KEY: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_CACHE_TTL: int = 600
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()