import logging
import mapping

logging.basicConfig(filename=mapping.error_log, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


class ErrorHandler:
    def __init__(self):
        self.log = logging.getLogger(__name__)


class SensorDataError(Exception):
    def __init__(self, sensor_name):
        logging.exception(f"| sensor: {sensor_name} -> No sensor_data check wiring or replace")
