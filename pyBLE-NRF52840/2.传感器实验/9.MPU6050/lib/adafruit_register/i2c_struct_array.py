# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
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
`adafruit_register.i2c_struct_array`
====================================================

Array of structured registers based on `struct`

* Author(s): Scott Shawcroft
"""

import struct

__version__ = "1.8.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Register.git"


class _BoundStructArray:
    """
    Array object that `StructArray` constructs on demand.

    :param object obj: The device object to bind to. It must have a `i2c_device` attribute
    :param int register_address: The register address to read the bit from
    :param type struct_format: The struct format string for each register element
    :param int count: Number of elements in the array
    """

    def __init__(self, obj, register_address, struct_format, count):
        self.format = struct_format
        self.first_register = register_address
        self.obj = obj
        self.count = count

    def _get_buffer(self, index):
        """Shared bounds checking and buffer creation."""
        if not 0 <= index < self.count:
            raise IndexError()
        size = struct.calcsize(self.format)
        # We create the buffer every time instead of keeping the buffer (which is 32 bytes at least)
        # around forever.
        buf = bytearray(size + 1)
        buf[0] = self.first_register + size * index
        return buf

    def __getitem__(self, index):
        buf = self._get_buffer(index)
        with self.obj.i2c_device as i2c:
            i2c.write_then_readinto(buf, buf, out_end=1, in_start=1)
        return struct.unpack_from(self.format, buf, 1)  # offset=1

    def __setitem__(self, index, value):
        buf = self._get_buffer(index)
        struct.pack_into(self.format, buf, 1, *value)
        with self.obj.i2c_device as i2c:
            i2c.write(buf)

    def __len__(self):
        return self.count


class StructArray:
    """
    Repeated array of structured registers that are readable and writeable.

    Based on the index, values are offset by the size of the structure.

    Values are tuples that map to the values in the defined struct.  See struct
    module documentation for struct format string and its possible value types.

    .. note:: This assumes the device addresses correspond to 8-bit bytes. This is not suitable for
      devices with registers of other widths such as 16-bit.

    :param int register_address: The register address to begin reading the array from
    :param str struct_format: The struct format string for this register.
    :param int count: Number of elements in the array
    """

    def __init__(self, register_address, struct_format, count):
        self.format = struct_format
        self.address = register_address
        self.count = count
        self.array_id = "_structarray{}".format(register_address)

    def __get__(self, obj, objtype=None):
        # We actually can't handle the indexing ourself due to data descriptor limits. So, we return
        # an object that can instead. This object is bound to the object passed in here by its
        # initializer and then cached on the object itself. That way its lifetime is tied to the
        # lifetime of the object itself.
        if not hasattr(obj, self.array_id):
            setattr(
                obj,
                self.array_id,
                _BoundStructArray(obj, self.address, self.format, self.count),
            )
        return getattr(obj, self.array_id)
