"""
Phép khử Gauss với Partial Pivoting và giải hệ phương trình tuyến tính.
Đồ án 1 - Toán Ứng Dụng và Thống Kê (MTH00051)
"""


def back_substitution(U, c):
    '''Giải hệ tam giác trên.'''
    n = len(U)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_val = 0
        for j in range(i + 1, n):
            sum_val += U[i][j] * x[j]
        if U[i][i] == 0:
            raise ValueError("Không thể giải (chia cho 0)")
        x[i] = (c[i] - sum_val) / U[i][i]
    return x


def gaussian_eliminate(A, b):
    '''Trả về ma trận sau khi khử, nghiệm x, số lần hoán đổi.'''
    n = len(A)
    # Tạo bản sao để không làm thay đổi ma trận gốc
    A = [row[:] for row in A]
    b = b[:]
    swap_count = 0

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            swap_count += 1

        pivot = A[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError("Ma trận suy biến hoặc không có nghiệm duy nhất.")

        for k in range(i + 1, n):
            factor = A[k][i] / pivot
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    x = back_substitution(A, b)

    return A, b, x, swap_count
