from pico_weather_station.peripherals_manager import PeripheralsManager
from pico_weather_station.modules import Voltmeter, InternalTempSensor


peripherals_manager = PeripheralsManager()
battery_voltmeter = Voltmeter()
internal_temp_sensor = InternalTempSensor()


def create_routers(app):
    from pico_weather_station.routes import core

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_app(app):
    peripherals_manager.setup_modules()

    create_routers(app)
