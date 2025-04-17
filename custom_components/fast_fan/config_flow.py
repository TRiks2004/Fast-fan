from __future__ import annotations

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

import ipaddress
import voluptuous as vol
import logging
import re

from .const import DOMAIN 

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("ip"): str,
    vol.Required("token"): str
})


class InvalidIP(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidToken(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

def validate_ip(ip: str) -> None:
    try:
        ipaddress.ip_address(ip)
    except ValueError as e:
        raise InvalidIP(f"Invalid IP address: {e}")
    
def validate_token(token: str) -> None:
    if not re.fullmatch(r'[a-fA-F0-9]{32}', token):
        raise InvalidToken("Token must be a 32-character hexadecimal string")

def validate_input(hass: HomeAssistant, data):
    validate_ip(data.get("ip", ""))
    validate_token(data.get("token", ""))
        

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):

        errors = {}
        if user_input is not None:
            try:
                validate_input(self.hass, user_input)
                
                return self.async_create_entry(
                    title="Fan", 
                    data=user_input
                )
            except InvalidIP:
                errors["ip"] = "invalid_ip"
                _LOGGER.error("Invalid IP address provided: %s", user_input.get("ip"))
            except InvalidToken:
                errors["token"] = "invalid_token"
                _LOGGER.error("Invalid token provided: %s", user_input.get("token"))
            except Exception:
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )