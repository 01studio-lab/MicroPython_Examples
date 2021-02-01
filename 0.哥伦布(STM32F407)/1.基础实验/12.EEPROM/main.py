'''
实验名称：EEPROM（AT24C02）
版本：v1.0
日期：2020.12
作者：01Studio
说明：EEPROM的读写实验
'''

from at24c02 import AT24C02
import time

EE = AT24C02(i2c_num=1) #哥伦布的B8,B9为I2C1

EE.write(1,8)      #往地址1写入数字8（用户可以更改自己写的数字）
time.sleep_ms(5)   #需要适当延时再读取
print(EE.read(1))  #读取地址1数据，等于前面写入的数字

