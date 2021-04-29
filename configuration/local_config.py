import configparser
import mapping
from helper.log_helper import ErrorHandler


class LocalConfig:
    def __init__(self):
        self.path = mapping.config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.error_handler = ErrorHandler()

        self.settings = dict()
        self.audio = dict()
        self.scale = dict()
        self.data = dict()
        self.error = dict()

        self.usb_path = ""
        self.get_config_data()

    def get_config_data(self):
        try:
            self.config.read(self.path)
            for key, value in self.config.items("SETTINGS"):
                value = self.is_bool(value)
                self.settings[key] = value
            for key, value in self.config.items("SCALE"):
                value = self.is_bool(value)
                self.scale[key] = value
            for key, value in self.config.items("AUDIO"):
                value = self.is_bool(value)
                self.audio[key] = value
            for key, value in self.config.items("DATA"):
                value = self.is_bool(value)
                self.data[key] = value
            for key, value in self.config.items("ERROR"):
                value = self.is_bool(value)
                self.error[key] = value

            self.usb_path = f"{mapping.usb_path}/{self.settings['device_id']}"
        except IOError:
            return False

    @staticmethod
    def is_bool(value):
        if value == "1":
            return True
        elif value == "0":
            return False
        else:
            return value

    def set_error(self, sensor, value):
        self.set_config_data("ERROR", sensor, value)

    def set_config_data(self, section, key, value):
        self.config.set(section, key, str(value))
        self.write_config()

    def write_config(self):
        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)
            configfile.close()
        except Exception as e:
            self.error_handler.log.exception(e)
