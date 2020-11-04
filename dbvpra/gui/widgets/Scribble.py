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
from PySide2.QtGui import QPainter, QImage
from PySide2.QtWidgets import QWidget, QLabel

from dbvpra.gui.widgets.AddonCanvas import AddonCanvas
from dbvpra.gui.widgets.AddonPicture import AddonPicture


class Scribble(QLabel, AddonPicture, AddonCanvas):
    _pen_enable: bool
    _pen_pos: QPoint

    def __init__(self, parent: QWidget, width=256, height=256):
        QLabel.__init__(self, parent)
        AddonPicture.__init__(self, width, height)
        AddonCanvas.__init__(self, width, height)

        self.setFixedSize(width, height)
        self._pen_enable = False
        self._pen_first = False
        self._pen_pos = QPoint(0, 0)

    def on_canvas_changed(self, image: QImage):
        self.repaint()

    def on_picture_changed(self, image: QImage):
        self.setFixedSize(image.size())
        self.canvas_reset(image.width(), image.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.picture_paint(painter)
        self.canvas_paint(painter)
        painter.end()

    def mousePressEvent(self, event):
        self.canvas_step()
        self._pen_enable = True
        self._pen_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self._pen_enable:
            self.canvas_draw_line(self._pen_pos, event.pos())
            self._pen_pos = event.pos()
            self.repaint()

    def mouseReleaseEvent(self, event):
        self.canvas_draw_line(self._pen_pos, event.pos())
        self._pen_enable = False
        self.repaint()
