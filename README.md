## Crop Recommendation System

## Giới thiệu

Crop Recommendation System là hệ thống hỗ trợ dự đoán loại cây trồng phù hợp dựa trên các đặc trưng của đất và điều kiện môi trường bằng Machine Learning.

Dự án sử dụng:
- Random Forest Classifier
- FastAPI
- Streamlit
- SQLite
- Docker

---

## Cấu trúc thư mục

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
│   │   ├── crops/ (chứa ảnh các loại cây)
│   │   ├── dashboard.jpg
│   │   └── logo.png
│   ├── pages/
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Predict.py
│   │   ├── 3_History.py
│   │   ├── 4_Batch_Prediction.py
│   │   └── 5_Model_Infomation.py
│   ├── app.py
│   └── style.css
├── tests/
│   ├── sample.csv
│   └── test_api.py
├── .coverage
├── .gitignore
├── create_database.py
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.streamlit
├── README.md
├── requirements.txt
└── supervisord.conf

## Yêu cầu môi trường
- Python 3.11
- pip
- Docker Desktop (nếu chạy Docker)

## Cài đặt
- Clone project:
    git clone <repository_url>
    cd Crop-Recommendation-Project  
- Cài đặt thư viện:
    pip install -r requirements.txt

## Chạy Backend FastAPI

    uvicorn api.app:app --reload

API sẽ chạy tại:
http://localhost:8000

## Chạy giao diện Streamlit
Mở Terminal mới:

    streamlit run streamlit/app.py

Giao diện sẽ chạy tại:
http://localhost:8501

## Chạy bằng Docker
- Build image:
    docker compose build

- Run container:
    docker compose up

- Sau khi chạy thành công:
    FastAPI: http://localhost:8000
    Streamlit: http://localhost:8501

## Công nghệ sử dụng

Python
Scikit-learn
Random Forest
FastAPI
Streamlit
SQLite
Docker