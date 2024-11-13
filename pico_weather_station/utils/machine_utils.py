import time


def get_iso_time() -> str | None:
    try:
        tt = time.localtime()
        return f"{tt[0]}-{tt[1]}-{tt[2]}T{tt[3]:02d}:{tt[4]:02d}:{tt[5]:02d}.000Z"
    except:
        return None
