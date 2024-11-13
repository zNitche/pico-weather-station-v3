import time
import gc
from ds3231 import DateTime
from pico_weather_station import machine_interfaces


def set_internal_rtc_time(datetime: DateTime):
    machine_interfaces.rtc.datetime([
        datetime.year, datetime.month, datetime.day, 0,
        datetime.hour, datetime.minutes, datetime.seconds, 0
    ])


def get_iso_time() -> str | None:
    try:
        tt = time.localtime()
        return f"{tt[0]}-{tt[1]}-{tt[2]}T{tt[3]:02d}:{tt[4]:02d}:{tt[5]:02d}.000Z"
    except:
        return None


def reset_heap(threshold: int = 8192):
    """use before memory heavy operations like allocating large lists / dicts"""
    gc.collect()

    #gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
    gc.threshold(threshold)
