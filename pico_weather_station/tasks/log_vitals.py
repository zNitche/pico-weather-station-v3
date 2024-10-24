from lightberry import ATaskBase, typing
from pico_weather_station.data_loggers import VitalsDataLogger
from pico_weather_station import logger

if typing.TYPE_CHECKING:
    from lightberry.config import AppConfig
    from typing import Type


class LogVitals(ATaskBase):
    def __init__(self, config: Type[AppConfig]):
        super().__init__(periodic_interval=30, init_delay=30, logging=config.get("DEBUG"))

        self.__logs_per_hour = config.get("VITALS_LOGS_PER_HOUR")

        self.__data_logger = VitalsDataLogger(logs_per_hour=self.__logs_per_hour)

    async def task(self):
        try:
            self.__data_logger.log()

        except Exception as e:
            self._print_log(message="Error while logging station vitals", exception=e)
            logger.exception(message="Error while logging station vitals", exception=e)
