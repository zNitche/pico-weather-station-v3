from lightberry import Router, Response, typing
from pico_weather_station import devices_manager

if typing.TYPE_CHECKING:
    from lightberry import Request


settings = Router("settings", url_prefix="/api/settings")


@settings.route("/set_date", methods=["POST"])
async def set_date(request: Request):
    success = False
    target_datetime: str | None = request.body.get("datetime") if request.body else None

    if target_datetime:
        success = devices_manager.set_datetime(target_datetime)

    return Response(status_code=200 if success else 400)
