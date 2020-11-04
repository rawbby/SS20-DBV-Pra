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

from dbvpra.assert_util import assert_image, assert_mask, assert_image_mask, assert_patch_size


def _patchify(image: np.ndarray, patch_size: int):
    """
    :param image: The Image to patchify
    :param patch_size: The size of the patches
    :return: The patches as two dimensional array
    """

    assert_image(image)
    assert_patch_size(patch_size, image)

    patch_pad = patch_size >> 1
    patches_width = image.shape[0]
    patches_height = image.shape[1]

    patches = np.empty((patches_width, patches_height, patch_size, patch_size, 3), np.float64)
    image = np.pad(image, ((patch_pad, patch_pad), (patch_pad, patch_pad), (0, 0)), mode='edge')

    for x in range(0, patches_width):
        for y in range(0, patches_height):
            patch = image[x:x + patch_size, y:y + patch_size]
            patches[x, y] = patch

    return patches


def _patchify_info(image: np.ndarray, patch_size: int):
    """
    :param image: The Image to patchify
    :param patch_size: The size of the patches
    :return: The patch info as two dimensional array
    """

    coordinates = [np.array([x, y], dtype=np.float64)
                   for x in range(0, image.shape[0])
                   for y in range(0, image.shape[1])]

    patches = _patchify(image, patch_size)

    patches = patches.reshape((image.shape[0] * image.shape[1], patch_size * patch_size * 3))

    return np.append(patches, coordinates, axis=1)


def _patchify_from_mask(image: np.ndarray, patch_size: int, mask: np.ndarray):
    """
    :param image: The Image to patchify
    :param patch_size: The size of the patches
    :param mask: The Mask to filter the patches
    :return: The patches as one dimensional array
    """

    patches = _patchify(image, patch_size)
    assert_mask(mask)
    assert_image_mask(image, mask)

    return patches[mask]


def _patchify_info_from_mask(image: np.ndarray, patch_size: int, mask: np.ndarray):
    """
    :param image: The Image to patchify
    :param patch_size: The size of the patches
    :param mask: The Mask to filter the patches
    :return: The patch info as two dimensional array
    """

    info = _patchify_info(image, patch_size)
    assert_mask(mask)
    assert_image_mask(image, mask)

    return info[mask.flatten()]
