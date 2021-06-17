import time
import ws2812b
import random

numpix = 30  # Number of NeoPixels
# Pin where NeoPixels are connected
strip = ws2812b.ws2812b(numpix, 0,27)

colors = [
    [232, 100, 255],  # Purple
    [200, 200, 20],  # Yellow
    [30, 200, 200],  # Blue
    [150,50,10],
    [50,200,10],
]

max_len=20
min_len = 5
#pixelnum, posn in flash, flash_len, direction
flashing = []

num_flashes = 10

for i in range(num_flashes):
    pix = random.randint(0, numpix - 1)
    col = random.randint(1, len(colors) - 1)
    flash_len = random.randint(min_len, max_len)
    flashing.append([pix, colors[col], flash_len, 0, 1])
    
strip.fill(0,0,0)

while True:
    strip.show()
    for i in range(num_flashes):

        pix = flashing[i][0]
        brightness = (flashing[i][3]/flashing[i][2])
        colr = (int(flashing[i][1][0]*brightness), 
                int(flashing[i][1][1]*brightness), 
                int(flashing[i][1][2]*brightness))
        strip.set_pixel(pix, colr[0], colr[1], colr[2])

        if flashing[i][2] == flashing[i][3]:
            flashing[i][4] = -1
        if flashing[i][3] == 0 and flashing[i][4] == -1:
            pix = random.randint(0, numpix - 1)
            col = random.randint(0, len(colors) - 1)
            flash_len = random.randint(min_len, max_len)
            flashing[i] = [pix, colors[col], flash_len, 0, 1]
        flashing[i][3] = flashing[i][3] + flashing[i][4]
        time.sleep(0.005)
            
 
