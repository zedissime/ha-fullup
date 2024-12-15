"""API client for Fullup."""

import logging
import asyncio
from typing import Optional

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)


class FullupApiClient:
    """API client for Fullup."""

    def __init__(self, session: aiohttp.ClientSession, email: str, password: str):
        """Initialize the API client."""
        self._session = session
        self._email = email
        self._password = password
        self._token = None
        self._base_url = "https://api.fullup.be"
        self._tank_ids = []

    async def authenticate(self) -> bool:
        """Authenticate with Fullup API."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(
                    f"{self._base_url}/loginApi",
                    params={"email": self._email, "password": self._password},
                ) as response:
                    try:
                        response.raise_for_status()
                        data = await response.json()
                        tank_ids = data.get("result", [])
                        self._tank_ids = tank_ids
                    except aiohttp.ClientError as err:
                        _LOGGER.error("Failed to get tank IDs: %s", err)
                        return False

            async with async_timeout.timeout(10):
                async with self._session.post(
                    f"{self._base_url}/auth/generate",
                    json={"email": self._email, "password": self._password},
                ) as response:
                    try:
                        response.raise_for_status()
                        data = await response.json()
                        self._token = data.get("result", {}).get("token")
                    except aiohttp.ClientError as err:
                        _LOGGER.error(
                            "Failed to generate authentication token: %s", err
                        )
                        return False
            return bool(self._token and self._tank_ids)

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Failed to authenticate with Fullup: %s", err)
            return False

    async def get_tanks(self) -> Optional[list]:
        if not self._token or not self._tank_ids:
            if not await self.authenticate():
                return None

        try:
            tanks_data = []
            headers = {"Authorization": f"Bearer {self._token}"}

            for tank_id in self._tank_ids:
                async with async_timeout.timeout(10):
                    async with self._session.get(
                        f"{self._base_url}/tanks_public/{tank_id}", headers=headers
                    ) as response:
                        response.raise_for_status()
                        tank_info = await response.json()

                async with async_timeout.timeout(10):
                    async with self._session.get(
                        f"{self._base_url}/tanks/{tank_id}/data", headers=headers
                    ) as response:
                        response.raise_for_status()
                        tank_data = await response.json()

                tank = tank_info.get("result", {})
                tanks_data.append(tank)

            return tanks_data

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Failed to get tanks data: %s", err)
            return None
