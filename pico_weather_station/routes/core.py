from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import peripherals_manager, battery_voltmeter, internal_temp_sensor

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/sensors")
async def sensors(request: Request):
    temperature, pressure, humidity = peripherals_manager.get_env_readings()
    bat_voltage = battery_voltmeter.measure()
    internal_temp = internal_temp_sensor.get_temp()

    data = {
        "bat_voltage": bat_voltage,
        "temp": temperature,
        "internal_temp": internal_temp,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))
