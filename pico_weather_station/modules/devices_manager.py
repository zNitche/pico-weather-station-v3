from lightberry import typing
from lightberry.utils import common_utils
from bme280 import BME280
from ds3231 import DS3231, DateTime
from pico_weather_station import machine_interfaces
from pico_weather_station.modules import Voltmeter, InternalTempSensor

if typing.TYPE_CHECKING:
    from typing import Callable


class DevicesManager:
    def __init__(self, logging: bool = False):
        self.logging = logging

        self.__rtc: DS3231 | None = None
        self.__bme_280: BME280 | None = None

        self.__battery_voltmeter = Voltmeter()
        self.__internal_temp_sensor = InternalTempSensor()

    def setup_modules(self):
        self.__init_device("__rtc", lambda: DS3231(machine_interfaces.i2c_0))
        self.__init_device("__bme_280", lambda: BME280(machine_interfaces.i2c_0))

    def __init_device(self, module: str, init_handler: Callable):
        try:
            setattr(self, module, init_handler())

        except Exception as e:
            common_utils.print_debug(f"error while initializing {module}: {str(e)}",
                                     debug_enabled=self.logging)

    def __get_readings(self, handler: Callable, fallback_value=None):
        try:
            return handler()

        except Exception as e:
            common_utils.print_debug(f"error while getting sensor readings: {str(e)}",
                                     debug_enabled=self.logging)
            return fallback_value

    def get_env_readings(self) -> tuple[float, float, float]:
        return self.__get_readings(lambda: self.__bme_280.get_readings(), fallback_value=(0, 0, 0))

    def get_datetime(self) -> DateTime | None:
        return self.__get_readings(lambda: self.__rtc.get_datetime())

    def set_datetime(self, datetime: DateTime) -> bool:
        try:
            self.__rtc.set_datetime(datetime)
            return True

        except:
            return False

    def get_battery_voltage(self):
        return self.__battery_voltmeter.measure_with_sampling()

    def get_internal_temp(self):
        return self.__internal_temp_sensor.get_temp()
