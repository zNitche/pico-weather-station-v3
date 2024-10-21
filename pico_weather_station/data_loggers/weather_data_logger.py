from pico_weather_station import devices_manager, logger
from pico_weather_station.data_loggers.data_logger_base import DataLoggerBase


class WeatherDataLogger(DataLoggerBase):
    def __init__(self, logs_per_hour: int):
        super().__init__(logs_per_hour=logs_per_hour, name="weather_logger")

    def get_logs_header(self):
        return ["datetime", "temperature", "humidity", "pressure"]

    def __get_log_row(self):
        temp, humidity, pressure = devices_manager.get_env_readings()
        datetime = devices_manager.get_datetime().to_iso_string()

        return [datetime, temp, humidity, pressure]

    def __after_logged(self):
        logger.info(message="weather data has been logged successfully")
