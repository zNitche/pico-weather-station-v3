from lightberry import Router, Response
from lightberry.shortcuts import jsonify
from pico_weather_station import devices_manager, integrations_manager


sensors = Router("sensors", url_prefix="/api/sensors")


@sensors.route("/")
async def bulk(request):
    temperature, pressure, humidity = devices_manager.get_env_readings()
    internal_temp = devices_manager.get_internal_temp()

    data = {
        "temp": temperature,
        "internal_temp": internal_temp,
        "pressure": pressure,
        "humidity": humidity
    }

    return Response(payload=jsonify(data))


@sensors.route("/pv")
async def pv_data(request):
    data = await integrations_manager.get_pv_readings()

    if not data:
        return Response(status_code=204)

    res = {
        "battery_capacity": data[0].value,
        "battery_voltage": data[1].value,
        "battery_current": data[2].value,
        "load_voltage": data[5].value,
        "load_current": data[6].value,
        "solar_voltage": data[9].value,
        "solar_current": data[10].value,
    }

    return Response(payload=jsonify(res))
