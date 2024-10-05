from pico_weather_station.modules import Voltmeter
from pico_weather_station import machine_interfaces
from bme280 import BME280
from ds3231 import DS3231, DateTime


class PeripheralsManager:
    def __init__(self):
        self.__battery_voltmeter: Voltmeter | None = None
        self.__rtc: DS3231 | None = None
        self.__bme_280: BME280 | None = None

    def setup_modules(self):
        self.__init_device("__battery_voltmeter", lambda: Voltmeter())
        self.__init_device("__rtc", lambda: DS3231(machine_interfaces.i2c_0))
        self.__init_device("__bme_280", lambda: BME280(machine_interfaces.i2c_0))

    def __init_device(self, attr, initializer):
        try:
            setattr(self, attr, initializer())

        except Exception as e:
            print(f"error while initializing {attr}: {str(e)}")

    def __get_readings(self, handler, fallback_value=None):
        try:
            return handler()

        except:
            return fallback_value

    def get_battery_voltage(self) -> float:
        return self.__get_readings(lambda: self.__battery_voltmeter.measure(), fallback_value=0)

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
