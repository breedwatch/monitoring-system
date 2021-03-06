from dataset import Dataset
from configuration.local_config import LocalConfig
from helper.log_helper import ErrorHandler
import time
import os
import csv
from helper.time_helper import get_file_time, set_timezone
from helper.usb_helper import USBHelper
from sensorlib.rgb import RGB
from subprocess import call
from datetime import datetime
import git
import mapping

repo = git.Repo(mapping.app_path)
master = repo.head.reference

led = RGB()
usb_handler = USBHelper()
usb_handler.prepare_usb_drive()

config = LocalConfig()
error = ErrorHandler()

current_version = config.settings['version']
git_version = master.commit.message

try:
    is_tmp = config.data['tmp117']
except KeyError:
    config.set_config_data('DATA', 'tmp117', 0)


dataset = Dataset()


if current_version != git_version:
    config.set_config_data('SETTINGS', 'version', git_version)


set_timezone(config.settings["timezone"])


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
    except Exception:
        return False


if not config.scale["calibrated"]:

    # config.get_config_data()
    # timestamp = datetime.now().strftime("%d.%M.%Y")
    # hive_id = config.settings['device_id']
    #
    # csv_name = f"{timestamp}_{hive_id}"

    # calibration
    try:
        # calibration mode
        led.blink("blue", 3, 0.3)
        # remove all items from scale please
        led.blink("red", 5, 1)
        dataset.scale.setup()
        # put the calibration weight on the scale
        led.blink("green", 15, 1)
        dataset.scale.calibrate(int(config.scale["calibrate_weight"]))
        # calibration done
        led.blink("green", 3, 0.3)

        try:
            # manual says: The syncTime.sh script is not supposed to be manually run...
            # call("/home/pi/wittypi/syncTime.sh")
            os.system("i2cset -y 1 0x69 10 1")
        except Exception as e:
            error.log.exception(e)

        if not usb_handler.test_system():
            led.red()
            time.sleep(3600)

        os.system("sudo reboot")
    except Exception as e:
        led.blink("red", 5, 0.5)
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
            csv_data.append(f"{config.settings['device_id']}")

            # add hum from aht20 to csv
            if 'hum' in dataset.data:
                csv_data.append(dataset.data["hum"])
            else:
                csv_data.append('NA')

            # add temp from aht20 or tmp117 to csv
            if 'temp' in dataset.data:
                csv_data.append(dataset.data["temp"])
            else:
                csv_data.append('NA')

            # add weight to csv
            if 'weight' in dataset.data:
                csv_data.append(dataset.data["weight"])
            else:
                csv_data.append('NA')

            # add all ds18b20
            ds18b20_counter = 0
            for key, val in dataset.data.items():
                if "ds18b20" in key:
                    csv_data.append(val)
                    ds18b20_counter += 1

            # add two values of zero if no temp sensor is available
            if ds18b20_counter == 0:
                csv_data.append('NA')
                csv_data.append('NA')

            # add one value of zero if one of two temp sensors are not available
            if ds18b20_counter == 1:
                csv_data.append('NA')

            if not write_data(csv_data):
                error.log.exception("data writing failed")

            if bool(config.settings["autoshutdown"]):
                os.system("sudo shutdown now")
            else:
                # sleep x Seconds (app_weight_seconds) (conf.ini)
                print('done')
                time.sleep(int(config.settings["app_wait_seconds"]))
        except Exception as e:
            print(e)
            error.log.exception(e)
            led.blink("red", 10, 0.3)
            continue