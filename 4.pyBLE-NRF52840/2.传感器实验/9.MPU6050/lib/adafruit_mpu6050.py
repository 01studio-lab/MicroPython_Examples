# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
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
`adafruit_mpu6050`
================================================================================

CircuitPython helper library for the MPU6050 6-DoF Accelerometer and Gyroscope


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**
* Adafruit's MPU6050 Breakout: https://adafruit.com/products/3886

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "1.1.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MPU6050.git"

from time import sleep
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits
import adafruit_bus_device.i2c_device as i2c_device

# pylint: disable=bad-whitespace
_MPU6050_DEFAULT_ADDRESS = 0x68  # MPU6050 default i2c address w/ AD0 low
_MPU6050_DEVICE_ID = 0x68  # The correct MPU6050_WHO_AM_I value

_MPU6050_SELF_TEST_X = 0x0D  # Self test factory calibrated values register
_MPU6050_SELF_TEST_Y = 0x0E  # Self test factory calibrated values register
_MPU6050_SELF_TEST_Z = 0x0F  # Self test factory calibrated values register
_MPU6050_SELF_TEST_A = 0x10  # Self test factory calibrated values register
_MPU6050_SMPLRT_DIV = 0x19  # sample rate divisor register
_MPU6050_CONFIG = 0x1A  # General configuration register
_MPU6050_GYRO_CONFIG = 0x1B  # Gyro specfic configuration register
_MPU6050_ACCEL_CONFIG = 0x1C  # Accelerometer specific configration register
_MPU6050_INT_PIN_CONFIG = 0x37  # Interrupt pin configuration register
_MPU6050_ACCEL_OUT = 0x3B  # base address for sensor data reads
_MPU6050_TEMP_OUT = 0x41  # Temperature data high byte register
_MPU6050_GYRO_OUT = 0x43  # base address for sensor data reads
_MPU6050_SIG_PATH_RESET = 0x68  # register to reset sensor signal paths
_MPU6050_USER_CTRL = 0x6A  # FIFO and I2C Master control register
_MPU6050_PWR_MGMT_1 = 0x6B  # Primary power/sleep control register
_MPU6050_PWR_MGMT_2 = 0x6C  # Secondary power/sleep control register
_MPU6050_WHO_AM_I = 0x75  # Divice ID register

STANDARD_GRAVITY = 9.80665
# pylint: enable=bad-whitespace


class Range:  # pylint: disable=too-few-public-methods
    """Allowed values for `accelerometer_range`.

    - ``Range.RANGE_2_G``
    - ``Range.RANGE_4_G``
    - ``Range.RANGE_8_G``
    - ``Range.RANGE_16_G``

    """

    RANGE_2_G = 0  # +/- 2g (default value)
    RANGE_4_G = 1  # +/- 4g
    RANGE_8_G = 2  # +/- 8g
    RANGE_16_G = 3  # +/- 16g


class GyroRange:  # pylint: disable=too-few-public-methods
    """Allowed values for `gyro_range`.

    - ``GyroRange.RANGE_250_DPS``
    - ``GyroRange.RANGE_500_DPS``
    - ``GyroRange.RANGE_1000_DPS``
    - ``GyroRange.RANGE_2000_DPS``

    """

    RANGE_250_DPS = 0  # +/- 250 deg/s (default value)
    RANGE_500_DPS = 1  # +/- 500 deg/s
    RANGE_1000_DPS = 2  # +/- 1000 deg/s
    RANGE_2000_DPS = 3  # +/- 2000 deg/s


class Bandwidth:  # pylint: disable=too-few-public-methods
    """Allowed values for `filter_bandwidth`.

    - ``Bandwidth.BAND_260_HZ``
    - ``Bandwidth.BAND_184_HZ``
    - ``Bandwidth.BAND_94_HZ``
    - ``Bandwidth.BAND_44_HZ``
    - ``Bandwidth.BAND_21_HZ``
    - ``Bandwidth.BAND_10_HZ``
    - ``Bandwidth.BAND_5_HZ``

    """

    BAND_260_HZ = 0  # Docs imply this disables the filter
    BAND_184_HZ = 1  # 184 Hz
    BAND_94_HZ = 2  # 94 Hz
    BAND_44_HZ = 3  # 44 Hz
    BAND_21_HZ = 4  # 21 Hz
    BAND_10_HZ = 5  # 10 Hz
    BAND_5_HZ = 6  # 5 Hz


class Rate:  # pylint: disable=too-few-public-methods
    """Allowed values for `cycle_rate`.

    - ``Rate.CYCLE_1_25_HZ``
    - ``Rate.CYCLE_5_HZ``
    - ``Rate.CYCLE_20_HZ``
    - ``Rate.CYCLE_40_HZ``

    """

    CYCLE_1_25_HZ = 0  # 1.25 Hz
    CYCLE_5_HZ = 1  # 5 Hz
    CYCLE_20_HZ = 2  # 20 Hz
    CYCLE_40_HZ = 3  # 40 Hz


