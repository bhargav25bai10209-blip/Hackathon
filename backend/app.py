import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

sys.path.append(str(Path(__file__).resolve().parent))
from services.breed_lookup import breed_lookup
from services.predictor import predictor

app = FastAPI(
    title="AI Cattle & Buffalo Breed Identification API",
    description="Identifies cattle and buffalo breeds from images and provides native region information.",
    version="1.0"
)

# Enable CORS for all origins (useful for hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the models directory for static files like the confusion matrix
app.mount("/models", StaticFiles(directory=str(Path(__file__).resolve().parent / "models")), name="models")

# Serve the frontend UI
@app.get("/")
async def serve_frontend():
    return FileResponse(str(Path(__file__).resolve().parent / "static" / "index.html"))

# Enable CORS for all origins (useful for hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopPrediction(BaseModel):
    breed: str
    confidence: float
    native_region: List[str]
    type: str

class PredictionResponse(BaseModel):
    top_3: List[TopPrediction]
    model_version: str

from fastapi.staticfiles import StaticFiles

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": predictor.model is not None,
        "lookup_loaded": len(breed_lookup.all_breeds) > 0
    }

@app.get("/breeds")
async def get_all_breeds():
    return breed_lookup.get_all_breeds()

@app.get("/metrics")
async def get_model_metrics():
    metrics_path = Path(__file__).resolve().parent / "models" / "metrics.json"
    
    if not metrics_path.exists():
        return {
            "error": "Metrics file not found. Ensure model has been trained and metrics.json generated."
        }
        
    with open(metrics_path, 'r') as f:
        metrics_data = json.load(f)
        
    metrics_data["confusion_matrix_url"] = "/models/confusion_matrix.png"
    return metrics_data

# Serve the models directory for static files like the confusion matrix
app.mount("/models", StaticFiles(directory=str(Path(__file__).resolve().parent / "models")), name="models")

@app.post("/predict", response_model=PredictionResponse)
async def predict_breed(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = [
        "image/jpeg", "image/png", "image/webp", 
        "image/avif", "image/bmp", "image/tiff", "image/gif"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")
        
    try:
        image_bytes = await file.read()
        
        # Max file size 10MB
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max size is 10MB.")
            
        # Get predictions
        top_preds = predictor.predict(image_bytes, top_k=3)
        
        response_preds = []
        for p in top_preds:
            class_label = p['class_label']
            # Split class_label back into animal_type and canonical_breed
            # e.g. "cattle_Gir" -> "cattle", "Gir"
            parts = class_label.split('_', 1)
            animal_type = parts[0]
            canonical_breed = parts[1] if len(parts) > 1 else class_label
            
            # Lookup region info
            region_info = breed_lookup.get_region(canonical_breed, animal_type)
            
            response_preds.append(
                TopPrediction(
                    breed=canonical_breed,
                    confidence=p['confidence'],
                    native_region=region_info.get('native_region', ["Data unavailable"]),
                    type=animal_type
                )
            )
            
        return PredictionResponse(
            top_3=response_preds,
            model_version="v1.0"
        )
        
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail="Model service unavailable. Please check server logs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
