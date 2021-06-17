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

"""
`adafruit_bus_device.i2c_device` - I2C Bus Device
====================================================
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BusDevice.git"


class I2CDevice:
    """
    Represents a single I2C device and manages locking the bus and the device
    address.

    :param ~busio.I2C i2c: The I2C bus the device is on
    :param int device_address: The 7 bit device address
    :param bool probe: Probe for the device upon object creation, default is true

    .. note:: This class is **NOT** built into CircuitPython. See
      :ref:`here for install instructions <bus_device_installation>`.

    Example:

    .. code-block:: python

        import busio
        from board import *
        from adafruit_bus_device.i2c_device import I2CDevice

        with busio.I2C(SCL, SDA) as i2c:
            device = I2CDevice(i2c, 0x70)
            bytes_read = bytearray(4)
            with device:
                device.readinto(bytes_read)
            # A second transaction
            with device:
                device.write(bytes_read)
    """

    def __init__(self, i2c, device_address, probe=True):

        self.i2c = i2c
        self._has_write_read = hasattr(self.i2c, "writeto_then_readfrom")
        self.device_address = device_address

        if probe:
            self.__probe_for_device()

    def readinto(self, buf, *, start=0, end=None):
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param bytearray buffer: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include; if None, use ``len(buf)``
        """
        if end is None:
            end = len(buf)
        self.i2c.readfrom_into(self.device_address, buf, start=start, end=end)

    def write(self, buf, *, start=0, end=None, stop=True):
        """
        Write the bytes from ``buffer`` to the device. Transmits a stop bit if
        ``stop`` is set.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        :param bytearray buffer: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include; if None, use ``len(buf)``
        :param bool stop: If true, output an I2C stop condition after the buffer is written
        """
        if end is None:
            end = len(buf)
        self.i2c.writeto(self.device_address, buf, start=start, end=end, stop=stop)

    # pylint: disable-msg=too-many-arguments
    def write_then_readinto(
        self,
        out_buffer,
        in_buffer,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False
    ):
        """
        Write the bytes from ``out_buffer`` to the device, then immediately
        reads into ``in_buffer`` from the device. The number of bytes read
        will be the length of ``in_buffer``.

        If ``out_start`` or ``out_end`` is provided, then the output buffer
        will be sliced as if ``out_buffer[out_start:out_end]``. This will
        not cause an allocation like ``buffer[out_start:out_end]`` will so
        it saves memory.

        If ``in_start`` or ``in_end`` is provided, then the input buffer
        will be sliced as if ``in_buffer[in_start:in_end]``. This will not
        cause an allocation like ``in_buffer[in_start:in_end]`` will so
        it saves memory.

        :param bytearray out_buffer: buffer containing the bytes to write
        :param bytearray in_buffer: buffer containing the bytes to read into
        :param int out_start: Index to start writing from
        :param int out_end: Index to read up to but not include; if None, use ``len(out_buffer)``
        :param int in_start: Index to start writing at
        :param int in_end: Index to write up to but not include; if None, use ``len(in_buffer)``
        :param bool stop: Deprecated
        """
        if out_end is None:
            out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)
        if stop:
            raise ValueError("Stop must be False. Use writeto instead.")
        if self._has_write_read:
            # In linux, at least, this is a special kernel function call
            self.i2c.writeto_then_readfrom(
                self.device_address,
                out_buffer,
                in_buffer,
                out_start=out_start,
                out_end=out_end,
                in_start=in_start,
                in_end=in_end,
            )

        else:
            # If we don't have a special implementation, we can fake it with two calls
            self.write(out_buffer, start=out_start, end=out_end, stop=False)
            self.readinto(in_buffer, start=in_start, end=in_end)

    # pylint: enable-msg=too-many-arguments

    def __enter__(self):
        while not self.i2c.try_lock():
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.i2c.unlock()
        return False

    def __probe_for_device(self):
        """
        Try to read a byte from an address,
        if you get an OSError it means the device is not there
        or that the device does not support these means of probing
        """
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.device_address, b"")
        except OSError:
            # some OS's dont like writing an empty bytesting...
            # Retry by reading a byte
            try:
                result = bytearray(1)
                self.i2c.readfrom_into(self.device_address, result)
            except OSError:
                raise ValueError("No I2C device at address: %x" % self.device_address)
        finally:
            self.i2c.unlock()
