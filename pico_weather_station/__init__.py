from lightberry import typing
from pico_weather_station import consts
from pico_weather_station.modules import InternalTempSensor, CacheDB, DevicesManager, Logger

if typing.TYPE_CHECKING:
    from lightberry import App


cache_db = CacheDB()
devices_manager = DevicesManager()

logger = Logger(max_log_files=7, datetime_getter=devices_manager.get_datetime)


def create_routers(app: App):
    from pico_weather_station.routes import core, api

    app.add_router(api.settings)

    app.add_router(api.sensors)
    app.add_router(api.data_logs)

    app.add_router(api.logs)
    app.add_router(api.vitals)

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_tasks(app: App):
    from pico_weather_station import tasks

    app.add_background_task(tasks.ToggleWlan(config=app.config, server_handler=app.server_handlers_manager))

    app.add_background_task(tasks.LogWeather(config=app.config))
    app.add_background_task(tasks.LogVitals(config=app.config))

    if app.config.get("MPPT_LOGGING_ENABLED"):
        app.add_background_task(tasks.LogMPPTData(config=app.config))


def setup_app(app: App):
    debug_enabled = app.config.get("DEBUG")

    logger.debug_enabled = debug_enabled

    devices_manager.logging = debug_enabled
    devices_manager.set_logger(logger)

    devices_manager.setup_modules()

    setup_tasks(app)
    create_routers(app)

    logger.info(message="app setup completed...")
