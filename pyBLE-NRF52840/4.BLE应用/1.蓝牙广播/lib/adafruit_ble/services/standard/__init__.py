# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries
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

This module provides Service classes for BLE defined standard services.

"""

import time

from .. import Service
from ...uuid import StandardUUID
from ...characteristics.string import StringCharacteristic
from ...characteristics import StructCharacteristic
from ...characteristics.int import Uint8Characteristic

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE.git"


class AppearanceCharacteristic(StructCharacteristic):
    """What type of device it is"""

    # pylint: disable=too-few-public-methods
    uuid = StandardUUID(0x2A01)

    def __init__(self, **kwargs):
        super().__init__("<H", **kwargs)


class GenericAccess(Service):
    """Required service that provides basic device information"""

    uuid = StandardUUID(0x1800)
    device_name = StringCharacteristic(uuid=StandardUUID(0x2A00))
    appearance = AppearanceCharacteristic()
    # privacy_flag
    # reconnection_address
    # preferred_connection_parameters


class GenericAttribute(Service):
    """Required service that provides notifications when Services change"""

    uuid = StandardUUID(0x1801)
    # service_changed - indicate only


class BatteryService(Service):
    """Provides battery level information"""

    uuid = StandardUUID(0x180F)
    level = Uint8Characteristic(max_value=100, uuid=StandardUUID(0x2A19))


class CurrentTimeService(Service):
    """Provides the current time."""

    uuid = StandardUUID(0x1805)
    current_time = StructCharacteristic("<HBBBBBBBB", uuid=StandardUUID(0x2A2B))
    """A tuple describing the current time:
        (year, month, day, hour, minute, second, weekday, subsecond, adjust_reason)"""

    local_time_info = StructCharacteristic("<bB", uuid=StandardUUID(0x2A0F))
    """A tuple of location information: (timezone, dst_offset)"""

    @property
    def struct_time(self):
        """The current time as a `time.struct_time`. Day of year and whether DST is in effect
        are always -1.
        """
        year, month, day, hour, minute, second, weekday, _, _ = self.current_time
        # Bluetooth weekdays count from 1. struct_time counts from 0.
        return time.struct_time(
            (year, month, day, hour, minute, second, weekday - 1, -1, -1)
        )
