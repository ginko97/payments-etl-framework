from src.utils.config import settings
from src.utils.logger import logger
import pandas as pd
from pathlib import Path

def bronze_to_silver():
    logger.info("Starting Bronze → Silver transformation")
    
    settings.bronze_path.mkdir(parents=True, exist_ok=True)
    settings.silver_path.mkdir(parents=True, exist_ok=True)
    
    # Find latest raw file
    raw_files = sorted(settings.raw_path.glob("date=*/payments_raw.parquet"))
    if not raw_files:
        logger.error("No raw files found")
        return
    
    df = pd.read_parquet(raw_files[-1])
    
    # Production transformations
    df_clean = df.copy()
    df_clean = df_clean[df_clean["status"] != "pending"]
    df_clean["amount"] = df_clean["amount"].astype("float32")
    df_clean["transaction_date"] = df_clean["timestamp"].dt.date
    df_clean["risk_score"] = ((df_clean["amount"] > 500) * 50).astype("int8")
    
    # Save Silver (partitioned)
    partition_date = df_clean["transaction_date"].iloc[0].strftime("%Y-%m-%d")
    output_path = settings.silver_path / f"date={partition_date}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    df_clean.to_parquet(output_path / "payments_silver.parquet", compression="snappy")
    
    logger.info("Silver layer created", 
                records=len(df_clean), 
                path=str(output_path))

if __name__ == "__main__":
    bronze_to_silver()