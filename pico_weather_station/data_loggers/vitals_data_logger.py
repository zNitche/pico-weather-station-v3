from pico_weather_station import devices_manager
from pico_weather_station.data_loggers.data_logger_base import DataLoggerBase


class VitalsDataLogger(DataLoggerBase):
    def __init__(self, logs_per_hour: int):
        super().__init__(logs_per_hour=logs_per_hour, name="vitals_logger")

    def get_logs_header(self):
        return ["datetime", "internal_temperature", "battery_voltage"]

    def __get_log_row(self):
        bat_volt = devices_manager.get_battery_voltage()
        internal_temp = devices_manager.get_internal_temp()
        datetime = devices_manager.get_datetime().to_iso_string()

        return [datetime, internal_temp, bat_volt]
