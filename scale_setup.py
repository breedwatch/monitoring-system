from sensorlib.scale import Scale
import time
import os
scale = Scale()

print("hello! :)")
print("Bitte mal alles von der Waage nehmen...")
ready = input("Bereit? (Drueck Enter...)")

scale.setup()

print("das hat schonmal geklappt. Jetzt bitte 10Kg auflegen...")
yap = input("Ready? (Wieder Enter...)")
scale.calibrate(10000)
print("alles fertig... Starte neu in 10 Sekunden...")
time.sleep(10)
os.system("sudo reboot")
