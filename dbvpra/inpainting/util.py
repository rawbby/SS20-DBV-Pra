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
import scipy.sparse as sparse
import scipy.sparse.linalg


def _vec(matrix: np.ndarray):
    """
    :param matrix: the matrix to be vectorized
    :return: the vectorized matrix as view!
    """
    ny, nx = matrix.shape[:2]
    return matrix.reshape((nx * ny,) + matrix.shape[2:], order='F')


def _un_vec(matrix: np.ndarray, ny: int):
    """
    :param matrix: the matrix to be vectorized
    :return: the vectorized matrix as view!
    """
    nx = int(matrix.shape[0] / ny)
    return matrix.reshape((ny, nx,) + matrix.shape[1:], order='F')


def _kron(a: np.ndarray, b: np.ndarray):
    """
    :param a: matrix a
    :param b: matrix b
    :return: kronecker product of a and b
    """
    return sparse.kron(a, b)


def _lsqr(a: np.ndarray, b: np.ndarray):
    """
    :param a: matrix a
    :param b: matrix b
    :return: the result = arg minx ||ax-b||^2
    """
    return sparse.linalg.lsqr(a, b)[0]


def _id(length: int):
    """
    :param length: the length of the diagonal to generate
    :return: an identity matrix with the size of length x length
    """
    return sparse.identity(length, dtype=np.float64)
    # return np.diag(np.ones(length, dtype=np.float64))


def _d(length: int):
    """
    :param length: the length of the diagonal to generate
    :return: a 'D' matrix with the size of length+1 x length
    """

    s = length
    e = np.ones(s, dtype=np.float64)

    return sparse.spdiags([e, -e], [0, 1], s - 1, s)

    # w = length
    # v = w - 1
    # a = np.diag(np.ones(w), 0)[:v, :w]
    # b = np.diag(np.ones(w), 1)[:v, :w]
    # return a - b


def _d_hat(ny: int, nx: int):
    """
    :param ny: the height of the image
    :param nx: the width of the image
    :return: a 'D_hat' matrix
    """
    dy = sparse.kron(_id(nx), _d(ny))
    dx = sparse.kron(_d(nx), _id(ny))
    return sparse.vstack([dy, dx])


def _o(vec_mask: np.ndarray):
    """
    :param vec_mask: the mask to generate 1_I from (vectorised)
    :return: 1_I
    """
    return np.diag(vec_mask)[:, vec_mask]
    # n = len(vec_mask)
    # nr = np.sum(vec_mask)
    # data = np.ones(nr, dtype=np.float64)
    # j = range(nr)
    # i = np.where(vec_mask)[0]
    # return sparse.coo_matrix((data, (i, j)), shape=(n, nr))


def _mask_bounds(mask: np.ndarray):
    """
    :param mask: the mask to generate the bounds from
    :return: tuple of the masks bounds. (y_min, y_max, x_min, x_max)
    """
    n0 = 0
    ny, nx = mask.shape
    v = np.where(mask)

    return (max(n0, np.min(v[0]) - 1),
            min(ny, np.max(v[0]) + 2),
            max(n0, np.min(v[1]) - 1),
            min(nx, np.max(v[1]) + 2))
