from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    project_name: str = "payments-etl-framework"
    base_data_path: Path = Path("data")
    raw_path: Path = Path("data/raw")
    bronze_path: Path = Path("data/bronze")
    silver_path: Path = Path("data/silver")
    
    # New configurable parameters
    default_num_records: int = 200_000
    batch_size: int = 100_000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()