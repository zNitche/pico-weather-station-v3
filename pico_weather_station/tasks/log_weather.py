from lightberry.tasks.aio import ATaskBase


class LogWeather(ATaskBase):
    def __init__(self, config: dict[str, any]):
        debug_enabled = config.get("DEBUG")
        super().__init__(periodic_interval=60, init_delay=60, logging=debug_enabled)

        self.weather_logs_per_hour = config.get('WEATHER_LOGS_PER_HOUR')

    async def task(self):
        pass
