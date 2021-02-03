'''
is sensor in config?
is error counter <= 3?

get sensor data

has error? -> write error log -> set error counter + 1 -> restart?

is online? -> upload data (firebase?)

store data - read over usb or ftp?
'''

from dataset import Dataset
from helper.time_helper import get_time, get_diff_seconds
from helper.filesize_helper import get_filesize
from configuration.local_config import LocalConfig
from helper.error_helper import ErrorHandler
import time

new_time = get_time()
data = Dataset()
config = LocalConfig()
config.get_config_data()
error = ErrorHandler()

i = 1
while i <= 1000:
    try:
        print(f"attempt: {i}")
        data.get_dht22_data()
        data.get_ds18b20_data()
        data.get_scale_data()
        data.get_fft_data()
        time.sleep(int(config.app_wait_seconds))
        i = i + 1
    except Exception as e:
        print(e)
        error.log.exception(e)

print(f"start at: {new_time}")
print(f"end at: {get_time()}")
print("estimated filesize : 46MB")
print(f"filesize: {get_filesize('db.json')}")


# from helper.info_helper import InfoHelper
#
# infohelper = InfoHelper()
#
# infohelper.calc()