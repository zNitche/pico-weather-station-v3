from pico_weather_station.utils import csv_utils, files_utils
from pico_weather_station import devices_manager, cache_db
from ds3231 import DateTime


class DataLoggerBase:
    def __init__(self, logs_path: str, logs_per_hour: int, name: str):
        self.name = name

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
                iso_date_from_log = logs_content[0].get("datetime")

                if iso_date_from_log is not None:
                    self.last_logged = DateTime.from_iso(iso_date_from_log)

        cache_db.update(self.name, "last_logged", self.last_logged)

    def log(self):
        datetime = devices_manager.get_datetime()

        if self.last_logged is None:
            self.__log_handler()

        else:
            for schedule_time in self.logging_schedule:
                schedule_hour = schedule_time[0]
                schedule_minute = schedule_time[1]

                if schedule_hour == datetime.hour and schedule_minute == datetime.minutes:
                    if not (self.last_logged.hour == datetime.hour and self.last_logged.minutes == datetime.minutes):
                        self.__log_handler()
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

    def get_logs_path(self):
        datetime = devices_manager.get_datetime()

        if not datetime:
            return None

        logs_dir_path = f"{self.__logs_path}/{datetime.year}/{datetime.month}"
        files_utils.create_dir_if_doesnt_exist(logs_dir_path)

        return f"{logs_dir_path}/{datetime.day}.csv"

    def get_logs_header(self):
        raise NotImplemented()

    def __get_log_row(self):
        raise NotImplemented()

    def __log_handler(self):
        raise NotImplemented()
