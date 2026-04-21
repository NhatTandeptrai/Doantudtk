import math
from diagonalization import transpose, matmul, get_eigen, dot_product

def complete_basis(U_cols, m):
    """Hoàn thiện ma trận trực giao U bằng Gram-Schmidt nếu bị thiếu cột."""
    current_cols = len(U_cols)
    if current_cols == m:
        return U_cols
        
    for i in range(m):
        if len(U_cols) == m:
            break
            
        # Tạo vector cơ sở chuẩn e_i
        e = [0.0] * m
        e[i] = 1.0
        
        # Trực giao hóa e_i với tất cả các vector đã có trong U_cols
        for u in U_cols:
            proj = dot_product(e, u)
            e = [e[k] - proj * u[k] for k in range(m)]
            
        length = math.sqrt(sum(x**2 for x in e))
        # Nếu vector mới không bị triệt tiêu, chuẩn hóa và thêm vào U
        if length > 1e-10:
            e = [x / length for x in e]
            U_cols.append(e)
            
    return U_cols

def svd(A):
    m = len(A)
    n = len(A[0])
    
    # 1. Chéo hóa A^T * A
    A_T = transpose(A)
    AtA = matmul(A_T, A)
    eigenvalues, V = get_eigen(AtA)
    
    # 2. Sắp xếp giảm dần
    eigen_pairs = [(eigenvalues[i], [row[i] for row in V]) for i in range(n)]
    eigen_pairs.sort(key=lambda x: x[0], reverse=True)
    
    singular_values = []
    V_sorted_T = []
    for val, vec in eigen_pairs:
        val = max(0.0, val) # Tránh sai số âm cực nhỏ
        singular_values.append(math.sqrt(val))
        V_sorted_T.append(vec)
        
    V_sorted = transpose(V_sorted_T)
    
    # 3. Xây dựng Sigma (m x n)
    Sigma = [[0.0] * n for _ in range(m)]
    for i in range(min(m, n)):
        Sigma[i][i] = singular_values[i]
        
    # 4. Xây dựng U (m x m)
    U_cols = []
    for i in range(min(m, n)):
        if singular_values[i] > 1e-10:
            v_i = V_sorted_T[i]
            Avi = [sum(A[row][col] * v_i[col] for col in range(n)) for row in range(m)]
            u_i = [x / singular_values[i] for x in Avi]
            U_cols.append(u_i)
            
    # Vá lỗ hổng: Bổ sung các cột trực giao còn thiếu cho U
    U_cols = complete_basis(U_cols, m)
    
    U = transpose(U_cols)
    V_T = transpose(V_sorted)
    
    return U, Sigma, V_T

# --- Khối code kiểm chứng ---
if __name__ == "__main__":
    # Test với ma trận chữ nhật (3x2) để chứng minh thuật toán không bị crash
    A_test = [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ]
    U, Sigma, VT = svd(A_test)
    
    print("Ma tran U (3x3):")
    for row in U: print([round(x, 4) for x in row])
        
    print("\nMa tran Sigma (3x2):")
    for row in Sigma: print([round(x, 4) for x in row])
        
    print("\nMa tran V^T (2x2):")
    for row in VT: print([round(x, 4) for x in row])