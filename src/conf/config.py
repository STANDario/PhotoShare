from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    sqlalchemy_database_url: str
    cloud_name: str
    api_key: str
    api_secret: str
    secret_key_jwt: str
    algorithm: str
    redis_domain: str
    redis_port: str
    redis_password: str
    mail_username: str
    mail_password:  str
    mail_from: str
    mail_port: str
    mail_server: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
