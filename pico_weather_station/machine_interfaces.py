import machine

i2c_0 = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
adc_1 = machine.ADC(27)
