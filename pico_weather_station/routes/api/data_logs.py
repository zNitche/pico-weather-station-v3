import os
from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
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


@data_logs.route("/logs/:logger_name/:date")
async def log_for_date(request: Request, logger_name: str, date: str):
    split_date = date.split("-")
    year, month, day = split_date

    file_path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}/{month}/{day}.csv"

    if not files_utils.check_if_exists(file_path):
        return Response(status_code=404)

    content = csv_utils.get_csv_content(file_path)

    return Response(payload=jsonify(content))


@data_logs.route("/date/:logger_name/:year")
async def logged_months(request: Request, logger_name: str, year: str):
    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}"
    months_logs = os.listdir(path) if files_utils.check_if_exists(path) else []

    include_days = True if request.query_params.get("include_days") == "1" else False
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
    path = f"{consts.DATA_LOGS_DIR_PATH}/{logger_name}/{year}/{month}/{day}.csv"

    if not files_utils.check_if_exists(path):
        return Response(status_code=404)

    content = csv_utils.get_csv_content(path)

    return Response(payload=jsonify(content))
