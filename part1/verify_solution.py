"""
Kiểm chứng kết quả giải hệ phương trình bằng NumPy.
Đồ án 1 - Toán Ứng Dụng và Thống Kê (MTH00051)
"""

import numpy as np


def verify_solution(A, x, b):
    '''Kiểm chứng kết quả bằng Numpy'''
    A_np = np.array(A, dtype=float)
    x_np = np.array(x, dtype=float)
    b_np = np.array(b, dtype=float)
    Ax = A_np.dot(x_np)
    print("Ax =", Ax)
    print("b  =", b_np)
    if np.allclose(Ax, b_np):
        print("=> Ket qua: Nghiem DUNG!")
        return True
    else:
        print("=> Ket qua: Nghiem SAI!")
        return False
