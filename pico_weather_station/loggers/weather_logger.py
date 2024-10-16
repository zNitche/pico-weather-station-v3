from pico_weather_station.utils import csv_utils, files_utils
from pico_weather_station import sensors_manager, cache_db
from ds3231 import DateTime


class WeatherLogger:
    def __init__(self, logs_path: str, logs_per_hour: int):
        self.__logs_path = logs_path
        self.__logs_per_hour = logs_per_hour

        self.logging_schedule = self.__get_logging_schedule()

        self.last_logged: DateTime | None = None

        self.__setup()

    def __setup(self):
        logs_path = self.get_logs_path()

        if files_utils.check_if_exists(logs_path):
            logs_content = csv_utils.get_csv_content(logs_path)

            if len(logs_content) > 0:
                iso_date_from_log = logs_content[0].get("DATETIME")

                if iso_date_from_log is not None:
                    self.last_logged = DateTime.from_iso(iso_date_from_log)

        cache_db.update("weather_logger", "last_logged", self.last_logged)

    def log(self):
        datetime = sensors_manager.get_datetime()

        if self.last_logged is None:
            self.__log_sensors_data()

        else:
            for schedule_time in self.logging_schedule:
                schedule_hour = schedule_time[0]
                schedule_minute = schedule_time[1]

                if schedule_hour == datetime.hour and schedule_minute == datetime.minutes:
                    if not (self.last_logged.hour == datetime.hour and self.last_logged.minutes == datetime.minutes):
                        self.__log_sensors_data()
                        break

    def __get_logging_schedule(self):
        schedule = []

        for hour in range(24):
            minutes_every_log = 60 // self.__logs_per_hour
            current_minutes = 0

            for _ in range(self.__logs_per_hour):
                schedule.append([hour, current_minutes])
                current_minutes += minutes_every_log

        return schedule

    def get_logs_header(self):
        return ["DATETIME", "TEMPERATURE", "HUMIDITY", "PRESSURE", "BATTERY_VOLTAGE", "INTERNAL_TEMP"]

    def __get_log_row(self):
        temp, humidity, pressure = sensors_manager.get_env_readings()
        bat_volt = sensors_manager.get_battery_voltage()
        internal_temp = sensors_manager.get_internal_temp()
        datetime = sensors_manager.get_datetime().to_iso_string()

        readings = [datetime, temp, humidity, pressure, bat_volt, internal_temp]

        return ",".join([str(v) for v in readings])

    def get_logs_path(self):
        datetime = sensors_manager.get_datetime()

        if not datetime:
            return None

        log_parts_paths = [
            f"{self.__logs_path}",
            f"{self.__logs_path}/{datetime.year}",
            f"{self.__logs_path}/{datetime.year}/{datetime.month}"
        ]

        for path in log_parts_paths:
            files_utils.create_dir_if_doesnt_exit(path)

        return f"{self.__logs_path}/{datetime.year}/{datetime.month}/{datetime.day}.csv"

    def __log_sensors_data(self):
        files_utils.create_dir_if_doesnt_exit(self.__logs_path)
        log_path = self.get_logs_path()

        if log_path is not None:
            if not files_utils.check_if_exists(log_path):
                csv_utils.init_csv_file(log_path, self.get_logs_header())

            csv_utils.write_row(log_path, self.__get_log_row())

            self.last_logged = sensors_manager.get_datetime()
            cache_db.update("weather_logger", "last_logged", self.last_logged)
