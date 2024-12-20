from lightberry import typing
from lightberry.utils import common_utils
from bme280 import BME280
from ds3231 import DS3231, DateTime
from pico_weather_station import machine_interfaces
from pico_weather_station.modules import Voltmeter, InternalTempSensor, Logger

if typing.TYPE_CHECKING:
    from typing import Callable


class DevicesManager:
    def __init__(self, logging: bool = False, logger: Logger | None = None):
        self.logging = logging
        self.__logger = logger

        self.__rtc: DS3231 | None = None
        self.__bme280: BME280 | None = None

        self.__battery_voltmeter = Voltmeter()
        self.__internal_temp_sensor = InternalTempSensor()

    def set_logger(self, logger: Logger):
        self.__logger = logger

    def setup_modules(self):
        self.__init_device("__rtc", lambda: DS3231(machine_interfaces.i2c_0))
        self.__init_device("__bme280", lambda: BME280(machine_interfaces.i2c_0),
                           post_init=lambda: self.__bme280.get_readings()) # <- workaround for bme280 first read spike

    def __init_device(self, module: str, init_handler: Callable, post_init: Callable | None = None):
        try:
            if hasattr(self, module):
                mod = init_handler()
                setattr(self, module, mod)

                if post_init is not None:
                    post_init()

        except Exception as e:
            self.__log(message=f"error while initializing {module}", exception=e)

    def __get_readings(self, module: str, handler: Callable, fallback_value=None):
        try:
            return handler()

        except Exception as e:
            self.__log(message=f"error while getting sensor readings {module}", exception=e)

            return fallback_value

    def get_env_readings(self) -> tuple[float, float, float]:
        return self.__get_readings("bme280", lambda: self.__bme280.get_readings(), fallback_value=(0, 0, 0))

    def get_datetime(self) -> DateTime | None:
        return self.__get_readings("rtc", lambda: self.__rtc.get_datetime())

    def set_datetime(self, datetime: DateTime | str) -> DateTime | None:
        try:
            dt = DateTime.from_iso(datetime) if type(datetime) == str else datetime
            self.__rtc.set_datetime(dt)
            return self.__rtc.get_datetime()

        except:
            return None

    def is_rtc_accurate(self) -> bool:
        try:
            return not self.__rtc.is_osf_set()

        except:
            return False

    def get_battery_voltage(self):
        return self.__battery_voltmeter.measure_with_sampling()

    def get_internal_temp(self):
        return self.__internal_temp_sensor.get_temp()

    def __log(self, message: str, exception: Exception | None):
        common_utils.print_debug(origin="DEVICES_MANAGER",
                                 message=message, exception=exception,
                                 debug_enabled=self.logging)

        if self.__logger:
            if exception:
                self.__logger.exception(message=message, exception=exception)

            else:
                self.__logger.info(message=message)
