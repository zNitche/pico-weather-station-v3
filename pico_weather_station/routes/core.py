from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import sensors_manager

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/sensors")
async def sensors(request: Request):
    temperature, pressure, humidity = sensors_manager.get_env_readings()
    bat_voltage = sensors_manager.get_battery_voltage()
    internal_temp = sensors_manager.get_internal_temp()

    data = {
        "bat_voltage": bat_voltage,
        "temp": temperature,
        "internal_temp": internal_temp,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))
