from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import random
import csv
import io

from app.core.database import get_db
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse
from app.models.site import Site, BuildingType

router = APIRouter()

@router.get("/", response_model=List[SiteResponse])
async def get_sites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer tous les sites"""
    sites = db.query(Site).offset(skip).limit(limit).all()
    return sites

@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(site_id: int, db: Session = Depends(get_db)):
    """Récupérer un site par son ID"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    return site

@router.post("/", response_model=SiteResponse)
async def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    """Créer un nouveau site"""
    from app.services.weather_service import weather_service
    
    db_site = Site(**site.dict())
    
    try:
        # Calculer le score de risque basé sur la météo réelle
        weather_risk = await weather_service.get_weather_risk_for_site(
            site.latitude, 
            site.longitude
        )
        db_site.risk_score = weather_risk["risk_score"]
    except Exception as e:
        print(f"Erreur lors du calcul du risque météo: {e}")
        # Fallback vers un score aléatoire si l'API météo échoue
        db_site.risk_score = random.uniform(10, 80)
    
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(
    site_id: int,
    site_update: SiteUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un site"""
    db_site = db.query(Site).filter(Site.id == site_id).first()
    if not db_site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    update_data = site_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_site, field, value)
    
    db.commit()
    db.refresh(db_site)
    return db_site

@router.delete("/{site_id}")
async def delete_site(site_id: int, db: Session = Depends(get_db)):
    """Supprimer un site"""
    db_site = db.query(Site).filter(Site.id == site_id).first()
    if not db_site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site non trouvé"
        )
    
    db.delete(db_site)
    db.commit()
    return {"message": "Site supprimé avec succès"}

@router.post("/import-csv")
async def import_sites_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Importer des sites depuis un fichier CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être au format CSV"
        )
    
    try:
        # Lire le contenu du fichier
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parser le CSV
        csv_reader = csv.DictReader(io.StringIO(content_str))
        
        imported_sites = []
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):  # start=2 car l'en-tête est ligne 1
            try:
                # Valider et convertir les données
                building_type_str = row['building_type'].strip()
                # Convertir le string en enum BuildingType
                try:
                    building_type_enum = BuildingType(building_type_str)
                except ValueError:
                    errors.append(f"Ligne {row_num}: Type de bâtiment invalide '{building_type_str}'")
                    continue
                
                site_data = {
                    'name': row['name'].strip(),
                    'address': row['address'].strip(),
                    'city': row['city'].strip(),
                    'postal_code': row['postal_code'].strip(),
                    'country': row.get('country', 'France').strip(),
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'building_type': building_type_enum,
                    'building_value': float(row['building_value']),
                    'surface_area': float(row['surface_area']) if row['surface_area'] else None,
                    'construction_year': int(row['construction_year']) if row['construction_year'] else None,
                    'notes': row.get('notes', '').strip()
                }
                
                # Créer le site
                db_site = Site(**site_data)
                
                # Calculer le score de risque basé sur la météo réelle
                try:
                    from app.services.weather_service import weather_service
                    weather_risk = await weather_service.get_weather_risk_for_site(
                        site_data['latitude'], 
                        site_data['longitude']
                    )
                    db_site.risk_score = weather_risk["risk_score"]
                except Exception as e:
                    print(f"Erreur lors du calcul du risque météo pour {site_data['name']}: {e}")
                    # Fallback vers un score aléatoire si l'API météo échoue
                    db_site.risk_score = random.uniform(10, 80)
                
                db.add(db_site)
                imported_sites.append(site_data['name'])
                
            except (ValueError, KeyError) as e:
                errors.append(f"Ligne {row_num}: {str(e)}")
                continue
        
        # Commiter tous les sites valides
        if imported_sites:
            db.commit()
        
        return {
            "message": f"Import terminé",
            "imported_count": len(imported_sites),
            "imported_sites": imported_sites,
            "errors": errors
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'import: {str(e)}"
        ) 