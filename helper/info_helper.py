from configuration.local_config import LocalConfig
import shutil
from helper.time_helper import get_new_date
import os
import mapping


class InfoHelper:
    def __init__(self):
        self.config = LocalConfig()
        self.attempt_size = 0.046  # constant
        self.wav_attempt_size = 0.061  # constant

    def calc(self):
        self.config.get_config_data()
        is_wav = self.config.audio_is_wav
        if is_wav:
            self.attempt_size = self.wav_attempt_size * int(self.config.audio_duration)

        total, used, free = shutil.disk_usage("/")
        free_space = (free / 1024 / 1024)
        possible_cycles = float(free_space) / self.attempt_size
        measure_cycle = ((3 * int(self.config.median)) + int(self.config.audio_duration)) * 2
        cycles_per_hour = (((float(self.config.app_wait_seconds)) + float(measure_cycle)) / 60) / 60
        mb_per_hour = (1 / cycles_per_hour) * self.attempt_size
        estimated_cycles = round(free_space / mb_per_hour, 2)

        if not os.path.exists(mapping.info_log):
            print("no info log")
            os.system(f"sudo touch {mapping.info_log}")
            os.system(f"sudo chmod 777 {mapping.info_log}")
        f = open(mapping.info_log, "r+")
        f.write(f"Name: {self.config.device_name} \n")
        f.write(f"Standort: {self.config.device_location} \n")
        f.write("Speicherplatz gesamt: %d GiB \n" % (total // (2**30)))
        f.write("Speicherplatz belegt: %d MB \n" % (used / 1024 / 1024))
        f.write("Speicherplatz frei: %d MB \n" % (free / 1024 / 1024))
        f.write("------------------------------------------------------- \n")
        f.write(f"Gesamt Anzahl Messungen bis Speicher voll: {round(possible_cycles, 2)} \n")
        f.write(f"Messungen pro Stunde: {round(cycles_per_hour, 2)} \n")
        f.write(f"Stunden bis Speicher voll: {estimated_cycles} Stunden \n")
        f.write(f"Tage bis Speicher voll: {round(estimated_cycles / 24, 1)} Tage \n")
        f.write(f"Datum bis Speicher voll: {get_new_date(estimated_cycles)} \n")
        f.close()
