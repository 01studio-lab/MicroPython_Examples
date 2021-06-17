# use WeBee TLS-02 BLE Module

from machine import UART

class TLS02():
    def __init__(self, uart=3, baud_rate=9600):
        self.uart = UART(uart, baud_rate)

################################
########### 参数查看 ############
################################

    #查看模块名字,返回字符
    def Name_Check(self):
        name_check="AT+NAME"
        self.uart.write(name_check)
        while not self.uart.any():
            pass
        return self.uart.read(128).strip() #strip()去掉\r\n

    #查看模块广播间隔,返回int
    def BI_Check(self):
        BI_check="AT+ADV"
        self.uart.write(BI_check)
        while not self.uart.any():
            pass
        return int(self.uart.read(128).strip())*0.625 #例 160*0.625=100ms

    #查看模块波特率
    def Baudrate_Check(self):
        Baudrate_check="AT+UART"
        self.uart.write(Baudrate_check)#发送一条数据
        while not self.uart.any():
            pass
        return int(self.uart.read(128).strip())


############################
######## 参数设置 ###########
############################

#设置模块名字,例如 name='01Studio',18byte以内
    def Name_Set(self,name):

        name_set="AT+NAME="+name
        print(name_set)
        self.uart.write(name_set)#发送一条数据
        while not self.uart.any():
            pass
        return self.uart.read(128).strip()

#设置广播间隔，例BI=200 ，单位ms，广播间隔越大，功耗越低，出厂默认100ms
    def BI_Set(self,BI):

        BI_set="AT+ADV="+str(int(BI/0.625))
        self.uart.write(BI_set)#发送一条数据
        while not self.uart.any():
            pass
        return self.uart.read(128).strip()

#设置波特率，设置完后修改开发板波特率以适应；默认出厂是9600
    def Baudrate_Set(self,Baudrate):

        Baudrate_set="AT+UART="+str(Baudrate)
        self.uart.write(Baudrate_set)#发送一条数据
        while not self.uart.any():
            pass
        return self.uart.read(128).strip()

#重启,复位
    def RST(self):
        rst="AT+RST"
        self.uart.write(rst)#发送一条数据
        while not self.uart.any():
            pass
        return self.uart.read(128).strip()

#恢复出厂设置
    def RESET(self):

        reset="AT+RESTORE"
        self.uart.write(reset)#发送一条数据
        while not self.uart.any():
            pass
        return self.uart.read(128).strip()
