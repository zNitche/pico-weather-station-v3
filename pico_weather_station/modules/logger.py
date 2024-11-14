import os
import sys
import time
from lightberry import typing
from lightberry.utils import common_utils, files_utils
from pico_weather_station.utils import files_utils
from pico_weather_station import consts

if typing.TYPE_CHECKING:
    from typing import Callable
    from ds3231 import DateTime


class LoggerLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    EXCEPTION = "EXCEPTION"


class Logger:
    def __init__(self,
                 datetime_getter: Callable[[], DateTime],
                 debug_enabled: bool = False,
                 max_log_files: int = 7):

        self.debug_enabled = debug_enabled

        self.__datetime_getter = datetime_getter

        self.logs_path = consts.LOGS_DIR_PATH
        self.max_log_files = max_log_files

    def __log(self, message: str, level: str = LoggerLevel.INFO, exception: Exception = None):
        try:
            files_utils.create_dir_if_doesnt_exist(self.logs_path)
            self.__check_logs_files()

            datetime = self.__datetime_getter()
            # micropython doesn't seem to support sorting files by its creation date, use timestamp in name instead
            log_file_path = f"{self.logs_path}/{self.__get_current_log_file()}"

            with open(log_file_path, "a+") as file:
                file.write(f"{datetime.hour:02d}:{datetime.minutes:02d}:{datetime.seconds:02d} - {level} - {message}")
                file.write("\n")

                if exception is not None:
                    sys.print_exception(exception, file)

        except Exception as e:
            common_utils.print_debug(f"error while writing to log file: {str(e)}",
                                     debug_enabled=self.debug_enabled)

    def __check_logs_files(self):
        log_files = os.listdir(self.logs_path)
        files_count_diff = len(log_files) - self.max_log_files

        if files_count_diff > 0:
            sorted_log_files = files_utils.get_files_sorted_by_timestamp(files=log_files)

            for ind in range(files_count_diff):
                os.remove(f"{self.logs_path}/{sorted_log_files[ind]}")

    def __get_current_log_file(self):
        datetime = self.__datetime_getter()
        log_file_name = f"{datetime.year}-{datetime.month}-{datetime.day}.txt"

        for file in os.listdir(self.logs_path):
            if file.endswith(log_file_name):
                return file

        return f"{time.time()}_{log_file_name}"

    def exception(self, message: str, exception: Exception = None):
        self.__log(message=message, exception=exception, level=LoggerLevel.EXCEPTION)

    def error(self, message: str):
        self.__log(message=message, level=LoggerLevel.ERROR)

    def info(self, message: str):
        self.__log(message=message, level=LoggerLevel.INFO)

    def debug(self, message: str):
        if self.debug_enabled:
            self.__log(message=message, level=LoggerLevel.DEBUG)
