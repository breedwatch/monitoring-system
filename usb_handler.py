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

    def prepare_usb_drive(self):
        try:
            found, self.stick_path = self.is_mounted()
            if found:
                # list files / dirs on stick
                stick_files = os.listdir(self.stick_path)
                stick_device_path = f"{self.stick_path}/{self.config.settings['device_name']}"

                for files in stick_files:
                    if self.config.settings['device_name'] not in files:
                        if not os.path.exists(stick_device_path):
                            os.mkdir(stick_device_path)
                    else:
                        device_stick_files = os.listdir(stick_device_path)
                        for stick_files in device_stick_files:
                            if "conf.ini" in stick_files:
                                self.config.get_config_data()
                                scale_offset = self.config.scale["offset"]
                                scale_ratio = self.config.scale["ratio"]
                                is_calibrated = self.config.scale["calibrated"]
                                shutil.copy(os.path.join(stick_device_path, "conf.ini"), mapping.config_path)
                                self.config.set_config_data("SCALE", "ratio", scale_ratio)
                                self.config.set_config_data("SCALE", "offset", scale_offset)
                                self.config.set_config_data("SCALE", "calibrated", is_calibrated)
                                break

                self.config.get_config_data()
                if self.config.settings["delete_after_usb"]:
                    shutil.move(mapping.data_dir_path, f"{self.stick_path}/{self.config.settings['device_name']}")

                    # create new data dir
                    os.mkdir(os.path.join(mapping.data_dir_path, "data"))
                    # create fft dir
                    os.mkdir(os.path.join(mapping.data_dir_path, "fft"))
                    # create wav dir
                    os.mkdir(os.path.join(mapping.data_dir_path, "wav"))
                    # create data.csv
                    os.system(f"touch {mapping.csv_data_path}")

                else:
                    shutil.copytree(mapping.data_dir_path,
                                    f"{self.stick_path}/{self.config.settings['device_name']}/data")
                    time.sleep(0.5)

                if self.info_helper.calc():
                    shutil.move(mapping.info_log, f"{stick_device_path}/info.log")
                    time.sleep(0.5)

                shutil.move(mapping.error_log, f"{stick_device_path}/error.log")
                time.sleep(0.5)
                os.mknod(mapping.error_log)
                os.system(f"sudo chmod 755 {mapping.error_log}")
                time.sleep(0.5)

                os.system(f"sudo umount {self.stick_path}")
                os.system("sudo reboot")

        except Exception as e:
            os.system(f"sudo umount {self.stick_path}")
        time.sleep(5)
