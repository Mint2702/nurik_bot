from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    token: str = Field(..., env="TOKEN")

    psql_db_name: str = Field(..., env="PSQL_DB_NAME")
    psql_user: str = Field(..., env="PSQL_DB_USER")
    psql_password: str = Field(..., env="PSQL_DB_PASSWORD")
    psql_host: str = Field(..., env="PSQL_DB_HOST")
    psql_port: str = Field(..., env="PSQL_DB_PORT")

    password: str = Field(..., env="PASSWORD")
    dev: bool = Field(..., env="DEV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file="../.env")
