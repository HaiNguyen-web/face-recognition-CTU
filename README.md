# Face Recognition CTU

## Mô tả
Đây là dự án nhận diện khuôn mặt sử dụng **FaceNet** với FastAPI để quản lý dữ liệu khuôn mặt và DeepFace để nhận diện.

## Yêu cầu hệ thống
- Python 3.11 hoặc mới hơn
- Git

## Hướng dẫn cài đặt

### 1. Clone repository
```bash
git clone https://github.com/HaiNguyen-web/face-recognition-CTU.git
cd face-recognition-CTU
```

### 2. Tạo và kích hoạt môi trường ảo `.venv`
```bash
python -m venv .venv
```
- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Cài đặt các dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy FastAPI để import dữ liệu vào database
```bash
uvicorn main:app --reload
```
API sẽ chạy tại: `http://127.0.0.1:8000`

### 5. Sử dụng notebook `deepface.ipynb` để nhận diện khuôn mặt
Mở file Jupyter Notebook:
```bash
jupyter notebook
```
Sau đó, vào **deepface.ipynb** để chạy nhận diện.

## Thông tin thêm
- **Thư mục `db_data/`**: Chứa dữ liệu khuôn mặt đã được lưu.
- **Thư mục `templates/`**: Chứa giao diện HTML nếu cần.
- **Thư mục `__pycache__/`**: Chứa file bytecode của Python (có thể bị bỏ qua).

---
**Tác giả:** HaiNguyen-web

