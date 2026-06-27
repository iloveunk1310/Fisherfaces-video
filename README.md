# Project: Video Minh Họa Học Thuật Thuật Toán Fisherfaces (PCA + FLD)

Một sản phẩm video học thuật trực quan sinh động được xây dựng hoàn toàn bằng thư viện **Manim (Python)**, giúp đơn giản hóa và cụ thể hóa các khái niệm đại số tuyến tính phức tạp trong xử lý ảnh và khoa học máy tính.

---

## Giới thiệu Video
Video giới thiệu và giải thích trực quan về bài toán nhận dạng khuôn mặt trên không gian con (Face Recognition in Subspaces), cùng với các phương pháp giải quyết cổ điển: PCA, FLD và đặc biệt là Fisherfaces.

---

## Cấu trúc Nội dung & Kịch bản các Phân cảnh

### Phần 0: Giới thiệu tổng quan

Giới thiệu tổng quan về bài toán **Face recognition** và ứng dụng của nó, đồng thời dẫn nhập tới bài toán xử lí ma trận.

### Phần 1: Bài toán
*   **Biểu diễn toán học:** Cách máy tính xử lý hình ảnh -> ma trận -> điểm trong không gian.
*   **Trực quan hóa:** Phép giảm chiều.

### Phần 2: Các phương pháp giảm chiều

Giới thiệu tổng quan mục tiêu của **PCA** và **FLD**.

### Phần 3: PCA

Giới thiệu mục tiêu, công thức và điểm yếu của PCA.

### Phần 4: FLD
*   **Mục tiêu:** Tách cụm bằng giảm chiều như thế nào
*   **Công thức:** Tối ưu hoá khoảng cách nội cụm / ngoại cụm như thế nào.
*   **Điểm mạnh và điểm yếu:** Dẫn nhập tới Fisherfaces.

### Phần 5: Fisherfaces
*   **Quy trình**: Cách Fisherfaces kết hợp PCA và LDA để phân cụm ảnh, cách để nhận diện và phân loại ảnh vào các nhóm cho trước.
*   **Công thức**: Giải thích tại sao Fisherfaces lại hiệu quả.\

### Phần 6: Final
*   **Điểm yếu và thay thế**: Kernel trick.
*   **Credit**: Tác giả và lời cảm ơn.
---

## 👥 Thông tin Tác giả & Giảng viên hướng dẫn

*   **Đơn vị:** Khoa Công nghệ Thông tin - Trường Đại học Khoa học Tự nhiên (FIT@HCMUS).
*   **Môn học:** Nhận dạng.
*   **Biên kịch & Đạo diễn hình ảnh:** Nguyễn Nhật Minh.
*   **Sinh viên thực hiện:** Nguyễn Nhật Minh.
*   **Mã số sinh viên (MSSV):** 23122010.

---

## 💻 Hướng dẫn Cài đặt & Cấu hình môi trường

Yêu cầu hệ thống chạy trên hệ điều hành **Windows** (Khuyến khích chạy Terminal dưới quyền Administrator).

### Bước 1: Cài đặt Font chữ "Be Vietnam Pro" trực tiếp vào OS
Toàn bộ chữ hiển thị tiếng Việt trong video sử dụng font này nhằm tránh lỗi hiển thị:
1. Tải bộ font miễn phí tại [Google Fonts - Be Vietnam Pro](https://fonts.google.com/specimen/Be+Vietnam+Pro).
2. Giải nén tệp tin vừa tải về.
3. Bôi đen toàn bộ các file `.ttf` $\rightarrow$ Click chuột phải $\rightarrow$ Chọn **Install for all users**.

### Bước 2: Cài đặt Trình biên dịch MiKTeX (LaTeX)
Manim cần LaTeX để sinh và vẽ các công thức toán học (`MathTex`):
1. Tải bản cài đặt Windows tại [MiKTeX Official Website](https://miktex.org/download).
2. Tiến hành cài đặt theo các bước mặc định của phần mềm.
3. **Lưu ý cực kỳ quan trọng:** Tại bước cấu hình cơ chế tải gói tự động (*Always install missing packages on-the-fly*), bắt buộc chọn mục **Always**.

### Bước 3: Tạo môi trường độc lập bằng Conda
1. Tạo môi trường: conda create -n manim_env python=3.10 -y
2. Kích hoạt môi trường: conda activate manim_env
3. Cài đặt môi trường: pip install manim numpy
