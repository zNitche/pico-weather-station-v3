import os
from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import consts
from pico_weather_station.utils import files_utils, csv_utils

if typing.TYPE_CHECKING:
    from lightberry import Request


weather = Router("weather_data", url_prefix="/api/weather")


@weather.route("/years")
async def logged_years(request: Request):
    logs = os.listdir(consts.WEATHER_LOGS_DIR_PATH)\
        if files_utils.check_if_exists(consts.WEATHER_LOGS_DIR_PATH) else []

    return Response(payload=jsonify({"years": logs}))


@weather.route("/date/:year")
async def logged_months(request: Request, year: str):
    path = f"{consts.WEATHER_LOGS_DIR_PATH}/{year}"
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


@weather.route("/date/:year/:month")
async def logged_days(request: Request, year: str, month: str):
    path = f"{consts.WEATHER_LOGS_DIR_PATH}/{year}/{month}"

    if not files_utils.check_if_exists(path):
        return Response(status_code=404)

    logs = [file.replace(".csv", "") for file in os.listdir(path)] if files_utils.check_if_exists(path) else []

    return Response(payload=jsonify({"days": logs}))


@weather.route("/date/:year/:month/:day")
async def log_data(request: Request, year: str, month: str, day: str):
    path = f"{consts.WEATHER_LOGS_DIR_PATH}/{year}/{month}/{day}.csv"

    if not files_utils.check_if_exists(path):
        return Response(status_code=404)

    content = csv_utils.get_csv_content(path)

    return Response(payload=jsonify(content))


@weather.route("/log/:date")
async def log_for_date(request: Request, date: str):
    split_date = date.split("-")
    year, month, day = split_date

    file_path = f"{consts.WEATHER_LOGS_DIR_PATH}/{year}/{month}/{day}.csv"

    if not files_utils.check_if_exists(file_path):
        return Response(status_code=404)

    content = csv_utils.get_csv_content(file_path)

    return Response(payload=jsonify(content))
