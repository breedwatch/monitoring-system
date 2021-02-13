import pyudev
import psutil
import os
import time
from configuration.local_config import LocalConfig
from helper.info_helper import InfoHelper
import mapping
import shutil


class USBHandler:
    def __init__(self):
        from sensorlib.rgb import RGB
        self.led = RGB()
        self.config = LocalConfig()
        self.config.get_config_data()
        self.info_helper = InfoHelper()
        self.stick_path = ""

    @staticmethod
    def is_mounted():
        while True:
            context = pyudev.Context()
            removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if
                         device.attributes.asstring('removable') == "1"]

            for device in removable:
                partitions = [device.device_node for device in
                              context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]

                for partion in partitions:
                    path = f"/home/pi/usb-drive{partion}"
                    if not os.path.exists(os.path.join(path)):
                        os.system(f"sudo mkdir {os.path.join(path)}")
                    os.system(f"sudo mount {partion} {path}")
                    usb_found = True
                    print(path)
                    return usb_found, path
            time.sleep(5)

    def listen(self):
        while True:
            try:
                found, self.stick_path = self.is_mounted()
                if found:
                    # indicate that the stick was mounted
                    self.led.blink("green", 3, 0.3)

                    # list files / dirs on stick
                    stick_files = os.listdir(self.stick_path)
                    stick_device_path = f"{self.stick_path}/{self.config.device_name}"

                    for files in stick_files:
                        if self.config.device_name not in files:
                            if not os.path.exists(stick_device_path):
                                os.system(f"sudo mkdir {stick_device_path}")
                        else:
                            device_stick_files = os.listdir(stick_device_path)
                            for stick_files in device_stick_files:
                                if "conf.ini" in stick_files:
                                    os.system(f"sudo cp {stick_device_path}/conf.ini {mapping.config_path}")

                    self.info_helper.calc()

                    self.config.get_config_data()
                    if self.config.delete_after_usb:
                        shutil.move(mapping.info_log, f"{stick_device_path}/info.log")
                        time.sleep(0.5)
                        shutil.move(mapping.error_log, f"{stick_device_path}/error.log")
                        time.sleep(0.5)
                        os.system(f"touch {mapping.error_log}")
                        time.sleep(0.5)
                        shutil.move(mapping.data_dir_path, f"{self.stick_path}/{self.config.device_name}")

                        # create new data dir
                        os.system(f"mkdir {mapping.data_dir_path}")
                        # create fft dir
                        os.system(f"mkdir {mapping.data_dir_path}fft")
                        # create wav dir
                        os.system(f"mkdir {mapping.data_dir_path}wav")
                        # create data.json
                        os.system(f"touch {mapping.database_path}")

                    else:
                        shutil.copy(mapping.info_log, f"{stick_device_path}/info.log")
                        time.sleep(0.5)
                        shutil.copy(mapping.error_log, f"{stick_device_path}/error.log")
                        time.sleep(0.5)
                        shutil.copytree(mapping.data_dir_path, f"{self.stick_path}/{self.config.device_name}/data")
                        time.sleep(0.5)

                    os.system(f"sudo umount {self.stick_path}")
                    self.led.green()
                    time.sleep(30)
                    self.led.off()
                    os.system("sudo reboot")

            except Exception as e:
                print(e)
                self.led.blink("red", 2, 4)
                os.system(f"sudo umount {self.stick_path}")
            time.sleep(5)


config = LocalConfig()
config.get_config_data()
if config.scale_calibrated:
    handler = USBHandler()
    handler.listen()
