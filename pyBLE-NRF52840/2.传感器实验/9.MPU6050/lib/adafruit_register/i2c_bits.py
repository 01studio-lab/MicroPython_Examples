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
`adafruit_register.i2c_bits`
====================================================

Multi bit registers

* Author(s): Scott Shawcroft
"""

__version__ = "1.8.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Register.git"


class RWBits:
    """
    Multibit register (less than a full byte) that is readable and writeable.
    This must be within a byte register.

    Values are `int` between 0 and 2 ** ``num_bits`` - 1.

    :param int num_bits: The number of bits in the field.
    :param int register_address: The register address to read the bit from
    :param type lowest_bit: The lowest bits index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.
    :param bool lsb_first: Is the first byte we read from I2C the LSB? Defaults to true
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, num_bits, register_address, lowest_bit, register_width=1, lsb_first=True,
    ):
        self.bit_mask = ((1 << num_bits) - 1) << lowest_bit
        # print("bitmask: ",hex(self.bit_mask))
        if self.bit_mask >= 1 << (register_width * 8):
            raise ValueError("Cannot have more bits than register size")
        self.lowest_bit = lowest_bit
        self.buffer = bytearray(1 + register_width)
        self.buffer[0] = register_address
        self.lsb_first = lsb_first

    def __get__(self, obj, objtype=None):
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        # read the number of bytes into a single variable
        reg = 0
        order = range(len(self.buffer) - 1, 0, -1)
        if not self.lsb_first:
            order = reversed(order)
        for i in order:
            reg = (reg << 8) | self.buffer[i]
        return (reg & self.bit_mask) >> self.lowest_bit

    def __set__(self, obj, value):
        value <<= self.lowest_bit  # shift the value over to the right spot
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
            reg = 0
            order = range(len(self.buffer) - 1, 0, -1)
            if not self.lsb_first:
                order = range(1, len(self.buffer))
            for i in order:
                reg = (reg << 8) | self.buffer[i]
            # print("old reg: ", hex(reg))
            reg &= ~self.bit_mask  # mask off the bits we're about to change
            reg |= value  # then or in our new value
            # print("new reg: ", hex(reg))
            for i in reversed(order):
                self.buffer[i] = reg & 0xFF
                reg >>= 8
            i2c.write(self.buffer)


class ROBits(RWBits):
    """
    Multibit register (less than a full byte) that is read-only. This must be
    within a byte register.

    Values are `int` between 0 and 2 ** ``num_bits`` - 1.

    :param int num_bits: The number of bits in the field.
    :param int register_address: The register address to read the bit from
    :param type lowest_bit: The lowest bits index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.
    """

    def __set__(self, obj, value):
        raise AttributeError()
