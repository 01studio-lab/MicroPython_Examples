
from time import sleep_us,ticks_us,sleep

class HCSR04():
    def __init__(self,trig,echo):
        self.trig=trig
        self.echo=echo

    def getDistance(self):
        distance=0
        self.trig.value(1)
        sleep_us(20)
        self.trig.value(0)
        while self.echo.value() == 0:
            pass
        if self.echo.value() == 1:
            ts=ticks_us()                   #开始时间
            while self.echo.value() == 1:   #等待脉冲高电平结束
                pass
            te=ticks_us()                   #结束时间
            tc=te-ts                        #回响时间（单位us，1us=1*10^(-6)s）
            distance=(tc*170)/10000         #距离计算 （单位为:cm）
        return distance