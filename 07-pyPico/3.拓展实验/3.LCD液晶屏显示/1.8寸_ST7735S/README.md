# MicroPython_ST7735S

Last update added support for a cheap 128x128 TFT display.
offset - offsets the display by that number of pixels horizontally and vertically
c_mode - Swaps around Blue and Red in the 565 colour packet. It seems some displays swap these.

Sample usage
```python
import st7735

# height defaults to 160
st7735.ST7735_TFTHEIGHT = 128
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)

# move image 3 pixels across and down
# RGB is reversed = c_mode fixes that
d = st7735.ST7735(offset=3, c_mode='BGR')
d.reset()
d.begin()
d._bground = 0xffff
d.fill_screen(d._bground)
```

This is for a 128 x 160 display that uses a different set of pins to the default
```python
import st7735
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
d = st7735.ST7735(spi, rst=4, ce=5, dc=16)
d.reset()
d.begin()
d._bground = 0xffff
d.fill_screen(d._bground)
```

.mpy versions are available in the releases
