# PicoWeatherStation v3

### Requirements (Microcontroller)

- [lightberryAPI v1.3.0](https://github.com/zNitche/lightberryAPI/releases/tag/v1.3.0) - frozen module
- [bme280.py](https://github.com/zNitche/pico-bme280/blob/master/bme280.py) - frozen module

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
