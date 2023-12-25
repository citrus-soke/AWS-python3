import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import math
adc = Adafruit_ADS1x15.ADS1115()
GAIN1 = 1
PIN = 7
GAIN2 = 2
values = [0]*100
influx = influxdb.InfluxDBClient(
    host='localhost',
    port=8086,
    database='mydb',
    username='python',
    password='python',
)
device_id='sensor01'


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(0.1)
    

def get_data():
    humidity = adc.read_adc(0, gain=GAIN1)
    temperature = adc.read_adc(1, gain=GAIN2)
    data = {}
    data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = temperature
    data['humidity'] = humidity
    return data
