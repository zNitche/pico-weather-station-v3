import machine


class InternalTempSensor:
    def __init__(self):
        self.__adc = machine.ADC(4)

    def get_temp(self):
        voltage = self.__adc.read_u16() * (2.99 / 65535)
        return 27 - (voltage - 0.706) / 0.001721
