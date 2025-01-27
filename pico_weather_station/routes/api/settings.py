from lightberry import Router, Response, typing
from lightberry.shortcuts import jsonify
from pico_weather_station import devices_manager
from pico_weather_station.utils import machine_utils

if typing.TYPE_CHECKING:
    from lightberry import Request


settings = Router("settings", url_prefix="/api/settings")


@settings.route("/set-date", methods=["POST"])
async def set_date(request: Request):
    new_datetime = None
    target_datetime: str | None = request.body.get("datetime") if request.body else None

    if target_datetime:
        new_datetime = devices_manager.set_datetime(target_datetime)

        if new_datetime:
            machine_utils.set_internal_rtc_time(new_datetime)

    iso_datetime = new_datetime.to_iso_string() if new_datetime is not None else None

    return Response(status_code=200 if new_datetime else 400, payload=jsonify({"datetime": iso_datetime}))
