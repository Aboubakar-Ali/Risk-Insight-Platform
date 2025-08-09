from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.risk import RiskAssessment, RiskScore
from app.models.risk_data import RiskData

router = APIRouter()

@router.get("/site/{site_id}", response_model=RiskAssessment)
async def get_risk_assessment(site_id: int, db: Session = Depends(get_db)):
    """Récupérer l'évaluation des risques pour un site"""
    risk_data = db.query(RiskData).filter(RiskData.site_id == site_id).first()
    if not risk_data:
        # Retourner une évaluation par défaut
        return RiskAssessment(
            site_id=site_id,
            overall_score=50.0,
            flood_risk=30.0,
            earthquake_risk=20.0,
            storm_risk=40.0,
            wildfire_risk=15.0,
            factors=["Localisation", "Type de bâtiment", "Historique météo"]
        )
    return risk_data

@router.post("/calculate/{site_id}")
async def calculate_risk_score(site_id: int, db: Session = Depends(get_db)):
    """Recalculer le score de risque pour un site"""
    # TODO: Implémenter le calcul de risque avancé
    return {
        "site_id": site_id,
        "message": "Calcul de risque à implémenter",
        "score": 65.5
    } 