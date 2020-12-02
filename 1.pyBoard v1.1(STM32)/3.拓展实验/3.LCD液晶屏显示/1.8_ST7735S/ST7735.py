#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ST7735.py
#
from machine import Pin, SPI
import time
import math
import sys

#constants
DELAY = 0x80
ST7735_TFTWIDTH = 128
ST7735_TFTHEIGHT = 160

ST7735_NOP = 0x00
ST7735_SWRESET = 0x01
ST7735_RDDID = 0x04
ST7735_RDDST = 0x09

ST7735_SLPIN = 0x10
ST7735_SLPOUT = 0x11
ST7735_PTLON = 0x12
ST7735_NORON = 0x13

ST7735_INVOFF = 0x20
ST7735_INVON = 0x21
ST7735_DISPOFF = 0x28
ST7735_DISPON = 0x29
ST7735_CASET = 0x2A
ST7735_RASET = 0x2B
ST7735_RAMWR = 0x2C
ST7735_RAMRD = 0x2E

ST7735_PTLAR = 0x30
ST7735_COLMOD = 0x3A
ST7735_MADCTL = 0x36

ST7735_FRMCTR1 = 0xB1
ST7735_FRMCTR2 = 0xB2
ST7735_FRMCTR3 = 0xB3
ST7735_INVCTR = 0xB4
ST7735_DISSET5 = 0xB6

ST7735_PWCTR1 = 0xC0
ST7735_PWCTR2 = 0xC1
ST7735_PWCTR3 = 0xC2
ST7735_PWCTR4 = 0xC3
ST7735_PWCTR5 = 0xC4
ST7735_VMCTR1 = 0xC5

ST7735_RDID1 = 0xDA
ST7735_RDID2 = 0xDB
ST7735_RDID3 = 0xDC
ST7735_RDID4 = 0xDD

ST7735_PWCTR6 = 0xFC

ST7735_GMCTRP1 = 0xE0
ST7735_GMCTRN1 = 0xE1

# for the rotation definition
ST7735_MADCTL_MY = 0x80
ST7735_MADCTL_MX = 0x40
ST7735_MADCTL_MV = 0x20
ST7735_MADCTL_ML = 0x10
ST7735_MADCTL_RGB = 0x00
ST7735_MADCTL_BGR = 0x08
ST7735_MADCTL_MH = 0x04

