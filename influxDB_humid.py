import influxdb
import schedule
import datetime
import sys, time
import math
import Adafruit_ADS1x15
import time

adc = Adafruit_ADS1x15.ADS1115()
GAIN1 = 1
GAIN2 = 2
LOG_FILE = "/home/pi/Desktop/water.log"

# dbへのアクセス
influx = influxdb.InfluxDBClient(
    host='localhost',
    port=8086,
    database='mydb',
    username='python',
    password='python',
)

device_id='sensor01'

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
    main()

