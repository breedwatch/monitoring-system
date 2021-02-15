# Version 0.1
from dataset import Dataset
from configuration.local_config import LocalConfig
from helper.logger import ErrorHandler
import time
import os

data = Dataset()
config = LocalConfig()
config.get_config_data()
error = ErrorHandler()

if not config.scale["calibrated"]:
    # calibration
    try:
        from sensorlib.rgb import RGB
        led = RGB()
        # calibration mode
        led.blink("blue", 3, 0.3)
        # remove all items from scale please
        led.blink("red", 30, 1)
        data.scale.setup()
        # put the calibration weight on the scale
        led.blink("green", 15, 1)
        data.scale.calibrate(int(config.scale["calibrate_weight"]))
        # all done
        led.blink("green", 3, 0.3)
        # reboot system
        os.system("sudo reboot")
    except Exception as e:
        error.log.exception(e)
else:
    while True:
        # start measuring
        try:
            # iterate all sensors in DATA (conf.ini)
            for sensor in config.data:
                # get data from sensor
                data.get_data(sensor)

            # sleep x Seconds (app_weight_seconds) (conf.ini)
            time.sleep(int(config.settings["app_wait_seconds"]))
        except Exception as e:
            error.log.exception(e)
            continue
        except KeyboardInterrupt:
            exit()
