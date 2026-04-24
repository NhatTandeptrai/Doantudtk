# PHẦN 1: PHÉP KHỬ GAUSS VÀ CÁC ỨNG DỤNG

Phần này tập trung vào việc xây dựng từ đầu (from scratch) các thuật toán cốt lõi của Đại số tuyến tính dựa trên Phép khử Gauss, đảm bảo tính chính xác số học và khả năng ứng dụng linh hoạt.

## 1. Cấu trúc mã nguồn
Dự án phân chia các chức năng đại số thành các module độc lập để dễ dàng quản lý và kiểm thử:
- `gaussian.py`: Cốt lõi của phép khử Gauss, tích hợp kỹ thuật Partial Pivoting và thế ngược (back substitution) để giải hệ phương trình tuyến tính.
- `determinant.py`: Module kế thừa phép khử Gauss để tính định thức ma trận.
- `inverse.py`: Triển khai phương pháp Gauss-Jordan trên ma trận khối mở rộng $[A | I]$ để tìm ma trận nghịch đảo.
- `rank_basis.py`: Đưa ma trận về dạng bậc thang rút gọn (RREF) để trích xuất hạng (Rank) và cơ sở của các không gian: dòng, cột và nghiệm (Null space).
- `verify_solution.py`: Công cụ kiểm chứng tính đúng đắn của nghiệm tự tính bằng cách đối chiếu với thư viện NumPy.
- `part1_demo.ipynb`: Notebook chứa các kịch bản kiểm thử (Test Cases) thực tế cho toàn bộ các chức năng trên.

## 2. Đặc điểm kỹ thuật
### Xử lý sai số và Partial Pivoting
Trong quá trình khử Gauss, thuật toán thực hiện tìm phần tử có giá trị tuyệt đối lớn nhất ở các dòng phía dưới để hoán vị lên làm phần tử trục (pivot). Kỹ thuật này giúp hạn chế tối đa sai số làm tròn và tránh lỗi chia cho 0. Các giá trị tuyệt đối nhỏ hơn ngưỡng máy tính ($10^{-12}$) được xử lý như số 0 để nhận diện chính xác ma trận suy biến.

### Tính Định thức và Ma trận nghịch đảo
- **Định thức:** Kết quả được tính bằng tích các phần tử trên đường chéo chính của ma trận sau khi khử. Do áp dụng Partial Pivoting, định thức cuối cùng được hiệu chỉnh bằng cách nhân với $(-1)^s$, trong đó $s$ là tổng số lần hoán đổi dòng.
- **Nghịch đảo:** Sử dụng thuật toán Gauss-Jordan để biến đổi đồng thời cả ma trận gốc và ma trận đơn vị. Quá trình bao gồm khử xuôi để tạo tam giác trên và khử ngược để triệt tiêu các phần tử ngoài đường chéo chính.

### Trích xuất Không gian Cơ sở (Rank & Basis)
Thuật toán đưa ma trận về dạng RREF để thực hiện các phép trích xuất:
- **Hạng (Rank):** Xác định bằng số lượng phần tử trục (pivots) tìm được.
- **Không gian dòng/cột:** Lấy trực tiếp từ các dòng khác không của RREF và các cột tương ứng trong ma trận gốc.
- **Không gian nghiệm (Null Space):** Tự động xác định các biến tự do (free variables) và xây dựng hệ cơ sở tương ứng bằng cách giải hệ phương trình đồng nhất từ ma trận RREF.

## 3. Hướng dẫn sử dụng
Để kiểm chứng các chức năng của Phần 1, nhóm đã chuẩn bị file `part1_demo.ipynb` với các kịch bản thử nghiệm:

### Chạy thử nghiệm qua Notebook
1. Mở file `part1_demo.ipynb` bằng Jupyter Notebook hoặc VS Code.
2. Chạy lần lượt các cell để quan sát kết quả cho 5 Test Cases:
    - Giải hệ phương trình $Ax = b$ có nghiệm duy nhất.
    - Tính định thức cho ma trận bình thường và ma trận suy biến.
    - Tìm ma trận nghịch đảo và kiểm tra tính chất $A \cdot A^{-1} = I$.
    - Trích xuất hạng và cơ sở không gian cho ma trận chữ nhật $3 \times 4$.
    - Kiểm chứng tổng hợp ma trận $4 \times 4$ quy mô lớn hơn với NumPy.
# PHẦN 2: PHÂN RÃ MA TRẬN VÀ TRỰC QUAN HÓA VỚI MANIM
## 1. Cấu trúc mã nguồn
Dự án được chia thành các module chức năng riêng biệt:
- `diagonalization.py`: Triển khai các phép toán ma trận cơ bản, phân rã QR và tìm trị riêng/vector riêng.
- `decomposition.py`: Thuật toán SVD cốt lõi, bao gồm cả kỹ thuật trực giao hóa Gram-Schmidt để xử lý ma trận chữ nhật.
- `part2_demo.ipynb`: File kiểm chứng so sánh độ chính xác giữa code tự viết và thư viện NumPy.
- `manim_scene.py`: Kịch bản hoạt ảnh chi tiết về bản chất Pixel, công thức toán học và ứng dụng thực tế.
- `Ending.py`: Hoạt ảnh kết thúc hiển thị thông tin nhóm.

