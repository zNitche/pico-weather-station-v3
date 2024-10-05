from sdcard import SDCard
import uos
from lightberry import Server, App, AppContext
from lightberry.utils import common_utils, files_utils
from pico_weather_station import setup_app, machine_interfaces
import consts


def mount_sd_card():
    sd_card = SDCard(machine_interfaces.spi, machine_interfaces.cs)

    vfs = uos.VfsFat(sd_card)
    uos.mount(vfs, consts.SD_CARD_PATH)


def main():
    app = App()

    with AppContext(app):
        setup_app(app)

        server = Server(app=app)
        server.start()


if __name__ == '__main__':
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB", debug_enabled=True)

    mount_sd_card()
    main()
