import Adafruit_DHT
from helper.error_helper import ErrorHandler


class DHT22:
    def __init__(self, pin):
        self.pin = pin
        self.data = {}
        self.error = ErrorHandler()

    def get_data(self):
        try:
            sensor = Adafruit_DHT.DHT22
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
            self.data = {"temp": round(float(temperature), 2), "hum": round(float(humidity), 2)}

            return self.data

        except Exception as e:
            self.error.log.exception(e)
