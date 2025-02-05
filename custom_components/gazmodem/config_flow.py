"""
Gestion de la configuration via l'interface utilisateur Home Assistant.
"""
from homeassistant import config_entries
import voluptuous as vol

DATA_SCHEMA = vol.Schema({
    vol.Required("host"): str,
    vol.Optional("port", default=23): int,
})

class GazModemConfigFlow(config_entries.ConfigFlow, domain="gazmodem"):
    """Gestion du flux de configuration."""

    async def async_step_user(self, user_input=None):
        """Étape de configuration utilisateur."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="GazModem", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
