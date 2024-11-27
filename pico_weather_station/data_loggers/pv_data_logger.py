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
        rounded_data = [round(v.value, 2) if isinstance(v.value, float) else v.value for v in data]

        battery_capacity = rounded_data[0]
        battery_voltage = rounded_data[1]
        battery_current = rounded_data[2]
        load_voltage = rounded_data[5]
        load_current = rounded_data[6]
        solar_voltage = rounded_data[9]
        solar_current = rounded_data[10]

        return [datetime, battery_capacity, battery_voltage, battery_current, load_voltage,
                load_current, solar_voltage, solar_current]

    def __after_logged(self):
        logger.info(message="pv data has been logged successfully")
