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
`adafruit_bluefruit_connect.packet`
====================================================

Bluefruit Connect App packet superclass

* Author(s): Dan Halbert for Adafruit Industries

"""

import struct


class Packet:
    """
    A Bluefruit app controller packet. A packet consists of these bytes, in order:

      - '!' - The first byte is always an exclamation point.
      - *type* - A single byte designating the type of packet: b'A', b'B', etc.
      - *data ...* - Multiple bytes of data, varying by packet type.
      - *checksum* - A single byte checksum, computed by adding up all the data bytes and
          inverting the sum.

    This is an abstract class.
    """

    # All concrete subclasses should define these class attributes. They're listed here
    # as a reminder and to make pylint happy.
    # _FMT_PARSE is the whole packet.
    _FMT_PARSE = None
    # In each class, set PACKET_LENGTH = struct.calcsize(_FMT_PARSE).
    PACKET_LENGTH = None
    # _FMT_CONSTRUCT does not include the trailing byte, which is the checksum.
    _FMT_CONSTRUCT = None
    # The first byte of the prefix is always b'!'. The second byte is the type code.
    _TYPE_HEADER = None

    _type_to_class = dict()

    @classmethod
    def register_packet_type(cls):
        """Register a new packet type, using this class and its ``cls._TYPE_HEADER``.
        The ``from_bytes()`` and ``from_stream()`` methods will then be able
        to recognize this type of packet.
        """

        Packet._type_to_class[cls._TYPE_HEADER] = cls

    @classmethod
    def from_bytes(cls, packet):
        """Create an appropriate object of the correct class for the given packet bytes.
        Validate packet type, length, and checksum.
        """
        if len(packet) < 3:
            raise ValueError("Packet too short")
        packet_class = cls._type_to_class.get(packet[0:2], None)
        if not packet_class:
            raise ValueError("Unregistered packet type {}".format(packet[0:2]))

        # In case this was called from a subclass, make sure the parsed
        # type matches up with the current class.
        if not issubclass(packet_class, cls):
            raise ValueError("Packet type is not a {}".format(cls.__name__))

        if len(packet) != packet_class.PACKET_LENGTH:
            raise ValueError("Wrong length packet")

        if cls.checksum(packet[0:-1]) != packet[-1]:
            raise ValueError("Bad checksum")

        # A packet class may do further validation of the data.
        return packet_class.parse_private(packet)

    @classmethod
    def from_stream(cls, stream):
        """Read the next packet from the incoming stream. Wait as long as the timeout
        set on stream, using its own preset timeout.
        Return None if there was no input, otherwise return an instance
        of one of the packet classes registered with ``Packet``.
        Raise an Error if the packet was not recognized or was malformed

        :param stream stream: an input stream that provides standard stream read operations,
          such as ``ble.UARTServer`` or ``busio.UART``.
        """
        # Loop looking for a b'!' packet start. If the buffer has overflowed,
        # or there's been some other problem, we may need to skip some characters
        # to get to a packet start.
        while True:
            start = stream.read(1)
            if not start:
                # Timeout: nothing read.
                return None
            if start == b"!":
                # Found start of packet.
                packet_type = stream.read(1)
                if not packet_type:
                    # Timeout: nothing more read.
                    return None
                break
            # Didn't find a packet start. Loop and try again.

        header = start + packet_type
        packet_class = cls._type_to_class.get(header, None)
        if not packet_class:
            raise ValueError("Unregistered packet type {}".format(header))
        packet = header + stream.read(packet_class.PACKET_LENGTH - 2)
        return cls.from_bytes(packet)

    @classmethod
    def parse_private(cls, packet):
        """Default implementation for subclasses.
        Assumes arguments to ``__init__()`` are exactly the values parsed using
        ``cls._FMT_PARSE``. Subclasses may need to reimplement if that assumption
        is not correct.

        Do not call this directly. It's called from ``cls.from_bytes()``.
        pylint makes it difficult to call this method _parse(), hence the name.
        """
        return cls(*struct.unpack(cls._FMT_PARSE, packet))

    @staticmethod
    def checksum(partial_packet):
        """Compute checksum for bytes, not including the checksum byte itself."""
        return ~sum(partial_packet) & 0xFF

    def add_checksum(self, partial_packet):
        """Compute the checksum of partial_packet and return a new bytes
        with the checksum appended.
        """
        return partial_packet + bytes((self.checksum(partial_packet),))
