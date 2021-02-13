import mapping
import os


def clear_data():
    os.system(f"sudo rm -R {mapping.data_dir_path}")
    os.system(f"sudo mkdir {mapping.data_dir_path}")
    os.system(f"sudo mkdir {mapping.data_dir_path}fft")
    os.system(f"sudo mkdir {mapping.data_dir_path}wav")
    os.system(f"sudo chmod 777 -R {mapping.data_dir_path}")
    os.system(f"sudo rm {mapping.error_log}")
    os.system(f"sudo touch {mapping.error_log}")
    os.system(f"sudo chmod 777 {mapping.error_log}")
    os.system(f"sudo touch {mapping.database_path}")
    os.system(f"sudo chmod 777 {mapping.database_path}")
