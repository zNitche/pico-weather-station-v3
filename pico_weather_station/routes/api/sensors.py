from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import sensors_manager

if typing.TYPE_CHECKING:
    from lightberry import Request


sensors = Router("sensors", url_prefix="/api/sensors")


@sensors.route("/")
async def bulk(request: Request):
    temperature, pressure, humidity = sensors_manager.get_env_readings()
    internal_temp = sensors_manager.get_internal_temp()

    data = {
        "temp": temperature,
        "internal_temp": internal_temp,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))
