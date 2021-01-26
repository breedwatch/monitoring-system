'''
is sensor in config?
is error counter <= 3?

get sensor data

has error? -> write error log -> set error counter + 1 -> restart?

is online? -> upload data (firebase?)

store data - read over usb or ftp?
'''

from helper.connection_helper import is_online
from helper.error_helper import ErrorHandler
from configuration.local_config import LocalConfig
config = LocalConfig()

error_handler = ErrorHandler()  # error_handler.log.exception(e)
