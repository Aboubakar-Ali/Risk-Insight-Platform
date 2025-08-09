from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
import asyncio

from app.core.database import get_db
from app.services.ai_agent_service import ai_agent_service
from app.services.weather_service import weather_service
from app.services.disaster_service import disaster_service
from app.services.vulnerability_service import vulnerability_service
from app.services.risk_calculator_service import risk_calculator_service
from app.models.site import Site
from app.models.insurance_contract import InsuranceContract
from app.schemas.ai_agent import (
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    StrategicRecommendationsRequest,
    StrategicRecommendationsResponse,
    RiskMitigationRequest,
    RiskMitigationResponse
)

router = APIRouter()

@router.post("/analyze-contract", response_model=ContractAnalysisResponse)
async def analyze_contract_profitability(
    request: ContractAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyser la rentabilité d'un contrat d'assurance"""
    try:
        # Récupérer les données du site
        site = db.query(Site).filter(Site.id == request.site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Récupérer les données du contrat
        contract = db.query(InsuranceContract).filter(InsuranceContract.id == request.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contrat non trouvé")
        
        # Récupérer toutes les données de risque
        risk_data = {}
        
        # Données météo
        weather_data = await weather_service.get_current_weather(site.latitude, site.longitude)
        risk_data["weather_risk"] = weather_data
        
        # Données catastrophes
        disaster_data = await disaster_service.get_disaster_risk_for_site(
            site.latitude, site.longitude, site.building_type, site.building_value
        )
        risk_data["disaster_risk"] = disaster_data
        
        # Données vulnérabilité
        vulnerability_data = await vulnerability_service.get_vulnerability_risk_for_site(
            site.latitude, site.longitude, site.building_type, site.building_value
        )
        risk_data["vulnerability_risk"] = vulnerability_data
        
        # Données de risque global
        comprehensive_risk = await risk_calculator_service.calculate_comprehensive_risk(
            site.latitude, site.longitude, site.building_type, site.building_value
        )
        risk_data["comprehensive_risk"] = comprehensive_risk
        
        # Convertir les modèles en dictionnaires
        site_data = {
            "id": site.id,
            "name": site.name,
            "building_type": site.building_type,
            "building_value": site.building_value,
            "surface_area": site.surface_area,
            "risk_score": site.risk_score,
            "latitude": site.latitude,
            "longitude": site.longitude,
            "city": site.city
        }
        
        contract_data = {
            "id": contract.id,
            "annual_premium": contract.premium_amount,
            "deductible": contract.deductible,
            "coverage_type": "Standard",  # Valeur par défaut
            "status": contract.status,
            "start_date": contract.start_date.isoformat() if contract.start_date else None,
            "end_date": contract.end_date.isoformat() if contract.end_date else None
        }
        
        # Analyser avec l'agent IA
        analysis = await ai_agent_service.analyze_contract_profitability(
            contract_data, site_data, risk_data
        )
        
        return ContractAnalysisResponse(
            success=True,
            analysis=analysis,
            site_data=site_data,
            contract_data=contract_data,
            risk_data=risk_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@router.post("/strategic-recommendations", response_model=StrategicRecommendationsResponse)
async def get_strategic_recommendations(
    request: StrategicRecommendationsRequest,
    db: Session = Depends(get_db)
):
    """Obtenir des recommandations stratégiques pour le portefeuille"""
    try:
        # Récupérer tous les sites
        sites = db.query(Site).all()
        
        # Récupérer tous les contrats
        contracts = db.query(InsuranceContract).all()
        
        # Calculer les métriques du portefeuille
        total_sites = len(sites)
        total_value = sum(site.building_value for site in sites)
        total_premiums = sum(contract.premium_amount for contract in contracts)
        average_risk = sum(site.risk_score for site in sites) / total_sites if total_sites > 0 else 0
        
        # Distribution des types de bâtiments
        type_distribution = {}
        for site in sites:
            building_type = site.building_type
            type_distribution[building_type] = type_distribution.get(building_type, 0) + 1
        
        portfolio_data = {
            "total_sites": total_sites,
            "total_value": total_value,
            "total_premiums": total_premiums,
            "average_risk": average_risk,
            "type_distribution": type_distribution,
            "sites": [
                {
                    "id": site.id,
                    "name": site.name,
                    "building_type": site.building_type.value if site.building_type else None,
                    "building_value": site.building_value,
                    "risk_score": site.risk_score
                }
                for site in sites
            ],
            "contracts": [
                {
                    "id": contract.id,
                    "annual_premium": contract.premium_amount,
                    "status": contract.status.value if contract.status else None,
                    "coverage_type": "Standard"
                }
                for contract in contracts
            ]
        }
        
        # Obtenir les recommandations IA
        recommendations = await ai_agent_service.get_strategic_recommendations(portfolio_data)
        
        return StrategicRecommendationsResponse(
            success=True,
            recommendations=recommendations.get("recommendations", {}),
            portfolio_data=recommendations.get("portfolio_data", portfolio_data)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors des recommandations: {str(e)}")

@router.post("/risk-mitigation", response_model=RiskMitigationResponse)
async def analyze_risk_mitigation(
    request: RiskMitigationRequest,
    db: Session = Depends(get_db)
):
    """Analyser les mesures de mitigation des risques pour un site"""
    try:
        # Récupérer les données du site
        site = db.query(Site).filter(Site.id == request.site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Récupérer toutes les données de risque
        risk_data = {}
        
        # Données météo
        weather_data = await weather_service.get_current_weather(site.latitude, site.longitude)
        risk_data["weather_risk"] = weather_data
        
        # Données catastrophes
        disaster_data = await disaster_service.get_disaster_risk_for_site(
            site.latitude, site.longitude, site.building_type, site.building_value
        )
        risk_data["disaster_risk"] = disaster_data
        
        # Données vulnérabilité
        vulnerability_data = await vulnerability_service.get_vulnerability_risk_for_site(
            site.latitude, site.longitude, site.building_type, site.building_value
        )
        risk_data["vulnerability_risk"] = vulnerability_data
        
        # Convertir le site en dictionnaire
        site_data = {
            "id": site.id,
            "name": site.name,
            "building_type": site.building_type,
            "building_value": site.building_value,
            "surface_area": site.surface_area,
            "risk_score": site.risk_score,
            "latitude": site.latitude,
            "longitude": site.longitude,
            "city": site.city,
            "construction_year": site.construction_year
        }
        
        # Analyser la mitigation avec l'agent IA
        mitigation = await ai_agent_service.analyze_risk_mitigation(site_data, risk_data)
        
        return RiskMitigationResponse(
            success=True,
            mitigation=mitigation,
            site_data=site_data,
            risk_data=risk_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de mitigation: {str(e)}")

@router.get("/health")
async def ai_agent_health():
    """Vérifier l'état de l'agent IA"""
    try:
        return {
            "status": "healthy",
            "ai_available": ai_agent_service.ai_available,
            "message": "Agent IA opérationnel"
        }
    except Exception as e:
        return {
            "status": "error",
            "ai_available": False,
            "message": f"Erreur agent IA: {str(e)}"
        }
