import adafruit_dht
from helper.error_helper import ErrorHandler
import board


class DHT22:
    def __init__(self, pin):
        self.pin = pin
        self.data = {}
        self.error = ErrorHandler()

    def get_data(self):
        try:
            sensor = adafruit_dht.DHT22(board.D21, use_pulseio=False)
            # humidity, temperature = adafruit_dht.DHT22.read(sensor, self.pin)
            # self.data = {"temp": round(float(temperature), 2), "hum": round(float(humidity), 2)}
            self.data = sensor.temperature

            print(self.data)

            return self.data

        except Exception as e:
            print(e)
            self.error.log.exception(e)
            return False
