from solvers import gauss_elimination
from solvers import gauss_seidel_solve
from solvers import lu_solve
import numpy as np
import time
from scipy.linalg import hilbert
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# Cấu hình đồ thị
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True

np.random.seed(42)  # Đảm bảo tính tái lập
print("Thư viện đã được import thành công!")

## 2. Thực Nghiệm với Ma Trận Ngẫu 
### 2.1 Hàm hỗ trợ đo thời gian và sai số

def generate_random_spd_matrix(n):
    """
    Tạo ma trận đối xứng xác định dương (SPD) ngẫu nhiên.
    SPD đảm bảo Gauss-Seidel hội tụ.
    """
    B = np.random.randn(n, n)
    A = B @ B.T + n * np.eye(n)  # Thêm n*I để đảm bảo well-conditioned
    return A


def compute_relative_residual(A, x, b):
    """Tính sai số tương đối: ||Ax - b||_2 / ||b||_2"""
    residual = np.linalg.norm(A @ x - b)
    b_norm = np.linalg.norm(b)
    if b_norm < 1e-15:
        return residual
    return residual / b_norm


def benchmark_method(method, A, b, num_runs=5):
    """
    Đo thời gian và sai số của một phương pháp.
    
    Returns:
    --------
    avg_time : float
        Thời gian trung bình (giây)
    rel_error : float
        Sai số tương đối
    """
    times = []
    
    for _ in range(num_runs):
        start = time.perf_counter()
        x = method(A.copy(), b.copy())
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = np.mean(times)
    rel_error = compute_relative_residual(A, x, b)
    
    return avg_time, rel_error

print("✓ Các hàm hỗ trợ đã sẵn sàng")


### 2.2 Chạy thực nghiệm
# Kích thước ma trận cần test
sizes = [50, 100, 200, 500, 1000]
num_runs = 5

# Lưu kết quả
results = {
    'n': [],
    'gauss_time': [], 'gauss_error': [],
    'lu_time': [], 'lu_error': [],
    'gs_time': [], 'gs_error': []
}

methods = {
    'Gauss': gauss_elimination,
    'LU': lu_solve,
    'Gauss-Seidel': gauss_seidel_solve
}

print("="*80)
print("THỰC NGHIỆM VỚI MA TRẬN NGẪU NHIÊN SPD")
print(f"Kích thước: {sizes}")
print(f"Số lần chạy: {num_runs}")
print("="*80)

for n in sizes:
    print(f"\n>>> n = {n}")
    
    # Tạo ma trận và vector
    A = generate_random_spd_matrix(n)
    x_true = np.random.randn(n)
    b = A @ x_true
    
    results['n'].append(n)
    
    # Gauss Elimination
    t, e = benchmark_method(gauss_elimination, A, b, num_runs)
    results['gauss_time'].append(t)
    results['gauss_error'].append(e)
    print(f"    Gauss:        {t:.6f}s, error = {e:.2e}")
    
    # LU Decomposition
    t, e = benchmark_method(lu_solve, A, b, num_runs)
    results['lu_time'].append(t)
    results['lu_error'].append(e)
    print(f"    LU:           {t:.6f}s, error = {e:.2e}")
    
    # Gauss-Seidel
    t, e = benchmark_method(gauss_seidel_solve, A, b, num_runs)
    results['gs_time'].append(t)
    results['gs_error'].append(e)
    print(f"    Gauss-Seidel: {t:.6f}s, error = {e:.2e}")

print("\n" + "="*80)
print("✓ Hoàn thành thực nghiệm!")
print("="*80)

### 2.3 Bảng số liệu chi tiết

# Tạo DataFrame từ kết quả
df_results = pd.DataFrame({
    'n': results['n'],
    'Gauss - Thời gian (s)': results['gauss_time'],
    'Gauss - Sai số': results['gauss_error'],
    'LU - Thời gian (s)': results['lu_time'],
    'LU - Sai số': results['lu_error'],
    'Gauss-Seidel - Thời gian (s)': results['gs_time'],
    'Gauss-Seidel - Sai số': results['gs_error']
})

