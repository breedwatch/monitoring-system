from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS18B20
from sensorlib.scale import Scale
from sensorlib.microphone import Microphone
from tinydb import TinyDB
from helper.logger import ErrorHandler
from helper.time_helper import get_time, get_file_time
import mapping
from configuration.local_config import LocalConfig
import time
from numpy import median


class Dataset:
    def __init__(self):
        self.config = LocalConfig()
        self.config.get_config_data()
        self.error = ErrorHandler()
        # todo: wenn die Datei groesser als 5MB ist, erstelle eine neue db und benutz die
        self.db = TinyDB(mapping.database_path)
        self.db.truncate()
        self.dht22 = DHT22(21)
        self.temp_sensor = DS18B20()
        self.microphone = Microphone()
        self.scale = Scale()

    def get_ds18b20_data(self):
        self.update_config()
        try:
            sensor_counter = self.temp_sensor.device_count()
            ds_temp = []
            if sensor_counter != 0 and sensor_counter != "NoneType":
                for x in range(sensor_counter):
                    for i in range(int(self.config.median)):
                        value = self.temp_sensor.tempC(x)
                        if value == 998 or value == 85.0:
                            return False
                        else:
                            ds_temp.append(self.temp_sensor.tempC(x))
                            time.sleep(3)

                    if range(len(ds_temp)) != 0 or ds_temp != "nan":
                        median_ds_temp = median(ds_temp)
                        self.db.insert({
                            "source": f"ds18b20-{x}",
                            "time": get_time(is_dataset=True),
                            "temperature": median_ds_temp,
                        })
                return True
            else:
                return False

        except Exception as e:
            self.error.log.exception(e)
            return False

    def get_dht22_data(self):
        self.update_config()
        try:
            temp = []
            hum = []
            for i in range(int(self.config.median)):
                dhtdata = self.dht22.get_data()
                temp.append(dhtdata['temp'])
                hum.append(dhtdata['hum'])
                time.sleep(1)

            median_temp = median(temp)
            median_hum = median(hum)

            self.db.insert({
                "source": "dht22",
                "time": get_time(is_dataset=True),
                "temperature": median_temp,
                "humidity": median_hum
            })
            return True

        except Exception as e:
            print(e)
            self.error.log.exception(e)
            return False

    def get_scale_data(self):
        self.update_config()
        try:
            weight = self.scale.get_data()

            self.db.insert({
                "source": "scale",
                "time": get_time(is_dataset=True),
                "weight": weight,
            })

            return True

        except Exception as e:
            self.error.log.exception(e)
            return False

    def update_config(self):
        self.config.get_config_data()
        self.microphone.write_configuration_data(self.config.audio_duration, self.config.audio_fs)

    def get_fft_data(self):
        self.update_config()
        try:
            is_fft, fft_data = self.microphone.get_fft_data()

            if is_fft:
                self.db.insert({
                    "source": "microphone",
                    "time": get_time(is_dataset=True),
                    "data": str(fft_data),
                })
                return True
            else:
                return False

        except Exception as e:
            self.error.log.exception(e)
            return False

    def write_wav(self):
        # todo wav dateien in extra Ordner ablegen mit Datum und Uhrzeit - Ein Ordner pro Datum und darin die Dateien mit Uhrzeit
        self.update_config()
        try:
            filename = get_file_time()
            filepath = f"{mapping.wav_path}/{filename}"

            if self.microphone.write_wav_data(filepath):
                return True
            else:
                return False

        except Exception as e:
            self.error.log.exception(e)
            return False
