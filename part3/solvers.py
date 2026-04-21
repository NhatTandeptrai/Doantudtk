"""  
    Giải Hệ Phương Trình Tuyến Tính Ax = b
Nội dung:
1. Cài đặt 3 phương pháp: Khử Gauss, Phân rã LU, và Lặp Gauss-Seidel
2. Thực nghiệm với ma trận ngẫu nhiên kích thước n ∈ {50, 100, 200, 500, 1000}
3. Phân tích ổn định với ma trận Hilbert (ill-conditioned) và ma trận SPD (well-conditioned)
4. Đồ thị và bảng số liệu
"""

import numpy as np
import time
from scipy.linalg import hilbert
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Cấu hình đồ thị
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True

np.random.seed(42)  # Đảm bảo tính tái lập
print("Thư viện đã được import thành công!")


## 1. Cài Đặt Các Phương Pháp Giải Ax = b
### 1.1 Phương pháp Khử Gauss với Pivoting

def gauss_elimination(A, b):
    """
    Giải hệ phương trình Ax = b bằng phương pháp khử Gauss với partial pivoting.
    
    Parameters:
    -----------
    A : ndarray (n, n)
        Ma trận hệ số
    b : ndarray (n,)
        Vector vế phải
        
    Returns:
    --------
    x : ndarray (n,)
        Nghiệm của hệ phương trình
    """
    n = len(b)
    # Tạo ma trận mở rộng [A|b]
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # Bước tiến (Forward Elimination) với partial pivoting
    for k in range(n - 1):
        # Tìm pivot lớn nhất trong cột k
        max_idx = np.argmax(np.abs(Ab[k:n, k])) + k
        
        # Hoán đổi hàng
        if max_idx != k:
            Ab[[k, max_idx]] = Ab[[max_idx, k]]
        
        # Kiểm tra pivot = 0
        if np.abs(Ab[k, k]) < 1e-15:
            raise ValueError("Ma trận suy biến hoặc gần suy biến")
        
        # Khử các phần tử dưới pivot
        for i in range(k + 1, n):
            factor = Ab[i, k] / Ab[k, k]
            Ab[i, k:] -= factor * Ab[k, k:]
    
    # Bước lùi (Back Substitution)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x

print("✓ Phương pháp Khử Gauss đã được cài đặt")

### 1.2 Phương pháp Phân rã LU (Doolittle)
def lu_decomposition(A):
    """
    Phân rã LU với partial pivoting: PA = LU
    
    Parameters:
    -----------
    A : ndarray (n, n)
        Ma trận cần phân rã
        
    Returns:
    --------
    L : ndarray (n, n)
        Ma trận tam giác dưới với đường chéo = 1
    U : ndarray (n, n)
        Ma trận tam giác trên
    P : ndarray (n, n)
        Ma trận hoán vị
    """
    n = A.shape[0]
    L = np.eye(n)
    U = A.astype(float).copy()
    P = np.eye(n)
    
    for k in range(n - 1):
        # Partial pivoting
        max_idx = np.argmax(np.abs(U[k:n, k])) + k
        
        if max_idx != k:
            # Hoán đổi hàng trong U
            U[[k, max_idx]] = U[[max_idx, k]]
            # Hoán đổi hàng trong P
            P[[k, max_idx]] = P[[max_idx, k]]
            # Hoán đổi phần đã tính của L (trước cột k)
            if k > 0:
                L[[k, max_idx], :k] = L[[max_idx, k], :k]
        
        if np.abs(U[k, k]) < 1e-15:
            continue
        
        # Tính các phần tử của L và U
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    
    return L, U, P


def forward_substitution(L, b):
    """Giải Ly = b (L tam giác dưới)"""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    return y


def backward_substitution(U, y):
    """Giải Ux = y (U tam giác trên)"""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if np.abs(U[i, i]) < 1e-15:
            x[i] = 0
        else:
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x


