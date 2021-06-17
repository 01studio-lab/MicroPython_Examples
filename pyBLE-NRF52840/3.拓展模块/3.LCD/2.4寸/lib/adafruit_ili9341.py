# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ili9341`
====================================================

Display driver for ILI9341

* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

* 2.2" 18-bit color TFT LCD display with microSD card breakout
  <https://www.adafruit.com/product/1480>
* 2.4" TFT LCD with Touchscreen Breakout Board w/MicroSD Socket
  <https://www.adafruit.com/product/2478>
* 2.8" TFT LCD with Touchscreen Breakout Board w/MicroSD Socket
  <https://www.adafruit.com/product/1770>
* 3.2" TFT LCD with Touchscreen Breakout Board w/MicroSD Socket
  <https://www.adafruit.com/product/1743>
* TFT FeatherWing - 2.4" 320x240 Touchscreen For All Feathers
  <https://www.adafruit.com/product/3315>

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ILI9341.git"

_INIT_SEQUENCE = (
    b"\x01\x80\x80"  # Software reset then delay 0x80 (128ms)
    b"\xEF\x03\x03\x80\x02"
    b"\xCF\x03\x00\xC1\x30"
    b"\xED\x04\x64\x03\x12\x81"
    b"\xE8\x03\x85\x00\x78"
    b"\xCB\x05\x39\x2C\x00\x34\x02"
    b"\xF7\x01\x20"
    b"\xEA\x02\x00\x00"
    b"\xc0\x01\x23"  # Power control VRH[5:0]
    b"\xc1\x01\x10"  # Power control SAP[2:0];BT[3:0]
    b"\xc5\x02\x3e\x28"  # VCM control
    b"\xc7\x01\x86"  # VCM control2
    b"\x36\x01\x38"  # Memory Access Control
    b"\x37\x01\x00"  # Vertical scroll zero
    b"\x3a\x01\x55"  # COLMOD: Pixel Format Set
    b"\xb1\x02\x00\x18"  # Frame Rate Control (In Normal Mode/Full Colors)
    b"\xb6\x03\x08\x82\x27"  # Display Function Control
    b"\xF2\x01\x00"  # 3Gamma Function Disable
    b"\x26\x01\x01"  # Gamma curve selected
    b"\xe0\x0f\x0F\x31\x2B\x0C\x0E\x08\x4E\xF1\x37\x07\x10\x03\x0E\x09\x00"  # Set Gamma
    b"\xe1\x0f\x00\x0E\x14\x03\x11\x07\x31\xC1\x48\x08\x0F\x0C\x31\x36\x0F"  # Set Gamma
    b"\x11\x80\x78"  # Exit Sleep then delay 0x78 (120ms)
    b"\x29\x80\x78"  # Display on then delay 0x78 (120ms)
)

# pylint: disable=too-few-public-methods
class ILI9341(displayio.Display):
    """ILI9341 display driver"""

    def __init__(self, bus, **kwargs):
        super().__init__(bus, _INIT_SEQUENCE, **kwargs)
