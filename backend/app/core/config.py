import os
from dotenv import load_dotenv
load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
WAQI_TOKEN = os.getenv("WAQI_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")