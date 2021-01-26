import pyudev
import psutil
import os
import time
from sensorlib.rgb import RGB
from configuration.local_config import LocalConfig

'''
    Beim Start (die ersten 30 Sekunden) - schaue ob USB Stick vorhanden
    Wenn ja:
        welche Daten sind auf dem Stick?
        ist conf.ini -> ueberschreibe alte conf.ini
        ist data -> uebertrage Daten auf stick und loesche alte Daten auf Karte
        ist tara -> tara waage

        schreibe error.log auf stick
        schreibe info.log auf stick (wieviel Platz ist auf der SD, wieviel belegt und wieviel insgesamt. 
        Dazu wie lange noch bis SD voll ist (Was soll passieren wenn SD voll?
        Sobald der Stick abgezogen wird, wird neugestartet und das Hauptprogramm gestartet
'''
led = RGB()
config = LocalConfig()
config.get_config_data()


def is_mounted():
    attempts = 0
    while attempts <= 30:
        context = pyudev.Context()
        removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if
                     device.attributes.asstring('removable') == "1"]

        for device in removable:
            partitions = [device.device_node for device in
                          context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            for partion in partitions:
                path = f"/home/pi/usb-drive{partion}"
                if not os.path.exists(os.path.join(path)):
                    os.makedirs(f"{os.path.join(path)}")
                os.system(f"sudo mount {partion} {path}")
                print(f"mounted {partion}")
                os.system(f"ls {path}")
                usb_found = True
                return usb_found, path
        attempts += 1
        print(f"{attempts} try ...")
        time.sleep(5)


def listen():
    try:
        found, path = is_mounted()
        if found:
            # mark that the stick was mounted
            led.green()
            time.sleep(3)
            led.off()

            stick_files = os.listdir(path)
            device_config = f"config_{config.device_name}"
            for files in stick_files:

                if device_config in files:
                    os.system(f"sudo cp {path}/{device_config}/conf.ini /home/pi/conf.ini")
                    # todo hier berechnung einfuegen fuer info.log

                data_files = os.listdir("/home/pi/beemo/data")
                device_path = f"{path}/{config.device_name}"

                if not os.path.exists(device_path):
                    os.system(f"sudo mkdir {device_path}")
                    os.system(f"sudo cp /home/pi/beemo/helper/error.log {path}/{config.device_name}/error.log")
                    # os.system(f"sudo cp /home/pi/beemo/helper/info.log {path}/{config.device_name}/info.log") # todo info.log muss erst geschrieben und berechnet werden mit neuer config

                for data_file in data_files:
                    done = os.system(
                        f"sudo cp /home/pi/beemo/data/{data_file} {path}/{config.device_name}/{data_file}")

                    if done == 0:
                        led.blink("blue", 1)
                    else:
                        led.blink("red", 2)

        os.system(f"sudo umount {path}")
        led.blink("green", 2)
    except Exception:
        led.blink("red", 2)


listen()