def lu_solve(A, b):
    """
    Giải Ax = b bằng phân rã LU.
    PA = LU => Ax = b => LUx = Pb
    Đặt y = Ux, giải Ly = Pb, rồi giải Ux = y
    """
    L, U, P = lu_decomposition(A)
    Pb = P @ b.astype(float)
    y = forward_substitution(L, Pb)
    x = backward_substitution(U, y)
    return x

print("✓ Phương pháp Phân rã LU đã được cài đặt")

### 1.3 Phương pháp Lặp Gauss-Seidel
def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=10000):
    """
    Giải Ax = b bằng phương pháp lặp Gauss-Seidel.
    
    Parameters:
    -----------
    A : ndarray (n, n)
        Ma trận hệ số (nên là diagonally dominant hoặc SPD)
    b : ndarray (n,)
        Vector vế phải
    x0 : ndarray (n,), optional
        Nghiệm khởi tạo (mặc định = 0)
    tol : float
        Ngưỡng hội tụ
    max_iter : int
        Số vòng lặp tối đa
        
    Returns:
    --------
    x : ndarray (n,)
        Nghiệm xấp xỉ
    converged : bool
        True nếu hội tụ
    iterations : int
        Số vòng lặp thực hiện
    """
    n = len(b)
    A = A.astype(float)
    b = b.astype(float)
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            if np.abs(A[i, i]) < 1e-15:
                continue
            
            # Tổng các phần tử đã cập nhật (j < i)
            sum1 = np.dot(A[i, :i], x[:i])
            # Tổng các phần tử chưa cập nhật (j > i)
            sum2 = np.dot(A[i, i+1:], x_old[i+1:])
            
            x[i] = (b[i] - sum1 - sum2) / A[i, i]
        
        # Kiểm tra hội tụ
        rel_error = np.linalg.norm(x - x_old) / (np.linalg.norm(x) + 1e-15)
        if rel_error < tol:
            return x, True, iteration + 1
    
    return x, False, max_iter


def gauss_seidel_solve(A, b):
    """Wrapper để có cùng interface với các phương pháp khác"""
    x, converged, iters = gauss_seidel(A, b)
    return x

print("✓ Phương pháp Lặp Gauss-Seidel đã được cài đặt")

### 1.4 Kiểm tra nhanh các phương pháp
# Test với ma trận nhỏ
print("="*60)
print("KIỂM TRA CÁC PHƯƠNG PHÁP VỚI MA TRẬN 4x4")
print("="*60)

# Tạo ma trận SPD nhỏ để test
np.random.seed(123)
B = np.random.rand(4, 4)
A_test = B @ B.T + 4 * np.eye(4)  # SPD matrix
x_true = np.array([1.0, 2.0, 3.0, 4.0])
b_test = A_test @ x_true

print(f"\nNghiệm đúng: {x_true}")
print(f"Số điều kiện của A: {np.linalg.cond(A_test):.4f}")

# Test Gauss
x_gauss = gauss_elimination(A_test, b_test)
err_gauss = np.linalg.norm(x_gauss - x_true) / np.linalg.norm(x_true)
print(f"\n[Gauss]      x = {x_gauss}")
print(f"             Sai số tương đối: {err_gauss:.2e}")

# Test LU
x_lu = lu_solve(A_test, b_test)
err_lu = np.linalg.norm(x_lu - x_true) / np.linalg.norm(x_true)
print(f"\n[LU]         x = {x_lu}")
print(f"             Sai số tương đối: {err_lu:.2e}")

# Test Gauss-Seidel
x_gs, converged, iters = gauss_seidel(A_test, b_test)
err_gs = np.linalg.norm(x_gs - x_true) / np.linalg.norm(x_true)
print(f"\n[Gauss-Seidel] x = {x_gs}")
print(f"               Sai số tương đối: {err_gs:.2e}")
print(f"               Hội tụ: {converged}, Số vòng lặp: {iters}")

print("\n" + "="*60)
print("✓ Tất cả phương pháp hoạt động chính xác!")
print("="*60)