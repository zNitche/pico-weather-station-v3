import machine
import time
from pico_weather_station import machine_interfaces, consts


class Voltmeter:
    def __init__(self, pin: int | None = None):
        self.__adc = machine.ADC(pin) if pin is not None else machine_interfaces.adc_1

        self.__voltage_divider_ratio = 2

    def measure(self):
        adc_value = self.__adc.read_u16()

        adc_voltage = adc_value * consts.ADC_TO_VOLT_CONVERSION_FACTOR
        return adc_voltage * self.__voltage_divider_ratio

    def measure_with_sampling(self, samples_count: int = 20, delay: float = 0.05):
        value = 0

        for _ in range(samples_count):
            value += self.measure()
            time.sleep(delay)

        value = value / samples_count

        return value
