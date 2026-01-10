""" ML Inference API Loads trained model on startup, serves predictions via HTTP """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
import joblib
import numpy as np
from pathlib import Path
import os

app = FastAPI(title="Iris Classifier API", version="1.0.0")

model = None

class_names = ["setosa", "versicolor", "virginica"]

@app.on_event("startup")
async def load_model():
    global model
    # Get the project root directory (parent of app/)
    project_root = Path(__file__).parent.parent
    model_path = project_root / "model" / "model.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
    
    model = joblib.load(model_path)
    print(f"✅ Model loaded from {model_path}")



class PredictionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }
    )
    
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: str
    prediction_index: int
    confidence: float
    all_probabilities: dict[str, float]


@app.get("/health")
async def health_check():
    return{
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(request.features) != 4:
        raise HTTPException(status_code=400, detail=f"expected 4 features, got {len(request.features)}")
    
    features = np.array([request.features])

    #make prediction
    prediction_idx = model.predict(features)[0]
    prediction_label = class_names[prediction_idx]

    #Get Confidence scores
    probabilities = model.predict_proba(features)[0]
    confidence = float(probabilities[prediction_idx])

    #build detailed response
    all_probabilities = {class_names[i]: float(probabilities[i]) for i in range(len(class_names))}

    return PredictionResponse(
        prediction=prediction_label,
        prediction_index=int(prediction_idx),
        confidence=confidence,
        all_probabilities=all_probabilities
    )


@app.get("/")
async def root():
    """ Root endpoint - shows API info """
    return{
        "message":"Iris Classifier API",
        "endpoints":{
            "POST /predict": "Make a prediction",
            "GET /health": "Health check endpoint",
            "GET /docs": "Interactive API documentation"
        }
    }