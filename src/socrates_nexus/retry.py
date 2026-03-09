"""Retry logic with exponential backoff for LLM API calls."""

import functools
import random
import time
from dataclasses import dataclass
from typing import Callable, Type, Tuple, Any

from .exceptions import (
    RateLimitError,
    TimeoutError as NexusTimeoutError,
)


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retry_on_rate_limit: bool = True
    retry_on_timeout: bool = True
    retry_on_server_error: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        RateLimitError,
        NexusTimeoutError,
    )


def exponential_backoff(attempt: int, config: RetryConfig) -> float:
    """
    Calculate delay for exponential backoff with optional jitter.

    Args:
        attempt: Current attempt number (0-indexed)
        config: Retry configuration

    Returns:
        Delay in seconds
    """
    delay = config.base_delay * (config.exponential_base**attempt)
    delay = min(delay, config.max_delay)

    if config.jitter:
        # Add jitter: delay * (0.5 + random() * 0.5)
        jitter_factor = 0.5 + random.random() * 0.5
        delay *= jitter_factor

    return delay


def retry_with_backoff(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
    max_delay: float = 32.0,
    jitter: bool = True,
):
    """
    Decorator for retrying with exponential backoff (legacy interface).

    Args:
        max_attempts: Maximum number of retry attempts
        backoff_factor: Multiplier for delay between retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter to delay
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, NexusTimeoutError, ConnectionError) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        # Add jitter if enabled
                        if jitter:
                            delay_with_jitter = delay * (0.5 + random.random())
                        else:
                            delay_with_jitter = delay

                        # Cap delay at max_delay
                        delay_with_jitter = min(delay_with_jitter, max_delay)

                        # Extract retry_after if available
                        if isinstance(e, RateLimitError) and e.retry_after:
                            delay_with_jitter = max(delay_with_jitter, e.retry_after)

                        time.sleep(delay_with_jitter)
                        delay = min(delay * backoff_factor, max_delay)

            if last_exception:
                raise last_exception

        return wrapper

    return decorator
