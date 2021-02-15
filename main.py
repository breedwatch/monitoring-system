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

            for sensor, sensor_is_on in config.get_all_sensors().items():
                if sensor_is_on:
                    if not data.get_data(sensor):
                        print("error")

            time.sleep(int(config.app_wait_seconds))
        except Exception as e:
            error.log.exception(e)
            continue
        except KeyboardInterrupt:
            exit()
