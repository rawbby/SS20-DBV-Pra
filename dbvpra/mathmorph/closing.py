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

from dbvpra.assert_util import assert_source, assert_kernel


def closing(source: np.ndarray, kernel: np.ndarray):
    """
    :param source: the source image to close
    :param kernel: the kernel used to close the source
    :return: the closed source
    """

    assert_source(source)
    assert_kernel(kernel)

    """1. Invent some aliases for the algorithm"""
    kernel_size = kernel.shape[0]
    (width, height) = source.shape

    """2. Pad the source for a more easy iteration"""
    source = np.pad(source, kernel_size >> 1, mode='edge')

    """3. The algorithm"""
    destination = np.empty((width, height), np.bool_)
    for x in range(0, width):
        for y in range(0, height):
            pat = source[x:x + kernel_size, y:y + kernel_size]
            destination[x, y] = np.any(np.multiply(pat, kernel))

    return destination
