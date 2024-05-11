import sympy as sp
import numpy as np

def rref(matrix):
    dtype = matrix.dtype
    matrix = sp.Matrix(matrix)
    res, pivot = matrix.rref()
    return np.array(res, dtype=dtype)
