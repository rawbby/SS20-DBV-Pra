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
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPainter, QImage, QPen, QColor

from dbvpra.assert_util import assert_mask
from dbvpra.gui.widgets.util import Q, Q2Np


class AddonCanvas:
    """
    The CanvasAddon wraps a QImage and allows operations no it using numpy data structures.
    Therefor it is more specific for this project. The CanvasAddon also remembers a history
    of changes made to the QImage. This way it allows to undo and redo changes.
    """

    _TRANSPARENT = QColor(0, 0, 0, 0)
    _PRIMARY_GREEN = QColor(50, 230, 50, 192)
    _SECONDARY_RED = QColor(255, 10, 10, 128)

    _canvas: QImage
    _pen: QPen

    _stack_size: int
    _undo_stack: [QImage]
    _redo_stack: [QImage]

    def __init__(self, width: int, height: int, max_steps: int = 48):
        """
        :param width: the width of the canvas
        :param height: the height of the canvas
        :param max_steps: the amount of steps you can undo/redo
        """

        self._canvas = Q.rgba_image_generate(width, height)

        self._stack_size = max_steps
        self._undo_stack = []
        self._redo_stack = []

        self._pen = QPen()
        self._pen.setStyle(Qt.SolidLine)
        self._pen.setJoinStyle(Qt.RoundJoin)
        self._pen.setWidth(12)
        self._pen.setColor(AddonCanvas._PRIMARY_GREEN)

        self._pen_enable = False
        self._pen_pos = QPoint(0, 0)

    def on_canvas_changed(self, image: QImage):
        """"""

    def canvas_paint(self, painter: QPainter):
        """
        :param painter: the painter to paint onto
        """
        painter.drawImage(QPoint(0, 0), self._canvas)

    def canvas_step(self):
        """
        Backup the current canvas
        """

        self._redo_stack.clear()
        if len(self._undo_stack) >= self._stack_size:
            self._undo_stack.pop(0)

        self._undo_stack.append(self._canvas.copy())

    def canvas_reset(self, width: int, height: int):
        """
        Clear the canvas history and adjust the size of the canvas.
        :param width: the width of the canvas
        :param height: the height of the canvas
        """
        self._canvas = Q.rgba_image_generate(width, height)
        self._undo_stack = []
        self._redo_stack = []
        self.on_canvas_changed(self._canvas)

    def canvas_undo(self):
        """
        Restore the last canvas
        """
        if len(self._undo_stack) > 0:
            self._redo_stack.append(self._canvas)
            self._canvas = self._undo_stack.pop()
            self.on_canvas_changed(self._canvas)

    def canvas_redo(self):
        """
        Restore the canvas last undone
        """
        if len(self._redo_stack) > 0:
            self._undo_stack.append(self._canvas)
            self._canvas = self._redo_stack.pop()
        self.on_canvas_changed(self._canvas)

    def canvas_set_pen_primary(self):
        """
        Use the primary pen from now on to draw onto the canvas
        """
        self._pen.setColor(AddonCanvas._PRIMARY_GREEN)

    def canvas_set_pen_secondary(self):
        """
        Use the secondary pen from now on to draw onto the canvas
        """
        self._pen.setColor(AddonCanvas._SECONDARY_RED)

    def canvas_set_pen_erase(self):
        """
        Use the erase pen from now on to draw onto the canvas
        """
        self._pen.setColor(AddonCanvas._TRANSPARENT)

    def _canvas_mask(self, q_color: QColor) -> np.ndarray:
        """
        :param q_color: the color to extract the mask from
        :return: the mask of the color passed
        """

        np_color = Q2Np.rgb_color(q_color)
        np_canvas = Q2Np.rgb_image(self._canvas)
        ny, nx = np_canvas.shape[:2]

        np_mask = [[np.all(np_canvas[y, x] == np_color) for x in range(nx)] for y in range(ny)]
        np_mask = np.array(np_mask, dtype=np.bool_)
        return np_mask

    def canvas_primary_mask(self) -> np.ndarray:
        """
        :return: the mask of the primary color
        """
        return self._canvas_mask(AddonCanvas._PRIMARY_GREEN)

    def canvas_secondary_mask(self) -> np.ndarray:
        """
        :return: the mask of the secondary color
        """
        return self._canvas_mask(AddonCanvas._SECONDARY_RED)

    def canvas_erase_mask(self) -> np.ndarray:
        """
        :return: the mask of the erase color
        """
        return self._canvas_mask(AddonCanvas._TRANSPARENT)

    def _canvas_fill_mask(self, np_mask: np.ndarray, q_color: QColor):
        """
        :param np_mask: the mask to stamp on the canvas
        :param q_color: the color used to stamp
        """

        assert_mask(np_mask)

        self.canvas_clear()

        painter = QPainter(self._canvas)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        pixel_pen = QPen()
        pixel_pen.setWidth(1)
        pixel_pen.setColor(q_color)
        painter.setPen(pixel_pen)

        for y, x in zip(*np.where(np_mask)):
            painter.drawPoint(x, y)

        painter.end()
        self.on_canvas_changed(self._canvas)

    def canvas_fill_primary_mask(self, np_mask: np.ndarray):
        """
        :param np_mask: the mask to stamp on the canvas
        """
        self._canvas_fill_mask(np_mask, AddonCanvas._PRIMARY_GREEN)

    def canvas_clear(self):
        """
        clears all content on the canvas
        """
        self._canvas = Q.rgba_image_clear(self._canvas)
        self.on_canvas_changed(self._canvas)

    def canvas_draw_line(self, start: QPoint, end: QPoint):
        """
        :param start: the start position of the line to draw
        :param end: the end position of the line to draw
        """
        painter = QPainter(self._canvas)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.setPen(self._pen)
        painter.drawLine(start, end)
        painter.end()
        self.on_canvas_changed(self._canvas)
