from lightberry import ATaskBase, typing
from pico_weather_station import logger, devices_manager
from pico_weather_station.utils import machine_utils

if typing.TYPE_CHECKING:
    from lightberry.config import AppConfig
    from typing import Type

# onboard RTC can lose up to 3 seconds per day, this task aims to prevent it
class SyncInternalRTC(ATaskBase):
    def __init__(self, config: Type[AppConfig]):
        super().__init__(periodic_interval=21600, init_delay=300, logging=config.get("DEBUG"))

    async def task(self):
        try:
            current_time = devices_manager.get_datetime()

            if current_time is None:
                raise Exception("rtc datetime is None")

            machine_utils.set_internal_rtc_time(current_time)
            synced_time = machine_utils.get_iso_time()

            self._print_log(message=f"internal rtc has been synced, current datetime: {synced_time}")
            logger.info(message=f"internal rtc has been synced, current datetime: {synced_time}")

        except Exception as e:
            self._print_log(message="Error while toggling wlan", exception=e)
            logger.exception(message="Error while toggling wlan", exception=e)
