#
#    WORK IN PROGRESS
#
# lcd.py - contains ILI controllers TFT LCD driving classes
# Data transfer using 4-line Serial protocol (Series II)
# 16-bit RGB Color (R:5-bit; G:6-bit; B:5-bit)
# About 30Hz monocolor screen refresh
#
# Default is portrait mode:
# lcd = LCD( [ portrait = True ] )
#    width is 240px
#    height is 320px
#
# Setup landscape mode:
# lcd = LCD( portrait = False )
#    width is 320px
#    height is 240px
#
# Template method for orientation management by Accel:
#    Changing mode on the air by calling:
#    lcd.setPortrait( True [or False] )

import os
import struct
import math
import array

import pyb, micropython
from pyb import SPI, Pin

from decorators import dimensions
from registers import regs
from colors import *

micropython.alloc_emergency_exception_buf(100)

imgcachedir = 'images/cache'
if 'cache' not in os.listdir('images'):
    try:
        os.mkdir(imgcachedir)
    except OSError: pass

rate = 42000000

class ILI:
    _cnt  = 0
    _regs = dict()
    _spi  = object()
    _rst  = object()
    _csx  = object()
    _dcx  = object()
    _portrait  = True

    _tftwidth  = 240    # TFT width Constant
    _tftheight = 320    # TFT height Constant

    _curwidth  = 240   # Current TFT width
    _curheight = 320   # Current TFT height

    def __init__(self, rstPin='Y4', csxPin='Y5', dcxPin='Y3', port=2, rate=rate,
                chip='ILI9341', portrait=True):
        if ILI._cnt == 0:
            ILI._regs = regs[chip]
            ILI._spi  = SPI(port, SPI.MASTER, baudrate=rate, polarity=1, phase=1)
            ILI._rst  = Pin(rstPin, Pin.OUT_PP)    # Reset Pin
            ILI._csx  = Pin(csxPin, Pin.OUT_PP)    # CSX Pin
            ILI._dcx  = Pin(dcxPin, Pin.OUT_PP)    # D/Cx Pin
            self.reset()
            self._initILI()

        self.setPortrait(portrait)
        ILI._cnt += 1

    def reset(self):
        ILI._rst.low()                #
        pyb.delay(1)                  #    RESET LCD SCREEN
        ILI._rst.high()               #

    def setPortrait(self, portrait):
        if ILI._portrait != portrait:
            ILI._portrait = portrait
        self._setWH()

    def _setWH(self):
        if ILI._portrait:
            ILI._curheight = self.TFTHEIGHT = ILI._tftheight
            ILI._curwidth  = self.TFTWIDTH  = ILI._tftwidth
        else:
            ILI._curheight = self.TFTHEIGHT = ILI._tftwidth
            ILI._curwidth  = self.TFTWIDTH  = ILI._tftheight
        self._graph_orientation()

    def _initILI(self):
        self._write_cmd(ILI._regs['LCDOFF'])   # Display OFF
        pyb.delay(10)
        self._write_cmd(ILI._regs['SWRESET'])  # Reset SW
        pyb.delay(50)
        self._graph_orientation()
        self._write_cmd(ILI._regs['PTLON'])    # Partial mode ON
        self._write_cmd(ILI._regs['PIXFMT'])   # Pixel format set
        #self._write_data(0x66)    # 18-bit/pixel
        self._write_data(0x55)    # 16-bit/pixel
        self._write_cmd(ILI._regs['GAMMASET'])
        self._write_data(0x01)
        self._write_cmd(ILI._regs['ETMOD'])    # Entry mode set
        self._write_data(0x07)
        self._write_cmd(ILI._regs['SLPOUT'])   # sleep mode OFF
        pyb.delay(10)
        self._write_cmd(ILI._regs['LCDON'])
        pyb.delay(10)
        self._write_cmd(ILI._regs['RAMWR'])

    def _write(self, word, dc, recv, recvsize=2):
        dcs = ['cmd', 'data']

        DCX = dcs.index(dc) if dc in dcs else None
        ILI._csx.low()
        ILI._dcx.value(DCX)
        if recv:
            fmt = '>B{0}'.format('B' * recvsize)
            recv = bytearray(1+recvsize)
            data = self.spi.send_recv(struct.pack(fmt, word), recv=recv)
            ILI._csx.high()
            return data

        ILI._spi.send(word)
        ILI._csx.high()

    def _write_cmd(self, word, recv=None):
        data = self._write(word, 'cmd', recv)
        return data

    def _write_data(self, word):
        self._write(word, 'data', recv=None)

    def _write_words(self, words):
        wordL = len(words)
        wordL = wordL if wordL > 1 else ""
        fmt = '>{0}B'.format(wordL)
        words = struct.pack(fmt, *words)
        self._write_data(words)

    def _graph_orientation(self):
        self._write_cmd(ILI._regs['MADCTL'])   # Memory Access Control
        # Portrait:
        # | MY=0 | MX=1 | MV=0 | ML=0 | BGR=1 | MH=0 | 0 | 0 |
        # OR Landscape:
        # | MY=0 | MX=0 | MV=1 | ML=0 | BGR=1 | MH=0 | 0 | 0 |
        data = 0x48 if ILI._portrait else 0x28
        self._write_data(data)

    def _char_orientation(self):
        self._write_cmd(ILI._regs['MADCTL'])   # Memory Access Control
        # Portrait:
        # | MY=1 | MX=1 | MV=1 | ML=0 | BGR=1 | MH=0 | 0 | 0 |
        # OR Landscape:
        # | MY=0 | MX=1 | MV=1 | ML=0 | BGR=1 | MH=0 | 0 | 0 |
        data = 0xE8 if ILI._portrait else 0x58
        self._write_data(data)

    def _image_orientation(self):
        self._write_cmd(ILI._regs['MADCTL'])   # Memory Access Control
        # Portrait:
        # | MY=0 | MX=1 | MV=0 | ML=0 | BGR=1 | MH=0 | 0 | 0 |
        # OR Landscape:
        # | MY=0 | MX=1 | MV=0 | ML=1 | BGR=1 | MH=0 | 0 | 0 |
        data = 0xC8 if ILI._portrait else 0x68
        self._write_data(data)

    def _set_window(self, x0, y0, x1, y1):
        # Column Address Set
        self._write_cmd(ILI._regs['CASET'])
        self._write_words(((x0>>8) & 0xFF, x0 & 0xFF, (y0>>8) & 0xFF, y0 & 0xFF))
        # Page Address Set
        self._write_cmd(ILI._regs['PASET'])
        self._write_words(((x1>>8) & 0xFF, x1 & 0xFF, (y1>>8) & 0xFF, y1 & 0xFF))
        # Memory Write
        self._write_cmd(ILI._regs['RAMWR'])

    def _get_Npix_monoword(self, color):
        if color == WHITE:
            word = 0xFFFF
        elif color == BLACK:
            word = 0
        else:
            R, G, B = color
            word = (R<<11) | (G<<5) | B
        word = struct.pack('>H', word)
        return word

