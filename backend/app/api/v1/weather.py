from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
import asyncio

from app.core.database import get_db
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/site/{site_id}")
async def get_weather_for_site(site_id: int, db: Session = Depends(get_db)):
    """Récupérer les données météo pour un site spécifique"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        weather_risk = await weather_service.get_weather_risk_for_site(
            site.latitude, 
            site.longitude
        )
        
        return {
            "site_id": site_id,
            "site_name": site.name,
            "location": f"{site.city}, {site.country}",
            "coordinates": {
                "latitude": site.latitude,
                "longitude": site.longitude
            },
            "weather_risk": weather_risk
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération météo: {str(e)}"
        )

@router.get("/current/{site_id}")
async def get_current_weather(site_id: int, db: Session = Depends(get_db)):
    """Récupérer les conditions météo actuelles pour un site"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        weather_data = await weather_service.get_current_weather(
            site.latitude, 
            site.longitude
        )
        
        return {
            "site_id": site_id,
            "site_name": site.name,
            "current_weather": weather_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération météo: {str(e)}"
        )

@router.post("/update-risk-scores")
async def update_all_sites_risk_scores(db: Session = Depends(get_db)):
    """Mettre à jour les scores de risque de tous les sites basés sur la météo"""
    from app.models.site import Site
    
    try:
        sites = db.query(Site).all()
        updated_sites = []
        
        for site in sites:
            try:
                weather_risk = await weather_service.get_weather_risk_for_site(
                    site.latitude, 
                    site.longitude
                )
                
                # Mettre à jour le score de risque avec les données météo
                site.risk_score = weather_risk["risk_score"]
                updated_sites.append({
                    "id": site.id,
                    "name": site.name,
                    "new_risk_score": weather_risk["risk_score"],
                    "weather_conditions": weather_risk["risk_factors"]["conditions"]
                })
                
            except Exception as e:
                print(f"Erreur lors de la mise à jour du site {site.id}: {e}")
                continue
        
        # Commiter les changements
        db.commit()
        
        return {
            "message": f"Mise à jour terminée pour {len(updated_sites)} sites",
            "updated_sites": updated_sites
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour des scores: {str(e)}"
        ) 