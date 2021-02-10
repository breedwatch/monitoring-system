from dataset import Dataset
from helper.time_helper import get_time
from configuration.local_config import LocalConfig
from helper.logger import ErrorHandler
import time
from sensorlib.rgb import RGB
from sensorlib.scale import Scale
import os

new_time = get_time()
data = Dataset()
config = LocalConfig()
config.get_config_data()
error = ErrorHandler()
led = RGB()
scale = Scale()

if not config.scale_calibrated:
    led.blink("blue", 3, 0.3)
    led.red()
    time.sleep(30)
    scale.setup()
    led.off()
    led.green()
    time.sleep(30)
    scale.calibrate(config.calibrate_weight)
    config.set_config_data("SCALE", "calibrated", 1)
    led.off()
    led.blink("green", 3, 0.3)
    os.system("sudo reboot")
else:
    while True:
        try:
            if config.sensor_microphone and not config.audio_is_wav:
                data.get_fft_data()
            if config.audio_is_wav:
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
            error.log(e)
            continue
        except KeyboardInterrupt:
            exit()
