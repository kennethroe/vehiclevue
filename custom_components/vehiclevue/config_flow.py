"""Config flow for Emporia Vue integration."""
import logging
import asyncio
import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from pyemvue import PyEmVue

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    vue = PyEmVue()
    loop = asyncio.get_event_loop()    
    result = await loop.run_in_executor(None, vue.login, data[CONF_EMAIL], data[CONF_PASSWORD])
    if not result:
        raise InvalidAuth
    
    # Return data to store in the config entry.
    return {
        "title": f"Emporia User {data[CONF_EMAIL]}",
        "gid": f"{vue.customer.customer_gid}",
    }


class ConfigFlow(config_entries.ConfigFlow, domain="vehiclevue"):
    """Handle a config flow for Emporia Vue settings."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                #prevent setting up the same account twice
                await self.async_set_unique_id(info["gid"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""

