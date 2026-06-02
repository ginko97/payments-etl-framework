import time
from functools import wraps
from src.utils.logger import logger

def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt}/{max_retries} failed", error=str(e))
                    if attempt == max_retries:
                        logger.error("All retries failed", error=str(e))
                        raise
                    time.sleep(delay * attempt)  # exponential backoff
            return None
        return wrapper
    return decorator