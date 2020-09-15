"""
实验名称： mpu6050六轴传感器
版本： v1.0
日期： 2020.9
作者： 01Studio
实验内容：传感器接线：SCL-->TX, SDA-->RX.
"""
import time
import board
import busio
import adafruit_mpu6050

i2c = busio.I2C(board.TX, board.RX)
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    print("Temperature: %.2f C" % mpu.temperature)
    print("")
    time.sleep(1)
