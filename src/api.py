from fastapi import FastAPI
import joblib

app = FastAPI()

# Load model + vectorizer
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

@app.post("/predict")
def predict(data: dict):
    text = data["text"]
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return {"prediction": str(pred)}

@app.get("/health")
def health():
    return {"status": "RMD-OK"}