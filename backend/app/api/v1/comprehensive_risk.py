from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.services.risk_calculator_service import risk_calculator_service

router = APIRouter()

@router.get("/site/{site_id}")
async def get_comprehensive_risk_for_site(site_id: int, db: Session = Depends(get_db)):
    """Récupérer l'analyse de risque globale pour un site spécifique"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        comprehensive_risk = await risk_calculator_service.calculate_comprehensive_risk(
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
            "site_info": {
                "building_type": site.building_type.value,
                "building_value": site.building_value,
                "surface_area": site.surface_area,
                "construction_year": site.construction_year
            },
            "comprehensive_analysis": comprehensive_risk
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse globale: {str(e)}"
        )

@router.post("/update-all-sites")
async def update_all_sites_comprehensive_risk(db: Session = Depends(get_db)):
    """Mettre à jour les scores de risque global pour tous les sites"""
    from app.models.site import Site
    
    try:
        sites = db.query(Site).all()
        updated_sites = []
        
        for site in sites:
            try:
                comprehensive_risk = await risk_calculator_service.calculate_comprehensive_risk(
                    site.latitude,
                    site.longitude,
                    site.building_type.value,
                    site.building_value
                )
                
                # Mettre à jour le score de risque global
                global_score = comprehensive_risk.get("comprehensive_risk", {}).get("global_risk_score", 30.0)
                site.risk_score = global_score
                
                risk_level = comprehensive_risk.get("comprehensive_risk", {}).get("risk_level", "modéré")
                risk_category = comprehensive_risk.get("comprehensive_risk", {}).get("risk_category", "acceptable")
                
                updated_sites.append({
                    "id": site.id,
                    "name": site.name,
                    "new_risk_score": global_score,
                    "risk_level": risk_level,
                    "risk_category": risk_category,
                    "weather_score": comprehensive_risk.get("weather_risk", {}).get("risk_score", 25.0),
                    "disaster_score": comprehensive_risk.get("disaster_risk", {}).get("disaster_risk", {}).get("disaster_risk_score", 15.0),
                    "vulnerability_score": comprehensive_risk.get("vulnerability_risk", {}).get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0)
                })
                
            except Exception as e:
                print(f"Erreur lors de la mise à jour du site {site.id}: {e}")
                continue
        
        # Commiter les changements
        db.commit()
        
        return {
            "message": f"Analyse globale terminée pour {len(updated_sites)} sites",
            "updated_sites": updated_sites
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour des scores: {str(e)}"
        )

@router.get("/statistics")
async def get_comprehensive_risk_statistics(db: Session = Depends(get_db)):
    """Obtenir des statistiques sur les risques globaux"""
    from app.models.site import Site
    
    try:
        sites = db.query(Site).all()
        
        if not sites:
            return {
                "total_sites": 0,
                "average_global_risk": 0,
                "risk_distribution": {},
                "risk_categories": {},
                "high_risk_sites": 0,
                "component_analysis": {}
            }
        
        # Analyser les risques pour tous les sites
        global_risks = []
        weather_risks = []
        disaster_risks = []
        vulnerability_risks = []
        risk_categories = {}
        
        for site in sites:
            try:
                comprehensive_risk = await risk_calculator_service.calculate_comprehensive_risk(
                    site.latitude,
                    site.longitude,
                    site.building_type.value,
                    site.building_value
                )
                
                global_score = comprehensive_risk.get("comprehensive_risk", {}).get("global_risk_score", 30.0)
                global_risks.append(global_score)
                
                weather_score = comprehensive_risk.get("weather_risk", {}).get("risk_score", 25.0)
                weather_risks.append(weather_score)
                
                disaster_score = comprehensive_risk.get("disaster_risk", {}).get("disaster_risk", {}).get("disaster_risk_score", 15.0)
                disaster_risks.append(disaster_score)
                
                vulnerability_score = comprehensive_risk.get("vulnerability_risk", {}).get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0)
                vulnerability_risks.append(vulnerability_score)
                
                # Compter les catégories de risque
                risk_category = comprehensive_risk.get("comprehensive_risk", {}).get("risk_category", "acceptable")
                risk_categories[risk_category] = risk_categories.get(risk_category, 0) + 1
                
            except Exception as e:
                print(f"Erreur lors de l'analyse du site {site.id}: {e}")
                continue
        
        if global_risks:
            avg_global_risk = sum(global_risks) / len(global_risks)
            high_risk_count = len([r for r in global_risks if r > 50])
            
            risk_distribution = {
                "faible": len([r for r in global_risks if r < 20]),
                "modéré": len([r for r in global_risks if 20 <= r < 40]),
                "élevé": len([r for r in global_risks if 40 <= r < 60]),
                "très élevé": len([r for r in global_risks if r >= 60])
            }
            
            component_analysis = {
                "weather": {
                    "average": round(sum(weather_risks) / len(weather_risks), 2),
                    "high_risk_count": len([r for r in weather_risks if r > 50])
                },
                "disasters": {
                    "average": round(sum(disaster_risks) / len(disaster_risks), 2),
                    "high_risk_count": len([r for r in disaster_risks if r > 40])
                },
                "vulnerability": {
                    "average": round(sum(vulnerability_risks) / len(vulnerability_risks), 2),
                    "high_risk_count": len([r for r in vulnerability_risks if r > 50])
                }
            }
        else:
            avg_global_risk = 0
            high_risk_count = 0
            risk_distribution = {"faible": 0, "modéré": 0, "élevé": 0, "très élevé": 0}
            component_analysis = {
                "weather": {"average": 0, "high_risk_count": 0},
                "disasters": {"average": 0, "high_risk_count": 0},
                "vulnerability": {"average": 0, "high_risk_count": 0}
            }
        
        return {
            "total_sites": len(sites),
            "average_global_risk": round(avg_global_risk, 2),
            "risk_distribution": risk_distribution,
            "risk_categories": risk_categories,
            "high_risk_sites": high_risk_count,
            "component_analysis": component_analysis
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul des statistiques: {str(e)}"
        )

@router.get("/recommendations/{site_id}")
async def get_site_recommendations(site_id: int, db: Session = Depends(get_db)):
    """Obtenir des recommandations détaillées pour un site"""
    from app.models.site import Site
    
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    try:
        comprehensive_risk = await risk_calculator_service.calculate_comprehensive_risk(
            site.latitude,
            site.longitude,
            site.building_type.value,
            site.building_value
        )
        
        recommendations = comprehensive_risk.get("recommendations", [])
        risk_breakdown = comprehensive_risk.get("risk_breakdown", {})
        
        return {
            "site_id": site_id,
            "site_name": site.name,
            "location": f"{site.city}, {site.country}",
            "global_risk_score": comprehensive_risk.get("comprehensive_risk", {}).get("global_risk_score", 30.0),
            "risk_level": comprehensive_risk.get("comprehensive_risk", {}).get("risk_level", "modéré"),
            "risk_category": comprehensive_risk.get("comprehensive_risk", {}).get("risk_category", "acceptable"),
            "confidence_score": comprehensive_risk.get("comprehensive_risk", {}).get("confidence_score", 0.7),
            "recommendations": recommendations,
            "risk_breakdown": risk_breakdown,
            "priority_actions": _generate_priority_actions(comprehensive_risk)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération des recommandations: {str(e)}"
        )

def _generate_priority_actions(comprehensive_risk: Dict) -> List[Dict]:
    """Générer des actions prioritaires basées sur l'analyse"""
    actions = []
    
    global_score = comprehensive_risk.get("comprehensive_risk", {}).get("global_risk_score", 30.0)
    weather_score = comprehensive_risk.get("weather_risk", {}).get("risk_score", 25.0)
    disaster_score = comprehensive_risk.get("disaster_risk", {}).get("disaster_risk", {}).get("disaster_risk_score", 15.0)
    vulnerability_score = comprehensive_risk.get("vulnerability_risk", {}).get("vulnerability_risk", {}).get("vulnerability_risk_score", 25.0)
    
    # Actions prioritaires basées sur le score global
    if global_score > 70:
        actions.append({
            "priority": "critique",
            "action": "Évaluation immédiate des vulnérabilités",
            "description": "Réaliser une évaluation détaillée et mettre en place des mesures de protection renforcées",
            "estimated_cost": "Élevé",
            "timeline": "Immédiat"
        })
    elif global_score > 50:
        actions.append({
            "priority": "élevée",
            "action": "Renforcement des mesures de protection",
            "description": "Améliorer les systèmes de protection existants",
            "estimated_cost": "Modéré",
            "timeline": "1-3 mois"
        })
    
    # Actions basées sur les composants spécifiques
    if weather_score > 60:
        actions.append({
            "priority": "élevée",
            "action": "Surveillance météo renforcée",
            "description": "Mettre en place un système de surveillance météo en temps réel",
            "estimated_cost": "Faible",
            "timeline": "1 mois"
        })
    
    if disaster_score > 50:
        actions.append({
            "priority": "élevée",
            "action": "Plan de préparation aux catastrophes",
            "description": "Élaborer et tester un plan de réponse aux catastrophes",
            "estimated_cost": "Modéré",
            "timeline": "2-4 mois"
        })
    
    if vulnerability_score > 60:
        actions.append({
            "priority": "élevée",
            "action": "Renforcement structurel",
            "description": "Considérer des renforcements structurels du bâtiment",
            "estimated_cost": "Élevé",
            "timeline": "3-6 mois"
        })
    
    # Actions générales de maintenance
    actions.append({
        "priority": "normale",
        "action": "Maintenance préventive",
        "description": "Maintenir les systèmes de protection existants",
        "estimated_cost": "Faible",
        "timeline": "Continue"
    })
    
    return actions 