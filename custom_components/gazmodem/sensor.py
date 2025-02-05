"""
Sensor pour récupérer les valeurs de la chaudière via TCP.
"""
import asyncio
import struct
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

SENSOR_TYPES = {
    "Ballon tampon": 30,
    "Depart radiateurs": 31,
    "ECS": 33,
    "Chaudiere": 35,
    "Temperature exterieure": 36,
    "Temperature de consigne": 90,
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Configuration des capteurs."""
    host = entry.data.get("host")
    port = entry.data.get("port", 23)
    sensors = [GazModemSensor(name, host, port, index) for name, index in SENSOR_TYPES.items()]
    async_add_entities(sensors, True)

class GazModemSensor(Entity):
    """Représentation du capteur de température de la chaudière."""

    def __init__(self, name, host, port, index):
        self._name = name
        self._host = host
        self._port = port
        self._index = index
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Récupération des données de la chaudière."""
        try:
            reader, writer = await asyncio.open_connection(self._host, self._port)
            writer.write(b'REQUEST_DATA')
            await writer.drain()
            data = await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            self._state = self.parse_data(data)
        except Exception:
            self._state = None

    def parse_data(self, data):
        """Parse les données reçues."""
        segments = data.split(b'\xC2')
        if len(segments) == 97:
            extracted_values = {}
            for name, index in SENSOR_TYPES.items():
                if index < len(segments) and len(segments[index]) >= 4:
                    try:
                        extracted_values[name] = struct.unpack('<f', segments[index][:4])[0]
                    except:
                        extracted_values[name] = None
            return extracted_values
        return None
