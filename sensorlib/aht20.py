import board
import adafruit_ahtx0
from helper.log_helper import ErrorHandler


class AHT20:
    def __init__(self):
        try:
            self.sensor = adafruit_ahtx0.AHTx0(board.I2C())
            self.error = ErrorHandler()
        except Exception as e:
            print("no AHT20!!!")
            print(e)

    def get_data(self):
        try:
            temp = self.sensor.temperature
            hum = self.sensor.relative_humidity
            status = True

            data = {"temp": round(float(temp), 2), "hum": round(float(hum), 2), "status": status}
            return data
        except Exception as e:
            self.error.log.exception(e)
            return False
