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
from PySide2.QtCore import QPoint
from PySide2.QtGui import QImage, QPainter, QImageWriter
from PySide2.QtWidgets import QWidget
from qimage2ndarray import alpha_view

from dbvpra.gui.widgets.QImageWidget import QImageWidget
from dbvpra.gui.widgets.util import generate_clean_transparent_image, transparent_np_image_to_q_image


class Merge(QImageWidget):
    _image: QImage

    _foreign: QImage
    _foreign_pos: QPoint

    _move_enable: bool
    _move_pos: QPoint
    _move_scale: float

    def __init__(self, parent: QWidget, width=256, height=256):
        QImageWidget.__init__(self, parent, width, height)

        self._foreign = generate_clean_transparent_image(width, height)
        self._foreign_pos = QPoint(0, 0)

        self._move_enable = False
        self._move_pos = QPoint(0, 0)
        self._move_scale = 1.0

    def on_image_changed(self, image: QImage):
        self._foreign = generate_clean_transparent_image(image.width(), image.height())
        self._foreign_pos = QPoint(0, 0)

    def export(self, export_path: str):
        merge_image = self.image().copy()

        painter = QPainter(merge_image)
        painter.drawImage(self._foreign_pos, self._foreign)
        painter.end()

        writer = QImageWriter(export_path)
        writer.write(merge_image)

    def set_np_foreign(self, np_foreign: np.ndarray):
        self.set_q_foreign(transparent_np_image_to_q_image(np_foreign))

    def set_q_foreign(self, q_foreign: QImage):
        self._foreign = q_foreign
        self._foreign.convertToFormat(QImage.Format_ARGB32)
        self._foreign_pos = QPoint(0, 0)
        self.repaint()

    def _foreign_mask(self):
        np_mask = alpha_view(self._canvas)
        np_mask = np.array(np_mask, dtype=np.bool_)
        np_mask = np_mask.reshape(np_mask.shape[:2])
        return np_mask

    def _translate_foreign(self, start: QPoint, end: QPoint):
        self._foreign_pos.setX(self._foreign_pos.x() + end.x() - start.x())
        self._foreign_pos.setY(self._foreign_pos.y() + end.y() - start.y())

        x_min = - self._foreign.width() + 1
        y_min = - self._foreign.height() + 1
        x_max = self._image.width() - 1
        y_max = self._image.height() - 1

        if self._foreign_pos.x() > x_max:
            self._foreign_pos.setX(x_max)
        elif self._foreign_pos.x() < x_min:
            self._foreign_pos.setX(x_min)

        if self._foreign_pos.y() > y_max:
            self._foreign_pos.setY(y_max)
        elif self._foreign_pos.y() < y_min:
            self._foreign_pos.setY(y_min)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)
        painter.drawImage(self._foreign_pos, self._foreign)
        painter.end()

    def mousePressEvent(self, event):
        self._move_enable = True
        self._move_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self._move_enable:
            self._translate_foreign(self._move_pos, event.pos())
            self._move_pos = event.pos()
            self.repaint()

    def mouseReleaseEvent(self, event):
        self._translate_foreign(self._move_pos, event.pos())
        self._move_enable = False
        self.repaint()
