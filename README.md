# PicoWeatherStation v3

### Microcontroller requirements (frozen modules)

- [lightberryAPI v1.3.5](https://github.com/zNitche/lightberryAPI/releases/tag/v1.3.5)
- [bme280.py](https://github.com/zNitche/pico-bme280/blob/master/bme280.py)
- [ds3231.py](https://github.com/zNitche/pico-rtc-ds3231/blob/master/ds3231.py)
- [sdcard.py](https://github.com/micropython/micropython-lib/blob/v1.22.2/micropython/drivers/storage/sdcard/sdcard.py)

### Extra

### Development
packages in `requirements.txt` are used for development

```
pip3 install -r requirements.txt
```

#### Remote Shell
for flashing pico you can use `rshell`
```
pip3 install rshell==0.0.32
```

enter REPL
```
rshell 
repl
```

flash
```
rshell -f commands/flash
```

clear all files
```
rshell -f commands/wipe
```


### Notes (WIP)

```
+ (5v)

- | + (3.3v) | sda | scl
```
