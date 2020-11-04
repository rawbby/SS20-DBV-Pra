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


def assert_source(source: np.ndarray):
    """
    :param source: the source to check for its properties
    """
    assert type(source) == np.ndarray, "The Source needs to be a numpy.ndarray!"
    assert source.dtype == np.bool_, "The Source elements need to be a bool!"
    assert len(source.shape) == 2, "The Source needs to have a dimension of two!"


def assert_kernel(kernel: np.ndarray):
    """
    :param kernel: the kernel to check for its properties
    """
    assert type(kernel) == np.ndarray, "The Kernel needs to be a numpy.ndarray!"
    assert kernel.dtype == np.bool_, "The Kernel needs to be a bool mask!"
    assert kernel.shape[0] == kernel.shape[1], "The Kernel needs to have a quadratic shape!"
    assert len(kernel.shape) == 2, "The Kernel needs to have a dimension of two!"
    assert kernel.shape[0] & 1 == 1, "The Kernel needs to have an uneven size!"


def assert_image(image: np.ndarray):
    """
    :param image: the image to check for its properties
    """
    assert type(image) == np.ndarray, "The Image needs to be a numpy.ndarray!"
    assert image.dtype == np.float64, "The Image elements to be a float!"
    assert len(image.shape) == 3, "The Image needs to have a dimension of three!"
    assert image.shape[2] == 3, "The Image needs to have a three color channels!"


def assert_mask(mask: np.ndarray):
    """
    :param mask: the mask to check for its properties
    """
    assert type(mask) == np.ndarray, "The Mask needs to be a numpy.ndarray!"
    assert mask.dtype == np.bool_, "The Mask needs to be a bool mask!"
    assert len(mask.shape) == 2, "The Mask needs to have a dimension of two!"


def assert_patch_size(patch_size: int, image: np.ndarray = None):
    """
    :param patch_size: the mask to check for its properties
    :param image: the image to use the patch on
    """
    assert patch_size & 1 == 1, "The patches need to have an uneven size! " \
                                "This patch function is used for patches with a center! "
    assert patch_size > 0, "The patches need to be bigger than zero to be meaningful!"

    if image is not None:
        assert patch_size <= image.shape[0], "The patches need to be smaller than the width of the Image!"
        assert patch_size <= image.shape[1], "The patches need to be smaller than the height of the Image!"


def assert_image_mask(image: np.ndarray, mask: np.ndarray):
    """
    :param image: the image to check for its properties
    :param mask: the mask to check for its properties
    """
    assert image.shape[0] == mask.shape[0], "The Image and Mask need to have the same width"
    assert image.shape[1] == mask.shape[1], "The Image and Mask need to have the same height"
