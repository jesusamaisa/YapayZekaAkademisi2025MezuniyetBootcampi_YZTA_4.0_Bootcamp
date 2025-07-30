from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2
import os, json
from keras.models import load_model
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # CORS engelini kaldırır
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları /static üzerinden sun
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

model = load_model("lung_cancer_detection_model.h5")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

IMG_SIZE = 150
STATS_FILE = "stats.json"

def preprocess_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    return img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

def update_stats(filename, result, confidence):
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
        if not isinstance(stats, list):
            raise ValueError("Eski format bulundu, liste bekleniyordu.")
    except:
        stats = []

    stats.append({
        "filename": filename,
        "result": result,
        "confidence": round(confidence * 100, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    img = preprocess_image(filepath)
    prediction = model.predict(img)[0][0]

    result = "NORMAL" if prediction > 0.5 else "PNEUMONIA"
    confidence = float(prediction if result == "NORMAL" else 1 - prediction)

    update_stats(file.filename, result, confidence)
    return JSONResponse({"result": result, "confidence": round(confidence * 100, 2)})

@app.get("/stats")
def get_stats():
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)

        total = len(stats)
        normal = sum(1 for s in stats if s["result"] == "NORMAL")
        pneumonia = total - normal
        mean_conf = round(np.mean([s["confidence"] for s in stats]), 2) if total > 0 else 0

        return {
            "total": total,
            "normal": normal,
            "pneumonia": pneumonia,
            "normal_percent": round((normal / total) * 100, 2) if total else 0,
            "pneumonia_percent": round((pneumonia / total) * 100, 2) if total else 0,
            "average_confidence": mean_conf
        }
    except:
        return {}

@app.get("/history")
def get_history():
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
        return stats
    except:
        return []
