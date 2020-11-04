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

from dbvpra.assert_util import assert_mask, assert_kernel


def opening(mask: np.ndarray, kernel: np.ndarray):
    """
    :param mask: the source image to open
    :param kernel: the kernel used to open the source
    :return: the opened source
    """

    assert_mask(mask)
    assert_kernel(kernel)

    """1. Invent some aliases for the algorithm"""
    kernel_size = kernel.shape[0]
    (width, height) = mask.shape

    """2. Pad the source for a more easy iteration"""
    mask = np.pad(mask, kernel_size >> 1, mode='edge')

    """3. The algorithm"""
    destination = np.empty((width, height), np.bool_)
    for x in range(0, width):
        for y in range(0, height):
            pat = mask[x:x + kernel_size, y:y + kernel_size]
            destination[x, y] = np.array_equal(np.multiply(pat, kernel), kernel)

    return destination
