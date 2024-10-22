from lightberry import ATaskBase
from pico_weather_station.data_loggers import MPPTDataLogger
from pico_weather_station import logger
from pico_weather_station.modules.integrations import RequestItem, MpptReader


class LogMPPTData(ATaskBase):
    def __init__(self, config: dict[str, any]):
        super().__init__(periodic_interval=60, init_delay=30, logging=config.get("DEBUG"))

        self.__device_address = config.get("SOLAR_REGULATOR_BLE_MAC_ADDRESS")
        self.__logs_per_hour = config.get("MPPT_DATA_LOGS_PER_HOUR")

        logging_retries = config.get("MPPT_LOGGING_RETRIES")
        self.__logging_retries = int(logging_retries) if logging_retries else 0

        self.__mppt_reader = self.__init_mppt_reader()
        self.__request_items = self.__init_request_items()

        self.__data_logger = MPPTDataLogger(logs_per_hour=self.__logs_per_hour)

    def __init_request_items(self):
        request_items = [
            RequestItem("12357", "Battery remaining capacity", 1, "%"),
            RequestItem("12358", "Battery voltage", 100, "V"),
            RequestItem("12359", "Battery current", 100, "A"),
            RequestItem("12360", "Battery power", 100, "W"),
            RequestItem("12361", "Battery power", 100, "W"),
            RequestItem("12362", "Load voltage", 100, "V"),
            RequestItem("12363", "Load current", 100, "A"),
            RequestItem("12364", "Load power", 100, "W"),
            RequestItem("12365", "Load power", 100, "W"),
            RequestItem("12366", "Solar voltage", 100, "V"),
            RequestItem("12367", "Solar current", 100, "A"),
        ]

        return request_items

    def __init_mppt_reader(self):
        return MpptReader(device_address=self.__device_address,
                          service_uuid=0xff00,
                          write_char_uuid=0xff02,
                          notify_char_uuid=0xff01,
                          logging=bool(self.logging))

    async def task(self):
        try:
            tries = self.__logging_retries + 1 if self.__logging_retries == 0 else self.__logging_retries

            if self.__data_logger.can_log():
                for _ in range(tries):
                    data = await self.__mppt_reader.read(self.__request_items)

                    if data is not None and len(data) == len(self.__request_items):
                        self.__data_logger.set_data_for_log(data)
                        self.__data_logger.log(force=True)

                        break

        except Exception as e:
            self._print_log(message="Error while logging mppt data", exception=e)
            logger.exception(message="Error while logging mppt data", exception=e)
