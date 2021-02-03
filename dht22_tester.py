from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS18B20
from sensorlib.scale import Scale

ds18 = DS18B20()
dht22 = DHT22(21)
scale = Scale()

print(dht22.get_data())
