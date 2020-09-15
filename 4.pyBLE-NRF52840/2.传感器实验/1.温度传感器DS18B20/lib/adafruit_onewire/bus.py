# The MIT License (MIT)
#
# Copyright (c) 2017 Carter Nelson for Adafruit Industries
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
`adafruit_onewire.bus`
====================================================

Provide access to a 1-Wire bus.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_OneWire.git"

import busio
from micropython import const

_SEARCH_ROM = const(0xF0)
_MATCH_ROM = const(0x55)
_SKIP_ROM = const(0xCC)
_MAX_DEV = const(10)


class OneWireError(Exception):
    """A class to represent a 1-Wire exception."""


class OneWireAddress:
    """A class to represent a 1-Wire address."""

    def __init__(self, rom):
        self._rom = rom

    @property
    def rom(self):
        """The unique 64 bit ROM code."""
        return self._rom

    @property
    def crc(self):
        """The 8 bit CRC."""
        return self._rom[7]

    @property
    def serial_number(self):
        """The 48 bit serial number."""
        return self._rom[1:7]

    @property
    def family_code(self):
        """The 8 bit family code."""
        return self._rom[0]


class OneWireBus:
    """A class to represent a 1-Wire bus."""

    def __init__(self, pin):
        # pylint: disable=no-member
        self._ow = busio.OneWire(pin)
        self._readbit = self._ow.read_bit
        self._writebit = self._ow.write_bit
        self._maximum_devices = _MAX_DEV

    @property
    def maximum_devices(self):
        """The maximum number of devices the bus will scan for. Valid range is 1 to 255.
        It is an error to have more devices on the bus than this number. Having less is OK.
        """
        return self._maximum_devices

    @maximum_devices.setter
    def maximum_devices(self, count):
        if not isinstance(count, int):
            raise ValueError("Maximum must be an integer value 1 - 255.")
        if count < 1 or count > 0xFF:
            raise ValueError("Maximum must be an integer value 1 - 255.")
        self._maximum_devices = count

    def reset(self, required=False):
        """
        Perform a reset and check for presence pulse.

        :param bool required: require presence pulse
        """
        reset = self._ow.reset()
        if required and reset:
            raise OneWireError("No presence pulse found. Check devices and wiring.")
        return not reset

    def readinto(self, buf, *, start=0, end=None):
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param bytearray buf: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include
        """
        if end is None:
            end = len(buf)
        for i in range(start, end):
            buf[i] = self._readbyte()

    def write(self, buf, *, start=0, end=None):
        """
        Write the bytes from ``buf`` to the device.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        :param bytearray buf: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        """
        if end is None:
            end = len(buf)
        for i in range(start, end):
            self._writebyte(buf[i])

    def scan(self):
        """Scan for devices on the bus and return a list of addresses."""
        devices = []
        diff = 65
        rom = False
        count = 0
        for _ in range(0xFF):
            rom, diff = self._search_rom(rom, diff)
            if rom:
                count += 1
                if count > self.maximum_devices:
                    raise RuntimeError(
                        "Maximum device count of {} exceeded.".format(
                            self.maximum_devices
                        )
                    )
                devices.append(OneWireAddress(rom))
            if diff == 0:
                break
        return devices

    def _readbyte(self):
        val = 0
        for i in range(8):
            val |= self._ow.read_bit() << i
        return val

    def _writebyte(self, value):
        for i in range(8):
            bit = (value >> i) & 0x1
            self._ow.write_bit(bit)

    def _search_rom(self, l_rom, diff):
        if not self.reset():
            return None, 0
        self._writebyte(_SEARCH_ROM)
        if not l_rom:
            l_rom = bytearray(8)
        rom = bytearray(8)
        next_diff = 0
        i = 64
        for byte in range(8):
            r_b = 0
            for bit in range(8):
                b = self._readbit()
                if self._readbit():
                    if b:  # there are no devices or there is an error on the bus
                        return None, 0
                else:
                    if not b:  # collision, two devices with different bit meaning
                        if diff > i or ((l_rom[byte] & (1 << bit)) and diff != i):
                            b = 1
                            next_diff = i
                self._writebit(b)
                r_b |= b << bit
                i -= 1
            rom[byte] = r_b
        return rom, next_diff

    @staticmethod
    def crc8(data):
        """
        Perform the 1-Wire CRC check on the provided data.

        :param bytearray data: 8 byte array representing 64 bit ROM code
        """
        crc = 0

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8C
                else:
                    crc >>= 1
                crc &= 0xFF
        return crc
