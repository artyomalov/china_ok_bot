from pydantic import BaseSettings, SecretStr, PostgresDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn
    sample_spreadsheet_id: SecretStr
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
