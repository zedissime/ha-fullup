"""Constants for the Fullup integration."""

from datetime import timedelta
from homeassistant.const import (
    PERCENTAGE,
    UnitOfVolume,
    UnitOfTemperature,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

DOMAIN = "fullup"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=30)

ATTR_TANK_ID = "tank_id"
ATTR_TANK_NAME = "tank_name"
ATTR_LAST_UPDATE = "last_update"
ATTR_ADDRESS_STREET = "address_street"
ATTR_ADDRESS_NUMBER = "address_number"
ATTR_ADDRESS_POSTCODE = "address_postcode"
ATTR_ADDRESS_CITY = "address_city"
ATTR_ADDRESS_COUNTRY = "address_country"
ATTR_OWNER_EMAIL = "owner_email"
ATTR_DEVICE_SERIAL = "device_full_serial"
ATTR_TANK_USAGE = "tank_usage"
ATTR_TANK_DIAMETER = "tank_diameter"
ATTR_TANK_HEIGHT = "tank_height"
ATTR_TANK_LENGTH = "tank_length"
ATTR_TANK_CHIMNEY = "tank_chimney"
ATTR_TANK_SHAPE = "tank_shape"
ATTR_TANK_TOTAL_VOLUME = "tank_total_volume"
ATTR_TANK_NOTIFICATION_LEVEL = "tank_notification_level"

# Sensor types
SENSOR_TYPES = {
    "current_volume": {
        "name": "Current Volume",
        "unit": UnitOfVolume.LITERS,
        "icon": "mdi:gauge",
        "device_class": SensorDeviceClass.VOLUME,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "current_volume_percentage": {
        "name": "Fill Level",
        "unit": PERCENTAGE,
        "icon": "mdi:gauge",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "current_temperature": {
        "name": "Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "battery_level": {
        "name": "Battery Level",
        "unit": "V",
        "icon": "mdi:battery",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "days_left": {
        "name": "Days Left",
        "unit": "days",
        "icon": "mdi:calendar-clock",
        "device_class": None,
        "state_class": None,
    },
    "last_measure_date": {
        "name": "Last Measure",
        "unit": None,
        "icon": "mdi:clock-outline",
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
    },
    "last_connection_date": {
        "name": "Last Connection",
        "unit": None,
        "icon": "mdi:clock-outline",
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
    },
    "total_volume": {
        "name": "Total Volume",
        "unit": UnitOfVolume.LITERS,
        "icon": "mdi:gauge",
        "device_class": SensorDeviceClass.VOLUME,
        "state_class": SensorStateClass.MEASUREMENT,
    },
}
