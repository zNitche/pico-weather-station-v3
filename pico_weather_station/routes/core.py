from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import peripherals_manager

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/sensors")
async def sensors(request: Request):
    temperature, pressure, humidity = peripherals_manager.get_env_readings()
    bat_voltage = peripherals_manager.get_battery_voltage()

    data = {
        "bat_voltage": bat_voltage,
        "temp": temperature,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))
