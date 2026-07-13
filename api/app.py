#thêm các thư viện cần thiết
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import joblib
import sqlite3
from io import StringIO
import numpy as np  

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
    input_scaled = scaler.transform(input_data)

    # Dự đoán
    prediction = model.predict(input_scaled)

    # Xác suất dự đoán
    probability = model.predict_proba(input_scaled)

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