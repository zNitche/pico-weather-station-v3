from lightberry import Router, Response
from lightberry.shortcuts import jsonify
from pico_weather_station import cache_db, sensors_manager


core = Router("core")


@core.route("/stats")
async def bulk_stats(request):
    datetime = sensors_manager.get_datetime()

    weather_logger_data = cache_db.read("weather_logger")
    last_weather_log = weather_logger_data.get("last_logged") if weather_logger_data else None

    data = {
        "datetime": datetime.to_iso_string() if datetime else None,
        "battery_voltage": sensors_manager.get_battery_voltage(),
        "last_weather_log": last_weather_log.to_iso_string() if last_weather_log else None
    }

    return Response(payload=jsonify(data))
