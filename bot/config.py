import json

from pydantic import BaseSettings, validator


class DB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class Redis(BaseSettings):
    host: str
    db: int


class Bot(BaseSettings):
    token: str
    use_redis: bool


class Settings(BaseSettings):
    tg_bot: Bot
    db: DB
    redis: Redis

    class Config:
        env_file = '.env.dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


def load_config(env_file='.env.dev') -> Settings:
    settings = Settings(_env_file=env_file)
    return settings