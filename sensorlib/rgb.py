
from gpiozero import RGBLED
from time import sleep

# for RGB LED


class RGB:
    def __init__(self):
        self.led = RGBLED(red=19, green=16, blue=20)
        self.led.off()

    def green(self):
        self.led.color = (0, 1, 0)

    def red(self):
        self.led.color = (1, 0, 0)

    def blue(self):
        self.led.color = (0, 0, 1)

    def off(self):
        self.led.color = (0, 0, 0)

    def blink(self, color, times):
        for i in range(times):
            if color == "green":
                self.green()
                sleep(0.5)
                self.off()
                sleep(0.5)

            if color == "red":
                self.red()
                sleep(0.5)
                self.off()
                sleep(0.5)

            if color == "blue":
                self.blue()
                sleep(0.5)
                self.off()
                sleep(0.5)
