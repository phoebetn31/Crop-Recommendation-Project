#thêm các thư viện cần thiết
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import joblib
import sqlite3
from io import StringIO
import numpy as np  
import os
import sqlite3

#tạo một app API
app = FastAPI(
    title="Crop Recommendation API",
    description="API dự đoán cây trồng bằng Random Forest",
    version="1.0"
)

prediction_history = []

# Load model
model = joblib.load("models/crop_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
scaler = joblib.load("models/scaler.pkl")

# Kết nối SQLite
def get_connection():
    conn = sqlite3.connect("database/crop_prediction.db")
    conn.row_factory = sqlite3.Row
    return conn

# Input Schema
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

# Home - Trang chủ
@app.get("/")
def home():
    return {"message": "Crop Recommendation API is running!"}

# Health Check - Kiểm tra tình trạng của API
@app.get("/health")
def health():
    return {"status": "OK"}

# Model Information
@app.get("/model-info")
def model_info():
    return {
        "model_name": "Random Forest",
        "version": "1.0",
        "algorithm": "RandomForestClassifier",
        "features": [
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]
    }

# Predict - Phần chính, phần dự đoán
@app.post("/predict")
def predict(data: CropInput):

    input_data = pd.DataFrame([{
        "N": data.N,
        "P": data.P,
        "K": data.K,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,
        "rainfall": data.rainfall
    }])

    # Chuẩn hóa dữ liệu
    #input_scaled = scaler.transform(input_data)

    # Dự đoán
    #prediction = model.predict(input_scaled)

    # Xác suất dự đoán
    #probability = model.predict_proba(input_scaled)

    prediction = model.predict(input_data)

    probability = model.predict_proba(input_data)

    crop = label_encoder.inverse_transform(prediction)[0]

    confidence = float(probability.max())

    # Lưu vào SQLite
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prediction_history
    (
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall,
        prediction,
        confidence
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data.N,
        data.P,
        data.K,
        data.temperature,
        data.humidity,
        data.ph,
        data.rainfall,
        crop,
        confidence
    ))

    conn.commit()
    conn.close()

    return {
        "prediction": crop,
        "confidence": round(confidence, 4)
    }

@app.get("/history")
def history(limit: int = 10):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM prediction_history
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):

    contents = await file.read()

    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # Chuẩn hóa
    X = scaler.transform(df)

    # Dự đoán
    prediction = model.predict(X)

    probability = model.predict_proba(X)

    df["prediction"] = label_encoder.inverse_transform(prediction)

    df["confidence"] = np.max(probability, axis=1)

    return df.to_dict(orient="records")

# Đảm bảo đường dẫn tuyệt đối chuẩn xác đập thẳng từ thư mục gốc của dự án
PROJECT_ROOT = "D:\\Crop-Recommendation-Project"
DB_PATH = os.path.join(PROJECT_ROOT, "database", "crop_prediction.db")

@app.delete("/history")
def clear_history():
    try:
        # 1. Kết nối đúng file database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 2. Tự động tìm tên bảng thực tế đang lưu lịch sử dự đoán để tránh ghi sai tên bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Tìm xem trong các bảng có bảng nào tên là 'predictions', 'prediction', 'history' hoặc tương tự không
        target_table = None
        for t in ["predictions", "prediction", "history", "crop_predictions"]:
            if t in tables:
                target_table = t
                break
        
        if not target_table and tables:
            active_tables = [t for t in tables if t != "sqlite_sequence"]
            if active_tables:
                target_table = active_tables[0]
                
        if not target_table:
            conn.close()
            return {"status": "error", "message": f"Không tìm thấy bảng lưu trữ nào trong DB. Các bảng hiện có: {tables}"}
            
        cursor.execute(f"DELETE FROM {target_table}")
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success", 
            "message": f"Đã xóa sạch dữ liệu bảng '{target_table}' thành công!"
        }
    except Exception as e:
        print(f"❌ LỖI SQLITE THỰC TẾ: {str(e)}")
        return {"status": "error", "message": str(e)}