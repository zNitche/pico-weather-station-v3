from pico_weather_station.modules import Voltmeter
from pico_weather_station import machine_interfaces
from bme280 import BME280


voltmeter = Voltmeter()
bme_280 = BME280(machine_interfaces.i2c_0)


def create_routers(app):
    from pico_weather_station.routes import core

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_app(app):
    create_routers(app)
