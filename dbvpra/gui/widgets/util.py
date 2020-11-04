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
from PySide2.QtGui import QPainter, QImage
from qimage2ndarray import rgb_view, alpha_view, array2qimage


def load_q_image_from_path(image_path: str):
    """
    :param image_path:
    :return:
    """
    image = QImage(image_path)
    image.convertTo(QImage.Format_RGB32)
    return image


def q_image_to_np_image(q_image: QImage) -> np.ndarray:
    """
    :param q_image:
    :return:
    """
    np_image = rgb_view(q_image)
    np_image = np_image / 255
    np_image = np.array(np_image, dtype=np.float64)
    return np_image


def transparent_q_image_to_np_image(q_image: QImage) -> np.ndarray:
    """
    :param q_image:
    :return:
    """
    np_image = np.dstack((rgb_view(q_image), alpha_view(q_image)))
    np_image = np.array(np_image, dtype=np.float64)
    np_image = np_image / 255
    return np_image


def np_image_to_q_image(np_image: np.ndarray) -> QImage:
    """
    :param np_image:
    :return:
    """
    q_image = np_image * 255
    q_image = array2qimage(q_image)
    q_image.convertTo(QImage.Format_RGB32)
    return q_image


def transparent_np_image_to_q_image(np_image: np.ndarray) -> QImage:
    """
    :param np_image:
    :return:
    """
    q_image = np_image * 255
    q_image = array2qimage(q_image)
    q_image.convertTo(QImage.Format_ARGB32)
    return q_image


def clear_transparent_image(image: QImage):
    """
    :param image: the image to clear
    :return: the clean image
    """
    image.convertTo(QImage.Format_ARGB32)
    width, height = image.width(), image.height()

    painter = QPainter(image)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.fillRect(0, 0, width, height, Qt.transparent)
    painter.end()

    # TODO check if return is needed
    return image


def generate_clean_transparent_image(width, height):
    """
    :param width: the width of the image
    :param height: the height of the image
    :return: transparent image
    """
    return clear_transparent_image(QImage(width, height, QImage.Format_ARGB32))


def clear_image(image: QImage):
    """
    :param image: the image to clear
    :return: the clean image
    """
    image.convertTo(QImage.Format_RGB32)
    width, height = image.width(), image.height()

    painter = QPainter(image)
    painter.fillRect(0, 0, width, height, Qt.white)
    painter.end()

    # TODO check if return is needed
    return image


def generate_clean_image(width, height):
    """
    :param width: the width of the image
    :param height: the height of the image
    :return: white image
    """
    return clear_image(QImage(width, height, QImage.Format_RGB32))
