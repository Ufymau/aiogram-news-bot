import functools

import asyncio

from utils.logger_config import logger

def log_func_access(func):
    """
    The decorator blocks the entry and exit of a function, including the function name and arguments.
    Supports both sync and async functions.
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.info(f"Entering async function '{func.__name__}' with args={args}, kwargs={kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Exiting async function '{func.__name__}' with result={result!r}")
                return result
            except Exception as e:
                logger.exception(f"Exception in async function '{func.__name__}': {e}")
                raise
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.info(f"Entering function '{func.__name__}' with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Exiting function '{func.__name__}' with result={result!r}")
                return result
            except Exception as e:
                logger.exception(f"Exception in function '{func.__name__}': {e}")
                raise
        return sync_wrapper
