from dataset import Dataset
from configuration.local_config import LocalConfig

config = LocalConfig()
dataset = Dataset()

print("start testing sensors...")
duration = config.audio["duration"]
config.set_config_data("AUDIO", "duration", 10)

try:

    for sensor, is_active in config.data.items():
        # get data from sensor if active
        if is_active:
            is_ok = dataset.get_data(sensor)
            if is_ok:
                print(f"{sensor}...ok!")
            else:
                print(f"{sensor}...failed!")
except Exception as e:
    print("something went wrong!")
    print(e)
finally:
    config.set_config_data("AUDIO", "duration", duration)


