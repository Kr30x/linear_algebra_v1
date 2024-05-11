import numpy as np
import sympy as sp


def find_basis(matrix, detailed_logging=False):
    dtype = matrix.dtype
    matrix = sp.Matrix(matrix)
    res, pivot = matrix.rref()
    print(pivot)
    return np.array(res, dtype=dtype)
