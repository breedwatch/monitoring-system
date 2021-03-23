
from gpiozero import RGBLED
from time import sleep

# for RGB LED


class RGB:
    def __init__(self):
        self.led = RGBLED(red=23, green=24, blue=25)
        self.led.off()

    def green(self):
        self.led.color = (0, 1, 0)

    def red(self):
        self.led.color = (1, 0, 0)

    def blue(self):
        self.led.color = (0, 0, 1)

    def off(self):
        self.led.color = (0, 0, 0)

    def blink(self, color, times, break_seconds):
        for i in range(times):
            if color == "green":
                self.green()
                sleep(break_seconds)
                self.off()
                sleep(break_seconds)

            if color == "red":
                self.red()
                sleep(break_seconds)
                self.off()
                sleep(break_seconds)

            if color == "blue":
                self.blue()
                sleep(break_seconds)
                self.off()
                sleep(break_seconds)
