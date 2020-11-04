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


def assert_rgb_image(image: np.ndarray):
    """
    :param image: the image to check for its properties
    """
    assert type(image) == np.ndarray, "The Image needs to be a numpy.ndarray!"
    assert image.dtype == np.float64, "The Image elements to be a float!"
    assert len(image.shape) == 3, "The Image needs to have a dimension of three!"
    assert image.shape[2] == 3, "The Image needs to have three color channels!"


def assert_rgba_image(image: np.ndarray):
    """
    :param image: the image to check for its properties
    """
    assert type(image) == np.ndarray, "The Image needs to be a numpy.ndarray!"
    assert image.dtype == np.float64, "The Image elements to be a float!"
    assert len(image.shape) == 3, "The Image needs to have a dimension of three!"
    assert image.shape[2] == 4, "The Image needs to have four color channels!"


def assert_a_image(image: np.ndarray):
    """
    :param image: the image to check for its properties
    """
    assert type(image) == np.ndarray, "The Image needs to be a numpy.ndarray!"
    assert image.dtype == np.float64, "The Image elements to be a float!"
    assert len(image.shape) == 3, "The Image needs to have a dimension of three!"
    assert image.shape[2] == 1, "The Image needs to have only one alpha channel!"


def assert_mask(mask: np.ndarray):
    """
    :param mask: the mask to check for its properties
    """
    assert type(mask) == np.ndarray, "The Mask needs to be a numpy.ndarray!"
    assert mask.dtype == np.bool_, "The Mask needs to be a bool mask!"
    assert len(mask.shape) == 2, "The Mask needs to have a dimension of two!"


def assert_image_mask(image: np.ndarray, mask: np.ndarray):
    """
    :param image: the image to check for its properties
    :param mask: the mask to check for its properties
    """
    assert image.shape[0] == mask.shape[0], "The Image and Mask need to have the same width"
    assert image.shape[1] == mask.shape[1], "The Image and Mask need to have the same height"


def assert_kernel(kernel: np.ndarray):
    """
    :param kernel: the kernel to check for its properties
    """
    assert type(kernel) == np.ndarray, "The Kernel needs to be a numpy.ndarray!"
    assert kernel.dtype == np.bool_, "The Kernel needs to be a bool mask!"
    assert kernel.shape[0] == kernel.shape[1], "The Kernel needs to have a quadratic shape!"
    assert len(kernel.shape) == 2, "The Kernel needs to have a dimension of two!"
    assert kernel.shape[0] & 1 == 1, "The Kernel needs to have an uneven size!"


def assert_kernel_size(kernel_size: int):
    """
    :param kernel_size: the mask to check for its properties
    """
    assert kernel_size & 1 == 1, "The kernel needs to have an uneven size as it needs a center!"
    assert kernel_size > 0, "The kernel needs to be bigger than zero to be meaningful!"
