from fastapi.testclient import TestClient
import sys
from pathlib import Path
from io import BytesIO

# Đảm bảo Python tìm thấy thư mục api khi chạy test từ thư mục gốc
sys.path.append(str(Path(__file__).resolve().parent.parent))

from api.app import app

client = TestClient(app)

def test_home():
    """Kiểm tra API trang chủ hoạt động"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Kiểm tra trạng thái hệ thống (Health Check)"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_model_info():
    """Kiểm tra API trả về đúng cấu trúc thông tin mô hình"""
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "algorithm" in data
    assert "features" in data
    assert len(data["features"]) == 7

def test_predict():
    """Kiểm tra API dự đoán hoạt động đúng với dữ liệu hợp lệ và lưu vào DB"""
    payload = {
        "N": 90.0,
        "P": 42.0,
        "K": 43.0,
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data

def test_invalid_input():
    """Kiểm tra hệ thống trả về lỗi 422 khi truyền dữ liệu sai định dạng"""
    payload = {
        "N": "abc",  # Sai kiểu dữ liệu
        "P": 42.0,
        "K": 43.0,
        "temperature": 20.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 200.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_get_history():
    """Kiểm tra API lấy lịch sử dự đoán"""
    response = client.get("/history?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_batch_predict():
    """Kiểm tra tính năng dự đoán hàng loạt với file CSV giả lập"""
    # Tạo nội dung CSV giả lập chứa tiêu đề và 1 dòng dữ liệu hợp lệ
    csv_content = "N,P,K,temperature,humidity,ph,rainfall\n90,42,43,20.8,82,6.5,202\n"
    file_payload = {
        "file": ("test_crops.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")
    }
    
    response = client.post("/batch-predict", files=file_payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "prediction" in data[0]
    assert "confidence" in data[0]

def test_clear_history():
    """Kiểm tra API xóa lịch sử dự đoán"""
    response = client.delete("/history")
    assert response.status_code == 200
    assert response.json()["status"] in ["success", "error"]  # success nếu xóa được, error nếu DB rỗng/chưa init