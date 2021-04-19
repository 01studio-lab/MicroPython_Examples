# DTH11温湿度传感器
# 实验平台：01Studio pyAI-K210开发板

import time
from fpioa_manager import fm
from Maix import GPIO
from dht11 import DHT11

while True:

    # initialize GPIOHS3 using io 11
    fm.register(11, fm.fpioa.GPIOHS3, force=True)
    gpio = GPIO(GPIO.GPIOHS3, GPIO.OUT)

    # read data using gpio
    instance = DHT11(gpio)

    try:
        while True:
            result = instance.read()
            if result.is_valid():

                print("Temperature: %-3.1f C" % result.temperature)
                print("Humidity: %-3.1f %%" % result.humidity)
            time.sleep_ms(1000)

    except Exception as e:
        print(e)
