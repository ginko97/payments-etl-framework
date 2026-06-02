from src.utils.config import settings
from src.utils.logger import logger
import pandas as pd

def validate_silver():
    logger.info("Starting Silver layer validation")
    
    silver_files = sorted(settings.silver_path.glob("date=*/payments_silver.parquet"))
    if not silver_files:
        logger.error("No silver files found")
        return False
    
    df = pd.read_parquet(silver_files[-1])
    
    logger.info("Silver validation results",
                total_records=len(df),
                null_amount=df['amount'].isna().sum(),
                negative_amount=(df['amount'] < 0).sum(),
                high_risk_count=(df['risk_score'] > 0).sum())
    
    return True

if __name__ == "__main__":
    validate_silver()