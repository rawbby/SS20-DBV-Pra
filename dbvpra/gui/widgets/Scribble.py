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
from PySide2.QtWidgets import QWidget

from dbvpra.gui.widgets.QCanvas import QCanvas
from dbvpra.gui.widgets.QImageWidget import QImageWidget


class Scribble(QImageWidget, QCanvas):
    """
    """

    _pen_enable: bool
    _pen_pos: QPoint

    def __init__(self, parent: QWidget, width=256, height=256):
        """
        :param parent:
        :param width:
        :param height:
        """

        QImageWidget.__init__(self, parent, width, height)
        QCanvas.__init__(self, width, height)

        self._pen_enable = False
        self._pen_pos = QPoint(0, 0)

    def on_canvas_changed(self):
        """"""
        QImageWidget.repaint(self)

    def on_image_changed(self, image: QImage):
        """"""
        QCanvas.canvas_reset(self, image.width(), image.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)
        QCanvas.canvas_paint(self, painter)
        painter.end()

    def mousePressEvent(self, event):
        self._pen_enable = True
        self._pen_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self._pen_enable:
            QCanvas.canvas_draw_line(self, self._pen_pos, event.pos(), step=False)
            self._pen_pos = event.pos()
            QImageWidget.repaint(self)

    def mouseReleaseEvent(self, event):
        QCanvas.canvas_draw_line(self, self._pen_pos, event.pos())
        self._pen_enable = False
        QImageWidget.repaint(self)
