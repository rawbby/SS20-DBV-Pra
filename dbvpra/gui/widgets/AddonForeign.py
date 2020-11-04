#  Copyright (c) 2020 Robert Andreas Fritsch
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import numpy as np
from PySide2.QtGui import QPainter, QImage

from dbvpra.assert_util import assert_rgba_image
from dbvpra.gui.widgets.util import Q, Np2Q


class AddonForeign:
    _foreign_x_min: int
    _foreign_y_min: int
    _foreign_x_max: int
    _foreign_y_max: int

    _foreign: QImage
    _foreign_x: int
    _foreign_y: int

    def __init__(self, width, height):
        self._foreign_x_min = 0
        self._foreign_y_min = 0
        self._foreign_x_max = width - 1
        self._foreign_y_max = height - 1
        self._foreign = Q.rgba_image_generate(0, 0)
        self._foreign_x = 0
        self._foreign_y = 0

    def on_foreign_changed(self):
        """"""

    def foreign_translate(self, x: int, y: int):
        def clip(_x, _l, _u):
            return max(_l, min(_u, _x))

        x = self._foreign_x + x
        y = self._foreign_y + y

        self._foreign_x = clip(x, self._foreign_x_min, self._foreign_x_max)
        self._foreign_y = clip(y, self._foreign_y_min, self._foreign_y_max)
        self.on_foreign_changed()

    def foreign_reset(self, width, height):
        self._foreign_x_min = 0
        self._foreign_y_min = 0
        self._foreign_x_max = width - 1
        self._foreign_y_max = height - 1
        self._foreign = Q.rgba_image_generate(0, 0)
        self._foreign_x = 0
        self._foreign_y = 0

        self.on_foreign_changed()

    def foreign_set_foreign(self, foreign: np.ndarray):
        assert_rgba_image(foreign)
        self._foreign = Np2Q.rgba_image(foreign)
        self._foreign_x_min = -self._foreign.width() + 1
        self._foreign_y_min = -self._foreign.height() + 1
        self._foreign_x = 0
        self._foreign_y = 0

        self.on_foreign_changed()

    def foreign_rgba_image(self) -> np.ndarray:
        nx = self._foreign_x_max + 1
        ny = self._foreign_y_max + 1
        image = Q.rgba_image_generate(nx, ny)
        painter = QPainter(image)
        self.foreign_paint(painter)
        painter.end()
        return image

    def foreign_paint(self, painter: QPainter):
        painter.drawImage(self._foreign_x, self._foreign_y, self._foreign)
