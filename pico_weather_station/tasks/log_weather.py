from lightberry import ATaskBase
from pico_weather_station.loggers import WeatherLogger
from pico_weather_station import consts


class LogWeather(ATaskBase):
    def __init__(self, config: dict[str, any]):
        debug_enabled = config.get("DEBUG")
        super().__init__(periodic_interval=30, init_delay=30, logging=debug_enabled)

        self.weather_logs_per_hour = config.get('WEATHER_LOGS_PER_HOUR')

        self.__logger = WeatherLogger(logs_path=consts.WEATHER_LOGS_DIR_PATH,
                                      logs_per_hour=self.weather_logs_per_hour)

    async def task(self):
        try:
            self.__logger.log()

        except Exception as e:
            self._print_log(message="Error while logging weather", exception=e)
