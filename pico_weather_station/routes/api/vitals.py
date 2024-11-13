from lightberry import Router, Response
from lightberry.shortcuts import jsonify
from pico_weather_station import cache_db, devices_manager
from pico_weather_station.utils import machine_utils


vitals = Router("vitals", url_prefix="/api/vitals")


@vitals.route("/healthcheck")
async def healthcheck(request):
    return Response(status_code=200)


@vitals.route("/stats")
async def stats(request):
    last_log_for_loggers = {}
    active_loggers = cache_db.read(key="active_data_loggers", fallback_value=[])

    for logger in active_loggers:
        logger_data = cache_db.read(logger)
        last_log_date = logger_data.get("last_logged") if logger_data else None

        last_log_for_loggers[logger] = last_log_date.to_iso_string() if last_log_date else None

    datetime = devices_manager.get_datetime()

    data = {
        "datetime": {
            "internal": machine_utils.get_iso_time(),
            "external": datetime.to_iso_string() if datetime else None,
        },
        "battery_voltage": devices_manager.get_battery_voltage(),
        "internal_temperature": devices_manager.get_internal_temp(),
        "active_loggers": active_loggers,
        "last_log_for_loggers": last_log_for_loggers
    }

    return Response(payload=jsonify(data))