class MPU6050:
    """Driver for the MPU6050 6-DoF accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the MPU6050 is connected to.
        :param address: The I2C slave address of the sensor

    """

    def __init__(self, i2c_bus, address=_MPU6050_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != _MPU6050_DEVICE_ID:
            raise RuntimeError("Failed to find MPU6050 - check your wiring!")

        self.reset()

        self._sample_rate_divisor = 0
        self._filter_bandwidth = Bandwidth.BAND_260_HZ
        self._gyro_range = GyroRange.RANGE_500_DPS
        self._accel_range = Range.RANGE_2_G
        sleep(0.100)
        self._clock_source = 1  # set to use gyro x-axis as reference
        sleep(0.100)
        self.sleep = False
        sleep(0.010)

    def reset(self):
        """Reinitialize the sensor"""
        self._reset = True
        while self._reset is True:
            sleep(0.001)
        sleep(0.100)

        _signal_path_reset = 0b111  # reset all sensors
        sleep(0.100)

    _clock_source = RWBits(3, _MPU6050_PWR_MGMT_1, 0)
    _device_id = ROUnaryStruct(_MPU6050_WHO_AM_I, ">B")

    _reset = RWBit(_MPU6050_PWR_MGMT_1, 7, 1)
    _signal_path_reset = RWBits(3, _MPU6050_SIG_PATH_RESET, 3)

    _gyro_range = RWBits(2, _MPU6050_GYRO_CONFIG, 3)
    _accel_range = RWBits(2, _MPU6050_ACCEL_CONFIG, 3)

    _filter_bandwidth = RWBits(2, _MPU6050_CONFIG, 3)

    _raw_accel_data = StructArray(_MPU6050_ACCEL_OUT, ">h", 3)
    _raw_gyro_data = StructArray(_MPU6050_GYRO_OUT, ">h", 3)
    _raw_temp_data = ROUnaryStruct(_MPU6050_TEMP_OUT, ">h")

    _cycle = RWBit(_MPU6050_PWR_MGMT_1, 5)
    _cycle_rate = RWBits(2, _MPU6050_PWR_MGMT_2, 6, 1)

    sleep = RWBit(_MPU6050_PWR_MGMT_1, 6, 1)
    """Shuts down the accelerometers and gyroscopes, saving power. No new data will
    be recorded until the sensor is taken out of sleep by setting to `False`"""
    sample_rate_divisor = UnaryStruct(_MPU6050_SMPLRT_DIV, ">B")
    """The sample rate divisor. See the datasheet for additional detail"""

    @property
    def temperature(self):
        """The current temperature in  º C"""
        raw_temperature = self._raw_temp_data
        temp = (raw_temperature / 340.0) + 36.53
        return temp

    @property
    def acceleration(self):
        """Acceleration X, Y, and Z axis data in m/s^2"""
        raw_data = self._raw_accel_data
        raw_x = raw_data[0][0]
        raw_y = raw_data[1][0]
        raw_z = raw_data[2][0]

        accel_range = self._accel_range
        accel_scale = 1
        if accel_range == Range.RANGE_16_G:
            accel_scale = 2048
        if accel_range == Range.RANGE_8_G:
            accel_scale = 4096
        if accel_range == Range.RANGE_4_G:
            accel_scale = 8192
        if accel_range == Range.RANGE_2_G:
            accel_scale = 16384

        # setup range dependant scaling
        accel_x = (raw_x / accel_scale) * STANDARD_GRAVITY
        accel_y = (raw_y / accel_scale) * STANDARD_GRAVITY
        accel_z = (raw_z / accel_scale) * STANDARD_GRAVITY

        return (accel_x, accel_y, accel_z)

    @property
    def gyro(self):
        """Gyroscope X, Y, and Z axis data in º/s"""
        raw_data = self._raw_gyro_data
        raw_x = raw_data[0][0]
        raw_y = raw_data[1][0]
        raw_z = raw_data[2][0]

        gyro_scale = 1
        gyro_range = self._gyro_range
        if gyro_range == GyroRange.RANGE_250_DPS:
            gyro_scale = 131
        if gyro_range == GyroRange.RANGE_500_DPS:
            gyro_scale = 65.5
        if gyro_range == GyroRange.RANGE_1000_DPS:
            gyro_scale = 32.8
        if gyro_range == GyroRange.RANGE_2000_DPS:
            gyro_scale = 16.4

        # setup range dependant scaling
        gyro_x = raw_x / gyro_scale
        gyro_y = raw_y / gyro_scale
        gyro_z = raw_z / gyro_scale

        return (gyro_x, gyro_y, gyro_z)

    @property
    def cycle(self):
        """Enable or disable perodic measurement at a rate set by `cycle_rate`.
        If the sensor was in sleep mode, it will be waken up to cycle"""
        return self._cycle

    @cycle.setter
    def cycle(self, value):
        self.sleep = not value
        self._cycle = value

    @property
    def gyro_range(self):
        """The measurement range of all gyroscope axes. Must be a `GyroRange`"""
        return self._gyro_range

    @gyro_range.setter
    def gyro_range(self, value):
        if (value < 0) or (value > 3):
            raise ValueError("gyro_range must be a GyroRange")
        self._gyro_range = value
        sleep(0.01)

    @property
    def accelerometer_range(self):
        """The measurement range of all accelerometer axes. Must be a `Range`"""
        return self._accel_range

    @accelerometer_range.setter
    def accelerometer_range(self, value):
        if (value < 0) or (value > 3):
            raise ValueError("accelerometer_range must be a Range")
        self._accel_range = value
        sleep(0.01)

    @property
    def filter_bandwidth(self):
        """The bandwidth of the gyroscope Digital Low Pass Filter. Must be a `GyroRange`"""
        return self._filter_bandwidth

    @filter_bandwidth.setter
    def filter_bandwidth(self, value):
        if (value < 0) or (value > 6):
            raise ValueError("filter_bandwidth must be a Bandwidth")
        self._filter_bandwidth = value
        sleep(0.01)

    @property
    def cycle_rate(self):
        """The rate that measurements are taken while in `cycle` mode. Must be a `Rate`"""
        return self._cycle_rate

    @cycle_rate.setter
    def cycle_rate(self, value):
        if (value < 0) or (value > 3):
            raise ValueError("cycle_rate must be a Rate")
        self._cycle_rate = value
        sleep(0.01)
