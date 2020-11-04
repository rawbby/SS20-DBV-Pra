#  Copyright (c) 2020 Robert Andreas Fritsch
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
from PySide2.QtCore import QPoint
from PySide2.QtGui import QImage, QPainter, QImageWriter
from PySide2.QtWidgets import QWidget, QLabel

from dbvpra.gui.widgets.AddonForeign import AddonForeign
from dbvpra.gui.widgets.AddonPicture import AddonPicture
from dbvpra.gui.widgets.util import Q


class Merge(QLabel, AddonPicture, AddonForeign):
    _move_enable: bool
    _move_pos: QPoint

    def __init__(self, parent: QWidget, width=256, height=256):
        QLabel.__init__(self, parent)
        AddonPicture.__init__(self, width, height)
        AddonForeign.__init__(self, width, height)

        self.setFixedSize(width, height)
        self._move_enable = False
        self._move_pos = QPoint(0, 0)

    def on_foreign_changed(self):
        self.repaint()

    def on_picture_changed(self, image: QImage):
        self.setFixedSize(image.size())
        self.foreign_reset(image.width(), image.height())

    def export(self, export_path: str):
        nx = self.picture_width()
        ny = self.picture_height()
        merge = Q.rgba_image_generate(nx, ny)

        painter = QPainter(merge)
        self.picture_paint(painter)
        self.foreign_paint(painter)
        painter.end()

        writer = QImageWriter(export_path)
        writer.write(merge)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.picture_paint(painter)
        self.foreign_paint(painter)
        painter.end()

    def _move(self, p: QPoint):
        diff = p - self._move_pos
        self.foreign_translate(diff.x(), diff.y())
        self._move_pos = p

    def mousePressEvent(self, event):
        self._move_enable = True
        self._move_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self._move_enable:
            self._move(event.pos())
            self.repaint()

    def mouseReleaseEvent(self, event):
        self._move(event.pos())
        self._move_enable = False
        self.repaint()
