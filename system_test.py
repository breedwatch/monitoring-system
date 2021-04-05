from dataset import Dataset
from configuration.local_config import LocalConfig

config = LocalConfig()
dataset = Dataset()

print("start testing sensors...")

for sensor, is_active in config.data.items():
    # get data from sensor if active
    if is_active:
        is_ok = dataset.get_data(sensor)
        if is_ok:
            print(f"{sensor}...ok!")
        else:
            print(f"{sensor}...failed!")
