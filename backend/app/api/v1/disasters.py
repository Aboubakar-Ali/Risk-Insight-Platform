from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.services.disaster_service import disaster_service

router = APIRouter()

@router.get("/site/{site_id}")
async def get_disaster_risk_for_site(site_id: int, db: Session = Depends(get_db)):
    """Récupérer le risque de catastrophe pour un site spécifique"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        disaster_risk = await disaster_service.get_disaster_risk_for_site(
            site.latitude,
            site.longitude,
            site.building_type.value,
            site.building_value
        )
        
        return {
            "site_id": site_id,
            "site_name": site.name,
            "location": f"{site.city}, {site.country}",
            "coordinates": {
                "latitude": site.latitude,
                "longitude": site.longitude
            },
            "disaster_risk": disaster_risk
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du risque catastrophe: {str(e)}"
        )

@router.get("/historical/{site_id}")
async def get_historical_disasters(site_id: int, db: Session = Depends(get_db)):
    """Récupérer l'historique des catastrophes pour un site"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        disaster_risk = await disaster_service.get_disaster_risk_for_site(
            site.latitude,
            site.longitude,
            site.building_type.value,
            site.building_value
        )
        
        return {
            "site_id": site_id,
            "site_name": site.name,
            "historical_disasters": disaster_risk.get("disasters", []),
            "data_sources": disaster_risk.get("data_sources", {}),
            "risk_summary": disaster_risk.get("disaster_risk", {})
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'historique: {str(e)}"
        )

@router.post("/update-all-sites")
async def update_all_sites_disaster_risk(db: Session = Depends(get_db)):
    """Mettre à jour les scores de risque catastrophe pour tous les sites"""
    from app.models.site import Site
    
    try:
        sites = db.query(Site).all()
        updated_sites = []
        
        for site in sites:
            try:
                disaster_risk = await disaster_service.get_disaster_risk_for_site(
                    site.latitude,
                    site.longitude,
                    site.building_type.value,
                    site.building_value
                )
                
                # Mettre à jour le score de risque avec les données de catastrophes
                disaster_score = disaster_risk.get("disaster_risk", {}).get("disaster_risk_score", 15.0)
                
                # Calculer un nouveau score global (moyenne avec l'existant)
                new_risk_score = (site.risk_score + disaster_score) / 2
                site.risk_score = new_risk_score
                
                updated_sites.append({
                    "id": site.id,
                    "name": site.name,
                    "new_risk_score": new_risk_score,
                    "disaster_score": disaster_score,
                    "historical_events": disaster_risk.get("disaster_risk", {}).get("risk_factors", {}).get("historical_events", 0)
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

@router.get("/statistics")
async def get_disaster_statistics(db: Session = Depends(get_db)):
    """Obtenir des statistiques sur les risques de catastrophes"""
    from app.models.site import Site
    
    try:
        sites = db.query(Site).all()
        
        if not sites:
            return {
                "total_sites": 0,
                "average_disaster_risk": 0,
                "risk_distribution": {},
                "high_risk_sites": 0,
                "disaster_types": {}
            }
        
        # Analyser les risques pour tous les sites
        disaster_risks = []
        disaster_types = {}
        
        for site in sites:
            try:
                disaster_risk = await disaster_service.get_disaster_risk_for_site(
                    site.latitude,
                    site.longitude,
                    site.building_type.value,
                    site.building_value
                )
                
                risk_score = disaster_risk.get("disaster_risk", {}).get("disaster_risk_score", 15.0)
                disaster_risks.append(risk_score)
                
                # Compter les types de catastrophes
                disasters = disaster_risk.get("disasters", [])
                for disaster in disasters:
                    disaster_type = disaster.get("type", "inconnu")
                    disaster_types[disaster_type] = disaster_types.get(disaster_type, 0) + 1
                    
            except Exception as e:
                print(f"Erreur lors de l'analyse du site {site.id}: {e}")
                continue
        
        if disaster_risks:
            avg_risk = sum(disaster_risks) / len(disaster_risks)
            high_risk_count = len([r for r in disaster_risks if r > 40])
            
            risk_distribution = {
                "faible": len([r for r in disaster_risks if r < 20]),
                "modéré": len([r for r in disaster_risks if 20 <= r < 40]),
                "élevé": len([r for r in disaster_risks if 40 <= r < 60]),
                "très élevé": len([r for r in disaster_risks if r >= 60])
            }
        else:
            avg_risk = 0
            high_risk_count = 0
            risk_distribution = {"faible": 0, "modéré": 0, "élevé": 0, "très élevé": 0}
        
        return {
            "total_sites": len(sites),
            "average_disaster_risk": round(avg_risk, 2),
            "risk_distribution": risk_distribution,
            "high_risk_sites": high_risk_count,
            "disaster_types": disaster_types
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul des statistiques: {str(e)}"
        ) 