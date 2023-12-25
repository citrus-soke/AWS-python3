import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
LOG_FILE = "/home/pi/Desktop/water.log"

def log_sensor_value(value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {value}\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

def main():
    while True:
        value = adc.read_adc(0, gain=GAIN)
        log_sensor_value(value)
        time.sleep(2)  # 何秒ごとに保存するか秒単位で書き換えてください。

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
