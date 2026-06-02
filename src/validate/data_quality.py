from src.utils.config import settings
from src.utils.logger import logger
import pandas as pd

def run_data_quality_checks():
    logger.info("Starting data quality validation")
    
    # Check latest silver file
    silver_files = sorted(settings.silver_path.glob("date=*/payments_silver.parquet"))
    if not silver_files:
        logger.error("No silver files found for validation")
        return False
    
    df = pd.read_parquet(silver_files[-1])
    
    checks = {
        "total_records": len(df),
        "null_amount": df['amount'].isna().sum(),
        "negative_amount": (df['amount'] < 0).sum(),
        "high_risk_tx": (df['risk_score'] > 0).sum(),
        "duplicate_tx": df['transaction_id'].duplicated().sum(),
        "pending_status": (df['status'] == 'pending').sum()
    }
    
    logger.info("Data quality check completed", **checks)
    
    if checks["null_amount"] > 0 or checks["negative_amount"] > 0 or checks["duplicate_tx"] > 0:
        logger.warning("Data quality issues detected", **checks)
        return False
    
    logger.info("✅ Data quality validation passed")
    return True

if __name__ == "__main__":
    run_data_quality_checks()