from lightberry import ATaskBase
from pico_weather_station.loggers import WeatherLogger
from pico_weather_station import consts, logger


class LogWeather(ATaskBase):
    def __init__(self, config: dict[str, any]):
        super().__init__(periodic_interval=30, init_delay=30, logging=config.get("DEBUG"))

        self.weather_logs_per_hour = config.get('WEATHER_LOGS_PER_HOUR')

        self.__weather_logger = WeatherLogger(logs_path=consts.WEATHER_LOGS_DIR_PATH,
                                              logs_per_hour=self.weather_logs_per_hour)

    async def task(self):
        try:
            self.__weather_logger.log()

        except Exception as e:
            self._print_log(message="Error while logging weather", exception=e)
            logger.exception(message="Error while logging weather", exception=e)
