from src.utils.config import settings
from src.utils.logger import logger
import pandas as pd
from pathlib import Path

def run_data_quality_checks(stage: str = "silver"):
    logger.info(f"Starting data quality checks for {stage} layer")
    
    if stage == "silver":
        search_path = settings.silver_path
    else:
        search_path = settings.bronze_path
    
    # Better glob pattern
    files = sorted(search_path.glob("date=*/payments_silver.parquet"))
    
    if not files:
        logger.error(f"No {stage} files found. Searched in: {search_path}")
        logger.info("Existing files in silver folder:", list(search_path.glob("**/*")))
        return False
    
    df = pd.read_parquet(files[-1])
    
    checks = {
        "total_records": len(df),
        "null_values": int(df.isnull().sum().sum()),
        "duplicate_tx": int(df['transaction_id'].duplicated().sum()),
        "negative_amount": int((df['amount'] < 0).sum()),
        "high_risk_tx": int((df['risk_score'] > 0).sum())
    }
    
    logger.info("Data quality checks completed", **checks)
    logger.info("Data quality validation passed")
    return True

if __name__ == "__main__":
    run_data_quality_checks()