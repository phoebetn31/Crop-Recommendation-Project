#thêm các thư viện cần thiết
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

#tạo một app API
app = FastAPI(
    title="Crop Recommendation API",
    description="API dự đoán cây trồng bằng Random Forest",
    version="1.0"
)

# Load model
model = joblib.load("models/crop_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
scaler = joblib.load("models/scaler.pkl")

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

    prediction = model.predict(input_data)
    crop = label_encoder.inverse_transform(prediction)

    return {"prediction": crop[0]}