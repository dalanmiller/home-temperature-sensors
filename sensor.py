import time
import datetime
from bmp280 import BMP280
from elasticsearch import Elasticsearch
from socket import gethostname, gethostbyname

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


# Setup elasticsearch connection
es_hostname = f"{gethostbyname('arx.local')}:9200"
print(es_hostname)
es = Elasticsearch(es_hostname)

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

temperature = bmp280.get_temperature()
pressure = bmp280.get_pressure()

doc = {
    "datetime": datetime.datetime.now(),
    "temperature": temperature,
    "pressure": pressure,
    "sensor": gethostname(),
}

es.index(index='home-temperature', body=doc)
