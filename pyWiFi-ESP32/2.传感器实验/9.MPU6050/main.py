# 在这里写上你的代码 :-)
from machine import I2C,Pin
import mpu6050,time
i2c = I2C(scl=Pin(17), sda=Pin(16))
accelerometer = mpu6050.accel(i2c)

while True:
    print(accelerometer.get_values())
    time.sleep_ms(300)
