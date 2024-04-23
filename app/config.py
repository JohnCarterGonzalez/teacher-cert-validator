from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    openai_url: str = "https://api.openai.com/v1/chat/completions"

    class Config:
        env_file = ".env"

settings = Settings()

