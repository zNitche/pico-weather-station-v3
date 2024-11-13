import machine


rtc = machine.RTC()

i2c_0 = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
adc_1 = machine.ADC(27)

cs = machine.Pin(9, machine.Pin.OUT)
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(8))
