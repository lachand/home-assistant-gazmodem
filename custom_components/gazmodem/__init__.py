"""
Initialisation du composant Home Assistant pour la chaudière.
"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configuration via configuration.yaml (optionnel)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration via l'interface utilisateur."""
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Suppression de l'entrée."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
