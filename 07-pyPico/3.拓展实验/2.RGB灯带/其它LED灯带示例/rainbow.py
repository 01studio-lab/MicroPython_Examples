import time
import ws2812b

numpix = 30
strip = ws2812b.ws2812b(numpix, 0,27)

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

while True:
    for color in COLORS:
        for i in range(numpix):
            strip.set_pixel(i, color[0], color[1], color[2])
            time.sleep(0.01)
            strip.show()