class BaseDraw(ILI):
    def __init__(self, **kwargs):
        super(BaseDraw, self).__init__(**kwargs)

    def _set_ortho_line(self, width, length, color):
        pixels = width * length
        word = self._get_Npix_monoword(color) * pixels
        self._write_data(word)

    def drawPixel(self, x, y, color, pixels=4):
        if pixels not in [1, 4]:
            raise ValueError("Pixels count must be 1 or 4")

        self._set_window(x, x+1, y, y+1)
        self._write_data(self._get_Npix_monoword(color) * pixels)

    def drawVline(self, x, y, length, color, width=1):
        if length > self.TFTHEIGHT: length = self.TFTHEIGHT
        if width > 10: width = 10
        self._set_window(x, x+(width-1), y, y+length)
        self._set_ortho_line(width, length, color)

    def drawHline(self, x, y, length, color, width=1):
        if length > self.TFTWIDTH: length = self.TFTWIDTH
        if width > 10: width = 10
        self._set_window(x, x+length, y, y+(width-1))
        self._set_ortho_line(width, length, color)

    # Method writed by MCHobby https://github.com/mchobby
    # TODO:
    # 1. support border > 1
    def drawLine(self, x, y, x1, y1, color):
        if x==x1:
            self.drawVline( x, y if y<=y1 else y1, abs(y1-y), color )
        elif y==y1:
            self.drawHline( x if x<=x1 else x1, y, abs(x-x1), color )
        else:
            # keep positive range for x
            if x1 < x:
              x,x1 = x1,x
              y,y1 = y1,y
            r = (y1-y)/(x1-x)
            # select ratio > 1 for fast drawing (and thin line)
            if abs(r) >= 1:
                for i in range( x1-x+1 ):
                    if (i==0): # first always a point
                        self.drawPixel( x+i, math.trunc(y+(r*i)), color )
                    else:
                        # r may be negative when drawing to wrong way > Fix it when drawing
                        self.drawVline( x+i, math.trunc(y+(r*i)-r)+(0 if r>0 else math.trunc(r)), abs(math.trunc(r)), color )
            else:
                # keep positive range for y
                if y1 < y:
                    x,x1 = x1,x
                    y,y1 = y1,y
                # invert the ratio (should be close of r = 1/r)
                r = (x1-x)/(y1-y)
                for i in range( y1-y+1 ):
                    if( i== 0): # starting point is always a point
                        self.drawPixel( math.trunc(x+(r*i)), y+i, color )
                    else:
                        # r may be negative when drawing the wrong way > fix it to draw positive
                        self.drawHline( math.trunc(x+(r*i)-r)+(0 if r>0 else math.trunc(r)), y+i, abs(math.trunc(r)), color )

    def drawRect(self, x, y, width, height, color, border=1, fillcolor=None):
        border = 10 if border > 10 else border
        if width > self.TFTWIDTH: width = self.TFTWIDTH
        if height > self.TFTHEIGHT: height = self.TFTHEIGHT
        if border:
            if border > width//2:
                border = width//2-1
            X, Y = x, y
            for i in range(2):
                Y = y+height-(border-1) if i == 1 else y
                self.drawHline(X, Y, width, color, border)

                if border > 1:
                    Y = y+1
                    H = height
                else:
                    Y = y
                    H = height + 1
                X = x+width-(border-1) if i == 1 else x
                self.drawVline(X, Y, H, color, border)
        else:
            fillcolor = color

        if fillcolor:
            xsum = x+border
            ysum = y+border
            dborder = border*2
            self._set_window(xsum, xsum+width-dborder, ysum, ysum+height-dborder)
            pixels = width * 8

            word = self._get_Npix_monoword(fillcolor) * pixels
            part = 1 if height < 20 else 7
            i=0
            while i < (height//part):
                self._write_data(word)
                i+=1

    def fillMonocolor(self, color, margin=0):
        margin = 80 if margin > 80 else margin
        width = self.TFTWIDTH-margin*2
        height = self.TFTHEIGHT-margin*2
        self.drawRect(margin, margin, width, height, color, border=0)

    def _get_x_perimeter_point(self, x, degrees, radius):
        sin = math.sin(math.radians(degrees))
        x = int(x+(radius*sin))
        return x

    def _get_y_perimeter_point(self, y, degrees, radius):
        cos = math.cos(math.radians(degrees))
        y = int(y-(radius*cos))
        return y

    def drawCircleFilled(self, x, y, radius, color):
        tempY = 0
        for i in range(180):
            xNeg = self._get_x_perimeter_point(x, 360-i, radius-1)
            xPos = self._get_x_perimeter_point(x, i, radius)
            if i > 89:
                Y = self._get_y_perimeter_point(y, i, radius-1)
            else:
                Y = self._get_y_perimeter_point(y, i, radius+1)
            if i == 90: xPos = xPos-1
            if tempY != Y and tempY > 0:
                length = xPos+1
                self.drawHline(xNeg, Y, length-xNeg, color, width=4)
            tempY = Y

    def drawCircle(self, x, y, radius, color, border=1, degrees=360, startangle=0):
        border = 5 if border > 5 else border
        # adding startangle to degrees
        if startangle > 0:
            degrees += startangle
        if border > 1:
            x = x - border//2
            y = y - border//2
            radius = radius-border//2
        for i in range(startangle, degrees):
            X = self._get_x_perimeter_point(x, i, radius)
            Y = self._get_y_perimeter_point(y, i, radius)
            if   i == 90:  X = X-1
            elif i == 180: Y = Y-1
            self.drawRect(X, Y, border, border, color, border=0)

    def drawOvalFilled(self, x, y, xradius, yradius, color):
        tempY = 0
        for i in range(180):
            xNeg = self._get_x_perimeter_point(x, 360-i, xradius)
            xPos = self._get_x_perimeter_point(x, i, xradius)
            Y    = self._get_y_perimeter_point(y, i, yradius)

            if i > 89: Y = Y-1
            if tempY != Y and tempY > 0:
                length = xPos+1
                self.drawHline(xNeg, Y, length-xNeg, color, width=4)
            tempY = Y

class BaseChars(ILI, BaseDraw):
    def __init__(self, color=BLACK, font=None, bgcolor=WHITE, scale=1,
                bctimes=7, **kwargs):
        super(BaseChars, self).__init__(**kwargs)
        self._fontColor = color
        if font:
            self._font = font
        else:
            raise ValueError("""Font not defined. Define font using argument:
                lcd.initCh(font=fontname, **kwargs)""")
        self._bgcolor = bgcolor
        self._fontscale = scale
        self._bctimes = bctimes    # blink carriage times

    def initCh(self, **kwargs):
        ch = BaseChars(portrait=ILI._portrait, **kwargs)
        return ch

    @staticmethod
    @micropython.asm_thumb
    def _asm_get_charpos(r0, r1, r2):
        mul(r0, r1)
        adc(r0, r2)

    def _set_word_length(self, word):
        return bin(word)[3:]

    def _fill_bicolor(self, data, x, y, width, height, scale=None):
        if not scale:
            scale = self._fontscale
        bgcolor = self._bgcolor
        color = self._fontColor
        self._set_window(x, x+(height*scale)-1, y, y+(width*scale)-1)
        bgpixel = self._get_Npix_monoword(bgcolor) * scale
        pixel = self._get_Npix_monoword(color) * scale
        words = ''.join(map(self._set_word_length, data))
        words = bytes(words, 'ascii').replace(b'0', bgpixel).replace(b'1', pixel)
        self._write_data(words)

    def printChar(self, char, x, y, cont=False, scale=None):
        if not scale:
            scale = self._fontscale
        font = self._font
        scale = 3 if scale > 3 else scale
        index = ord(char)
        chrwidth = len(font[index])
        height = font['height']
        data   = font[index]
        X = self.TFTHEIGHT - y - (height*scale)+scale
        Y = x
        self._char_orientation()
        self._fill_bicolor(data, X, Y, chrwidth, height, scale=scale)
        if not cont:
            self._graph_orientation()

    def printLn(self, string, x, y, bc=False, scale=None):
        if not scale:
            scale = self._fontscale
        font = self._font
        X, Y = x, y
        scale = 3 if scale > 3 else scale
        for word in string.split(' '):
            lnword = len(word)
            if (x + lnword*7*scale) >= (self.TFTWIDTH-10):
                x = X
                y += (font['height']+2)*scale
            for i in range(lnword):
                chpos = scale-(scale//2)
                chrwidth = len(font[ord(word[i])])
                cont = False if i == len(word)-1 else True
                self.printChar(word[i], x, y, cont=cont, scale=scale)
                if chrwidth == 1:
                    chpos = scale+1 if scale > 2 else scale-1
                x += self._asm_get_charpos(chrwidth, chpos, 3)
            x += self._asm_get_charpos(len(font[32]), chpos, 3)
        if bc:                                                    # blink carriage
            if (x + 2 * scale) >= (self.TFTWIDTH - 10):
                x = X
                y += (font['height']+2) * scale
            else:
                x -= 4 * scale//2
            self._blinkCarriage(x, y, scale=scale)

    # Blinking rectangular carriage on the end of line
    def _blinkCarriage(self, x, y, scale=None):
        if not scale:
            scale = self._fontscale
        font = self._font
        bgcolor = self._bgcolor
        color = self._fontColor
        times = self._bctimes
        height = font['height'] * scale
        width = 2 * scale
        i = 0
        while i != times:
            self.drawVline(x, y, height, color, width=width)
            pyb.delay(500)
            self.drawVline(x, y, height, bgcolor, width=width)
            pyb.delay(500)
            i+=1


class BaseImages(ILI):

    def __init__(self, **kwargs):
        super(BaseImages, self).__init__(**kwargs)

    # solution from forum.micropython.org
    # Need to be understandet
    @staticmethod
    @micropython.asm_thumb
    def _reverse(r0, r1):               # bytearray, len(bytearray)
        b(loopend)
        label(loopstart)
        ldrb(r2, [r0, 0])
        ldrb(r3, [r0, 1])
        strb(r3, [r0, 0])
        strb(r2, [r0, 1])
        add(r0, 2)
        label(loopend)
        sub (r1, 2)  # End of loop?
        bpl(loopstart)

    def _set_image_headers(self, f):
        headers = list()
        if f.read(2) != b'BM':
            raise OSError('Not a valid BMP image')
        for pos in (10, 18, 22):                                 # startbit, width, height
            f.seek(pos)
            headers.append(struct.unpack('<H', f.read(2))[0])    # read double byte
        return headers

    def _get_image_points(self, pos, width, height):
        if isinstance(pos, (list, tuple)):
            x, y = pos
        else:
            x = 0 if width == self.TFTWIDTH else (self.TFTWIDTH-width)//2
            y = 0 if height == self.TFTHEIGHT else (self.TFTHEIGHT-height)//2
        return x, y

    # Using in renderBmp method
    def _render_bmp_image(self, filename, pos):
        path = 'images/'
        memread = 480
        with open(path + filename, 'rb') as f:
            startbit, width, height = self._set_image_headers(f)
            if width < self.TFTWIDTH:
                width -= 1
            x, y = self._get_image_points(pos, width, height)
            self._set_window(x, (width)+x, y, (height)+y)
            f.seek(startbit)
            while True:
                try:
                    data = bytearray(f.read(memread))
                    self._reverse(data, len(data))
                    self._write_data(data)
                except OSError: break

    # Using in renderBmp method
    def _render_bmp_cache(self, filename, pos):
        filename = filename + '.cache'
        startbit = 8
        memread = 512
        with open(imgcachedir + '/' + filename, 'rb') as f:
            width = struct.unpack('H', f.readline())[0]
            height = struct.unpack('H', f.readline())[0]
            if width < self.TFTWIDTH:
                width -= 1
            x, y = self._get_image_points(pos, width, height)
            self._set_window(x, (width)+x, y, (height)+y)
            f.seek(startbit)
            while True:
                try:
                    self._write_data(f.read(memread))
                except OSError: break

    # TODO:
    # 1. resize large images to screen resolution
    # 2. if part of image goes out of the screen, must to be rendered
    # only displayed part
    def renderBmp(self, filename, pos=None, cached=True, bgcolor=None):
        self._image_orientation()
        if bgcolor:
            self.fillMonocolor(bgcolor)
        if filename + '.cache' not in os.listdir('images/cache'):
            cached = False
        if cached:
            self._render_bmp_cache(filename, pos)
        else:
            self._render_bmp_image(filename, pos)
        self._graph_orientation()

    def clearImageCache(self, path):
        for obj in os.listdir(path):
            if obj.endswith('.cache'):
                os.remove(path + '/' + obj)

    # TODO:
    # 1. resize large images to screen resolution
    def cacheImage(self, image):
        self.fillMonocolor(BLACK)
        strings = self.initCh(DARKGREY, bgcolor=BLACK)
        strings.printLn("Caching:", 25, 25)
        strings.printLn(image + '...', 45, 45)
        memread = 480
        path = 'images/cache/'
        with open('images/' + image, 'rb') as f:
            startbit, width, height = self._set_image_headers(f)

            c = open(path + image + '.cache', 'ab')
            for val in [width, height]:
                c.write(bytes(array.array('H', [val])) + b"\n")

            f.seek(startbit)
            data = '1'
            while len(data) != 0:
                try:
                    data = bytearray(f.read(memread))
                    self._reverse(data, len(data))
                    c.write(data)
                except OSError: break
            c.close()
        print('Cached:', image)

class BaseTests(BaseDraw, BaseChars, BaseImages):

    def __init__(self, **kwargs):
        super(BaseTests, self).__init__(**kwargs)

    def charsTest(self, color, font=None, bgcolor=WHITE, scale=1):
        ch = self.initCh(color=color, font=font, bgcolor=bgcolor, scale=scale)
        scale = 2 if scale > 1 else 1
        x = y = 7 * scale
        for i in range(33, 256):
            try: chrwidth = len(font[i])
            except KeyError: break
            cont = False if i == 127 else True
            ch.printChar(chr(i), x, y, cont=cont, scale=scale)
            x += self._asm_get_charpos(chrwidth, scale, 3)
            if x > (self.TFTWIDTH-10):
                x = 10
                y = self._asm_get_charpos(font['height'], scale, y)

    def renderImageTest(self, cached=True, path='images', cpath='cache'): # images/cache path
        starttime = pyb.micros()//1000
        for image in os.listdir(path):
            if image != cpath and image.endswith('bmp'):
                self.renderBmp(image, cached=cached, bgcolor=BLACK)
        return (pyb.micros()//1000-starttime)/1000

class BaseWidgets(BaseTests):

    def __init__(self, **kwargs):
        super(BaseWidgets, self).__init__(**kwargs)

class BaseObjects(BaseWidgets):

    def __init__(self, **kwargs):
        super(BaseObjects, self).__init__(**kwargs)

class LCD(BaseObjects):

    def __init__(self, **kwargs):
        super(LCD, self).__init__(**kwargs)

    def reset(self):
        super(LCD, self).reset()

    def setPortrait(self, *args):
        super(LCD, self).setPortrait(*args)

    def drawPixel(self, *args, **kwargs):
        super(LCD, self).drawPixel(*args, **kwargs)

    def drawVline(self, *args, **kwargs):
        super(LCD, self).drawVline(*args, **kwargs)

    def drawHline(self, *args, **kwargs):
        super(LCD, self).drawHline(*args, **kwargs)

    def drawLine(self, *args, **kwargs):
        super(LCD, self).drawLine(*args, **kwargs)

    def drawRect(self, *args, **kwargs):
        super(LCD, self).drawRect(*args, **kwargs)

    def fillMonocolor(self, *args, **kwargs):
        super(LCD, self).fillMonocolor(*args, **kwargs)

    def drawCircleFilled(self, *args, **kwargs):
        super(LCD, self).drawCircleFilled(*args, **kwargs)

    def drawCircle(self, *args, **kwargs):
        super(LCD, self).drawCircle(*args, **kwargs)

    def drawOvalFilled(self, *args, **kwargs):
        super(LCD, self).drawOvalFilled(*args, **kwargs)

    def initCh(self, **kwargs):
        return super(LCD, self).initCh(**kwargs)

    def printChar(self, *args, **kwargs):
        super(LCD, self).printChar(*args, **kwargs)

    def printLn(self, *args, **kwargs):
        super(LCD, self).printLn(*args, **kwargs)

    def renderBmp(self, *args, **kwargs):
        """
    Usage:
        With position definition:
            obj.renderBmp(f, [(tuple or list of x, y), cached or not, bgcolor or None])
        Without position definition image renders in center of screen:
            obj.renderBmp(f, [cached or not, bgcolor or None])
        By default method renders cached image, but only if BMP image cached
        before. For image caching see: lcd.cacheImage()
        """
        super(LCD, self).renderBmp(*args, **kwargs)

    def clearImageCache(self, *args, **kwargs):
        super(LCD, self).clearImageCache(*args, **kwargs)

    def cacheImage(self, *args, **kwargs):
        super(LCD, self).cacheImage(*args, **kwargs)

    def charsTest(self, *args, **kwargs):
        super(LCD, self).charsTest(*args, **kwargs)

    def renderImageTest(self, *args, **kwargs):
        return super(LCD, self).renderImageTest(*args, **kwargs)

if __name__ == '__main__':
    from fonts.arial_14 import Arial_14
    from fonts.vera_14  import Vera_14

    starttime = pyb.micros()//1000

    d = LCD() # or d = LCD(portrait=False) for landscape
    d.fillMonocolor(GREEN)
    d.drawRect(5, 5, 230, 310, BLUE, border=10, fillcolor=ORANGE)
    d.drawOvalFilled(120, 160, 60, 120, BLUE)
    d.drawCircleFilled(120, 160, 55, RED)
    d.drawCircle(120, 160, 59, GREEN, border=5)

    c = d.initCh(color=BLACK, bgcolor=ORANGE, font=Vera_14)         # define string obj
    p = d.initCh(color=BLACK, bgcolor=RED, font=Arial_14, scale=2)  # define string obj
    c.printChar('@', 30, 30)
    c.printLn('Hello BaseChar class', 30, 290)
    p.printLn('Python3', 89, 155)

    d.setPortrait(False)    # Changing mode to landscape
    d.renderBmp("test.bmp", (0, 0))



    # last time executed in: 1.379 seconds
    print('executed in:', (pyb.micros()//1000-starttime)/1000, 'seconds')
