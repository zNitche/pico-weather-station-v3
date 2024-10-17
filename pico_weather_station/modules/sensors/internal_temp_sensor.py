import machine
from pico_weather_station import consts


class InternalTempSensor:
    def __init__(self):
        self.__adc = machine.ADC(4)

    def get_temp(self):
        voltage = self.__adc.read_u16() * consts.ADC_TO_VOLT_CONVERSION_FACTOR
        return 27 - (voltage - 0.706) / 0.001721
