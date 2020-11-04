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
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QImage, QColor
from qimage2ndarray import rgb_view, alpha_view, array2qimage


class Np:

    @staticmethod
    def rgba_merge(rgb_image: np.ndarray, a_image: np.ndarray) -> np.ndarray:
        return np.dstack((rgb_image, a_image))

    @staticmethod
    def rgb_extract(rgba_image: np.ndarray) -> np.ndarray:
        """TODO check"""
        ny, nx = rgba_image.shape[:2]
        return [[rgba_image[y, x, :3] for y in range(ny)] for x in range(nx)]

    @staticmethod
    def a_extract(rgba_image: np.ndarray) -> np.ndarray:
        """TODO check"""
        ny, nx = rgba_image.shape[:2]
        return [[rgba_image[y, x, 3:4] for y in range(ny)] for x in range(nx)]


class Q2Np:

    @staticmethod
    def rgb_image(image: QImage) -> np.ndarray:
        image = rgb_view(image)
        image = np.array(image, dtype=np.float64)
        image = image / 255
        return image

    @staticmethod
    def a_image(image: QImage) -> np.ndarray:
        image = alpha_view(image)
        image = np.array(image, dtype=np.float64)
        image = image / 255
        return image

    @staticmethod
    def rgba_image(image: QImage) -> np.ndarray:
        image = np.dstack((rgb_view(image), alpha_view(image)))
        image = np.array(image, dtype=np.float64)
        image = image / 255
        return image

    @staticmethod
    def rgb_color(color: QColor) -> np.ndarray:
        color = [color.red(), color.green(), color.blue()]
        color = np.array(color, dtype=np.float64)
        color = color / 255
        return color

    @staticmethod
    def rgba_color(color: QColor) -> np.ndarray:
        color = [color.red(), color.green(), color.blue(), color.alpha()]
        color = np.array(color, dtype=np.float64)
        color = color / 255
        return color


class Np2Q:

    @staticmethod
    def rgb_image(image: np.ndarray) -> QImage:
        image = image * 255
        image = array2qimage(image)
        image.convertTo(QImage.Format_RGB32)
        return image

    @staticmethod
    def rgba_image(image: np.ndarray) -> QImage:
        image = image * 255
        image = array2qimage(image)
        image.convertTo(QImage.Format_ARGB32)
        return image

    @staticmethod
    def rgb_color(color: np.ndarray) -> QColor:
        color = color * 255
        color = QColor(color[0], color[1], color[2])
        return color

    @staticmethod
    def rgba_color(color: np.ndarray) -> QColor:
        color = color * 255
        color = QColor(color[0], color[1], color[2], color[3])
        return color


class Q:

    @staticmethod
    def assert_rgb_image(image: QImage):
        assert image.format() == QImage.Format_RGB32, "The QImage has the wrong format to be interpreted as rgb!"

    @staticmethod
    def assert_rgba_image(image: QImage):
        assert image.format() == QImage.Format_ARGB32, "The QImage has the wrong format to be interpreted as rgba!"

    @staticmethod
    def rgb_image_generate(width: int, height: int) -> QImage:
        image = QImage(width, height, QImage.Format_RGB32)
        image = Q.rgb_image_clear(image)
        return image

    @staticmethod
    def rgba_image_generate(width: int, height: int) -> QImage:
        image = QImage(width, height, QImage.Format_ARGB32)
        image = Q.rgba_image_clear(image)
        return image

    @staticmethod
    def rgb_image_load_from_path(path: str) -> QImage:
        image = QImage(path)
        image.convertTo(QImage.Format_RGB32)
        return image

    @staticmethod
    def rgba_image_load_from_path(path: str) -> QImage:
        image = QImage(path)
        image.convertTo(QImage.Format_ARGB32)
        return image

    @staticmethod
    def rgb_image_clear(image: QImage) -> QImage:
        nx, ny = image.width(), image.height()
        painter = QPainter(image)
        painter.fillRect(0, 0, nx, ny, Qt.white)
        painter.end()
        return image

    @staticmethod
    def rgba_image_clear(image: QImage) -> QImage:
        nx, ny = image.width(), image.height()
        painter = QPainter(image)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(0, 0, nx, ny, Qt.transparent)
        painter.end()
        return image
