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

from dbvpra.mathmorph.closing import closing
from dbvpra.mathmorph.opening import opening


def erosion(source: np.ndarray, kernel: np.ndarray):
    """
    :param source: the source image to erode
    :param kernel: the kernel used to erode the source
    :return: the eroded source
    """

    return closing(opening(source, kernel), kernel)
