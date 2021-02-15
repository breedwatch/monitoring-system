from configuration.local_config import LocalConfig

config = LocalConfig()

for sensor, val in config.get_all_sensors().items():
    if val:
        print(sensor)