# Format bảng
def format_time(x):
    return f"{x:.6f}"

def format_error(x):
    return f"{x:.2e}"

print("\n" + "="*100)
print("BẢNG KẾT QUẢ THỰC NGHIỆM")
print("="*100)

# Bảng thời gian
print("\nTHỜI GIAN THỰC THI (giây, trung bình 5 lần chạy):")
print("-"*70)
df_time = pd.DataFrame({
    'n': results['n'],
    'Gauss': [f"{t:.6f}" for t in results['gauss_time']],
    'LU': [f"{t:.6f}" for t in results['lu_time']],
    'Gauss-Seidel': [f"{t:.6f}" for t in results['gs_time']]
})
print(df_time.to_string(index=False))

# Bảng sai số
print("\nSAI SỐ TƯƠNG ĐỐI (||Ax̂ - b||₂ / ||b||₂):")
print("-"*70)
df_error = pd.DataFrame({
    'n': results['n'],
    'Gauss': [f"{e:.2e}" for e in results['gauss_error']],
    'LU': [f"{e:.2e}" for e in results['lu_error']],
    'Gauss-Seidel': [f"{e:.2e}" for e in results['gs_error']]
})
print(df_error.to_string(index=False))

### 2.4 Đồ thị Log-Log: Thời gian vs n

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

n_array = np.array(results['n'])

# ===== Đồ thị 1: Thời gian =====
ax1 = axes[0]
ax1.loglog(n_array, results['gauss_time'], 'o-', label='Gauss', linewidth=2, markersize=8)
ax1.loglog(n_array, results['lu_time'], 's-', label='LU', linewidth=2, markersize=8)
ax1.loglog(n_array, results['gs_time'], '^-', label='Gauss-Seidel', linewidth=2, markersize=8)

# Đường lý thuyết O(n³)
# Fit đường O(n³) qua điểm đầu tiên của Gauss
c = results['gauss_time'][0] / (n_array[0] ** 3)
theoretical_n3 = c * n_array ** 3
ax1.loglog(n_array, theoretical_n3, 'k--', label=r'$O(n^3)$ lý thuyết', linewidth=2, alpha=0.7)

ax1.set_xlabel('Kích thước ma trận n', fontsize=14)
ax1.set_ylabel('Thời gian (giây)', fontsize=14)
ax1.set_title('Thời gian thực thi vs Kích thước ma trận\n(Đồ thị Log-Log)', fontsize=14)
ax1.legend(fontsize=12)
ax1.grid(True, which="both", ls="-", alpha=0.5)

# ===== Đồ thị 2: Sai số =====
ax2 = axes[1]
ax2.semilogy(n_array, results['gauss_error'], 'o-', label='Gauss', linewidth=2, markersize=8)
ax2.semilogy(n_array, results['lu_error'], 's-', label='LU', linewidth=2, markersize=8)
ax2.semilogy(n_array, results['gs_error'], '^-', label='Gauss-Seidel', linewidth=2, markersize=8)

ax2.set_xlabel('Kích thước ma trận n', fontsize=14)
ax2.set_ylabel('Sai số tương đối', fontsize=14)
ax2.set_title('Sai số tương đối vs Kích thước ma trận', fontsize=14)
ax2.legend(fontsize=12)
ax2.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.savefig('benchmark_results.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n📈 Nhận xét về độ phức tạp:")
# Tính slope của log-log để xác định bậc
log_n = np.log(n_array)
log_t_gauss = np.log(results['gauss_time'])
log_t_lu = np.log(results['lu_time'])

slope_gauss = np.polyfit(log_n, log_t_gauss, 1)[0]
slope_lu = np.polyfit(log_n, log_t_lu, 1)[0]

print(f"   • Gauss:  slope ≈ {slope_gauss:.2f} (lý thuyết: 3.0 cho O(n³))")
print(f"   • LU:     slope ≈ {slope_lu:.2f} (lý thuyết: 3.0 cho O(n³))")
print(f"   • Gauss-Seidel: phụ thuộc vào số vòng lặp cần để hội tụ")

