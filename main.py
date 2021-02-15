from dataset import Dataset
from configuration.local_config import LocalConfig
from helper.logger import ErrorHandler
import time
import os

data = Dataset()
config = LocalConfig()
config.get_config_data()
error = ErrorHandler()


if not config.scale_calibrated:
    # calibration
    try:
        from sensorlib.rgb import RGB
        led = RGB()
        led.blink("blue", 3, 0.3)
        led.red()
        time.sleep(15)
        led.off()
        data.scale.setup()
        led.green()
        time.sleep(15)
        data.scale.calibrate(config.calibrate_weight)
        led.off()
        led.blink("green", 3, 0.3)
        os.system("sudo reboot")
    except Exception as e:
        print(e)
        error.log.exception(e)
else:
    while True:
        # start measuring
        try:
            config.get_config_data()
            if config.audio_is_fft and config.sensor_microphone:
                data.get_fft_data()
            else:
                sensor_error = config.error_microphone + 1
            if config.audio_is_wav and config.sensor_microphone:
                data.write_wav()
            if config.sensor_scale:
                data.get_scale_data()
            if config.sensor_aht20:
                data.get_aht20_data()
            if config.sensor_dht22:
                data.get_dht22_data()
            if config.sensor_ds18b20:
                data.get_ds18b20_data()
            time.sleep(int(config.app_wait_seconds))
        except Exception as e:
            print(e)
            error.log.exception(e)
            continue
        except KeyboardInterrupt:
            exit()
