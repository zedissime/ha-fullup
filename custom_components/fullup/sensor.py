"""Support for Fullup sensors."""

from datetime import datetime
import logging
from typing import Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Fullup sensor."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for sensor_data in coordinator.data:
        # Add standard sensors
        for sensor_type in SENSOR_TYPES:
            if sensor_type == "total_volume":
                # Special handling for total volume
                if "tank_total_volume" in sensor_data:
                    entities.append(
                        FullupSensor(
                            coordinator,
                            sensor_data["tank_id"],
                            sensor_type,
                            sensor_data["tank_name"],
                        )
                    )
            elif sensor_type in sensor_data:
                entities.append(
                    FullupSensor(
                        coordinator,
                        sensor_data["tank_id"],
                        sensor_type,
                        sensor_data["tank_name"],
                    )
                )

    async_add_entities(entities)


class FullupSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a Fullup sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        tank_id: str,
        sensor_type: str,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._tank_id = tank_id
        self._sensor_type = sensor_type
        self._tank_name = tank_name

        self._attr_name = f"{tank_name} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{tank_id}_{sensor_type}"
        self._attr_device_class = SENSOR_TYPES[sensor_type]["device_class"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_state_class = SENSOR_TYPES[sensor_type]["state_class"]

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, tank_id)},
            name=tank_name,
            manufacturer="Fullup",
            model="Tank Sensor",
        )

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        for tank_data in self.coordinator.data:
            if tank_data["tank_id"] == self._tank_id:
                if self._sensor_type == "current_volume_percentage":
                    return round(
                        (tank_data["current_volume"] / tank_data["tank_total_volume"])
                        * 100,
                        1,
                    )
                elif self._sensor_type == "total_volume":
                    return tank_data.get("tank_total_volume")
                elif self._sensor_type == "current_temperature":
                    temp = tank_data.get(self._sensor_type)
                    return round(temp, 1) if temp is not None else None
                elif self._sensor_type in ["last_measure_date", "last_connection_date"]:
                    date_str = tank_data[self._sensor_type]
                    if date_str:
                        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                return tank_data.get(self._sensor_type)
        return None
