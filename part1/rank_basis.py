"""
Tính hạng và cơ sở các không gian con của ma trận (cột, dòng, nghiệm).
Đồ án 1 - Toán Ứng Dụng và Thống Kê (MTH00051)
"""


def rank_and_basis(A):
    """Tính hạng và cơ sở của các không gian cột, dòng, nghiệm."""
    if not A or not A[0]:
        return 0, [], [], []

    m = len(A)
    n = len(A[0])

    # Copy A thành R và ép kiểu float
    R = [[float(A[i][j]) for j in range(n)] for i in range(m)]

    pivot_cols = []

    # Bước 1: Đưa về dạng bậc thang
    r = 0  # Chỉ số dòng
    for c in range(n):
        if r >= m:
            break

        max_row = r
        max_val = abs(R[r][c])
        for i in range(r + 1, m):
            if abs(R[i][c]) > max_val:
                max_val = abs(R[i][c])
                max_row = i

        if max_val < 1e-10:
            for i in range(r, m):
                R[i][c] = 0.0
            continue

        if max_row != r:
            R[r], R[max_row] = R[max_row], R[r]

        pivot_cols.append(c)

        pivot_val = R[r][c]
        for j in range(c, n):
            R[r][j] /= pivot_val

        for i in range(r + 1, m):
            factor = R[i][c]
            for j in range(c, n):
                R[i][j] -= factor * R[r][j]

        r += 1

    rank = len(pivot_cols)

    # Khử ngược để đưa về RREF
    for i in range(rank - 1, -1, -1):
        p_col = pivot_cols[i]
        for j in range(i - 1, -1, -1):
            factor = R[j][p_col]
            for k in range(p_col, n):
                R[j][k] -= factor * R[i][k]

    # Bước 2: Trích xuất không gian cơ sở

    # Cơ sở không gian dòng
    row_space_basis = [R[i] for i in range(rank)]

    # Cơ sở không gian cột
    col_space_basis = [[float(A[i][c]) for i in range(m)] for c in pivot_cols]

    # Cơ sở không gian nghiệm
    free_cols = [c for c in range(n) if c not in pivot_cols]
    null_space_basis = []

    for f in free_cols:
        null_vec = [0.0] * n
        null_vec[f] = 1.0

        for i in range(rank):
            p_col = pivot_cols[i]
            null_vec[p_col] = -R[i][f]

        null_space_basis.append(null_vec)

    return rank, row_space_basis, col_space_basis, null_space_basis
