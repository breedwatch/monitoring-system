from tinydb import TinyDB
from helper.logger import ErrorHandler, SensorDataError
from helper.time_helper import get_time, get_file_time, get_dir_time
import mapping
from configuration.local_config import LocalConfig
import time
from numpy import median
import os


class Dataset:
    def __init__(self):
        self.config = LocalConfig()
        self.config.get_config_data()
        self.sensors = self.config.data
        self.error = ErrorHandler()
        # deprecated
        if self.config.data["dht22"]:
            from sensorlib.dht22 import DHT22
            self.dht22 = DHT22()
        if self.config.data["ds18b20"]:
            from sensorlib.ds1820 import DS18B20
            self.temp_sensor = DS18B20()
        if self.config.data["fft"] or self.config.data["wav"]:
            from sensorlib.microphone import Microphone
            self.microphone = Microphone()
        if self.config.data["scale"]:
            from sensorlib.scale import Scale
            self.scale = Scale()
        if self.config.data["aht20"]:
            from sensorlib.aht20 import AHT20
            self.aht20 = AHT20()
        if not os.path.exists(mapping.csv_data_path):
            os.system(f"touch {mapping.csv_data_path}")

        self.data = dict()

    def get_data(self, sensor):
        try:
            return getattr(self, 'get_' + sensor)()
        except Exception as e:
            self.error.log.exception(e)

    def get_ds18b20(self):
        self.update_config()
        try:
            sensor_counter = self.temp_sensor.device_count()
            ds_temp = []
            if sensor_counter != 0 and sensor_counter != "NoneType":
                for x in range(sensor_counter):
                    for i in range(int(self.config.settings["median"])):
                        value = self.temp_sensor.tempC(x)
                        if value == 998 or value == 85.0:
                            raise SensorDataError("DS18B20")
                        else:
                            ds_temp.append(self.temp_sensor.tempC(x))
                            time.sleep(1)

                    if range(len(ds_temp)) != 0 or ds_temp != "nan":
                        median_ds_temp = median(ds_temp)
                        self.data[f"ds18b20-{x}"] = median_ds_temp
                return True
            else:
                raise SensorDataError("DS18B20")

        except Exception as e:
            self.error.log.exception(e)
            return False

    def get_aht20(self):
        try:
            self.update_config()
            aht_data = self.aht20.get_data()

            if aht_data["status"]:
                self.data["temp"] =  aht_data["temp"]
                self.data["hum"] =  aht_data["hum"]
                return True
            else:
                raise SensorDataError("AHT20")
        except Exception as e:
            self.error.log.exception(e)

    def get_dht22(self):
        self.update_config()
        try:
            dht_data = self.dht22.get_data()

            if dht_data:
                self.data["temp"] = dht_data["temp"]
                self.data["hum"] = dht_data["hum"]
                return True
            else:
                raise SensorDataError("DHT22")

        except Exception as e:
            self.error.log.exception(e)

    def get_scale(self):
        self.update_config()
        try:
            weight = self.scale.get_data()
            if weight:
                self.data["weight"] = weight
                return True
            else:
                raise SensorDataError("SCALE")

        except Exception as e:
            print(e)
            self.error.log.exception(e)

    def update_config(self):
        self.config.get_config_data()
        self.microphone.write_configuration_data(int(self.config.audio["duration"]), int(self.config.audio["fs"]))

    def get_fft(self):
        self.update_config()
        try:
            fft_data = self.microphone.get_fft_data()
            # todo add duration
            # todo fft halbe herz schritte messen?
            if fft_data["status"]:
                dir_name = get_dir_time()
                if not os.path.exists(f"{mapping.fft_path}/{dir_name}"):
                    os.system(f"sudo mkdir {mapping.fft_path}/{dir_name}")

                file_name = get_file_time()
                os.system(f"sudo touch {mapping.fft_path}/{dir_name}/{file_name}.json")
                os.system(f"sudo chmod 777 {mapping.fft_path}/{dir_name}/{file_name}.json")
                db = TinyDB(f"{mapping.fft_path}/{dir_name}/{file_name}.json")
                db.insert({
                    "source": "microphone",
                    "time": get_time(),
                    "data": str(fft_data["data"]),
                })
                return True
            else:
                raise SensorDataError("MICROPHONE")

        except Exception as e:
            self.error.log.exception(e)

    def get_wav(self):
        self.update_config()
        try:
            dir_name = get_dir_time()
            if not os.path.exists(f"{mapping.wav_path}/{dir_name}"):
                os.system(f"sudo mkdir {mapping.wav_path}/{dir_name}")
            filename = get_file_time()
            filepath = f"{mapping.wav_path}/{dir_name}/{filename}.wav"
            if self.microphone.write_wav_data(filepath):
                return True
            else:
                raise SensorDataError("MICROPHONE")

        except Exception as e:
            self.error.log.exception(e)
            return False
