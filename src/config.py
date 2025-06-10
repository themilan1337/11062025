from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field # Import Field for default values if needed

class Settings(BaseSettings):
    database_url: str
    sync_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Add the missing fields here
    openai_api_key: str # Assuming this is a string key
    celery_broker_url: str # Or AnyUrl if you want validation
    celery_result_backend: str # Or AnyUrl
    redis_url: str # Or AnyUrl

    # You can optionally configure Pydantic to ignore extra fields,
    # but adding them explicitly is generally better practice.
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     extra='ignore' # Uncomment this if you MUST ignore undeclared variables
    # )

    # Keep the original model_config if you added the fields above
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()