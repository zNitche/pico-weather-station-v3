from lightberry import typing
from pico_weather_station.sensors_manager import SensorsManager
from pico_weather_station.modules import InternalTempSensor

if typing.TYPE_CHECKING:
    from lightberry import App

sensors_manager = SensorsManager(logging=True)


def create_routers(app: App):
    from pico_weather_station.routes import core, api

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())

    app.add_router(core)
    app.add_router(api.sensors)
    app.add_router(api.weather_data)


def setup_tasks(app: App):
    from pico_weather_station import tasks

    app.add_background_task(tasks.LogWeather(config=app.config))


def setup_app(app: App):
    sensors_manager.setup_modules()

    setup_tasks(app)
    create_routers(app)
