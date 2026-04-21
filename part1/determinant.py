"""
Tính định thức ma trận bằng phép khử Gauss.
Đồ án 1 - Toán Ứng Dụng và Thống Kê (MTH00051)
"""

from gaussian import gaussian_eliminate


def determinant(A):
    '''Hàm tính định thức'''
    # Phải là ma trận vuông mới tính định thức
    if len(A) == 0 or len(A) != len(A[0]):
        raise ValueError("Ma trận phải là ma trận vuông để tính định thức.")

    n = len(A)
    b = [0] * n

    try:
        M, _, _, s = gaussian_eliminate(A, b)
    except ValueError as e:
        # Nếu là ma trận suy biến thì định thức chắc chắn bằng 0
        if str(e) == "Ma trận suy biến hoặc không có nghiệm duy nhất.":
            return 0.0
        raise e

    # Giá trị định thức = 1
    det_val = 1.0

    # Tích các phần tử trên đường chéo chính
    for i in range(n):
        det_val *= M[i][i]

    # Nhân với (-1)^s, với s là số lần hoán đổi dòng
    det_val *= (-1)**s

    return det_val
