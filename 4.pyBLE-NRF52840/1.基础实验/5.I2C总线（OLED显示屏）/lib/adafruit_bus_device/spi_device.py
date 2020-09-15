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
`adafruit_bus_device.spi_device` - SPI Bus Device
====================================================
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BusDevice.git"


class SPIDevice:
    """
    Represents a single SPI device and manages locking the bus and the device
    address.

    :param ~busio.SPI spi: The SPI bus the device is on
    :param ~digitalio.DigitalInOut chip_select: The chip select pin object that implements the
        DigitalInOut API.
    :param int extra_clocks: The minimum number of clock cycles to cycle the bus after CS is high.
        (Used for SD cards.)

    .. note:: This class is **NOT** built into CircuitPython. See
      :ref:`here for install instructions <bus_device_installation>`.

    Example:

    .. code-block:: python

        import busio
        import digitalio
        from board import *
        from adafruit_bus_device.spi_device import SPIDevice

        with busio.SPI(SCK, MOSI, MISO) as spi_bus:
            cs = digitalio.DigitalInOut(D10)
            device = SPIDevice(spi_bus, cs)
            bytes_read = bytearray(4)
            # The object assigned to spi in the with statements below
            # is the original spi_bus object. We are using the busio.SPI
            # operations busio.SPI.readinto() and busio.SPI.write().
            with device as spi:
                spi.readinto(bytes_read)
            # A second transaction
            with device as spi:
                spi.write(bytes_read)
    """

    def __init__(
        self,
        spi,
        chip_select=None,
        *,
        baudrate=100000,
        polarity=0,
        phase=0,
        extra_clocks=0
    ):
        self.spi = spi
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.extra_clocks = extra_clocks
        self.chip_select = chip_select
        if self.chip_select:
            self.chip_select.switch_to_output(value=True)

    def __enter__(self):
        while not self.spi.try_lock():
            pass
        self.spi.configure(
            baudrate=self.baudrate, polarity=self.polarity, phase=self.phase
        )
        if self.chip_select:
            self.chip_select.value = False
        return self.spi

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.chip_select:
            self.chip_select.value = True
        if self.extra_clocks > 0:
            buf = bytearray(1)
            buf[0] = 0xFF
            clocks = self.extra_clocks // 8
            if self.extra_clocks % 8 != 0:
                clocks += 1
            for _ in range(clocks):
                self.spi.write(buf)
        self.spi.unlock()
        return False
