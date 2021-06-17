# The MIT License (MIT)
#
# Copyright (c) 2017 Mike McWethy for Adafruit Industries
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
:mod:`adafruit_dhtlib`
======================

CircuitPython support for the DHT11 and DHT22 temperature and humidity devices.

* Author(s): Mike McWethy
"""

import array
import time
from digitalio import DigitalInOut, Pull, Direction

_USE_PULSEIO = False
try:
    from pulseio import PulseIn

    _USE_PULSEIO = True
except ImportError:
    pass  # This is OK, we'll try to bitbang it!


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DHT.git"


class DHTBase:
    """ base support for DHT11 and DHT22 devices
    """

    __hiLevel = 51

    def __init__(self, dht11, pin, trig_wait):
        """
        :param boolean dht11: True if device is DHT11, otherwise DHT22.
        :param ~board.Pin pin: digital pin used for communication
        :param int trig_wait: length of time to hold trigger in LOW state (microseconds)
        """
        self._dht11 = dht11
        self._pin = pin
        self._trig_wait = trig_wait
        self._last_called = 0
        self._humidity = None
        self._temperature = None
        # We don't use a context because linux-based systems are sluggish
        # and we're better off having a running process
        if _USE_PULSEIO:
            self.pulse_in = PulseIn(self._pin, 81, True)

    def _pulses_to_binary(self, pulses, start, stop):
        """Takes pulses, a list of transition times, and converts
        them to a 1's or 0's.  The pulses array contains the transition times.
        pulses starts with a low transition time followed by a high transistion time.
        then a low followed by a high and so on.  The low transition times are
        ignored.  Only the high transition times are used.  If the high
        transition time is greater than __hiLevel, that counts as a bit=1, if the
        high transition time is less that __hiLevel, that counts as a bit=0.

        start is the starting index in pulses to start converting

        stop is the index to convert upto but not including

        Returns an integer containing the converted 1 and 0 bits
        """

        binary = 0
        hi_sig = False
        for bit_inx in range(start, stop):
            if hi_sig:
                bit = 0
                if pulses[bit_inx] > self.__hiLevel:
                    bit = 1
                binary = binary << 1 | bit

            hi_sig = not hi_sig

        return binary

    def _get_pulses_pulseio(self):
        """ _get_pulses implements the communication protcol for
        DHT11 and DHT22 type devices.  It sends a start signal
        of a specific length and listens and measures the
        return signal lengths.

        return pulses (array.array uint16) contains alternating high and low
        transition times starting with a low transition time.  Normally
        pulses will have 81 elements for the DHT11/22 type devices.
        """
        pulses = array.array("H")
        if _USE_PULSEIO:
            # The DHT type device use a specialize 1-wire protocol
            # The microprocessor first sends a LOW signal for a
            # specific length of time.  Then the device sends back a
            # series HIGH and LOW signals.  The length the HIGH signals
            # represents the device values.
            self.pulse_in.pause()
            self.pulse_in.clear()
            self.pulse_in.resume(self._trig_wait)

            # loop until we get the return pulse we need or
            # time out after 1/4 second
            time.sleep(0.25)
            self.pulse_in.pause()
            while self.pulse_in:
                pulses.append(self.pulse_in.popleft())
        return pulses

    def _get_pulses_bitbang(self):
        """ _get_pulses implements the communication protcol for
        DHT11 and DHT22 type devices.  It sends a start signal
        of a specific length and listens and measures the
        return signal lengths.

        return pulses (array.array uint16) contains alternating high and low
        transition times starting with a low transition time.  Normally
        pulses will have 81 elements for the DHT11/22 type devices.
        """
        pulses = array.array("H")
        with DigitalInOut(self._pin) as dhtpin:
            # we will bitbang if no pulsein capability
            transitions = []
            # Signal by setting pin high, then low, and releasing
            dhtpin.direction = Direction.OUTPUT
            dhtpin.value = True
            time.sleep(0.1)
            dhtpin.value = False
            time.sleep(0.001)
            timestamp = time.monotonic()  # take timestamp
            dhtval = True  # start with dht pin true because its pulled up
            dhtpin.direction = Direction.INPUT
            dhtpin.pull = Pull.UP
            while time.monotonic() - timestamp < 0.25:
                if dhtval != dhtpin.value:
                    dhtval = not dhtval  # we toggled
                    transitions.append(time.monotonic())  # save the timestamp
            # convert transtions to microsecond delta pulses:
            # use last 81 pulses
            transition_start = max(1, len(transitions) - 81)
            for i in range(transition_start, len(transitions)):
                pulses_micro_sec = int(1000000 * (transitions[i] - transitions[i - 1]))
                pulses.append(min(pulses_micro_sec, 65535))
        return pulses

    def measure(self):
        """ measure runs the communications to the DHT11/22 type device.
            if successful, the class properties temperature and humidity will
            return the reading returned from the device.

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        delay_between_readings = 2  # 2 seconds per read according to datasheet
        # Initiate new reading if this is the first call or if sufficient delay
        # If delay not sufficient - return previous reading.
        # This allows back to back access for temperature and humidity for same reading
        if (
            self._last_called == 0
            or (time.monotonic() - self._last_called) > delay_between_readings
        ):
            self._last_called = time.monotonic()

            new_temperature = 0
            new_humidity = 0

            if _USE_PULSEIO:
                pulses = self._get_pulses_pulseio()
            else:
                pulses = self._get_pulses_bitbang()
            # print(len(pulses), "pulses:", [x for x in pulses])

            if len(pulses) < 10:
                # Probably a connection issue!
                raise RuntimeError("DHT sensor not found, check wiring")

            if len(pulses) < 80:
                # We got *some* data just not 81 bits
                raise RuntimeError("A full buffer was not returned. Try again.")

            buf = array.array("B")
            for byte_start in range(0, 80, 16):
                buf.append(self._pulses_to_binary(pulses, byte_start, byte_start + 16))

            if self._dht11:
                # humidity is 1 byte
                new_humidity = buf[0]
                # temperature is 1 byte
                new_temperature = buf[2]
            else:
                # humidity is 2 bytes
                new_humidity = ((buf[0] << 8) | buf[1]) / 10
                # temperature is 2 bytes
                # MSB is sign, bits 0-14 are magnitude)
                new_temperature = (((buf[2] & 0x7F) << 8) | buf[3]) / 10
                # set sign
                if buf[2] & 0x80:
                    new_temperature = -new_temperature
            # calc checksum
            chk_sum = 0
            for b in buf[0:4]:
                chk_sum += b

            # checksum is the last byte
            if chk_sum & 0xFF != buf[4]:
                # check sum failed to validate
                raise RuntimeError("Checksum did not validate. Try again.")

            if new_humidity < 0 or new_humidity > 100:
                # We received unplausible data
                raise RuntimeError("Received unplausible data. Try again.")

            self._temperature = new_temperature
            self._humidity = new_humidity

    @property
    def temperature(self):
        """ temperature current reading.  It makes sure a reading is available

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        self.measure()
        return self._temperature

    @property
    def humidity(self):
        """ humidity current reading. It makes sure a reading is available

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        self.measure()
        return self._humidity


class DHT11(DHTBase):
    """ Support for DHT11 device.

        :param ~board.Pin pin: digital pin used for communication
    """

    def __init__(self, pin):
        super().__init__(True, pin, 18000)


class DHT22(DHTBase):
    """ Support for DHT22 device.

        :param ~board.Pin pin: digital pin used for communication
    """

    def __init__(self, pin):
        super().__init__(False, pin, 1000)
