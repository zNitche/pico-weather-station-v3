from lightberry import typing
from pico_weather_station.modules.integrations import MpptReader, RequestItem

if typing.TYPE_CHECKING:
    from lightberry.config import AppConfig
    from typing import Type


class IntegrationsManager:
    def __init__(self):
        self.logging = False

        self.__mppt_reader: MpptReader | None = None

    def setup_devices(self, config: Type[AppConfig]):
        self.__init_mppt_reader(device_address=config.get("SOLAR_REGULATOR_BLE_MAC_ADDRESS"))

    def __init_mppt_reader(self, device_address: str):
        if not device_address:
            return

        self.__mppt_reader = MpptReader(device_address=device_address,
                                        service_uuid=0xff00,
                                        write_char_uuid=0xff02,
                                        notify_char_uuid=0xff01,
                                        logging=self.logging)

    def get_mppt_request_items(self):
        request_items = [
            RequestItem("12357", "Battery remaining capacity", 1, "%"),
            RequestItem("12358", "Battery voltage", 100, "V"),
            RequestItem("12359", "Battery current", 100, "A"),
            RequestItem("12360", "Battery power", 100, "W"),
            RequestItem("12361", "Battery power", 100, "W"),
            RequestItem("12362", "Load voltage", 100, "V"),
            RequestItem("12363", "Load current", 100, "A"),
            RequestItem("12364", "Load power", 100, "W"),
            RequestItem("12365", "Load power", 100, "W"),
            RequestItem("12366", "Solar voltage", 100, "V"),
            RequestItem("12367", "Solar current", 100, "A"),
        ]

        return request_items

    async def get_pv_readings(self, request_items: list[RequestItem] | None = None):
        request_items = request_items if request_items is not None else self.get_mppt_request_items()
        data = await self.__mppt_reader.read(request_items)

        if data is None or len(data) != len(request_items):
            return None

        return data
