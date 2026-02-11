"""Steam API client with error handling and rate limiting."""

import asyncio
import logging
import time
from typing import Any

import httpx

from config import settings

logger = logging.getLogger(__name__)


# Custom exceptions
class SteamAPIError(Exception):
    """Base exception for Steam API errors."""
    pass


class SteamRateLimitError(SteamAPIError):
    """Raised when Steam API rate limit is exceeded."""
    pass


class SteamAuthError(SteamAPIError):
    """Raised when API key is invalid or missing."""
    pass


class SteamNotFoundError(SteamAPIError):
    """Raised when requested resource is not found."""
    pass


class RateLimiter:
    """Token bucket rate limiter for Steam API requests."""

    def __init__(self, rate: int = 100, per: float = 60.0):
        """
        Args:
            rate: Number of requests allowed
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()

    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        await asyncio.sleep(0)  # Yield to event loop

        current = time.time()
        elapsed = current - self.last_check
        self.last_check = current

        self.allowance += elapsed * (self.rate / self.per)

        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1:
            sleep_time = self.per * (1 - self.allowance) / self.rate
            logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)
            self.allowance = 0
        else:
            self.allowance -= 1


# Global rate limiter
rate_limiter = RateLimiter(rate=100, per=60)


class SteamAPIClient:
    """Async HTTP client for Steam Web API with built-in error handling."""

    def __init__(self):
        self.base_url = settings.steam_api_base_url
        self.api_key = settings.steam_api_key
        self.timeout = settings.request_timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Initialize async HTTP client."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100
            )
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close async HTTP client."""
        if self._client:
            await self._client.aclose()

    async def get(
        self,
        interface: str,
        method: str,
        version: str = "v0002",
        params: dict[str, Any] | None = None,
        bypass_base_url: bool = False
    ) -> dict[str, Any]:
        """
        Make a GET request to Steam Web API.

        Args:
            interface: API interface name (e.g., ISteamUser)
            method: API method name (e.g., GetPlayerSummaries)
            version: API version (default: v0002)
            params: Query parameters (steamid, appid, etc.)
            bypass_base_url: If True, don't prepend base_url to the request

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPError: For HTTP errors
            ValueError: For invalid responses
        """
        # Acquire rate limit
        await rate_limiter.acquire()

        if params is None:
            params = {}

        # Always include API key
        params["key"] = self.api_key

        url = f"/{interface}/{method}/{version}/"

        if bypass_base_url:
            # For special endpoints that don't follow standard pattern
            full_url = url
        else:
            full_url = url

        try:
            response = await self._client.get(full_url, params=params)
            response.raise_for_status()

            data = response.json()

            # Check for Steam API errors
            if "error" in data:
                logger.error(f"Steam API error: {data['error']}")
                raise SteamAPIError(data["error"])

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            if e.response.status_code == 403:
                raise SteamAuthError("Invalid Steam API key") from e
            elif e.response.status_code == 429:
                raise SteamRateLimitError("Steam API rate limit exceeded") from e
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise SteamAPIError(f"Request failed: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise SteamAPIError(f"Unexpected error: {str(e)}") from e
