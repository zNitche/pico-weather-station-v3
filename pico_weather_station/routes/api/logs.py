import os
from lightberry import Router, Response
from lightberry.shortcuts import jsonify
from pico_weather_station import consts
from pico_weather_station.utils import files_utils


logs = Router("logs", url_prefix="/api/logs")


@logs.route("/")
async def all_logs(request):
    files = os.listdir(consts.LOGS_DIR_PATH)\
        if files_utils.check_if_exists(consts.LOGS_DIR_PATH) else []

    files = [file.replace(".txt", "") for file in files]

    return Response(payload=jsonify({"logs": files}))


@logs.route("/:date")
async def log_content(request, date: str):
    log_path = f"{consts.LOGS_DIR_PATH}/{date}.txt"

    if not files_utils.check_if_exists(log_path):
        return Response(status_code=404)

    with open(log_path, "r") as file:
        rows = [row.replace("\n", "") for row in file.readlines()]

    return Response(payload=jsonify(rows))
