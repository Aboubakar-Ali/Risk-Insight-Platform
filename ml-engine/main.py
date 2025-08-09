from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Risk Insight ML Engine",
    description="Moteur de scoring et d'IA pour Risk Insight Platform",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Risk Insight ML Engine",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict/risk")
async def predict_risk():
    """Prédiction de risque (placeholder)"""
    return {
        "risk_score": 65.5,
        "confidence": 0.85,
        "factors": ["Localisation", "Type de bâtiment", "Historique météo"]
    } 