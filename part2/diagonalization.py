import math

def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]

def matmul(A, B):
    B_T = transpose(B)
    return [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in B_T] for row_A in A]

def norm(vec):
    return math.sqrt(sum(x**2 for x in vec))

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q_T = []
    R = [[0.0] * n for _ in range(n)]
    A_T = transpose(A)
    
    for j in range(n):
        v = A_T[j][:]
        for i in range(j):
            q_i = Q_T[i]
            R[i][j] = dot_product(v, q_i)
            v = [v[k] - R[i][j] * q_i[k] for k in range(m)]
        
        R[j][j] = norm(v)
        if R[j][j] > 1e-10:
            q_j = [x / R[j][j] for x in v]
        else:
            q_j = [0.0] * m
        Q_T.append(q_j)
        
    return transpose(Q_T), R

def get_eigen(A, max_iters=2000, tol=1e-10):
    """Tìm trị riêng bằng QR lặp, dừng khi đạt hội tụ."""
    n = len(A)
    Ak = [row[:] for row in A]
    eigenvectors = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    for _ in range(max_iters):
        Q, R = qr_decomposition(Ak)
        Ak = matmul(R, Q)
        eigenvectors = matmul(eigenvectors, Q)
        
        # Kiểm tra điều kiện hội tụ (các phần tử ngoài đường chéo chính -> 0)
        off_diag_sum = sum(Ak[i][j]**2 for i in range(n) for j in range(n) if i != j)
        if off_diag_sum < tol:
            break
            
    eigenvalues = [Ak[i][i] for i in range(n)]
    return eigenvalues, eigenvectors