from pico_weather_station.routes.core import core

from lightberry import AppContext

current_app = AppContext.get_current_app()


@current_app.after_request()
async def after_request(response):
    response.add_header("Access-Control-Allow-Origin", "*")
    response.add_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.add_header("Access-Control-Allow-Headers", "Content-Type")

    return response
