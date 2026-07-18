
# Crop Recommendation System

## Giới thiệu

**Crop Recommendation System** là hệ thống hỗ trợ dự đoán loại cây trồng phù hợp dựa trên các đặc trưng của đất và điều kiện môi trường bằng Machine Learning.

Hệ thống sử dụng mô hình **Random Forest Classifier** (đã qua tinh chỉnh siêu tham số bằng `GridSearchCV`) để phân tích dữ liệu đầu vào và đề xuất loại cây trồng phù hợp nhất. Ngoài ra, hệ thống còn cung cấp dịch vụ REST API, giao diện Web trực quan, lưu lịch sử dự đoán bằng SQLite và hỗ trợ triển khai bằng Docker.

---

# 1. Repository Git & Thông tin chung

## Repository GitHub

https://github.com/phoebetn31/Crop-Recommendation-Project

## Giảng viên được mời làm Collaborator

```
khoa.vv@ou.edu.vn
```

## Thông tin khóa học

- **Môn học:** Trí tuệ Nhân tạo (ITEC3413)
- **Trường:** Đại học Mở Thành phố Hồ Chí Minh
- **Lớp:** CS24DH01
- **Học kỳ:** HK3 năm học 2025–2026
- **Nhóm:** 22_Nhân_Mai_Thái

### Commit dùng để chấm

Tag: nop-BTL
Commit: ef4c15712edf1dfd432a9cb5349b7e829e84966bS

---

# 2. Video Demo

**Link video:**

https://youtu.be/pa7BfAQApuE?si=xp6qiuzzQl6tYVN9

Video gồm các nội dung:

- Khởi động hệ thống bằng Docker Compose
- Dashboard
- Dự đoán cây trồng
- Lịch sử dự đoán
- Batch Prediction
- Model Information

---

# 3. Bảng phân công công việc

| Họ và tên | MSSV | Công việc | Đóng góp |
|-----------|------|-----------|-----------|
| Đặng Thị Tâm Nhân | 2451010031 | Tiền xử lý dữ liệu, huấn luyện & tinh chỉnh mô hình, xây dựng FastAPI, SQLite, Docker | 40% |
| Nguyễn Thị Trúc Mai | 2451012062 | Thu thập dữ liệu, EDA, đánh giá mô hình, phân tích kết quả | 32% |
| Nguyễn Quốc Thái | 2451012093 | Giao diện Streamlit, Docker, báo cáo, video demo | 28% |

**Tổng: 100%**

---

# 4. Khai báo sử dụng AI

| Công cụ | Mục đích | Phạm vi |
|----------|----------|----------|
| ChatGPT | Gợi ý ý tưởng, giải thích thuật toán, hỗ trợ sửa lỗi FastAPI, Streamlit, Docker, biên soạn tài liệu | Toàn bộ dự án |
| Gemini | Gợi ý bố cục báo cáo, chỉnh văn phong | Báo cáo |

---

# 5. Model Artifact

Mô hình được thử nghiệm trên bốn thuật toán:
    - KNN
    - SVC
    - XGBoost
    - Random Forest

Sau quá trình GridSearchCV, **Random Forest** đạt:
    - Accuracy: **99.55%**
    - Precision: **99.55%**
    - Recall: **99.55%**
    - F1-score: **99.55%**
    - AUC-ROC: **1.000**

Các artifact lưu tại thư mục `models/`:
    - `crop_model.pkl`
    - `label_encoder.pkl`
    - `scaler.pkl`

Ví dụ load model:
    import joblib

    model = joblib.load("models/crop_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")

---

# 6. Cấu trúc thư mục
Crop-Recommendation-Project/
├── api/
│   └── app.py
├── data/
│   └── Crop_recommendation.csv
├── database/
│   └── crop_prediction.db
├── models/
│   ├── crop_model.pkl
│   ├── label_encoder.pkl
│   └── scaler.pkl
├── notebook/
│   └── crop_prediction.ipynb
├── streamlit/
│   ├── assets/
│   ├── pages/
│   ├── app.py
│   └── style.css
├── tests/
│   ├── sample.csv
│   └── test_api.py
├── create_database.py
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.streamlit
├── requirements.txt
└── README.md

---

# 7. REST API

| Endpoint | Chức năng |
|-----------|-----------|
| GET / | Trang chủ |
| GET /health | Kiểm tra trạng thái hệ thống |
| GET /model-info | Thông tin mô hình |
| POST /predict | Dự đoán một mẫu |
| GET /history | Lấy lịch sử dự đoán |
| DELETE /history | Xóa lịch sử |
| POST /batch-predict | Dự đoán hàng loạt |

---

# 8. Cơ sở dữ liệu

Bảng `prediction_history`

| Trường | Kiểu | Ý nghĩa |
|---------|------|----------|
| id | INTEGER | Khóa chính |
| N | REAL | Nitơ |
| P | REAL | Photpho |
| K | REAL | Kali |
| temperature | REAL | Nhiệt độ |
| humidity | REAL | Độ ẩm |
| ph | REAL | Độ pH |
| rainfall | REAL | Lượng mưa |
| prediction | TEXT | Cây trồng dự đoán |
| confidence | REAL | Độ tin cậy |
| created_at | TIMESTAMP | Thời gian |

---

# 9. Chạy cục bộ

## Yêu cầu
    - Python 3.11
    - pip

## Clone project
    git clone <repository_url>
    cd Crop-Recommendation-Project

## Cài thư viện
    pip install -r requirements.txt

## Chạy FastAPI
    uvicorn api.app:app --reload

API:
    http://localhost:8000

Swagger:
    http://localhost:8000/docs

## Chạy Streamlit

streamlit run streamlit/app.py

Giao diện:
http://localhost:8501

---

# 10. Chạy bằng Docker

Build:
    docker compose build

Run:
    docker compose up

Run nền:
    docker compose up -d

Dừng:
    docker compose down

Sau khi chạy:

- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs

---

# 11. Kiểm thử

Thực hiện kiểm thử:
pytest --cov=api tests/ -W ignore

Các ca kiểm thử bao gồm:

- Load mô hình
- Health Check
- Predict API
- Batch Predict
- History API
- Delete History
- Schema đầu vào
- Dữ liệu không hợp lệ

Kết quả:

- 8/8 Test Passed
- Code Coverage: **91%**
