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

    @staticmethod
    def current_volt():
        try:
            v_out = []
            with open(mapping.witty_pi_log) as f:
                for i, line in enumerate(f):
                    if 'Current' in line:
                        v_out.append(line)
            length = len(v_out) - 1

            return v_out[length][:-1]
        except IOError:
            return False

    # calc data
    def calc(self, usb_path):
        try:
            self.config.get_config_data()
            if self.config.data["wav"]:
                self.attempt_size = self.wav_attempt_size * int(self.config.audio["duration"])

            total, used, free = shutil.disk_usage("/media/usb/")
            free_space = (free / 1024 / 1024)
            possible_cycles = float(free_space) / self.attempt_size
            measure_cycle = ((3 * int(self.config.settings["median"])) + int(self.config.audio["duration"])) * 2
            cycles_per_hour = (((float(self.config.settings["app_wait_seconds"])) + float(measure_cycle)) / 60) / 60
            mb_per_hour = (1 / cycles_per_hour) * self.attempt_size
            estimated_cycles = round(free_space / mb_per_hour, 2)

            log_file_path = os.path.join(usb_path, "info.log")

            if not os.path.exists(log_file_path):
                os.system(f"sudo touch {log_file_path}")
            f = open(log_file_path, "r+")
            f.write(f"ID: {self.config.settings['device_id']} \n")
            f.write("Filesize total: %d GiB \n" % (total // (2**30)))
            f.write("Filesize used: %d MB \n" % (used / 1024 / 1024))
            f.write("Filesize unused: %d MB \n" % (free / 1024 / 1024))
            f.write("------------------------------------------------------- \n")
            f.write(f"Total number of measurements until storage full: {round(possible_cycles, 2)} \n")
            f.write(f"Measurementse per hour: {round(cycles_per_hour, 2)} \n")
            f.write(f"Days until storage is full: {round(estimated_cycles / 24, 1)} days \n")
            f.write(f"Date unitl storage is full: {get_new_date(estimated_cycles)} \n")
            f.write("------------------------------------------------------- \n")
            f.write("WITTYPI")
            if self.current_volt():
                f.write(str(self.current_volt()))
            f.write("\n")
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
