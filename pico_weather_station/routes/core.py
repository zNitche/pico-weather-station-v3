from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import voltmeter, bme_280

if typing.TYPE_CHECKING:
    from lightberry import Request


core = Router("core")


@core.route("/sensors")
async def sensors(request: Request):
    temperature, pressure, humidity = bme_280.get_readings()

    data = {
        "bat_voltage": voltmeter.measure_with_sampling(),
        "temp": temperature,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))
