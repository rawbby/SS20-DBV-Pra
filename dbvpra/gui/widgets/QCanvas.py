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

from dbvpra.gui.widgets.util import q_image_to_np_image, clear_transparent_image, generate_clean_transparent_image


class QCanvas:
    """
    The QCanvas wraps a QImage and allows operations no it using numpy data structures.
    Therefor it is more specific for this project. The QCanvas also remembers a history
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

    def __init__(self, width, height, max_steps=48):
        """
        :param width: the width of the canvas
        :param height: the height of the canvas
        :param max_steps: the amount of steps you can undo/redo
        """

        self._canvas = generate_clean_transparent_image(width, height)

        self._stack_size = max_steps
        self._undo_stack = []
        self._redo_stack = []

        self._pen = QPen()
        self._pen.setStyle(Qt.SolidLine)
        self._pen.setJoinStyle(Qt.RoundJoin)
        self._pen.setWidth(12)
        self._pen.setColor(QCanvas._PRIMARY_GREEN)

        self._pen_enable = False
        self._pen_pos = QPoint(0, 0)

    def on_canvas_changed(self):
        """"""

    def canvas_paint(self, painter: QPainter):
        """
        :param painter: the painter to paint onto
        """
        painter.drawImage(QPoint(0, 0), self._canvas)

    def _canvas_step(self):
        """
        Backup the current canvas
        """
        self._redo_stack.clear()
        if len(self._undo_stack) >= self._stack_size:
            self._undo_stack.pop(0)

        self._undo_stack.append(QImage.copy(self._canvas))

    def canvas_reset(self, width, height):
        """
        Clear the canvas history and adjust the size of the canvas.
        :param width: the width of the canvas
        :param height: the height of the canvas
        """
        self._canvas = generate_clean_transparent_image(width, height)
        self._undo_stack = []
        self._redo_stack = []
        self.on_canvas_changed()

    def canvas_undo(self):
        """
        Restore the last canvas
        """
        if len(self._undo_stack) > 0:
            self._redo_stack.append(self._canvas)
            self._canvas = self._undo_stack.pop()
        self.on_canvas_changed()

    def canvas_redo(self):
        """
        Restore the canvas last undone
        """
        if len(self._redo_stack) > 0:
            self._undo_stack.append(self._canvas)
            self._canvas = self._redo_stack.pop()
        self.on_canvas_changed()

    def canvas_set_pen_primary(self):
        """
        Use the primary pen from now on to draw onto the canvas
        """
        self._pen.setColor(QCanvas._PRIMARY_GREEN)

    def canvas_set_pen_secondary(self):
        """
        Use the secondary pen from now on to draw onto the canvas
        """
        self._pen.setColor(QCanvas._SECONDARY_RED)

    def canvas_set_pen_erase(self):
        """
        Use the erase pen from now on to draw onto the canvas
        """
        self._pen.setColor(QCanvas._TRANSPARENT)

    def _canvas_mask(self, q_color: QColor):
        """
        :param q_color: the color to extract the mask from
        :return: the mask of the color passed
        """

        np_color = [q_color.red(), q_color.green(), q_color.blue()]
        np_color = np.array(np_color, dtype=np.float64)
        np_color = np_color / 255

        np_canvas = q_image_to_np_image(self._canvas)
        ny, nx = np_canvas.shape[:2]

        np_mask = [[np.any(np_canvas[y, x] == np_color) for x in range(nx)] for y in range(ny)]
        np_mask = np.array(np_mask, dtype=np.bool_)
        return np_mask

    def canvas_primary_mask(self):
        """
        :return: the mask of the primary color
        """
        return self._canvas_mask(QCanvas._PRIMARY_GREEN)

    def canvas_secondary_mask(self):
        """
        :return: the mask of the secondary color
        """
        return self._canvas_mask(QCanvas._SECONDARY_RED)

    def canvas_erase_mask(self):
        """
        :return: the mask of the erase color
        """
        return self._canvas_mask(QCanvas._TRANSPARENT)

    def _canvas_fill_mask(self, np_mask: np.ndarray, q_color: QColor, step=True):
        """
        :param np_mask: the mask to stamp on the canvas
        :param q_color: the color used to stamp
        """

        # implicit step
        QCanvas.canvas_clear(self, step=step)

        painter = QPainter(self._canvas)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        pixel_pen = QPen()
        pixel_pen.setWidth(1)
        pixel_pen.setColor(q_color)
        painter.setPen(pixel_pen)

        for y, x in zip(*np.where(np_mask)):
            painter.drawPoint(x, y)

        painter.end()
        self.on_canvas_changed()

    def canvas_fill_primary_mask(self, np_mask: np.ndarray, step=True):
        """
        (hint: this method steps!)
        :param np_mask: the mask to stamp on the canvas
        """

        if step:
            self._canvas_step()

        self._canvas_fill_mask(np_mask, QCanvas._PRIMARY_GREEN)

    def canvas_clear(self, step=True):
        """
        (hint: this method steps!)
        clears all content on the canvas
        """

        if step:
            self._canvas_step()

        self._canvas = clear_transparent_image(self._canvas)
        self.on_canvas_changed()

    def canvas_draw_line(self, start: QPoint, end: QPoint, step=True):
        """
        (hint: this method steps by default)
        :param start: the start position of the line to draw
        :param end: the end position of the line to draw
        :param step: whether to step or not
        """

        if step:
            self._canvas_step()

        painter = QPainter(self._canvas)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.setPen(self._pen)
        painter.drawLine(start, end)
        painter.end()
        self.on_canvas_changed()
