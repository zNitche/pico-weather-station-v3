import asyncio
from lightberry import ATaskBase, typing
from pico_weather_station.data_loggers import PVDataLogger
from pico_weather_station import logger, integrations_manager

if typing.TYPE_CHECKING:
    from lightberry.config import AppConfig
    from typing import Type


class LogPvData(ATaskBase):
    def __init__(self, config: Type[AppConfig]):
        super().__init__(periodic_interval=40, init_delay=60, logging=config.get("DEBUG"))

        self.__logs_per_hour = config.get("PV_DATA_LOGS_PER_HOUR")
        self.__logging_retries = int(config.get("PV_LOGGING_RETRIES")) if config.get("PV_LOGGING_RETRIES") else 0

        self.__data_logger = PVDataLogger(logs_per_hour=self.__logs_per_hour)

    async def task(self):
        try:
            tries = self.__logging_retries + 1 if self.__logging_retries == 0 else self.__logging_retries

            if self.__data_logger.can_log():
                data = None

                for _ in range(tries):
                    data = await integrations_manager.get_pv_readings()

                    if data is not None:
                        self.__data_logger.set_data_for_log(data)
                        self.__data_logger.log(force=True)

                        break

                    await asyncio.sleep(2)

                if data is None:
                    raise Exception("no data received")

        except Exception as e:
            self._print_log(message="Error while logging pv data", exception=e)
            logger.exception(message="Error while logging pv data", exception=e)
