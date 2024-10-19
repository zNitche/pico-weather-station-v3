from lightberry import ATaskBase, typing
from pico_weather_station import logger, devices_manager

if typing.TYPE_CHECKING:
    from lightberry.modules import ServerHandlersManager


class ToggleWlan(ATaskBase):
    def __init__(self, config: dict[str, any], server_handler: ServerHandlersManager):
        super().__init__(periodic_interval=300, init_delay=60, logging=config.get("DEBUG"))

        self.wlan_schedule = config.get('WLAN_SCHEDULE')
        self.__server_handler = server_handler

    async def task(self):
        try:
            datetime = devices_manager.get_datetime()

            disable_at = self.wlan_schedule[0]
            enable_at = self.wlan_schedule[1]

            wlan_state = False if disable_at <= datetime.hour <= enable_at else True
            self.__server_handler.toggle_wlan(wlan_state)

            self._print_log(message=f"WLAN state has been set to: {wlan_state}")
            logger.info(message=f"WLAN state has been set to: {wlan_state}")

        except Exception as e:
            self._print_log(message="Error while toggling wlan", exception=e)
            logger.exception(message="Error while toggling wlan", exception=e)
