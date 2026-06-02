from src.utils.config import settings
from src.utils.logger import logger
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_payments(num_records: int = None):
    if num_records is None:
        num_records = settings.default_num_records
    
    logger.info("Starting payments data generation", num_records=num_records)
    
    settings.raw_path.mkdir(parents=True, exist_ok=True)
    
    df = pd.DataFrame({
        "transaction_id": [f"TX-{i:010d}" for i in range(num_records)],
        "timestamp": pd.date_range(start=datetime.utcnow() - timedelta(days=7), periods=num_records, freq="s"),
        "user_id": np.random.randint(1000, 99999, num_records),
        "merchant_id": np.random.randint(100, 9999, num_records),
        "amount": np.round(np.random.lognormal(4, 1.5, num_records), 2),
        "currency": np.random.choice(["USD", "EUR", "SGD"], num_records),
        "status": np.random.choice(["success", "failed", "pending"], num_records, p=[0.92, 0.05, 0.03]),
        "payment_method": np.random.choice(["card", "wallet", "bank"], num_records),
    })
    
    partition_date = df["timestamp"].dt.date.iloc[0].strftime("%Y-%m-%d")
    output_path = settings.raw_path / f"date={partition_date}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    df.to_parquet(output_path / "payments_raw.parquet", compression="snappy")
    
    logger.info("✅ Raw data generated", records=num_records, path=str(output_path))
    return df

if __name__ == "__main__":
    generate_payments()