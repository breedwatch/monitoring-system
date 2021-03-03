from dataset import Dataset
# from configuration.local_config import LocalConfig
#
# conf = LocalConfig()
# conf.get_config_data()
# print(conf.data)

dataset = Dataset()

if dataset.get_fft():
    print("okay")
else:
    print("failed")
