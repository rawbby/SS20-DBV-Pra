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


def _slu(r: int, tr: int):
    assert 1 <= tr <= r
    return (r << 1) - 1, r - tr, r + tr - 1


def stripe(r: int, tr: int) -> np.ndarray:
    (s, l, u) = _slu(r, tr)
    patch = np.zeros((s, s), np.bool_)
    patch[l:u] = np.True_
    return patch


def cross(r: int, tr: int) -> np.ndarray:
    (s, l, u) = _slu(r, tr)
    patch = np.zeros((s, s), np.bool_)
    patch[l:u] = np.True_
    patch[0:s, l:u] = np.True_
    return patch


def point(r: int, tr: int) -> np.ndarray:
    (s, l, u) = _slu(r, tr)
    patch = np.zeros((s, s), np.bool_)
    patch[l:u, l:u] = np.True_
    return patch
