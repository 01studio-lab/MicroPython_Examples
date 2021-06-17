# The MIT License (MIT)
#
# Copyright (c) 2019 Limor Fried for Adafruit Industries
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
`polygon`
================================================================================

Various common shapes for use with displayio - Polygon shape!


* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes.git"


class Polygon(displayio.TileGrid):
    # pylint: disable=too-many-arguments,invalid-name
    """A polygon.

    :param points: A list of (x, y) tuples of the points
    :param fill: The color to fill the polygon. Can be a hex value for a color or
                 ``None`` for transparent.
    :param outline: The outline of the polygon. Can be a hex value for a color or
                    ``None`` for no outline.
    """

    def __init__(self, points, *, outline=None):
        xs = []
        ys = []

        for point in points:
            xs.append(point[0])
            ys.append(point[1])

        x_offset = min(xs)
        y_offset = min(ys)

        # Find the largest and smallest X values to figure out width for bitmap
        width = max(xs) - min(xs) + 1
        height = max(ys) - min(ys) + 1

        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(width, height, 3)

        if outline is not None:
            # print("outline")
            self.outline = outline
            for index, _ in enumerate(points):
                point_a = points[index]
                if index == len(points) - 1:
                    point_b = points[0]
                else:
                    point_b = points[index + 1]
                self._line(
                    point_a[0] - x_offset,
                    point_a[1] - y_offset,
                    point_b[0] - x_offset,
                    point_b[1] - y_offset,
                    1,
                )

        super().__init__(
            self._bitmap, pixel_shader=self._palette, x=x_offset, y=y_offset
        )

    # pylint: disable=invalid-name, too-many-locals, too-many-branches
    def _line(self, x0, y0, x1, y1, color):
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for _h in range(y0, y1):
                self._bitmap[x0, _h] = color
        elif y0 == y1:
            if x0 > x1:
                x0, x1 = x1, x0
            for _w in range(x0, x1):
                self._bitmap[_w, y0] = color
        else:
            steep = abs(y1 - y0) > abs(x1 - x0)
            if steep:
                x0, y0 = y0, x0
                x1, y1 = y1, x1

            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = abs(y1 - y0)

            err = dx / 2

            if y0 < y1:
                ystep = 1
            else:
                ystep = -1

            for x in range(x0, x1):
                if steep:
                    self._bitmap[y0, x] = color
                else:
                    self._bitmap[x, y0] = color
                err -= dy
                if err < 0:
                    y0 += ystep
                    err += dx

    # pylint: enable=invalid-name, too-many-locals, too-many-branches

    @property
    def outline(self):
        """The outline of the polygon. Can be a hex value for a color or
        ``None`` for no outline."""
        return self._palette[1]

    @outline.setter
    def outline(self, color):
        if color is None:
            self._palette[1] = 0
            self._palette.make_transparent(1)
        else:
            self._palette[1] = color
            self._palette.make_opaque(1)
