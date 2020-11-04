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

from dbvpra.assert_util import assert_rgb_image, assert_mask, assert_image_mask
from dbvpra.inpainting.util import _o, _d_hat, _lsqr, _vec, _un_vec, _mask_bounds


def inpainting(image: np.ndarray, mask: np.ndarray):
    """
    :param image: the image to inpaint
    :param mask: the mask where to inpaint
    :return: the inpainted image
    """

    assert_rgb_image(image)
    assert_mask(mask)
    assert_image_mask(image, mask)

    ###
    # chop down the image size to the needed area only
    # because the needed memory is exponential!

    y_min, y_max, x_min, x_max = _mask_bounds(mask)
    ny, nx = y_max - y_min, x_max - x_min

    vec_chop_image = _vec(image[y_min:y_max, x_min:x_max])
    vec_chop_mask = _vec(mask[y_min:y_max, x_min:x_max])

    ###
    # Begin algorithm

    vec_result = _vec(np.copy(image))
    vec_mask = _vec(mask)

    # 1_I
    o = _o(vec_chop_mask)

    # D_hat
    d_hat = _d_hat(ny, nx)

    # A
    a = d_hat @ o

    for c in range(3):
        b = -d_hat @ (~vec_chop_mask * vec_chop_image[:, c])
        vec_result[vec_mask, c] = _lsqr(a, b)  # x = arg min || Ax + b ||^2

    vec_result[vec_result < 0.0] = 0.0
    vec_result[vec_result > 1.0] = 1.0

    return _un_vec(vec_result, image.shape[0])

# def inpainting1d(image: np.ndarray, mask: np.ndarray):
#     """
#     :param image: the image to inpaint
#     :param mask: the mask where to inpaint
#     :return: the inpainted image
#     """
#
#     ##
#     # calculate 1_I and D
#
#     o = _o(mask)
#     d = _d(len(mask))
#
#     ##
#     # calculate A and b
#
#     a = d @ o
#     b = - (d @ (~mask * image))
#
#     ##
#     # calculate the result
#
#     result = np.copy(image)
#     result[mask] = _lsqr(a, b)
#
#     return result
