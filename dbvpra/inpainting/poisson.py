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

from dbvpra.assert_util import assert_image, assert_mask, assert_image_mask
from dbvpra.inpainting.util import _o, _d_hat, _lsqr, _vec, _unvec, _mask_bounds


def poisson(image: np.ndarray, foreign: np.ndarray, mask: np.ndarray):
    """
    :param image: the image to embed into
    :param foreign: the foreign image to embed
    :param mask: the mask where to poisson inpaint
    :return: the poisson inpainted image
    """

    assert_image(image)
    assert_image(foreign)
    assert_mask(mask)
    assert_image_mask(image, mask)
    assert_image_mask(foreign, mask)

    ###
    # chop down the image size to the needed area only
    # because the needed memory is exponential!

    y_min, y_max, x_min, x_max = _mask_bounds(mask)
    ny, nx = y_max - y_min, x_max - x_min

    vec_chop_image = _vec(image[y_min:y_max, x_min:x_max])
    vec_chop_foreign = _vec(foreign[y_min:y_max, x_min:x_max])
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
        b_add = d_hat @ vec_chop_foreign[:, c]
        vec_result[vec_mask, c] = _lsqr(a, b + b_add)

    vec_result = np.clip(vec_result, 0, 1)
    return _unvec(vec_result, image.shape[0])
