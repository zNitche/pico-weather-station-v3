from pico_weather_station.utils import csv_utils, files_utils
from pico_weather_station import devices_manager, cache_db, consts
from ds3231 import DateTime


class DataLoggerBase:
    def __init__(self, logs_per_hour: int, name: str):
        self.name = name

        self.__logs_path = consts.DATA_LOGS_DIR_PATH
        self.__logs_per_hour = logs_per_hour

        self.logging_schedule = self.__get_logging_schedule()
        self.last_logged: DateTime | None = None

        self._data_for_log: any = None

        self.__setup()

    def __setup(self):
        logs_path = self.get_logs_path()

        if files_utils.check_if_exists(logs_path):
            logs_content = csv_utils.get_csv_content(logs_path)
            iso_date_from_log = logs_content[-1].get("datetime") if len(logs_content) > 0 else None

            if iso_date_from_log is not None:
                self.last_logged = DateTime.from_iso(iso_date_from_log)

        cache_db.update(self.name, "last_logged", self.last_logged)

        active_loggers = cache_db.read(key="active_data_loggers", fallback_value=[])

        if self.name not in active_loggers:
            active_loggers.append(self.name)
            cache_db.write(key="active_data_loggers", value=active_loggers)

    def set_data_for_log(self, data: any):
        self._data_for_log = data

    def log(self, force: bool = False):
        if self.can_log() or force:
            self.__log_handler()

    def can_log(self):
        if self.last_logged is None:
            return True

        datetime = devices_manager.get_datetime()

        for schedule_time in self.logging_schedule:
            schedule_hour = schedule_time[0]
            schedule_minute = schedule_time[1]

            if schedule_hour == datetime.hour and schedule_minute == datetime.minutes:
                if not (self.last_logged.hour == datetime.hour and self.last_logged.minutes == datetime.minutes):
                    return True

        return False

    def __get_logging_schedule(self):
        schedule = []
        minutes_every_log = 60 // self.__logs_per_hour

        for hour in range(24):
            current_minutes = 0

            for _ in range(self.__logs_per_hour):
                schedule.append([hour, current_minutes])
                current_minutes += minutes_every_log

        return schedule

    def get_logs_path(self):
        datetime = devices_manager.get_datetime()

        if not datetime:
            return None

        logs_dir_path = f"{self.__logs_path}/{self.name}/{datetime.year}/{datetime.month}"
        files_utils.create_dir_if_doesnt_exist(logs_dir_path)

        return f"{logs_dir_path}/{datetime.day}.csv"

    def __log_handler(self):
        files_utils.create_dir_if_doesnt_exist(self.__logs_path)
        log_path = self.get_logs_path()

        if log_path is not None:
            if not files_utils.check_if_exists(log_path):
                csv_utils.init_csv_file(log_path, self.get_logs_header())

            rows = ",".join([str(v) for v in self.__get_log_row()])
            csv_utils.write_row(log_path, rows)

            self.last_logged = devices_manager.get_datetime()
            cache_db.update(self.name, "last_logged", self.last_logged)\

            self.__after_logged()
            self._data_for_log = None

    def get_logs_header(self):
        raise NotImplemented()

    def __get_log_row(self):
        raise NotImplemented()

    def __after_logged(self):
        pass
