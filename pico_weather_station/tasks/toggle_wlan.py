from lightberry import ATaskBase, typing
from pico_weather_station import logger, devices_manager

if typing.TYPE_CHECKING:
    from lightberry.modules import ServerHandlersManager
    from lightberry.config import AppConfig
    from typing import Type


class ToggleWlan(ATaskBase):
    def __init__(self, config: Type[AppConfig], server_handlers_manager: ServerHandlersManager):
        super().__init__(periodic_interval=300, init_delay=60, logging=config.get("DEBUG"))

        self.__wlan_schedule = config.get('WLAN_SCHEDULE')
        self.__server_handlers_manager = server_handlers_manager

    def __get_next_wlan_state(self):
        datetime = devices_manager.get_datetime()

        disable_at = self.__wlan_schedule[0]
        enable_at = self.__wlan_schedule[1]

        if datetime.hour >= disable_at or datetime.hour <= enable_at:
            return False

        if enable_at <= datetime.hour <= disable_at:
            return True

    async def task(self):
        try:
            wlan_state = self.__get_next_wlan_state()
            wlan_state_changed = self.__server_handlers_manager.toggle_wlan(wlan_state)

            if wlan_state_changed:
                self._print_log(message=f"WLAN state has been set to: {wlan_state}")
                logger.info(message=f"WLAN state has been set to: {wlan_state}")

        except Exception as e:
            self._print_log(message="Error while toggling wlan", exception=e)
            logger.exception(message="Error while toggling wlan", exception=e)
