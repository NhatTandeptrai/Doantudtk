"""
Tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
Đồ án 1 - Toán Ứng Dụng và Thống Kê (MTH00051)
"""

from determinant import determinant


def inverse(A):
    '''Hàm tính ma trận nghịch đảo bằng phương pháp Gauss–Jordan.'''
    n = len(A)
    # Kiểm tra tính khả nghịch
    if determinant(A) == 0:
        raise ValueError("Ma trận không khả nghịch")

    # Tạo ma trận đơn vị và ma trận ghép
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    M = [A[i] + I[i] for i in range(n)]

    # Khử xuôi
    for k in range(n):
        max_row = k
        for j in range(k + 1, n):
            if abs(M[j][k]) > abs(M[max_row][k]):
                max_row = j

        M[k], M[max_row] = M[max_row], M[k]

        pivot = M[k][k]
        for j in range(k, 2 * n):
            M[k][j] /= pivot

        for i in range(k + 1, n):
            factor = M[i][k]
            for j in range(k, 2 * n):
                M[i][j] -= factor * M[k][j]

    # Khử ngược
    for k in range(n - 1, -1, -1):
        for i in range(k - 1, -1, -1):
            factor = M[i][k]
            for j in range(k, 2 * n):
                M[i][j] -= factor * M[k][j]

    # Tách lấy ma trận nghịch đảo vế phải
    inv_A = [row[n:] for row in M]
    return inv_A


def multiply(A, B):
    '''Hàm nhân hai ma trận để kiểm tra ma trận nghịch đảo.'''
    return [[sum(a * b for a, b in zip(A_row, B_col))
             for B_col in zip(*B)] for A_row in A]
