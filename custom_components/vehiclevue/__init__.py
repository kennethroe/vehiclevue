"""The Emporia Vue integration."""
import asyncio
import logging
import voluptuous as vol

from pyemvue import PyEmVue

from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, VUE_DATA

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_EMAIL): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):

    hass.data.setdefault(DOMAIN, {})
    conf = config.get(DOMAIN)
    if not conf:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data={
                CONF_EMAIL: conf[CONF_EMAIL],
                CONF_PASSWORD: conf[CONF_PASSWORD],
            },
        )
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Emporia Vue from a config entry."""
    entry_data = entry.data
    email = entry_data[CONF_EMAIL]
    password = entry_data[CONF_PASSWORD]

    _LOGGER.info('Setting up Vue client for user ${email}')

    vue = PyEmVue(read_timeout=12)
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, vue.login, email, password)
        if not result:
            raise Exception("Could not authenticate with Emporia API")
        _LOGGER.debug("Logged in ${email}")
    except Exception:
        _LOGGER.error("Could not authenticate with Emporia API")
        return False

    try: 
        result = await loop.run_in_executor(None, vue.get_vehicles)
        if len(result) == 0: 
            raise Exception("No vehicles configured in Emporia account.")
    except Exception: 
        _LOGGER.error("No vehicles configured in Emporia account.")

    hass.data[DOMAIN][entry.entry_id] = {
        VUE_DATA: vue
    }

    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except Exception as err:
        _LOGGER.error("Error setting up platforms: %s", err)
        raise ConfigEntryNotReady(f"Error setting up platforms: {err}")

    return True
