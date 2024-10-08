from pico_weather_station.sensors_manager import SensorsManager
from pico_weather_station.modules import Voltmeter, InternalTempSensor


sensors_manager = SensorsManager()
battery_voltmeter = Voltmeter()
internal_temp_sensor = InternalTempSensor()


def create_routers(app):
    from pico_weather_station.routes import core

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_app(app):
    sensors_manager.setup_modules()

    create_routers(app)
