from configuration.local_config import LocalConfig
from dataset import Dataset
import csv
import mapping
from helper.time_helper import get_time


def write_data(data):
    with open(mapping.csv_data_path, mode='a+') as dataset_file:
        dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # time, device_id, temp, humidity, weight
        dataset_writer.writerow(data)
    dataset_file.close()


conf = LocalConfig()
csv_data = list()
dataset = {'weight': 7.53, 'ds18b20-0': 23.875}
conf.get_config_data()

# time, device+location, hum, temp, weight, ds18b20
# add time first
csv_data.append(get_time())
# add device id and location
csv_data.append(f"{conf.settings['device_location']}{conf.settings['device_name']}")
if 'hum' in dataset:
    csv_data.append(dataset["hum"])
else:
    csv_data.append(00)
if 'temp' in dataset:
    csv_data.append(dataset["temp"])
else:
    csv_data.append(00)
if 'weight' in dataset:
    csv_data.append(dataset["weight"])
else:
    csv_data.append(00)

for key, val in dataset.items():
    if "ds18b20" in key:
        csv_data.append(val)

write_data(csv_data)
