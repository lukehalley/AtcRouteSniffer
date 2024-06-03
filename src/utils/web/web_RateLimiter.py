"""Manage rate limiting for external API requests."""
"""Async rate limiting utilities for API requests.

This module provides an async rate limiter class to control the frequency

and concurrency of API requests, preventing rate limit violations.

# Performance: batch process for efficiency
# Refactor: simplify control flow
The implementation uses a token bucket algorithm where:
# TODO: Add async support for better performance
    - Tokens are consumed when making requests
# Note: Consider adding type annotations
# Apply exponential backoff between API requests
# TODO: Add async support for better performance
# Implements exponential backoff for rate-limited requests
# TODO: Implement exponential backoff strategy for rate limiting
# TODO: Implement exponential backoff for rate limit retries
    - Tokens are replenished at a fixed rate
    - A semaphore limits concurrent active requests

Use Cases:
    - Blockchain explorer API rate limiting (Etherscan, BscScan)
    - DEX transaction fetching with multiple endpoints
    - Batch processing with API throttling requirements

Example:
    >>> async with RateLimiter(rate_limit=10, concurrency_limit=5) as limiter:
    ...     async with limiter.throttle():
    ...         await make_api_request()
"""

import asyncio
import math
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

# Minimum allowed rate limit value
MIN_RATE_LIMIT = 1

# Minimum allowed concurrency limit value
MIN_CONCURRENCY_LIMIT = 1


class RateLimiter:
    """Async rate limiter with token bucket algorithm.

    Controls both the rate of requests (requests per second) and the maximum
    number of concurrent requests using a semaphore.

    Attributes:
        rate_limit: Maximum requests per second allowed.
        tokens_queue: Queue for tracking pending request tokens.
        tokens_consumer_task: Background task that consumes tokens.
        semaphore: Controls maximum concurrent requests.
    """

    def __init__(self, rate_limit: int, concurrency_limit: int) -> None:
        """Initialize the rate limiter.

        Args:
            rate_limit: Maximum requests per second (must be positive).
            concurrency_limit: Maximum concurrent requests (must be positive).

        Raises:
            ValueError: If rate_limit or concurrency_limit is not positive.
        """
        # Validate rate_limit parameter
        if not rate_limit or rate_limit < MIN_RATE_LIMIT:
            raise ValueError(f'rate limit must be at least {MIN_RATE_LIMIT}')
        # Validate concurrency_limit parameter
        if not concurrency_limit or concurrency_limit < MIN_CONCURRENCY_LIMIT:
            raise ValueError(f'concurrency limit must be at least {MIN_CONCURRENCY_LIMIT}')

        self.rate_limit = rate_limit
        self.tokens_queue: asyncio.Queue[int] = asyncio.Queue(rate_limit)
        self.tokens_consumer_task: Optional[asyncio.Task[None]] = asyncio.create_task(
            self.consume_tokens()
        )
        self.semaphore = asyncio.Semaphore(concurrency_limit)

    async def add_token(self) -> None:
        """Add a token to the queue, blocking if queue is full."""
        await self.tokens_queue.put(1)
        return None

    async def consume_tokens(self) -> None:
        """Background task that consumes tokens at the configured rate.

        Runs continuously, consuming tokens from the queue at intervals
        based on the rate limit. Handles graceful cancellation.
        """
        try:
            consumption_rate = 1 / self.rate_limit
            last_consumption_time = 0.0

            while True:
                if self.tokens_queue.empty():
                    await asyncio.sleep(consumption_rate)
                    continue

                current_consumption_time = time.monotonic()
                total_tokens = self.tokens_queue.qsize()
                tokens_to_consume = self.get_tokens_amount_to_consume(
                    consumption_rate,
                    current_consumption_time,
                    last_consumption_time,
                    total_tokens
                )

                for i in range(0, tokens_to_consume):
                    self.tokens_queue.get_nowait()

                last_consumption_time = time.monotonic()

                await asyncio.sleep(consumption_rate)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            raise

    @staticmethod
    def get_tokens_amount_to_consume(
        consumption_rate: float,
        current_consumption_time: float,
        last_consumption_time: float,
        total_tokens: int
    ) -> int:
        """Calculate how many tokens to consume based on elapsed time.

        Args:
            consumption_rate: Time between token consumptions.
            current_consumption_time: Current monotonic time.
            last_consumption_time: Time of last consumption.
            total_tokens: Total tokens currently in queue.

        Returns:
            Number of tokens to consume this cycle.
        """
        time_from_last_consumption = current_consumption_time - last_consumption_time
        calculated_tokens_to_consume = math.floor(time_from_last_consumption / consumption_rate)
        tokens_to_consume = min(total_tokens, calculated_tokens_to_consume)
        return tokens_to_consume

    @asynccontextmanager
    async def throttle(self) -> AsyncIterator[None]:
        """Context manager for rate-limited operations.

        Acquires the semaphore and adds a token before yielding,
        ensuring the operation respects both concurrency and rate limits.

        Yields:
            None - the caller can perform their rate-limited operation.
        """
        await self.semaphore.acquire()
        await self.add_token()
        try:
            yield
        finally:
            self.semaphore.release()

    async def __aenter__(self) -> 'RateLimiter':
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object]
    ) -> None:
        """Async context manager exit, ensures cleanup."""
        if exc_type:
            pass

        await self.close()

    async def close(self) -> None:
        """Clean up resources by cancelling the token consumer task."""
        if self.tokens_consumer_task and not self.tokens_consumer_task.cancelled():
            try:
                self.tokens_consumer_task.cancel()
                await self.tokens_consumer_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                raise
