import board
import adafruit_ahtx0
from helper.logger import ErrorHandler


class AHT20:
    def __init__(self):
        self.sensor = adafruit_ahtx0.AHTx0(board.I2C())
        self.error = ErrorHandler()

    def get_data(self):
        try:
            temp = self.sensor.temperature
            hum = self.sensor.relative_humidity
            status = True

            data = {"temp": round(float(temp), 1), "hum": round(float(hum), 1), "status": status}
            return data
        except Exception as e:
            self.error.log.exception(e)
            return False
