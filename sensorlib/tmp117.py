import time
import board
import adafruit_tmp117


class TMP117:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.tmp117 = adafruit_tmp117.TMP117(i2c)

    def get_data(self):
        try:
            return {'temp': round(float(self.tmp117.temperature), 2)}
        except:
            return False