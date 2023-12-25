import influxdb
import schedule
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import math
import sys, time
import datetime
adc = Adafruit_ADS1x15.ADS1115()
GAIN1 = 1
GAIN2 = 2
PIN = 7
values = [0]*100
devicce_id = 'sensor01'
influx = influxdb.InfluxDBClient(
    host='localhost',
    port=8086,
    database='mydb',
    username='python',
    password='python',
)

# 水やり
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(0.1)
def loop():
    while True:
        for i in range(100):
            values[i] = adc.read_adc(0, gain=GAIN1)
        print(max(values))
        if max(values) > 20000:  # 20000はセンサーの閾値です。適宜変更してください。おすすめは15000程度です。
            GPIO.output(PIN, GPIO.LOW)
            print("ON")
            print(PIN)
            time.sleep(0.1)
        else:
            GPIO.output(PIN, GPIO.HIGH)
            print("OFF")
            print(PIN)
            time.sleep(0.1)
def destroy():
    GPIO.output(PIN, GPIO.HIGH)
    GPIO.cleanup()

# dbへ保存
def get_data():
    humidity = adc.read_adc(0, gain=GAIN1)
    temperature = adc.read_adc(1, gain=GAIN2)
    data = {}
    data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = temperature
    data['humidity'] = humidity
    return data
def write_to_influxdb(data): # time
    json_body = [{
        'measurement': 'soil_moisture',
        'tags': {'macaddr': device_id},
        'time': datetime.datetime.utcnow(),
        'fields': data
    }]
    influx.write_points(json_body)
def on_minute():
    print('on_minute')
    try:
        data = get_data()
        print(data)
        write_to_influxdb(data)
    except KeyboardInterrupt:
        print("intrrupted Ctrl-C") 
        sys.exit(1)
def main():
    try:
        schedule.every(10).seconds.do(on_minute)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("intrrupted Ctrl-C")
        time.sleep(1)
        print("Process end")
        time.sleep(1)
        


if __name__ == '__main__':
    setup()
    try:

        loop()
    except KeyboardInterrupt:
        destroy()