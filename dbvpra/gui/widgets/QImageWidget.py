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
from PySide2.QtGui import QPainter, QImage
from PySide2.QtWidgets import QWidget, QLabel

from dbvpra.gui.widgets.util import generate_clean_image, q_image_to_np_image, np_image_to_q_image, \
    load_q_image_from_path


class QImageWidget(QLabel):
    _image: QImage

    def __init__(self, parent: QWidget, width=256, height=256):
        QLabel.__init__(self, parent)

        # generate a clean image
        self._image = generate_clean_image(width, height)

        # adjust the widget size to match the image
        self.setFixedSize(width, height)

    def on_image_changed(self, image: QImage):
        """"""

    def load_image_from_path(self, image_path: str, repaint=True):
        self.set_q_image(load_q_image_from_path(image_path), repaint=repaint)

    def get_np_image(self) -> np.ndarray:
        return q_image_to_np_image(self._image)

    def set_np_image(self, np_image: np.ndarray, repaint=True):
        self.set_q_image(np_image_to_q_image(np_image), repaint=repaint)

    def set_q_image(self, image: QImage, repaint=True):
        # load the image and convert into standard format
        self._image = image
        self._image.convertTo(QImage.Format_RGB32)

        # adjust the widget size to match the image and re-render
        self.setFixedSize(self._image.width(), self._image.height())

        # send image has changed event
        self.on_image_changed(image)

        if repaint:
            self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)
        painter.end()
