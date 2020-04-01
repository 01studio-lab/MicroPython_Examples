'''
实验名称：MPU6050六轴传感器
版本：v1.0
日期：2020.1
作者：01Studio
说明：通过编程获MPU6050的6轴（3轴加速度+3轴陀螺仪）和温度数据，并在OLED上显示。
'''
from machine import I2C,Pin
from ssd1306 import SSD1306_I2C
import mpu6050,time

#oled初始化
i2c1 = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c1, addr=0x3c)

#MPU6050初始化
i2c2 = I2C(sda=Pin("Y10"), scl=Pin("Y9"))
accelerometer = mpu6050.accel(i2c2)

while True:

    #获取传感器信息并串口打印
    value=accelerometer.get_values()
    print(value)

    oled.fill(0) #清屏

    #显示加速度数据
    oled.text('Ac-X:'+str(value["AcX"]),0,0)
    oled.text('Ac-Y:'+str(value["AcY"]),0,8)
    oled.text('Ac-Z:'+str(value["AcZ"]),0,16)

    #显示陀螺仪数据
    oled.text('Gy-X:'+str(value["GyX"]),0,28)
    oled.text('Gy-Y:'+str(value["GyY"]),0,36)
    oled.text('Gy-Z:'+str(value["GyZ"]),0,44)

    #显示温度数据
    oled.text('Temp:'+str(value["Tmp"])+' C',0,56)

    oled.show()

    time.sleep_ms(500) #延时500ms
