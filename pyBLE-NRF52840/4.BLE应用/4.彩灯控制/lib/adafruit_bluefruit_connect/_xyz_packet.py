# The MIT License (MIT)
#
# Copyright (c) 2019 Dan Halbert for Adafruit Industries
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
`adafruit_bluefruit_connect._xyz_packet`
====================================================

Bluefruit Connect App superclass for all data packets with (x, y, z) values

* Author(s): Dan Halbert for Adafruit Industries

"""

import struct

from .packet import Packet


class _XYZPacket(Packet):
    """A packet of x, y, z float values. Used for several different Bluefruit controller packets."""

    _FMT_PARSE = "<xxfffx"
    PACKET_LENGTH = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT = "<2sfff"
    # _TYPE_HEADER is set by each concrete subclass.

    def __init__(self, x, y, z):
        """Construct an _XYZPacket subclass object
        from the given x, y, and z float values, and type character.
        """
        self._x = x
        self._y = y
        self._z = z

    def to_bytes(self):
        """Return the bytes needed to send this packet.
        """
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT, self._TYPE_HEADER, self._x, self._y, self._z
        )
        return self.add_checksum(partial_packet)

    @property
    def x(self):
        """The x value."""
        return self._x

    @property
    def y(self):
        """The y value."""
        return self._y

    @property
    def z(self):
        """The z value."""
        return self._z
