from pico_weather_station.sensors_manager import SensorsManager
from pico_weather_station.modules import InternalTempSensor


sensors_manager = SensorsManager()


def create_routers(app):
    from pico_weather_station.routes import core

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_tasks(app):
    from pico_weather_station import tasks

    app.add_background_task(tasks.LogWeather(config=app.config))


def setup_app(app):
    sensors_manager.setup_modules()

    setup_tasks(app)
    create_routers(app)
