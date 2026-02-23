# Image-Checking 🖼️

Một khung kiểm thử tự động UI dựa trên Python kết hợp **tự động hóa web** với **nhận dạng hình ảnh**. Dự án sử dụng OpenCV để ghi đè mẫu hình ảnh và Playwright để tự động hóa trình duyệt, tạo ra các kịch bản kiểm thử dựa trên hình ảnh.

## Giới thiệu dự án

Image-Checking được thiết kế để kiểm thử các tình huống end-to-end khi các bộ chọn phần tử truyền thống không đáng tin cậy. Dự án tích hợp:
- **OpenCV**: Ghi đè mẫu hình ảnh và nhận dạng hình ảnh
- **Playwright**: Tự động hóa trình duyệt hiện đại
- **Robot Framework**: Kiểm thử dạng keyword
- **Pytest**: Framework kiểm thử và báo cáo

## Cấu trúc dự án

```
Image-Checking/
├── CompareImage.py       # Lớp so sánh hình ảnh với OpenCV
├── page.py               # Thư viện tương tác UI cấp cao
├── conftest.py           # Cấu hình Pytest và trình duyệt
├── test_demo_cv2.py      # Các trường hợp kiểm thử ví dụ
├── pyproject.toml        # Metadata dự án
├── pytest.ini            # Cấu hình Pytest
├── requirements.txt      # Các thư viện Python cần thiết
├── img/                  # Thư mục chứa ảnh tham chiếu
├── tmp/                  # Thư mục chứa ảnh chụp màn hình tạm thời
└── profile/              # Thư mục lưu hồ sơ trình duyệt
```

## Yêu cầu hệ thống

- Python 3.11 trở lên
- Windows, macOS hoặc Linux
- Chrome/Chromium đã cài đặt

## Cài đặt

### Bước 1: Sao chép hoặc tải dự án

Sao chép kho lưu trữ hoặc tải xuống dự án về máy tính.

### Bước 2: Tạo môi trường ảo (khuyến nghị)

Trên Windows:
```
python -m venv venv
venv\Scripts\activate
```

Trên macOS/Linux:
```
python -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện cần thiết

```
pip install -r requirements.txt
```

Thư viện chính cần thiết:
- opencv-python: Xử lý hình ảnh
- playwright: Tự động hóa trình duyệt
- pytest: Framework kiểm thử
- robotframework: Kiểm thử dạng keyword

### Bước 4: Cài đặt trình duyệt Playwright

```
playwright install chrome
```

## Hướng dẫn chạy dự án

### Chạy tất cả các trường hợp kiểm thử

```
pytest
```

### Chạy với chế độ chi tiết

```
pytest -v
```

### Chạy một tệp kiểm thử cụ thể

```
pytest test_demo_cv2.py
```

### Chạy một trường hợp kiểm thử cụ thể

```
pytest test_demo_cv2.py::Test_demo::test1_login
```

## Cấu hình chính

Các tham số quan trọng trong `conftest.py`:

- **DEFAULT_CONFIDENCE**: Ngưỡng độ tin cậy để nhận dạng hình ảnh (0.0-1.0, mặc định: 0.8)
- **TIMEOUT_WAIT_IMG**: Thời gian chờ tối đa để tìm hình ảnh (mặc định: 15 giây)
- **USER_AGENT**: Chuỗi nhận dạng trình duyệt

## Chuẩn bị hình ảnh tham chiếu

1. Đặt hình ảnh tham chiếu trong thư mục `img/` dưới dạng tệp PNG
2. Đặt tên tệp rõ ràng và dễ hiểu
3. Đảm bảo hình ảnh có độ tương phản cao để nhận dạng tốt hơn

## Các chức năng chính

### Lớp Lib (page.py)

- **wait_image_and_click()**: Chờ hình ảnh xuất hiện rồi click vào vị trí giữa
- **wait_and_input()**: Chờ hình ảnh rồi nhập văn bản
- **wait_and_verify()**: Chờ hình ảnh để xác minh sự hiện diện

### Lớp MyCompareImage (CompareImage.py)

- **my_find_image()**: Tìm hình ảnh mẫu trong ảnh chụp màn hình
- **my_click_image()**: Tìm và click vào hình ảnh mẫu

## Các thư mục quan trọng

- **img/**: Chứa hình ảnh tham chiếu cho quá trình nhận dạng
- **tmp/**: Lưu trữ ảnh chụp màn hình tạm thời trong quá trình kiểm thử
- **profile/**: Lưu hồ sơ trình duyệt cho các phiên làm việc

## Ghi chú

- Ảnh tham chiếu càng rõ ràng, càng nhỏ thì nhận dạng càng chính xác
- Thời gian chờ mặc định là 15 giây, có thể điều chỉnh theo nhu cầu
- Đảm bảo tất cả các ảnh được đặt tên rõ ràng và tổ chức hợp lý

---

**Cập nhật lần cuối**: Tháng 2 năm 2026
**Phiên bản Python**: 3.11+