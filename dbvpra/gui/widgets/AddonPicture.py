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

from dbvpra.gui.widgets.util import Q, Q2Np


class AddonPicture:
    _picture: QImage

    def __init__(self, width, height):
        self._picture = Q.rgb_image_generate(width, height)

    def on_picture_changed(self, image: QImage):
        """"""

    def picture_load_from_path(self, picture_path: str):
        self._picture = Q.rgb_image_load_from_path(picture_path)
        self._picture.convertTo(QImage.Format_RGB32)
        self.on_picture_changed(self._picture)

    def picture_rgb_image(self) -> np.ndarray:
        return Q2Np.rgb_image(self._picture)

    def picture_width(self) -> int:
        return self._picture.width()

    def picture_height(self) -> int:
        return self._picture.height()

    def picture_paint(self, painter: QPainter):
        painter.drawImage(0, 0, self._picture)
