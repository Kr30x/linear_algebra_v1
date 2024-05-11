import numpy as np
from sympy import Rational
from sympy.matrices import Matrix


def inverse_matrix(matrix):
    if matrix.dtype == object:
        matrix = Matrix(matrix)
        return np.array(matrix.inv(), dtype=Rational)
    inv_matrix = np.linalg.inv(matrix)

    return inv_matrix
