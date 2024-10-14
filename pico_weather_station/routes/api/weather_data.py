import os
from lightberry import Router, Response
from lightberry.shortcuts import jsonify
from pico_weather_station import consts
from pico_weather_station.utils import files_utils, csv_utils


weather_data = Router("weather_data", url_prefix="/api/weather")


@weather_data.route("/")
async def logs(request):
    log_files = os.listdir(consts.WEATHER_LOGS_DIR_PATH)\
        if files_utils.check_if_exists(consts.WEATHER_LOGS_DIR_PATH) else []

    return Response(payload=jsonify({"files": log_files}))


@weather_data.route("/:date")
async def date_logs(request, date):
    file_path = f"{consts.WEATHER_LOGS_DIR_PATH}/{date}.csv"

    if not files_utils.check_if_exists(file_path):
        return Response(status_code=404)

    content = csv_utils.get_csv_content(file_path)

    return Response(payload=jsonify(content))
