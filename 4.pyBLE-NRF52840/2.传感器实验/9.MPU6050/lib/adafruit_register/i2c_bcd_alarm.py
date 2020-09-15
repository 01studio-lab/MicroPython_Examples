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
`adafruit_register.i2c_bcd_alarm`
====================================================

Binary Coded Decimal alarm register

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


ALARM_COMPONENT_DISABLED = 0x80
FREQUENCY = ["secondly", "minutely", "hourly", "daily", "weekly", "monthly"]


class BCDAlarmTimeRegister:
    """
    Alarm date and time register using binary coded decimal structure.

    The byte order of the registers must* be: [second], minute, hour, day,
    weekday. Each byte must also have a high enable bit where 1 is disabled and
    0 is enabled.

    * If weekday_shared is True, then weekday and day share a register.
    * If has_seconds is True, then there is a seconds register.

    Values are a tuple of (`time.struct_time`, `str`) where the struct represents
    a date and time that would alarm. The string is the frequency:

    * "secondly", once a second (only if alarm has_seconds)
    * "minutely", once a minute when seconds match (if alarm doesn't seconds then when seconds = 0)
    * "hourly", once an hour when ``tm_min`` and ``tm_sec`` match
    * "daily", once a day when ``tm_hour``, ``tm_min`` and ``tm_sec`` match
    * "weekly", once a week when ``tm_wday``, ``tm_hour``, ``tm_min``, ``tm_sec`` match
    * "monthly", once a month when ``tm_mday``, ``tm_hour``, ``tm_min``, ``tm_sec`` match

    :param int register_address: The register address to start the read
    :param bool has_seconds: True if the alarm can happen minutely.
    :param bool weekday_shared: True if weekday and day share the same register
    :param int weekday_start: 0 or 1 depending on the RTC's representation of the first day of the
      week (Monday)
    """

    # Defaults are based on alarm1 of the DS3231.
    def __init__(
        self, register_address, has_seconds=True, weekday_shared=True, weekday_start=1
    ):
        buffer_size = 5
        if weekday_shared:
            buffer_size -= 1
        if has_seconds:
            buffer_size += 1
        self.has_seconds = has_seconds
        self.buffer = bytearray(buffer_size)
        self.buffer[0] = register_address
        self.weekday_shared = weekday_shared
        self.weekday_start = weekday_start

    def __get__(self, obj, objtype=None):
        # Read the alarm register.
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)

        frequency = None
        i = 1
        seconds = 0
        if self.has_seconds:
            if (self.buffer[1] & 0x80) != 0:
                frequency = "secondly"
            else:
                frequency = "minutely"
                seconds = _bcd2bin(self.buffer[1] & 0x7F)
            i = 2
        minute = 0
        if (self.buffer[i] & 0x80) == 0:
            frequency = "hourly"
            minute = _bcd2bin(self.buffer[i] & 0x7F)

        hour = 0
        if (self.buffer[i + 1] & 0x80) == 0:
            frequency = "daily"
            hour = _bcd2bin(self.buffer[i + 1] & 0x7F)

        mday = None
        wday = None
        if (self.buffer[i + 2] & 0x80) == 0:
            # day of the month
            if not self.weekday_shared or (self.buffer[i + 2] & 0x40) == 0:
                frequency = "monthly"
                mday = _bcd2bin(self.buffer[i + 2] & 0x3F)
            else:  # weekday
                frequency = "weekly"
                wday = _bcd2bin(self.buffer[i + 2] & 0x3F) - self.weekday_start

        # weekday
        if not self.weekday_shared and (self.buffer[i + 3] & 0x80) == 0:
            frequency = "monthly"
            mday = _bcd2bin(self.buffer[i + 3] & 0x7F)

        if mday is not None:
            wday = (mday - 2) % 7
        elif wday is not None:
            mday = wday + 2
        else:
            # Jan 1, 2017 was a Sunday (6)
            wday = 6
            mday = 1

        return (
            time.struct_time((2017, 1, mday, hour, minute, seconds, wday, mday, -1)),
            frequency,
        )

    def __set__(self, obj, value):
        if len(value) != 2:
            raise ValueError("Value must be sequence of length two")
        # Turn all components off by default.
        for i in range(len(self.buffer) - 1):
            self.buffer[i + 1] = ALARM_COMPONENT_DISABLED
        frequency_name = value[1]
        error_message = "%s is not a supported frequency" % frequency_name
        if frequency_name not in FREQUENCY:
            raise ValueError(error_message)

        frequency = FREQUENCY.index(frequency_name)
        if frequency <= 1 and not self.has_seconds:
            raise ValueError(error_message)

        # i is the index of the minute byte
        i = 2 if self.has_seconds else 1

        if frequency > 0 and self.has_seconds:  # minutely at least
            self.buffer[1] = _bin2bcd(value[0].tm_sec)

        if frequency > 1:  # hourly at least
            self.buffer[i] = _bin2bcd(value[0].tm_min)

        if frequency > 2:  # daily at least
            self.buffer[i + 1] = _bin2bcd(value[0].tm_hour)

        if value[1] == "weekly":
            if self.weekday_shared:
                self.buffer[i + 2] = (
                    _bin2bcd(value[0].tm_wday + self.weekday_start) | 0x40
                )
            else:
                self.buffer[i + 3] = _bin2bcd(value[0].tm_wday + self.weekday_start)
        elif value[1] == "monthly":
            self.buffer[i + 2] = _bin2bcd(value[0].tm_mday)

        with obj.i2c_device:
            obj.i2c_device.write(self.buffer)
