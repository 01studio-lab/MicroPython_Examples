# The MIT License (MIT)
#
# Copyright (c) 2017 Mike Mabey
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
`adafruit_hcsr04`
====================================================

A CircuitPython library for the HC-SR04 ultrasonic range sensor.

The HC-SR04 functions by sending an ultrasonic signal, which is reflected by
many materials, and then sensing when the signal returns to the sensor. Knowing
that sound travels through dry air at `343.2 meters per second (at 20 °C)
<https://en.wikipedia.org/wiki/Speed_of_sound>`_, it's pretty straightforward
to calculate how far away the object is by timing how long the signal took to
go round-trip and do some simple arithmetic, which is handled for you by this
library.

.. warning::

    The HC-SR04 uses 5V logic, so you will have to use a `level shifter
    <https://www.adafruit.com/product/2653?q=level%20shifter&>`_ or simple
    voltage divider between it and your CircuitPython board (which uses 3.3V logic)

* Authors:

  - Mike Mabey
  - Jerry Needell - modified to add timeout while waiting for echo (2/26/2018)
  - ladyada - compatible with `distance` property standard, renaming, Pi compat
"""

import time
from digitalio import DigitalInOut, Direction

_USE_PULSEIO = False
try:
    from pulseio import PulseIn

    _USE_PULSEIO = True
except ImportError:
    pass  # This is OK, we'll try to bitbang it!

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_HCSR04.git"


class HCSR04:
    """Control a HC-SR04 ultrasonic range sensor.

    Example use:

    ::

        import time
        import board

        import adafruit_hcsr04

        sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D2, echo_pin=board.D3)


        while True:
            try:
                print((sonar.distance,))
            except RuntimeError:
                print("Retrying!")
                pass
            time.sleep(0.1)
    """

    def __init__(self, trigger_pin, echo_pin, *, timeout=0.1):
        """
        :param trigger_pin: The pin on the microcontroller that's connected to the
            ``Trig`` pin on the HC-SR04.
        :type trig_pin: microcontroller.Pin
        :param echo_pin: The pin on the microcontroller that's connected to the
            ``Echo`` pin on the HC-SR04.
        :type echo_pin: microcontroller.Pin
        :param float timeout: Max seconds to wait for a response from the
            sensor before assuming it isn't going to answer. Should *not* be
            set to less than 0.05 seconds!
        """
        self._timeout = timeout
        self._trig = DigitalInOut(trigger_pin)
        self._trig.direction = Direction.OUTPUT

        if _USE_PULSEIO:
            self._echo = PulseIn(echo_pin)
            self._echo.pause()
            self._echo.clear()
        else:
            self._echo = DigitalInOut(echo_pin)
            self._echo.direction = Direction.INPUT

    def __enter__(self):
        """Allows for use in context managers."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically de-initialize after a context manager."""
        self.deinit()

    def deinit(self):
        """De-initialize the trigger and echo pins."""
        self._trig.deinit()
        self._echo.deinit()

    @property
    def distance(self):
        """Return the distance measured by the sensor in cm.

        This is the function that will be called most often in user code. The
        distance is calculated by timing a pulse from the sensor, indicating
        how long between when the sensor sent out an ultrasonic signal and when
        it bounced back and was received again.

        If no signal is received, we'll throw a RuntimeError exception. This means
        either the sensor was moving too fast to be pointing in the right
        direction to pick up the ultrasonic signal when it bounced back (less
        likely), or the object off of which the signal bounced is too far away
        for the sensor to handle. In my experience, the sensor can detect
        objects over 460 cm away.

        :return: Distance in centimeters.
        :rtype: float
        """
        return self._dist_two_wire()  # at this time we only support 2-wire meausre

    def _dist_two_wire(self):
        if _USE_PULSEIO:
            self._echo.clear()  # Discard any previous pulse values
        self._trig.value = True  # Set trig high
        time.sleep(0.00001)  # 10 micro seconds 10/1000/1000
        self._trig.value = False  # Set trig low

        pulselen = None
        timestamp = time.monotonic()
        if _USE_PULSEIO:
            self._echo.resume()
            while not self._echo:
                # Wait for a pulse
                if (time.monotonic() - timestamp) > self._timeout:
                    self._echo.pause()
                    raise RuntimeError("Timed out")
            self._echo.pause()
            pulselen = self._echo[0]
        else:
            # OK no hardware pulse support, we'll just do it by hand!
            # hang out while the pin is low
            while not self._echo.value:
                if time.monotonic() - timestamp > self._timeout:
                    raise RuntimeError("Timed out")
            timestamp = time.monotonic()
            # track how long pin is high
            while self._echo.value:
                if time.monotonic() - timestamp > self._timeout:
                    raise RuntimeError("Timed out")
            pulselen = time.monotonic() - timestamp
            pulselen *= 1000000  # convert to us to match pulseio
        if pulselen >= 65535:
            raise RuntimeError("Timed out")

        # positive pulse time, in seconds, times 340 meters/sec, then
        # divided by 2 gives meters. Multiply by 100 for cm
        # 1/1000000 s/us * 340 m/s * 100 cm/m * 2 = 0.017
        return pulselen * 0.017
