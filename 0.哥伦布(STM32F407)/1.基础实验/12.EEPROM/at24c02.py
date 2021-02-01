from pyb import I2C

#AT24C02 256*8bit, addr(0-255),data(0-255)
AT24C02_ADDR = const(0x50)

class AT24C02(object):
    def __init__(self, i2c_num, i2c_addr=AT24C02_ADDR, i2c_baud=400000):
        self.i2c_addr = i2c_addr
        self.i2c_buad = i2c_baud
        self.i2c = I2C(i2c_num, I2C.MASTER, baudrate = i2c_baud)

    def read(self, addr):
        return self.i2c.mem_read(1, self.i2c_addr, addr)[0]

    def write(self, addr, dat):
        self.i2c.mem_write(dat, self.i2c_addr, addr)