class ST7735():
	def __init__(self, spi, rst=4, ce=5, dc=16, offset=0, c_mode='RGB'):
		self._rst = Pin(rst, Pin.OUT)   	# 4
		self._ce = Pin(ce, Pin.OUT)    		# 5
		self._ce.high()
		self._dc = Pin(dc, Pin.OUT)    		# 16
		self._dc.high()	
		self._offset = offset
		self._x = 0
		self._y = 0
		self._width = ST7735_TFTWIDTH
		self._height = ST7735_TFTHEIGHT
		self._color = 0
		self._bground =  0x64bd
		if c_mode == 'RGB':
			self._color_mode = ST7735_MADCTL_RGB
		else:
			self._color_mode = ST7735_MADCTL_BGR

		# SPI
		self._spi = spi
		
	def command(self,c):
		b = bytearray(1)
		b[0] = c
		self._dc.low()
		self._ce.low()
		self._spi.write(b)     # write 1 byte on MOSI
		self._ce.high()
		# print ('C {0:2x}'.format(c))

	def data(self, c):
		b = bytearray(1)
		b[0] = c
		self._dc.high()
		self._ce.low()
		self._spi.write(b)     # write 1 byte on MOSI
		self._ce.high()
		# print ('D {0:2x}'.format(c))

	def reset(self):
		self._rst.low()
		time.sleep_ms(50)        # sleep for 50 milliseconds
		self._rst.high()
		time.sleep_ms(50)        # sleep for 50 milliseconds

	# begin
	def begin(self):
		self.reset()
		commands = bytearray([            # Initialization commands for 7735B screens
				ST7735_SWRESET,   DELAY,  #  1: Software reset, 0 args, w/delay
				  150,                    #     150 ms delay
				ST7735_SLPOUT ,   DELAY,  #  2: Out of sleep mode, 0 args, w/delay
				  255,                    #     500 ms delay
				ST7735_FRMCTR1, 3      ,  #  3: Frame rate ctrl - normal mode, 3 args:
				  0x01, 0x2C, 0x2D,       #     Rate = fosc/(1x2+40) * (LINE+2C+2D)
				ST7735_FRMCTR2, 3      ,  #  4: Frame rate control - idle mode, 3 args:
				  0x01, 0x2C, 0x2D,       #     Rate = fosc/(1x2+40) * (LINE+2C+2D)
				ST7735_FRMCTR3, 6      ,  #  5: Frame rate ctrl - partial mode, 6 args:
				  0x01, 0x2C, 0x2D,       #     Dot inversion mode
				  0x01, 0x2C, 0x2D,       #     Line inversion mode
				ST7735_INVCTR , 1      ,  #  6: Display inversion ctrl, 1 arg, no delay:
				  0x07,                   #     No inversion
				ST7735_PWCTR1 , 3      ,  #  7: Power control, 3 args, no delay:
				  0xA2,
				  0x02,                   #     -4.6V
				  0x84,                   #     AUTO mode
				ST7735_PWCTR2 , 1      ,  #  8: Power control, 1 arg, no delay:
				  0xC5,                   #     VGH25 = 2.4C VGSEL = -10 VGH = 3 * AVDD
				ST7735_PWCTR3 , 2      ,  #  9: Power control, 2 args, no delay:
				  0x0A,                   #     Opamp current small
				  0x00,                   #     Boost frequency
				ST7735_PWCTR4 , 2      ,  # 10: Power control, 2 args, no delay:
				  0x8A,                   #     BCLK/2, Opamp current small & Medium low
				  0x2A,
				ST7735_PWCTR5 , 2      ,  # 11: Power control, 2 args, no delay:
				  0x8A, 0xEE,
				ST7735_VMCTR1 , 1      ,  # 12: Power control, 1 arg, no delay:
				  0x0E,
				ST7735_INVOFF , 0      ,  # 13: Don't invert display, no args, no delay
				ST7735_MADCTL , 1      ,  # 14: Memory access control (directions), 1 arg:
				  0xC8,                   #     row addr/col addr, bottom to top refresh
				ST7735_COLMOD , 1      ,  # 15: set color mode, 1 arg, no delay:
				  0x05,                   #     16-bit color
				ST7735_CASET  , 4      ,  #  1: Column addr set, 4 args, no delay:
				  0x00, 0x00,             #     XSTART = 0
				  0x00, 0x7F,             #     XEND = 127
				ST7735_RASET  , 4      ,  #  2: Row addr set, 4 args, no delay:
				  0x00, 0x00,             #     XSTART = 0
				  0x00, 0x9F,             #     XEND = 159
				ST7735_GMCTRP1, 16      , #  1: Magical unicorn dust, 16 args, no delay:
				  0x02, 0x1c, 0x07, 0x12,
				  0x37, 0x32, 0x29, 0x2d,
				  0x29, 0x25, 0x2B, 0x39,
				  0x00, 0x01, 0x03, 0x10,
				ST7735_GMCTRN1, 16      , #  2: Sparkles and rainbows, 16 args, no delay:
				  0x03, 0x1d, 0x07, 0x06,
				  0x2E, 0x2C, 0x29, 0x2D,
				  0x2E, 0x2E, 0x37, 0x3F,
				  0x00, 0x00, 0x02, 0x10,
				ST7735_NORON  ,    DELAY, #  3: Normal display on, no args, w/delay
				  10,                     #     10 ms delay
				ST7735_DISPON ,    DELAY, #  4: Main screen turn on, no args w/delay
				  100,                    #     100 ms delay
				ST7735_MADCTL, 1	,	  # change MADCTL color filter
				  0xC0|self._color_mode
		])
					
		argcount = 0
		cmd = 1
		delay = 0
		for c in commands:
			if argcount == 0:				# no arguments collected
				if delay:					# if a delay flagged this is delay value
					if c == 255:			# if delay is 255ms make it 500ms
						c = 500
					time.sleep_ms(c)
					delay = 0
				else:
					if cmd == 1:					# need to send command byte
						self.command(c)			# send coommand
						cmd = 0					# clear flag to show command sent
					else:
						argcount = c & (0xff ^ DELAY)	# Clear delay bit and get arguments
						delay = c & DELAY		# set if delay required
						cmd = 1					# flag command now complete
			else:							# arguments to send
				self.data(c)				# send argument
				argcount -= 1				# decrement the counter
		
	# display
	def set_addr_window(self, x0, y0, x1, y1):
		self.command(ST7735_CASET) # Column addr setim
		
		self.data(0x00)
		self.data(x0 + self._offset)     # XSTART
		self.data(0x00)
		self.data(x1 + self._offset)     # XEND

		self.command(ST7735_RASET) # Row addr set
		self.data(0x00)
		self.data(y0 + self._offset)     # YSTART
		self.data(0x00)
		self.data(y1 + self._offset)     # YEND

		self.command(ST7735_RAMWR) # write to RAM
		
	def pixel(self, x, y, color):

		if(x < 0) or (x >= self._width) or (y < 0) or (y >= self._height):
			return

		self.set_addr_window(x,y,x+1,y+1)

		a=(color>>8)+((color & 0xff)<<8) # reverse bytes
		b=bytearray(a.to_bytes(2,sys.byteorder))
		self._dc.high()
		self._ce.low()
		self._spi.write(b)     # write 1 byte on MOSI
		self._ce.high()
		
	def draw_block(self,x,y,w,h,color):
		size = w * h
		max_rows = math.floor(500 / h)
		rows = 0
		while rows < h:
			block_rows = min(max_rows, h-rows)
			b=bytes([color>>8, color & 0xff])*w*block_rows
			self.draw_bmp(x,y+rows,w,block_rows,b)
			rows = rows + max_rows
		
	def draw_bmp(self,x,y,w,h,buffer):
		if((x >= self._width) or (y >= self._height)):
			return
		if (x + w - 1) >= self._width:
			w = self._width  - x
		if (y + h - 1) >= self._height:
			h = self._height - y
		self.set_addr_window(x,y,x+w-1,y+h-1)
		self._dc.high()
		self._ce.low()
		self._spi.write(buffer)     # write bytes on MOSI
		self._ce.high()
		
	def fill_screen(self,color):
		self.draw_block(0,0,self._width,self._height,color)
			
	def p_char(self, x, y, ch):
		fp = (ord(ch)-0x20) * 5
		f = open('font5x7.fnt','rb')
		f.seek(fp)
		b = f.read(5)
		char_buf=bytearray(b)
		char_buf.append(0)

		# make 8x6 image
		char_image = bytearray()
		for bit in range(8):
			for c in range (6):
				if ((char_buf[c]>>bit) & 1)>0:
					char_image.append(self._color >> 8)
					char_image.append(self._color & 0xff)
				else:
					char_image.append(self._bground >> 8)
					char_image.append(self._bground & 0xff)
		self.draw_bmp(x,y,6,8,char_image)
		
	def p_string(self, x, y, str):
		for ch in (str):
			self.p_char(x, y, ch)
			x += 6

	def rgb_to_565(self,r,g,b):
		return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

	def set_rotation(self, m):
		self.command(ST7735_MADCTL)
		rotation = m % 4 # can't be higher than 3
		if rotation == 0:
			self.data(ST7735_MADCTL_MX | ST7735_MADCTL_MY | self._color_mode)
			self._width  = ST7735_TFTWIDTH
			self._height = ST7735_TFTHEIGHT
		elif rotation == 1:
			self.data(ST7735_MADCTL_MY | ST7735_MADCTL_MV | self._color_mode)
			self._width  = ST7735_TFTHEIGHT
			self._height = ST7735_TFTWIDTH
		elif rotation == 2:
			self.data(self._color_mode)
			self._width  = ST7735_TFTWIDTH
			self._height = ST7735_TFTHEIGHT
		elif rotation == 3:
			self.data(ST7735_MADCTL_MX | ST7735_MADCTL_MV | self._color_mode)
			self._width  = ST7735_TFTHEIGHT
			self._height = ST7735_TFTWIDTH

