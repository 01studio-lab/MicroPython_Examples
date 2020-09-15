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
`adafruit_bluefruit_connect.button_packet`
====================================================

Bluefruit Connect App Button data packet (button_name, pressed/released)


* Author(s): Dan Halbert for Adafruit Industries

"""

import struct

from .packet import Packet


class ButtonPacket(Packet):
    """A packet containing a button name and its state."""

    BUTTON_1 = "1"
    """Code for Button 1 on the Bluefruit LE Connect app Control Pad screen."""
    BUTTON_2 = "2"
    """Button 2."""
    BUTTON_3 = "3"
    """Button 3."""
    BUTTON_4 = "4"
    """Button 4."""
    # pylint: disable= invalid-name
    UP = "5"
    """Up Button."""
    DOWN = "6"
    """Down Button."""
    LEFT = "7"
    """Left Button."""
    RIGHT = "8"
    """Right Button."""

    _FMT_PARSE = "<xxssx"
    PACKET_LENGTH = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT = "<2sss"
    _TYPE_HEADER = b"!B"

    def __init__(self, button, pressed):
        """Construct a ButtonPacket from a button name and the button's state.

        :param str button: a single character denoting the button
        :param bool pressed: ``True`` if button is pressed; ``False`` if it is release.
        """
        # This check will catch wrong length and also non-sequence args (like an int).
        try:
            assert len(button) == 1
        except:
            raise ValueError("Button must be a single char or byte.")

        self._button = button
        self._pressed = pressed

    @classmethod
    def parse_private(cls, packet):
        """Construct a ButtonPacket from an incoming packet.
        Do not call this directly; call Packet.from_bytes() instead.
        pylint makes it difficult to call this method _parse(), hence the name.
        """
        button, pressed = struct.unpack(cls._FMT_PARSE, packet)
        if not pressed in b"01":
            raise ValueError("Bad button press/release value")
        return cls(chr(button[0]), pressed == b"1")

    def to_bytes(self):
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT,
            self._TYPE_HEADER,
            self._button,
            b"1" if self._pressed else b"0",
        )
        return self.add_checksum(partial_packet)

    @property
    def button(self):
        """A single character string (not bytes) specifying the button."""
        return self._button

    @property
    def pressed(self):
        """True if button is pressed."""
        return self._pressed


# Register this class with the superclass. This allows the user to import only what is needed.
ButtonPacket.register_packet_type()
