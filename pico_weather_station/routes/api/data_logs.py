import os
from lightberry import Router, Response, typing, FileResponse
from lightberry.shortcuts import jsonify, is_query_param_equal, cast_query_param_to
from pico_weather_station import consts, cache_db
from pico_weather_station.utils import files_utils, csv_utils

if typing.TYPE_CHECKING:
    from lightberry import Request


data_logs = Router("data_logs", url_prefix="/api/data-logs")


@data_logs.route("/loggers")
async def loggers(request: Request):
    active_loggers = cache_db.read("active_data_loggers", fallback_value=[])

    return Response(payload=jsonify({"loggers": active_loggers}))


@data_logs.route("/logs/:logger_name/years")
async def logged_years(request: Request, logger_name: str):
    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}"

    if not files_utils.check_if_exists(path):
        Response(status_code=404)

    return Response(payload=jsonify({"years": os.listdir(path)}))


@data_logs.route("/date/:logger_name/:year")
async def logged_months(request: Request, logger_name: str, year: str):
    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}"
    months_logs = os.listdir(path) if files_utils.check_if_exists(path) else []

    include_days = is_query_param_equal(request, "include_days", "1")
    logs_data = []

    if not include_days:
        logs_data = months_logs
    else:
        for month in months_logs:
            log = {
                "month": month,
                "days": [file.replace(".csv", "") for file in os.listdir(f"{path}/{month}")]
            }

            logs_data.append(log)

    return Response(payload=jsonify({"months": logs_data}))


@data_logs.route("/date/:logger_name/:year/:month")
async def logged_days(request: Request, logger_name: str, year: str, month: str):
    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}/{month}"

    if not files_utils.check_if_exists(path):
        return Response(status_code=404)

    logs = [file.replace(".csv", "") for file in os.listdir(path)] if files_utils.check_if_exists(path) else []

    return Response(payload=jsonify({"days": logs}))


@data_logs.route("/date/:logger_name/:year/:month/:day")
async def log_data(request: Request, logger_name: str, year: str, month: str, day: str):
    raw = is_query_param_equal(request, "raw", "1")

    skip = cast_query_param_to(request, "skip", int, 0)
    limit = cast_query_param_to(request, "limit", int, 0)

    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}/{month}/{day}.csv"

    if not files_utils.check_if_exists(path):
        return Response(status_code=404)

    if raw:
        return FileResponse(file_path=path)

    content = csv_utils.get_csv_content(file_path=path, limit=limit, skip=skip)

    return Response(payload=jsonify(content))
