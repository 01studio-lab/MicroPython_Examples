'''
实验名称：MPU6050六轴传感器
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程获MPU6050的6轴（3轴加速度+3轴陀螺仪）和温度数据，并在LCD上显示。
'''

#导入相关模块
import mpu6050,time
from machine import SoftI2C,Pin
from tftlcd import LCD43M


#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色

#MPU6050初始化，这里使用软件I2C
i2c = SoftI2C(sda=Pin("B9"), scl=Pin("B8"))
accelerometer = mpu6050.accel(i2c)

#显示标题
d.printStr('01Studio MPU6050', 40, 10, BLACK, size=4)

while True:

    #获取传感器信息
    value=accelerometer.get_values()

    #显示加速度数据
    d.printStr('Ac-X:'+str(value["AcX"]), 10, 100, BLACK, size=4)
    d.printStr('Ac-Y:'+str(value["AcY"]), 10, 150, BLACK, size=4)
    d.printStr('Ac-Z:'+str(value["AcZ"]), 10, 200, BLACK, size=4)

    #显示陀螺仪数据
    d.printStr('Gy-X:'+str(value["GyX"]), 10, 300, BLACK, size=4)
    d.printStr('Gy-Y:'+str(value["GyY"]), 10, 350, BLACK, size=4)
    d.printStr('Gy-Z:'+str(value["GyZ"]), 10, 400, BLACK, size=4)

    pyb.delay(1000) #延时1秒
