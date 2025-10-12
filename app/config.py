from pydantic.v1 import BaseSettings
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATA_BASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    class Config:
        env_file = '.env'

    TEMPLATES = Jinja2Templates(directory='app/templates')


settings = Settings()