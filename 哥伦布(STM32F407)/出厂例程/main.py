'''
实验名称：出厂测试程序
版本：v1.0
日期：2021.1
作者：01Studio
说明：出厂测试例程。
'''

#导入相关模块
import pyb,time,gc,os,mpu6050,network,gui,audio,sensor
from pyb import Timer,I2C,LED,Switch
from machine import SoftI2C,Pin
from tftlcd import LCD43M
from touch import GT1151
from onewire import OneWire
from ds18x20 import DS18X20
from dht import DHT11

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# 构建4.3寸LCD对象并初始化
d = LCD43M(portrait=1) #默认方向
d.fill(WHITE)#填充白色

#触摸屏初始化
t = GT1151()#默认方向

#构建ADC对象，引脚PA5
adc = pyb.ADC('A5')

#初始化DS18B20
ow= OneWire(Pin('G6')) #使能单总线
ds = DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接

#创建DTH11对象dt
dt=DHT11(Pin('G7'))

#构建蜂鸣器对象
beep = Pin('F6',Pin.OUT_PP)
#显示标题
d.printStr('Beep TEST!', 100, 100, BLACK, size=4)
#蜂鸣器
for i in range (3):
    beep.low() #打开蜂鸣器
    time.sleep_ms(400) #延时500毫秒
    beep.high() #关闭蜂鸣器
    time.sleep_ms(400) #延时500毫秒


#摄像头显示5秒
try:
    cam = sensor.OV2640()
    cam.reset()
    cam.set_framesize(sensor.VGA) #640*480分辨率
    cam.display() #LCD显示
    time.sleep(5)
    cam.display_stop()
    cam.deinit()

except OSError as e:
    # Reading doesn't always work! Just print error and we'll try again
    print(e.args)

d.fill(WHITE)#填充白色

#####################
#定义网络连接触摸按键和回调函数
#####################
network_flag = 0 #以太网标志位

def fun1(B1):
    global network_flag
    network_flag = 1 #设置以太网标志位

B1 = gui.TouchButton(20,420,150,60,RED,'Network',WHITE,fun1)

#定义音频相关触摸按钮
audio_flag = 0
audio_use = 0

#开始播放
def fun2(B4):
    global audio_flag
    audio_flag = 1

#停止播放
def fun3(B5):
    wm.stop()
    wm.deinit()

B2 = gui.TouchButton(140,660,120,70,BLUE,'Play',WHITE,fun2)
B3 = gui.TouchButton(290,660,160,70,BLUE,'Stop play',WHITE,fun3)

#画network矩形
d.drawRect(5, 400, 470, 230, BLACK, border=5)
d.printStr('Click to Connect', 190, 435, BLACK, size=3)

#画Music矩形
d.drawRect(5, 640, 470, 105, BLACK, border=5)
d.printStr('Audio: ', 20, 675, BLACK, size=3)

#显示标题
d.printStr('01Studio Columbus Test', 50, 10, BLACK, size=3)

################
#按键LED测试
#################

#LED4
def LED_4():
    #消除抖动，sw按下返回1，松开返回0。
    if sw.value()==1:
        time.sleep_ms(10)
        if sw.value()==1:
            LED(4).toggle()

sw =Switch()
sw.callback(LED_4)

#LED3
KEY2 = Pin('A0',Pin.IN,Pin.PULL_UP) #构建按键A0

def LED_3(KEY2):
    #消除按键抖动
    if KEY2.value() == 0:
        time.sleep_ms(10)
        if KEY2.value() == 0:
            LED(3).toggle()

KEY2.irq(LED_3,Pin.IRQ_FALLING, hard=1) #定义中断，下降沿触发

#LED2
KEY3 = Pin('E3',Pin.IN,Pin.PULL_UP) #构建按键A0

def LED_2(KEY3):
    #消除按键抖动
    if KEY3.value() == 0:
        time.sleep_ms(10)
        if KEY3.value() == 0:
            LED(2).toggle()

KEY3.irq(LED_2,Pin.IRQ_FALLING) #定义中断，下降沿触发

#############################
#### 定时器用于触发按钮事件 ##
#############################
tim_flag = 0
tim_num = 0
def count(tim):
    global tim_flag
    tim_flag = 1

tim = Timer(1,freq=50) #20ms刷新一次
tim.callback(count)

while True:

    #执行按钮触发的任务
    if tim_flag == 1:
        t.tick_inc()
        gui.task_handler()
        tim_num = tim_num + 1
        tim_flag = 0

    if network_flag == 1:
        try:
            d.printStr('Connecting...', 20, 500, BLACK, size=3)
            #以太网初始化
            nic = network.Ethernet()
            nic.active(True)
            nic.ifconfig('dhcp')

        except OSError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print('Ethernet Init fail',e.args)

            #判断网络是否连接成功
        if nic.isconnected():

            #显示IP信息
            d.printStr('IP: ' + nic.ifconfig()[0], 20, 500, BLACK, size=3)
            d.printStr('Subnet: ' + nic.ifconfig()[1], 20, 540, BLACK, size=3)
            d.printStr('Gateway: ' + nic.ifconfig()[2], 20, 580, BLACK, size=3)


        network_flag = 0

    if audio_flag == 1:
        #音频对象
        wm=audio.WM8978()
        wm.load('/flash/music/Seasons In The Sun Short.mp3')
        wm.play()
        audio_flag = 0

    if tim_num == 70:

        tim_num =0

        #内存显示
        d.printStr('SRAM Free: '+str('%.1f'%(gc.mem_free()/1024))
                +' KBytes  ',10,70,BLACK,size=3)

        #储存空间显示
        d.printStr('Flash Free: '+str('%.1f'%(os.statvfs('/flash')[0]*os.statvfs('/flash')[3]/1024/1024))
                        +' MBytes  ',10,120,BLACK,size=3)


        #1、电压测量
        value = str(adc.read()) #原始值
        vol = str('%.2f'%(adc.read()/4095*3.3)) #电压值，0-3.3V
        d.printStr('1.Voltage: '+vol+" V", 10, 170, BLACK, size=3)

        #2、DS18B20获取温度
        ds.convert_temp()#温度采集转换
        temp = ds.read_temp(rom[0])#温度显示,rom[0]为第1个DS18B20
        d.printStr('2.DS18B20 Temp: '+str('%.2f'%temp)+' C',10,220,BLACK,size=3)

        #3、DHT11获取温湿度值
        dt.measure()
        d.printStr('3.DHT11 Temp:'+str(dt.temperature())
                    +' C,'+' Humi:'+str(dt.humidity())+'%',10,270,BLACK,size=3)

        #4、MPU6050获取传感器信息

        #MPU6050初始化，这里使用软件I2C
        i2c = SoftI2C(sda=Pin("B9"), scl=Pin("B8"))
        accelerometer = mpu6050.accel(i2c)

        value=accelerometer.get_values()
        d.printStr('4.MPU6050 Accel:',10, 310, BLACK, size=3)
        d.printStr('X:'+str(value["AcX"])+' Y:'+str(value["AcY"])
                        +' Z:'+str(value["AcZ"]),50, 350, BLACK, size=3)
        del i2c
