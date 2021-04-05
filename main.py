from dataset import Dataset
from configuration.local_config import LocalConfig
from helper.log_helper import ErrorHandler
import time
import os
import csv
from helper.time_helper import get_file_time
from helper.usb_helper import USBHelper
from sensorlib.rgb import RGB

led = RGB()
usb_handler = USBHelper()
usb_handler.prepare_usb_drive()
dataset = Dataset()
config = LocalConfig()
error = ErrorHandler()




def write_data(data):
    """
    format: time, device+location, hum, temp, weight, ds18b20x
    :param data: csv list data
    :return: bool
    """
    try:
        with open(os.path.join(f"{config.usb_path}/data.csv"),
                  mode='a+') as dataset_file:
            dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            dataset_writer.writerow(data)
        dataset_file.close()

        return True
    except Exception as e:
        print(e)
        return False


if not config.scale["calibrated"]:

    # calibration
    try:
        # calibration mode
        led.blink("blue", 3, 0.3)
        # remove all items from scale please
        led.blink("red", 30, 1)
        dataset.scale.setup()
        # put the calibration weight on the scale
        led.blink("green", 30, 1)
        dataset.scale.calibrate(int(config.scale["calibrate_weight"]))
        # all done
        led.blink("green", 3, 0.3)
        # reboot system
        os.system("sudo reboot")
    except Exception as e:
        led.blink("red", 5, 0.3)
        error.log.exception(e)
else:
    while True:
        # start measuring
        try:
            # reset csv_data list
            csv_data = list()

            # reset dataset data
            dataset.data = dict()

            # get config data
            config.get_config_data()

            # add time first
            dataset.timestamp = get_file_time()
            csv_data.append(dataset.timestamp)

            # iterate all sensors in DATA (conf.ini)
            for sensor, is_active in config.data.items():
                # get data from sensor if active
                if is_active:
                    dataset.get_data(sensor)

            # add device id and location
            csv_data.append(f"{config.settings['device_location']}{config.settings['device_name']}")

            # add hum from aht20 to csv
            if 'hum' in dataset.data:
                csv_data.append(dataset.data["hum"])
            else:
                csv_data.append(00)

            # add temp from aht20 to csv
            if 'temp' in dataset.data:
                csv_data.append(dataset.data["temp"])
            else:
                csv_data.append(00)

            # add weight to csv
            if 'weight' in dataset.data:
                csv_data.append(dataset.data["weight"])
            else:
                csv_data.append(00)

            # add all ds18b20
            for key, val in dataset.data.items():
                if "ds18b20" in key:
                    csv_data.append(val)

            if not write_data(csv_data):
                error.log.exception("data writing failed")

            os.system("sudo shutdown now")

            # sleep x Seconds (app_weight_seconds) (conf.ini)
            # time.sleep(int(config.settings["app_wait_seconds"]))
        except Exception as e:
            led.blink("red", 10, 0.3)
            error.log.exception(e)
            continue
