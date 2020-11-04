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
import torch
import torch.nn as nn
import torch.nn.functional as f

from dbvpra.assert_util import assert_image, assert_mask, assert_image_mask, assert_patch_size
from dbvpra.segmentation.patchify import _patchify_info


class _SegmentationNN(nn.Module):
    """
    TODO document
    """

    def __init__(self, patch_size: int):
        """
        TODO document
        """

        nn.Module.__init__(self)

        assert_patch_size(patch_size)
        channel = 3
        coordinates = 2

        inputs = (patch_size ** 2) * channel + coordinates
        hidden = ((patch_size + 1) ** 2) * channel + coordinates
        output = 1

        self.inputs = nn.Linear(inputs, hidden)
        self.hidden = nn.Linear(hidden, output)

    def forward(self, x):
        """
        TODO document
        """

        x = f.relu(self.inputs(x))
        x = self.hidden(x)

        return x


def _train_segmentation_nn(net: _SegmentationNN, inputs, labels, max_iterations=3000, break_precision=1e-3):
    """
    TODO document
    """

    loss_func = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(net.parameters())

    for i in range(max_iterations):

        # reset optimizer
        optimizer.zero_grad()

        loss = loss_func(net(inputs), labels)
        loss.backward()

        optimizer.step()

        if loss.item() < break_precision:
            break


def nn_segmentation_from_masks(image: np.ndarray, patch_size: int, keep_mask: np.ndarray, dump_mask: np.ndarray):
    """
    :param image: The Image to segment from
    :param patch_size: The Size of the patches
    :param keep_mask: The Mask of pixels to keep
    :param dump_mask: The Mask of pixels to dump
    :return: A Mask of pixels to keep.
             Pixels similar to keep_mask and different to to dump_pixels
    """

    assert_image(image)
    assert_mask(keep_mask)
    assert_mask(dump_mask)
    assert_image_mask(image, keep_mask)
    assert_image_mask(image, dump_mask)

    ###
    # formatting the data

    patch_info = _patchify_info(image, patch_size)

    keep_info = patch_info[keep_mask.flatten()]
    dump_info = patch_info[dump_mask.flatten()]
    inputs = np.append([keep_info], [dump_info], axis=1)[0]
    inputs = torch.from_numpy(inputs).float()

    keep = np.ones((len(keep_info)), dtype=int)
    dump = np.zeros((len(dump_info)), dtype=int)
    labels = np.append(keep, dump).reshape(len(keep_info) + len(dump_info), 1)
    labels = torch.from_numpy(labels).float()

    patch_info = torch.from_numpy(patch_info).float()

    ###
    # training the network

    net = _SegmentationNN(patch_size)
    _train_segmentation_nn(net, inputs, labels)

    ###
    # running the network

    result = net(patch_info)

    result = result.detach()
    result = result.numpy()
    result = result >= 0.5
    result = result.reshape(image.shape[0], image.shape[1])

    return result
