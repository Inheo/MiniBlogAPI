from pydantic import BaseModel
from pydantic_settings import BaseSettings

class TokenConfig:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    token_config: TokenConfig = TokenConfig()

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()