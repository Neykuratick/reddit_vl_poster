from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    COMMUNITY_ID: int
    OWNER_ID: str
    ALBUM_ID: int

    VK_TOKEN: str  # токен пользователя - админа

    @validator("OWNER_ID", always=True, pre=True)
    def validate_owner_id(cls, v):
        # owner_id должен быть равен community_id, только с минусом в начале
        assert int(v) < 0
        return v


settings = Settings()
