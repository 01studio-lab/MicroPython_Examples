
# Color definitions.
#     RGB 16-bit Color (R:5-bit; G:6-bit; B:5-bit)
BLACK       = (0,  0,  0 )        #   0,   0,   0
NAVY        = (0,  0,  15)        #   0,   0, 128
DARKGREEN   = (0,  31, 0 )        #   0, 128,   0
DARKCYAN    = (0,  31, 15)        #   0, 128, 128
MAROON      = (15, 0,  0 )        # 128,   0,   0
PURPLE      = (15, 0,  15)        # 128,   0, 128
OLIVE       = (15, 31, 0 )        # 128, 128,   0
LIGHTGREY   = (23, 47, 23)        # 192, 192, 192
DARKGREY    = (15, 31, 15)        # 128, 128, 128
BLUE        = (0,  0,  31)        #   0,   0, 255
GREEN       = (0,  63, 0 )        #   0, 255,   0
CYAN        = (0,  63, 31)        #   0, 255, 255
RED         = (31, 0,  0 )        # 255,   0,   0
MAGENTA     = (31, 0,  31)        # 255,   0, 255
YELLOW      = (31, 63, 0 )        # 255, 255,   0
WHITE       = (31, 63, 31)        # 255, 255, 255
ORANGE      = (31, 39, 0 )        # 255, 165,   0
GREENYELLOW = (18, 63, 4 )        # 173, 255,  47

def rgbTo565(r,g,b):
    """ Transform a RGB888 color color to RGB565 color tuple. """ 
    return (r//8, g//4, b//8)
