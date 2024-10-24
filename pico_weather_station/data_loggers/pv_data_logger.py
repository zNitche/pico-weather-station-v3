from pico_weather_station import devices_manager, logger
from pico_weather_station.data_loggers.data_logger_base import DataLoggerBase
from pico_weather_station.modules.integrations import ResponseItem


class PVDataLogger(DataLoggerBase):
    def __init__(self, logs_per_hour: int):
        super().__init__(logs_per_hour=logs_per_hour, name="pv_logger")

    def get_logs_header(self):
        return ["datetime", "battery_capacity", "battery_voltage", "battery_current", "load_voltage",
                "load_current", "solar_voltage", "solar_current"]

    def __get_log_row(self):
        data: list[ResponseItem] = self._data_for_log

        datetime = devices_manager.get_datetime().to_iso_string()
        battery_capacity = data[0].value
        battery_voltage = data[1].value
        battery_current = data[2].value
        load_voltage = data[5].value
        load_current = data[6].value
        solar_voltage = data[9].value
        solar_current = data[10].value

        return [datetime, battery_capacity, battery_voltage, battery_current, load_voltage,
                load_current, solar_voltage, solar_current]

    def __after_logged(self):
        logger.info(message="pv data has been logged successfully")
