'''
实验名称：声源定位
版本： v1.0
日期： 2019.12
翻译和注释： 01Studio
实验目的：通过麦克风阵列编程实现声源定位，并在LCD上显示。
'''

#导入MIC_ARRAY和LCD模块
from Maix import MIC_ARRAY as mic
import lcd

#初始化模块
lcd.init()
mic.init()

while True:

    #获取原始的声源黑白位图，尺寸 16*16
    imga = mic.get_map()

    #获取声源方向并设置LED显示
    b = mic.get_dir(imga)
    a = mic.set_led(b,(0,0,255))

    #将声源地图重置成正方形，彩虹色
    imgb = imga.resize(160,160)
    imgc = imgb.to_rainbow(1)

    #显示声源图
    lcd.display(imgc)

mic.deinit()

