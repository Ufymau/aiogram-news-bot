import asyncio
import functools
from typing import Callable

def print_result_decorator(func: Callable) -> Callable:
    """
        Decorator that wraps a synchronous or asynchronous function,
        preserving its signature and behavior.

        It detects whether the decorated function is a coroutine (async function)
        and returns an appropriate wrapper that calls the function and returns its result.

        Args:
            func (Callable): The function to decorate. Can be sync or async.

        Returns:
            Callable: The wrapped function with the same signature and return type.
    """
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
