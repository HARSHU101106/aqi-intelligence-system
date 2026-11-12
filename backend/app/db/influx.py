from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from app.core import config

client = InfluxDBClient(url=config.INFLUX_URL, token=config.INFLUX_TOKEN, org=config.INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()