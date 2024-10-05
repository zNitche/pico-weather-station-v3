from pico_weather_station.peripherals_manager import PeripheralsManager

peripherals_manager = PeripheralsManager()


def create_routers(app):
    from pico_weather_station.routes import core

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_app(app):
    peripherals_manager.setup_modules()

    create_routers(app)
