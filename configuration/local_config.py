import configparser


class LocalConfig:
    def __init__(self):
        self.path = "/home/pi/conf.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

        self.settings = {}
        self.audio = {}
        self.scale = {}
        self.data = {}
        self.error = {}
        for sections in self.config.sections():



        # DEFAULT
        self.device_name = ""
        self.device_location = ""
        self.timezone = ""
        self.app_wait_seconds = ""
        self.errors_before_restart = ""
        self.median = ""
        self.delete_after_usb = ""

        # SCALE
        self.scale_ratio = ""
        self.scale_offset = ""
        self.scale_calibrated = ""
        self.calibrate_weight = int(self.config['SCALE']['calibrate_weight'])

        # AUDIO
        self.audio_fs = ""
        self.audio_duration = ""
        self.audio_is_wav = ""
        self.audio_is_fft = ""

        # SENSORS
        self.sensor_dht22 = ""
        self.sensor_ds18b20 = ""
        self.sensor_scale = ""
        self.sensor_microphone = ""
        self.sensor_aht20 = ""

        # ERROR
        self.error_dht22 = ""
        self.error_ds18b20 = ""
        self.error_scale = ""
        self.error_microphone = ""
        self.error_aht20 = ""

    def get_config_data(self):
        try:
            self.config.read(self.path)

            # DEFAULT
            self.device_name = self.config['SETTINGS']['device_name']
            self.device_location = self.config['SETTINGS']['device_location']
            self.timezone = self.config['SETTINGS']['timezone']
            self.app_wait_seconds = self.config['SETTINGS']['app_wait_seconds']
            self.errors_before_restart = int(self.config['SETTINGS']['errors_before_restart'])
            self.median = int(self.config['SETTINGS']['median'])
            self.delete_after_usb = self.config['SETTINGS'].getboolean('delete_after_usb')

            # SCALE
            self.scale_ratio = self.config['SCALE']['ratio']
            self.scale_offset = self.config['SCALE']['offset']
            self.scale_calibrated = self.config['SCALE'].getboolean('calibrated')

            # AUDIO
            self.audio_fs = self.config['AUDIO']['fs']
            self.audio_duration = self.config['AUDIO']['duration']
            self.audio_is_wav = self.config['AUDIO'].getboolean('wav')
            self.audio_is_fft = self.config['AUDIO'].getboolean('fft')

            # SENSORS
            self.sensor_dht22 = self.config['SENSORS'].getboolean('dht22')
            self.sensor_ds18b20 = self.config['SENSORS'].getboolean('ds18b20')
            self.sensor_scale = self.config['SENSORS'].getboolean('scale')
            self.sensor_microphone = self.config['SENSORS'].getboolean('microphone')
            self.sensor_aht20 = self.config['SENSORS'].getboolean('aht20')

            # ERROR
            self.error_ds18b20 = int(self.config['ERROR']['ds18b20'])
            self.error_scale = int(self.config['ERROR']['scale'])
            self.error_microphone = int(self.config['ERROR']['microphone'])
            self.error_aht20 = int(self.config['ERROR']['aht20'])

            return True
        except IOError:
            return False

    def get_all_sensors(self):
        sensors = {}
        for (each_key, each_val) in self.config.items("SENSORS"):
            if each_val == "1":
                each_val = True
            else:
                each_val = False
            sensors[each_key] = each_val

        return sensors

    def set_error(self, sensor, value):
        self.set_config_data("ERROR", sensor, value)

    def set_config_data(self, section, key, value):
        print(f"set config data {value}")
        self.config.set(section, key, str(value))
        self.write_config()

    def write_config(self):
        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)
        except IOError as e:
            print(e)

