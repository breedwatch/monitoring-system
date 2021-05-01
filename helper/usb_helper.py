import os
import time
from configuration.local_config import LocalConfig
from helper.info_helper import InfoHelper
import mapping
import shutil
from helper.log_helper import ErrorHandler
from subprocess import call


class USBHelper:
    def __init__(self):
        self.config = LocalConfig()
        self.config.get_config_data()
        self.info_helper = InfoHelper()
        self.stick_path = mapping.usb_path
        self.error = ErrorHandler()

    def test_system(self):
        from dataset import Dataset
        sensor_is_ok = True

        dataset = Dataset()
        self.config.get_config_data()

        duration = self.config.audio["duration"]
        self.config.set_config_data("AUDIO", "duration", 10)

        try:
            for sensor, is_active in self.config.data.items():
                # get data from sensor if active
                if is_active:
                    is_data = dataset.get_data(sensor)
                    if not is_data:
                        sensor_is_ok = False

            if sensor_is_ok:
                return True
            else:
                return False

        except Exception as e:
            self.error.log.exception(e)
        finally:
            self.config.set_config_data("AUDIO", "duration", duration)

    def update_config(self):
        # copy conf.ini data to local from usb stick
        self.config.get_config_data()
        device_id = self.config.settings['device_id']
        scale_offset = self.config.scale["offset"]
        scale_ratio = self.config.scale["ratio"]
        scale_calibrated = self.config.scale["calibrated"]
        shutil.copy(os.path.join(self.config.usb_path, "conf.ini"), mapping.config_path)
        os.system(f"sudo chmod 755 {mapping.config_path}")
        self.config.get_config_data()
        self.config.set_config_data("SETTINGS", "device_id", device_id)
        self.config.set_config_data("SCALE", "ratio", scale_ratio)
        self.config.set_config_data("SCALE", "offset", scale_offset)
        self.config.set_config_data("SCALE", "calibrated", scale_calibrated)

        os.system(f"sudo rm {os.path.join(self.config.usb_path, 'conf.ini')}")

    def reset_scale(self):
        # set scale values to zero
        self.config.get_config_data()
        self.config.set_config_data("SCALE", "ratio", 0)
        self.config.set_config_data("SCALE", "offset", 0)
        self.config.set_config_data("SCALE", "calibrated", 0)

        os.system(f"sudo rm {os.path.join(self.config.usb_path, 'reset')}")

    def update_system(self):
        try:
            # update app data from github

            # create usb update file path
            usb_update_file = os.path.join(self.config.usb_path, "update.sh")

            # copy update file to local path
            shutil.copy(usb_update_file, mapping.update_file)

            # execute and remove update file
            os.system(f"sudo chmod 777 {mapping.update_file}")
            os.system(f"sudo rm {usb_update_file}")

            os.system(f"sudo sh {mapping.update_file}")

            os.system("sudo reboot")
        except Exception as e:
            self.error.log.exception(e)

        os.system("sudo reboot")

    def prepare_usb_drive(self):
        is_config = False
        is_scale_reset = False
        is_wittypi_script = False
        is_tara = False
        is_update = False
        is_wpa = False
        is_test = False
        is_sync_time = False
        try:
            # init
            if self.config.settings["device_id"] == "init":
                dirs = os.listdir(mapping.usb_path)
                for stick_dir in dirs:
                    if "." not in stick_dir and "System Volume Information" not in stick_dir:
                        self.config.set_config_data("SETTINGS", "device_id", stick_dir)
                        self.config.get_config_data()
            # create device dir on usb stick
            if not os.path.exists(self.config.usb_path):
                os.mkdir(self.config.usb_path)
                os.system(f"touch {os.path.join(self.config.usb_path, 'error.log')}")

            # calc information and write to stick
            self.info_helper.calc(self.config.usb_path)

            # create fft dir on usb stick
            if not os.path.exists(os.path.join(self.config.usb_path, "fft")):
                os.mkdir(os.path.join(self.config.usb_path, "fft"))

            # create wav dir on usb stick
            if not os.path.exists(os.path.join(self.config.usb_path, "wav")):
                os.mkdir(os.path.join(self.config.usb_path, "wav"))

            # list usb files
            device_stick_files = os.listdir(self.config.usb_path)
            for stick_files in device_stick_files:

                if "test" in stick_files:
                    is_test = True

                if "sync" in stick_files:
                    is_sync_time = True

                if "conf.ini" in stick_files:
                    is_config = True

                if "schedule.wpi" in stick_files:
                    is_wittypi_script = True

                if "tara" in stick_files:
                    is_tara = True

                if "reset" in stick_files:
                    is_scale_reset = True

                if "update.sh" in stick_files:
                    is_update = True

                if "wpa_supplicant.conf" in stick_files:
                    is_wpa = True

            if is_update:
                self.update_system()

            if is_sync_time:
                try:
                    call("/home/pi/wittypi/syncTime.sh")
                    os.system(f"sudo rm {os.path.join(self.config.usb_path, 'sync')}")
                except Exception as e:
                    self.error.log.exception(e)

            if is_test:
                from sensorlib.rgb import RGB
                os.system(f"sudo rm {os.path.join(self.config.usb_path, 'test')}")

                led = RGB()
                if not self.test_system():
                    led.red()
                    time.sleep(3600)
                else:
                    led.blink("green", 5, 1)
                os.system("sudo reboot")

            if is_config:
                self.update_config()

            if is_wittypi_script:
                # todo wittipy log wird voll
                shutil.copy(os.path.join(self.config.usb_path, "schedule.wpi"), mapping.witty_pi)
                os.system(f"sudo rm {os.path.join(self.config.usb_path, 'schedule.wpi')}")
                call(mapping.witty_pi)

            if is_tara:
                from sensorlib.scale import Scale
                scale = Scale()
                scale.tare()
                os.system(f"sudo rm {self.config.usb_path}/tara")
                time.sleep(5)
                os.system("sudo reboot")

            if is_scale_reset:
                self.reset_scale()

            if is_wpa:
                shutil.copy(os.path.join(self.config.usb_path, "wpa_supplicant.conf"), mapping.wpa_path)
                os.system(f"rm {os.path.join(self.config.usb_path, 'wpa_supplicant.conf')}")
                time.sleep(5)
                os.system("sudo reboot")

        except Exception as e:
            print(e)
