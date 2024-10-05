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

    def get_battery_voltage(self) -> float:
        if not self.__battery_voltmeter:
            return 0

        return self.__battery_voltmeter.measure()

    def get_env_readings(self):
        if not self.__bme_280:
            return 0, 0, 0

        return self.__bme_280.get_readings()

    def get_datetime(self):
        if not self.__rtc:
            return None

        return self.__rtc.get_datetime()

    def set_datetime(self, datetime: DateTime):
        if self.__rtc:
            self.__rtc.set_datetime(datetime)
