from pico_weather_station.utils import csv_utils, files_utils
from pico_weather_station import devices_manager, cache_db, logger
from pico_weather_station.data_loggers.data_logger_base import DataLoggerBase


class WeatherDataLogger(DataLoggerBase):
    def __init__(self, logs_path: str, logs_per_hour: int):
        super().__init__(logs_path, logs_per_hour, "weather_logger")

    def get_logs_header(self):
        return ["datetime", "temperature", "humidity", "pressure", "battery_voltage", "internal_temp"]

    def __get_log_row(self):
        temp, humidity, pressure = devices_manager.get_env_readings()
        bat_volt = devices_manager.get_battery_voltage()
        internal_temp = devices_manager.get_internal_temp()
        datetime = devices_manager.get_datetime().to_iso_string()

        readings = [datetime, temp, humidity, pressure, bat_volt, internal_temp]

        return ",".join([str(v) for v in readings])

    def __log_handler(self):
        files_utils.create_dir_if_doesnt_exist(self.__logs_path)
        log_path = self.get_logs_path()

        if log_path is not None:
            if not files_utils.check_if_exists(log_path):
                csv_utils.init_csv_file(log_path, self.get_logs_header())

            csv_utils.write_row(log_path, self.__get_log_row())

            self.last_logged = devices_manager.get_datetime()

            cache_db.update(self.name, "last_logged", self.last_logged)
            logger.info(message="weather data has been logged successfully")