## 2. Đặc điểm kỹ thuật
### Thuật toán SVD "From Scratch"
Nhóm đã triển khai quy trình phân rã ma trận $A$ thành $U \Sigma V^T$ mà không dựa vào các hàm tích hợp sẵn của thư viện lớn:
1. **Tính toán $A^TA$:** Để tìm ma trận vector suy biến phải $V$.
2. **Phân rã QR lặp:** Tìm trị riêng để xây dựng ma trận $\Sigma$.
3. **Trực giao hóa Gram-Schmidt:** Được sử dụng để hoàn thiện ma trận $U$ trong trường hợp ma trận bị thiếu cột, đảm bảo tính trực giao.
4. **Kiểm chứng:** Sai số tái tạo (Reconstruction Error) đạt mức cực thấp ($< 10^{-10}$), chứng minh tính đúng đắn của thuật toán.

### Ứng dụng minh họa
Video được thực hiện bằng Manim giải thích 3 bước hình học của SVD:
- **Xoay ($V^T$):** Tìm hướng dữ liệu quan trọng nhất.
- **Co giãn ($\Sigma$):** Ưu tiên các đặc điểm cốt lõi.
- **Xoay ($U$):** Đưa dữ liệu về không gian đích.

## 3. Hướng dẫn sử dụng
### Cài đặt môi trường
Yêu cầu Python và các thư viện hỗ trợ cơ bản. Bạn có thể cài đặt thông qua pip:
```bash
pip install numpy manim pillow
```
### Chạy demo thuật toán
Bạn có thể chạy trực tiếp file decomposition.py để xem kết quả phân rã SVD trên ma trận test có sẵn:
```bash
python decomposition.py
```
### Render Video Animation
Để xuất video giải thích thuật toán, chạy lệnh Manim trỏ tới class SVDTheFinalCut:
```bash
manim -pql manim_scene.py SVDTheFinalCut
```
(Ghi chú: Đổi -pql thành -pqh nếu bạn muốn render ở chất lượng High Quality)

# PHẦN 3: GIẢI HỆ PHƯƠNG TRÌNH VÀ PHÂN TÍCH HIỆU NĂNG

## 1. Cấu trúc mã nguồn
Dự án được chia thành các module chức năng riêng biệt:
- `solvers.py`: Triển khai thuật toán Gauss-Seidel với cơ chế kiểm tra hội tụ bằng sai số tương đối (Động cơ tính toán).
- `benchmark.py`: Hệ thống tự động đo lường thời gian thực thi và sai số tái tạo $||Ax - b||$ trên các quy mô dữ liệu khác nhau (Đo lường hiệu năng).
- `analysis.ipynb`: Tổng hợp kết quả, vẽ biểu đồ Log-Log để phân tích độ phức tạp thực tế và so sánh tính ổn định (Trực quan hóa).

## 2. Đặc điểm kỹ thuật
### Phương pháp lặp Gauss-Seidel
Thuật toán được tối ưu hóa để giải các hệ phương trình tuyến tính lớn:
- **Cơ chế cập nhật:** Tận dụng ngay giá trị nghiệm vừa tìm được trong cùng một vòng lặp để tăng tốc độ hội tụ so với phương pháp Jacobi.
- **Điều kiện dừng:** Sử dụng sai số tương đối (Relative Error) để đảm bảo độ chính xác trên nhiều thang đo giá trị khác nhau:
  $$\frac{\|x^{(k+1)} - x^{(k)}\|}{\|x^{(k+1)}\| + \text{eps}} < \text{tolerance}$$
- **Xử lý hội tụ:** Chỉ áp dụng cho các ma trận chéo trội chặt (Strictly Diagonally Dominant) hoặc ma trận đối xứng xác định dương (SPD) để đảm bảo thuật toán không bị phân kỳ.

### Phân tích Hiệu năng & Độ phức tạp
- **Thực nghiệm thời gian:** So sánh trực tiếp giữa các phương pháp giải đúng (Khử Gauss, phân rã LU) có độ phức tạp $O(n^3)$ và phương pháp lặp.
- **Biểu đồ Log-Log:** Trực quan hóa mối quan hệ giữa kích thước ma trận ($n=50$ đến $n=1000$) và thời gian xử lý, giúp xác định hệ số tăng trưởng thực tế của thuật toán.
- **Sai số tái tạo:** Đo lường độ lệch $||Ax - b||$ để đánh giá độ tin cậy của nghiệm xấp xỉ.

### Độ ổn định số học (Numerical Stability)
Nghiên cứu tác động của **Số điều kiện (Condition Number - $\kappa$)** đến kết quả:
- **Ma trận SPD:** Đại diện cho hệ ổn định (Well-conditioned), sai số duy trì ở mức $\approx 10^{-15}$.
- **Ma trận Hilbert:** Đại diện cho hệ kém ổn định (Ill-conditioned), minh họa hiện tượng sai số làm tròn bị khuếch đại cực đại khi kích thước ma trận tăng.

## 3. Hướng dẫn sử dụng
### Cài đặt yêu cầu
Mở `analysis.ipynb` và chạy cell đầu tiên để cài đặt các thư viện cần thiết:
```bash
pip install numpy matplotlib pandas seaborn
