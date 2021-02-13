import mapping
import os


def clear_data():
    # delete data dir
    os.system(f"sudo rm -R {mapping.data_dir_path}")
    # create new data dir
    os.system(f"mkdir {mapping.data_dir_path}")
    # create fft dir
    os.system(f"mkdir {mapping.data_dir_path}fft")
    # create wav dir
    os.system(f"mkdir {mapping.data_dir_path}wav")
    # set read/write all to data dir
    os.system(f"sudo chmod 777 -R {mapping.data_dir_path}")
    # remove error.log
    os.system(f"sudo rm {mapping.error_log}")
    # create new error.log
    os.system(f"touch {mapping.error_log}")
    # set read/write all to error.log
    os.system(f"sudo chmod 777 {mapping.error_log}")
    # create data.json
    os.system(f"touch {mapping.database_path}")
    # set read/write all to data.json
    os.system(f"sudo chmod 777 {mapping.database_path}")
