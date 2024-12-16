"""API client for Fullup."""

import logging
import asyncio
from typing import Optional, Any, List, Dict
from datetime import datetime, timedelta
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
            # First get tank IDs from public API
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

            # Then generate authentication token
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
        """Get all tanks data."""
        if not self._token or not self._tank_ids:
            if not await self.authenticate():
                return None

        try:
            tanks_data = []
            headers = {"Authorization": f"Bearer {self._token}"}

            for tank_id in self._tank_ids:
                # Get tank info
                async with async_timeout.timeout(10):
                    async with self._session.get(
                        f"{self._base_url}/tanks_public/{tank_id}", headers=headers
                    ) as response:
                        response.raise_for_status()
                        tank_info = await response.json()

                # Get tank data and history
                async with async_timeout.timeout(10):
                    async with self._session.get(
                        f"{self._base_url}/tanks/{tank_id}/data", headers=headers
                    ) as response:
                        response.raise_for_status()
                        tank_data = await response.json()

                # Combine tank info and data
                tank = tank_info.get("result", {})

                # Calculate daily consumption from history
                history = tank_data.get("result", [])
                tank["daily_consumption"] = self.calculate_daily_consumption(history)

                _LOGGER.debug("tank : %s", tank)
                tanks_data.append(tank)

            return tanks_data

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Failed to get tanks data: %s", err)
            return None

    async def get_tank_history(self, tank_id: str) -> List[Dict[str, Any]]:
        """Get historical data for a tank."""
        if not self._token:
            if not await self.authenticate():
                raise Exception("Authentication failed")

        headers = {"Authorization": f"Bearer {self._token}"}

        async with self._session.get(
            f"{self._base_url}/tanks/{tank_id}/data", headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("results", [])
            raise Exception(f"Failed to get tank history: {response.status}")

    def calculate_daily_consumption(self, history: List[Dict[str, Any]]) -> float:
        """Calculate daily consumption from historical data."""
        if not history or len(history) < 2:
            return 0.0

        # Sort history by date, most recent first
        sorted_history = sorted(
            history,
            key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00")),
            reverse=True,
        )

        latest = sorted_history[0]
        latest_date = datetime.fromisoformat(latest["date"].replace("Z", "+00:00"))

        # Find a measurement from approximately 24 hours ago
        target_date = latest_date - timedelta(days=1)
        previous = None

        for measure in sorted_history[1:]:
            measure_date = datetime.fromisoformat(
                measure["date"].replace("Z", "+00:00")
            )
            # Look for the closest measurement to 24h ago
            if measure_date <= target_date:
                previous = measure
                break

        if not previous:
            return 0.0

        # Calculate time difference in days
        previous_date = datetime.fromisoformat(previous["date"].replace("Z", "+00:00"))
        days_diff = (latest_date - previous_date).total_seconds() / 86400

        if days_diff <= 0:
            return 0.0

        # Calculate volume difference
        volume_diff = previous["volume"] - latest["volume"]

        # Calculate daily consumption
        daily_consumption = volume_diff / days_diff if days_diff > 0 else 0

        return round(
            max(0, daily_consumption), 1
        )  # Return positive value rounded to 1 decimal
