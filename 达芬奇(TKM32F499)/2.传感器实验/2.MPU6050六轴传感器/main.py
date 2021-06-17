'''
实验名称：MPU6050六轴传感器
版本：v1.0
日期：2021.5
作者：01Studio
说明：通过编程获MPU6050的6轴（3轴加速度+3轴陀螺仪）和温度数据，并在LCD上显示。
实验平台：01Studio 达芬奇
'''

#导入相关模块
import mpu6050,time
from machine import SoftI2C,Pin
from tftlcd import LCD43R


#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

#初始化LCD
d=LCD43R()
d.fill(WHITE)#填充白色

#MPU6050初始化，这里使用软件I2C
i2c = SoftI2C(sda=Pin("C0"), scl=Pin("C1"))
accelerometer = mpu6050.accel(i2c)

#显示标题
d.printStr('01Studio MPU6050', 40, 10, BLUE, size=4)

while True:

    #获取传感器信息
    value=accelerometer.get_values()
    print(value)

    #显示加速度数据
    d.printStr('Ac-X:'+str(value["AcX"]), 10, 100, BLACK, size=4)
    d.printStr('Ac-Y:'+str(value["AcY"]), 10, 150, BLACK, size=4)
    d.printStr('Ac-Z:'+str(value["AcZ"]), 10, 200, BLACK, size=4)

    #显示陀螺仪数据
    d.printStr('Gy-X:'+str(value["GyX"]), 10, 300, BLACK, size=4)
    d.printStr('Gy-Y:'+str(value["GyY"]), 10, 350, BLACK, size=4)
    d.printStr('Gy-Z:'+str(value["GyZ"]), 10, 400, BLACK, size=4)

    time.sleep_ms(300) #延时300毫秒
