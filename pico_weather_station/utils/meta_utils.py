import json
from ds3231 import DateTime
from pico_weather_station import consts


def write_startup_data(date: DateTime | None):
    current_data = get_metadata()

    with open(consts.META_FILE_PATH, "w") as file:
        current_data["startup_datetime"] = date.to_iso_string() if date else None

        file.write(json.dumps(current_data))


def get_metadata():
    try:
        with open(consts.META_FILE_PATH, "r") as file:
            return json.loads(file.read())

    except:
        return {}
