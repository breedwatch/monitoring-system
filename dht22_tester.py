from sensorlib.aht20 import AHT20

sensor = AHT20()

sensordata = sensor.get_data()
if sensordata[0]:
    print(sensordata[0])
else:
    print("nope")
