'''
实验名称：出厂测试程序
版本：v1.0
日期：2021.5
作者：01Studio
说明：出厂测试例程。
实验平台：01Studio-达芬奇
'''

#导入相关模块
import time,gc,os,mpu6050,network,gui,_thread
from machine import SoftI2C,Pin,ADC,Pin,LED,UART
from tftlcd import LCD43R
from touch import FT5436
from dht import DHT11

#修改成自己的WiFi网络
SSID='01Studio' # WiFi 账号
KEY='88888888'  # WiFi 密码

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# 构建4.3寸LCD对象并初始化
d = LCD43R(portrait=4) #默认方向
d.fill(WHITE)#填充白色

#触摸屏初始化
t = FT5436(portrait=4)#默认方向

#构建ADC对象，引脚ADC_4
adc = ADC('ADC_4')

#创建DTH11对象dt
dt=DHT11(Pin('C4'))

#MPU6050初始化，这里使用软件I2C
i2c = SoftI2C(sda=Pin("C0"), scl=Pin("C1"))
accelerometer = mpu6050.accel(i2c)

#构建蜂鸣器对象
beep = Pin('B13',Pin.OUT_PP)

#显示标题
d.printStr('Beep TEST!', 100, 100, RED, size=4)

#蜂鸣器
for i in range (3):
    beep.low() #打开蜂鸣器
    time.sleep_ms(400) #延时300毫秒
    beep.high() #关闭蜂鸣器
    time.sleep_ms(400) #延时300毫秒

d.fill(WHITE)#填充白色

#####################
#定义网络连接触摸按键和回调函数
#####################
network_flag = 0 #以太网标志位

def fun1(B1):
    global network_flag
    network_flag = 1 #设置以太网标志位

B1 = gui.TouchButton(20,420,150,60,RED,'Network',WHITE,fun1)


#画network矩形
d.drawRect(5, 400, 470, 230, BLACK, border=5)
d.printStr('Click to Connect', 190, 435, BLACK, size=3)

#显示标题
d.printStr('01Studio Davinci Test', 50, 10, BLUE, size=3)

################
#按键LED测试
#################

#构建LED对象
LED1=Pin('C2', Pin.OUT)
LED2=Pin('C3', Pin.OUT)
LED3=Pin('C6', Pin.OUT)
LED4=Pin('C7', Pin.OUT)

LED1_state=0 #LED 引脚状态
LED2_state=0 #LED 引脚状态
LED3_state=0 #LED 引脚状态
LED4_state=0 #LED 引脚状态

#LED1 & KEY1
KEY1 = Pin('A0',Pin.IN,Pin.PULL_DOWN) #构建按键A0

def LED_1(KEY1):
    
    global LED1_state
    
    #消除按键抖动
    #time.sleep_ms(2)
    if KEY1.value() == 1:
        LED1_state = not LED1_state
        LED1.value(LED1_state)

KEY1.irq(LED_1,Pin.IRQ_RISING) #定义中断，下降沿触发

#LED2 & KEY2
KEY2 = Pin('A1',Pin.IN,Pin.PULL_DOWN) #构建按键A0

def LED_2(KEY2):
    
    global LED2_state
    
    #消除按键抖动

    #time.sleep_ms(2)
    if KEY2.value() == 1:
        LED2_state = not LED2_state
        LED2.value(LED2_state)

KEY2.irq(LED_2,Pin.IRQ_RISING) #定义中断，下降沿触发

#LED3 & KEY3
KEY3 = Pin('A13',Pin.IN,Pin.PULL_DOWN) #构建按键A0

def LED_3(KEY3):
    
    global LED3_state,LED4_state
    
    #消除按键抖动    
    #time.sleep_ms(2)
    if KEY3.value() == 1:
        LED3_state = not LED3_state
        LED3.value(LED3_state)
        LED4_state = not LED4_state
        LED4.value(LED4_state)

KEY3.irq(LED_3,Pin.IRQ_RISING) #定义中断，下降沿触发

# #############################
# #### 线程用于触发按钮事件 ##
# #############################
tim_num = 0

#线程函数,任务检测
def func(name):
    global tim_num
    while True:
        t.tick_inc()
        gui.task_handler()
        tim_num = tim_num + 1
        time.sleep_ms(10)

_thread.start_new_thread(func,("1",)) #开启线程1,参数必须是元组


while True:

    if network_flag == 1: #进行网络连接

        try:
            d.printStr('Connecting...  ', 20, 500, BLACK, size=3)

            ###### WiFi模块初始化 ######
            uart = UART(1,115200)
            wlan = network.ESP8266(uart)
            
            wlan.connect(SSID, KEY) #连接

        except OSError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print('Ethernet Init fail',e.args)
            d.printStr('Connect Fail!', 20, 500, BLACK, size=3)

            #判断网络是否连接成功
        if wlan.isconnected():

            #显示IP信息
            d.printStr('IP: ' + wlan.ifconfig()[0], 20, 500, BLACK, size=3)
            d.printStr('Subnet: ' + wlan.ifconfig()[1], 20, 540, BLACK, size=3)
            d.printStr('Gateway: ' + wlan.ifconfig()[2], 20, 580, BLACK, size=3)


        network_flag = 0


    if tim_num == 150:

        tim_num =0

        #内存显示
        d.printStr('SRAM Free: '+str('%.1f'%(gc.mem_free()/1024/1024))
                +' MBytes  ',10,70,BLACK,size=3)

        #储存空间显示
        d.printStr('Flash Free: '+str('%.1f'%(os.statvfs('/flash')[0]*os.statvfs('/flash')[3]/1024/1024))
                        +' MBytes  ',10,120,BLACK,size=3)


        #1、电压测量        
        vol = str('%.2f'%(adc.read_u16()/4095*3.3)) #电压值，0-3.3V
        d.printStr('1.Voltage: '+vol+" V", 10, 170, BLACK, size=3)


        #2、DHT11获取温湿度值
        try: #异常处理
            dt.measure()
            d.printStr('2.DHT11 Temp:'+str(dt.temperature())
                    +' C,'+' Humi:'+str(dt.humidity())+'%',10,220,BLACK,size=3)
            print('DHT11 Temp:'+str(dt.temperature())
                    +' C,'+' Humi:'+str(dt.humidity())+'%')
            
        except Exception as e: #异常提示
            print('DHT11 Time Out!')

        #3、MPU6050获取传感器信息

        value=accelerometer.get_values()
        d.printStr('3.MPU6050 Accel:',10, 270, BLACK, size=3)
        d.printStr('X:'+str(value["AcX"])+' Y:'+str(value["AcY"])
                        +' Z:'+str(value["AcZ"])+'     ',50, 310, BLACK, size=3)