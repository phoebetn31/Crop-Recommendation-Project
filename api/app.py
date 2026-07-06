from fastapi import FastAPI
import joblib
import pandas as pd

#tạo ứng dụng FastAPI
app = FastAPI(
    title="Crop Recommendation API",
    description="API dự đoán cây trồng bằng Random Forest",
    version="1.0"
)

model = joblib.load("../models/crop_model.pkl")

label_encoder = joblib.load("../models/label_encoder.pkl")

scaler = joblib.load("../models/scaler.pkl")