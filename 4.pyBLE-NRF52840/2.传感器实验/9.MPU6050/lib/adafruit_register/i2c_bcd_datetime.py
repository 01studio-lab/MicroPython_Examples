# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
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
# pylint: disable=too-few-public-methods
"""
`adafruit_register.i2c_bcd_datetime`
====================================================

Binary Coded Decimal date and time register

* Author(s): Scott Shawcroft
"""

__version__ = "1.8.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Register.git"

import time


def _bcd2bin(value):
    """Convert binary coded decimal to Binary

    :param value: the BCD value to convert to binary (required, no default)
    """
    return value - 6 * (value >> 4)


def _bin2bcd(value):
    """Convert a binary value to binary coded decimal.

    :param value: the binary value to convert to BCD. (required, no default)
    """
    return value + 6 * (value // 10)


class BCDDateTimeRegister:
    """
    Date and time register using binary coded decimal structure.

    The byte order of the register must* be: second, minute, hour, weekday, day (1-31), month, year
    (in years after 2000).

    * Setting weekday_first=False will flip the weekday/day order so that day comes first.

    Values are `time.struct_time`

    :param int register_address: The register address to start the read
    :param bool weekday_first: True if weekday is in a lower register than the day of the month
        (1-31)
    :param int weekday_start: 0 or 1 depending on the RTC's representation of the first day of the
        week
    """

    def __init__(self, register_address, weekday_first=True, weekday_start=1):
        self.buffer = bytearray(8)
        self.buffer[0] = register_address
        if weekday_first:
            self.weekday_offset = 0
        else:
            self.weekday_offset = 1
        self.weekday_start = weekday_start

    def __get__(self, obj, objtype=None):
        # Read and return the date and time.
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        return time.struct_time(
            (
                _bcd2bin(self.buffer[7]) + 2000,
                _bcd2bin(self.buffer[6]),
                _bcd2bin(self.buffer[5 - self.weekday_offset]),
                _bcd2bin(self.buffer[3]),
                _bcd2bin(self.buffer[2]),
                _bcd2bin(self.buffer[1] & 0x7F),
                _bcd2bin(self.buffer[4 + self.weekday_offset] - self.weekday_start),
                -1,
                -1,
            )
        )

    def __set__(self, obj, value):
        self.buffer[1] = _bin2bcd(value.tm_sec) & 0x7F  # format conversions
        self.buffer[2] = _bin2bcd(value.tm_min)
        self.buffer[3] = _bin2bcd(value.tm_hour)
        self.buffer[4 + self.weekday_offset] = _bin2bcd(
            value.tm_wday + self.weekday_start
        )
        self.buffer[5 - self.weekday_offset] = _bin2bcd(value.tm_mday)
        self.buffer[6] = _bin2bcd(value.tm_mon)
        self.buffer[7] = _bin2bcd(value.tm_year - 2000)
        with obj.i2c_device:
            obj.i2c_device.write(self.buffer)
