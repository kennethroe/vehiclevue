from pyemvue import pyemvue, device
import json, datetime, asyncio
from datetime import datetime, timedelta
from pyemvue import PyEmVue
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry
from pyemvue.device import Vehicle, VehicleStatus
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from datetime import timedelta
import logging

from .const import DOMAIN, VUE_DATA, UPDATE_INTERVAL_SECONDS

# Update interval - too frequent will hit Emporia limits.
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL_SECONDS)

_LOGGER: logging.Logger = logging.getLogger(__name__)

device_information: dict[int, Vehicle] = {}  # data is the populated device objects

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    """Add vehicles in HA."""
    vue: PyEmVue = hass.data[DOMAIN][config_entry.entry_id][VUE_DATA]

    loop = asyncio.get_event_loop()
    vehicles = await loop.run_in_executor(None, vue.get_vehicles)

    vehicleSensors = []
    for vehicle in vehicles: 
        vehicleSensors.append(VehicleSensor(vue, vehicle))
        device_information[vehicle.vehicle_gid] = vehicle

    async_add_entities(vehicleSensors, True)
    _LOGGER.info("Monitoring ${len(vehicleSensors)} vehicles")

class VehicleSensor(SensorEntity, PyEmVue, Vehicle):

    """Representation of a Vehicle Battery Sensor."""
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, vueC, v):
       self.vue = vueC
       self.vehicle = v

    def update(self) -> None:
	
        # Fetch status from Vue client. 
        lastVehicleStatus  = self.vue.get_vehicle_status(self.vehicle.vehicle_gid)
        self.battery_level = lastVehicleStatus.battery_level 
        self.extra_attributes = lastVehicleStatus.as_dictionary()
      
        _LOGGER.info("Fetched vehicle status - battery level ${lastVehicleStatus.battery_level}")

    @property
    def native_value(self) -> str | None:
        return self.battery_level

    @property
    def name(self) -> str:
        return self.vehicle.display_name

    @property 
    def extra_state_attributes(self) -> str: 
        return  self.extra_attributes

    @property
    def unique_id(self):
        """Unique ID for the vehicle"""
        return f"sensor.vehiclevue.{self.vehicle.vehicle_gid}"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {
                # Unique identifiers within a specific domain
                (DOMAIN, self.vehicle.vehicle_gid)
            },
            "name": self.vehicle.display_name
        }
