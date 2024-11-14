import os
from lightberry import Router, Response, FileResponse
from lightberry.shortcuts import jsonify
from pico_weather_station import consts
from pico_weather_station.utils import files_utils


logs = Router("logs", url_prefix="/api/logs")


@logs.route("/")
async def all_logs(request):
    if not files_utils.check_if_exists(consts.LOGS_DIR_PATH):
        return Response(payload=jsonify({"logs": []}))

    sorted_files = files_utils.get_files_sorted_by_timestamp(path=consts.LOGS_DIR_PATH)
    files = [file.split("_")[1].replace(".txt", "") for file in sorted_files]

    return Response(payload=jsonify({"logs": files}))


@logs.route("/:date")
async def log_content(request, date: str):
    log_path = None

    for file in os.listdir(consts.LOGS_DIR_PATH):
        if file.endswith(f"{date}.txt"):
            log_path = f"{consts.LOGS_DIR_PATH}/{file}"

    if log_path is None:
        return Response(status_code=404)

    return FileResponse(file_path=log_path)
