import os
import sys
from lightberry import typing
from lightberry.utils import common_utils
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

            log_file_name = f"{datetime.year}-{datetime.month}-{datetime.day}.txt"
            log_file_path = f"{self.logs_path}/{log_file_name}"

            with open(log_file_path, "a+") as file:
                file.write(f"{datetime.hour}:{datetime.minutes}:{datetime.seconds} - {level} - {message}")
                file.write("\n")

                if exception is not None:
                    sys.print_exception(exception, file)

        except Exception as e:
            common_utils.print_debug(f"error while writing to log file: {str(e)}",
                                     debug_enabled=self.debug_enabled)

    def __check_logs_files(self):
        log_files = sorted(os.listdir(self.logs_path))

        if len(log_files) > self.max_log_files:
            os.remove(f"{self.logs_path}/{log_files[0]}")

    def exception(self, message: str, exception: Exception = None):
        self.__log(message=message, exception=exception, level=LoggerLevel.EXCEPTION)

    def error(self, message: str):
        self.__log(message=message, level=LoggerLevel.ERROR)

    def info(self, message: str):
        self.__log(message=message, level=LoggerLevel.INFO)

    def debug(self, message: str):
        if self.debug_enabled:
            self.__log(message=message, level=LoggerLevel.DEBUG)
