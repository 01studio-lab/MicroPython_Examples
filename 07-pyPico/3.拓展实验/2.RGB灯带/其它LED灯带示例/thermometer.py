import machine
import time
from ws2812b import ws2812b

num_leds = 30

pixels = ws2812b(num_leds, 0,27)

sensor_temp = machine.ADC(0)
conversion_factor = 3.3 / 65535

min_temp = 0
max_temp = 30

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    temp_int = int(temperature)
    for i in range(num_leds):
        if i < temp_int:
            pixels.set_pixel(i, 10,0,0)
        else:
            pixels.set_pixel(i,0,0,0)
    pixels.show()
    time.sleep(2)
    