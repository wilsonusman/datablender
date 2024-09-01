import logging
from datetime import datetime
import functools
import time  # Added for more precise timing

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def measure_time(func):
    """
    A decorator that measures the execution time of a function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function that logs its execution time.
    """
    @functools.wraps(func)
    def wrapper_measure_time(*args, **kwargs):
        start_time = time.perf_counter()  # Changed to perf_counter for better precision
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")  # Added error logging
            raise
        end_time = time.perf_counter()  # Changed to perf_counter
        elapsed = end_time - start_time
        logger.info(
            f"{func.__name__} function completed in {int(elapsed // 60)} minutes "
            f"and {elapsed % 60:.2f} seconds."
        )
        return result

    return wrapper_measure_time