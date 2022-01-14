from configuration.local_config import LocalConfig


class Reset:
    def __init__(self):
        self.config = LocalConfig()

    def reset_settings(self):
        self.config.set_config_data("SETTINGS", "timezone", "Europe/Berlin")
        self.config.set_config_data("SETTINGS", "device_id", "init")
        self.config.set_config_data("SETTINGS", "app_wait_seconds", 2700)
        self.config.set_config_data("SETTINGS", "errors_before_restart", 3)
        self.config.set_config_data("SETTINGS", "median", 5)
        self.config.set_config_data("SETTINGS", "version", "0.2.2")
        self.config.set_config_data("SETTINGS", "autoshutdown", 1)

    def reset_audio(self):
        self.config.set_config_data("AUDIO", "duration", 600)
        self.config.set_config_data("AUDIO", "fs", 8000)
        self.config.set_config_data("AUDIO", "nperseg", 4096)
        self.config.set_config_data("AUDIO", "noverlap", 2048)
        self.config.set_config_data("AUDIO", "nfft", 4096)

    def reset_scale(self):
        self.config.set_config_data("SCALE", "ratio", 0)
        self.config.set_config_data("SCALE", "offset", 0)
        self.config.set_config_data("SCALE", "calibrated", 0)
        self.config.set_config_data("SCALE", "calibrate_weight", 12250)

    def reset_data(self):
        self.config.set_config_data("DATA", "scale", 1)
        self.config.set_config_data("DATA", "dht22", 0)
        self.config.set_config_data("DATA", "ds18b20", 1)
        self.config.set_config_data("DATA", "fft", 0)
        self.config.set_config_data("DATA", "wav", 1)
        self.config.set_config_data("DATA", "aht20", 1)
        self.config.set_config_data("DATA", "tmp117", 0)


reset = Reset()
exiting = False
print("Reset all?")
user_input = input('(y/n): ')

if user_input == 'y':
    reset.reset_settings()
    reset.reset_audio()
    reset.reset_scale()
    reset.reset_data()
    print('done!')
    exiting = True

if not exiting:
    if user_input == "n":
        print("options:")
        print("(1) SETTINGS")
        print("(2) AUDIO")
        print("(3) SCALE")
        print("(4) DATA")
        print("(5) exit")
    while not exiting:
            user_option_input = input('what do you want?: ')
            if user_option_input == '1':
                reset.reset_settings()
            if user_option_input == '2':
                reset.reset_audio()
            if user_option_input == '3':
                reset.reset_scale()
            if user_option_input == '4':
                reset.reset_data()
            if user_option_input == '5':
                exiting = True

print('bye!')
