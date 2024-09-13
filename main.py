from lightberry import Server, App, AppContext
from lightberry.utils import common_utils, files_utils
from pico_weather_station import setup_app


def main():
    app = App()

    with AppContext(app):
        setup_app(app)

        server = Server(app=app)
        server.start()


if __name__ == '__main__':
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB", debug_enabled=True)

    main()
