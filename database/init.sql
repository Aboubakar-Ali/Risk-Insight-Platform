-- Script d'initialisation de la base de données Risk Insight Platform

-- Créer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "postgis"; -- Commenté car non disponible dans l'image de base

-- Créer les types enum personnalisés
DO $$ BEGIN
    CREATE TYPE building_type AS ENUM (
        'office', 'warehouse', 'factory', 'retail', 
        'residential', 'hospital', 'school', 'other'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE contract_status AS ENUM (
        'draft', 'active', 'expired', 'cancelled'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE disaster_type AS ENUM (
        'flood', 'earthquake', 'storm', 'wildfire', 
        'landslide', 'volcano', 'other'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Créer les tables (si elles n'existent pas déjà)
-- Les tables seront créées automatiquement par SQLAlchemy

-- Insérer des données de test (optionnel)
-- INSERT INTO sites (name, address, city, postal_code, country, latitude, longitude, building_type, building_value) 
-- VALUES 
--     ('Siège Social Paris', '123 Avenue des Champs-Élysées', 'Paris', '75008', 'France', 48.8566, 2.3522, 'office', 5000000),
--     ('Entrepôt Lyon', '456 Rue de la Soie', 'Lyon', '69001', 'France', 45.7578, 4.8320, 'warehouse', 2000000),
--     ('Usine Marseille', '789 Boulevard de la Mer', 'Marseille', '13001', 'France', 43.2965, 5.3698, 'factory', 8000000);

-- Créer des index pour optimiser les performances
-- Ces index seront créés automatiquement par SQLAlchemy

-- Créer des vues utiles (optionnel)
CREATE OR REPLACE VIEW sites_with_risk AS
SELECT 
    s.id,
    s.name,
    s.city,
    s.building_type,
    s.building_value,
    s.risk_score,
    s.last_risk_update,
    COUNT(c.id) as contract_count,
    COALESCE(SUM(c.premium_amount), 0) as total_premiums
FROM sites s
LEFT JOIN insurance_contracts c ON s.id = c.site_id
GROUP BY s.id, s.name, s.city, s.building_type, s.building_value, s.risk_score, s.last_risk_update;

-- Créer des fonctions utiles (optionnel)
CREATE OR REPLACE FUNCTION calculate_distance(lat1 float, lon1 float, lat2 float, lon2 float)
RETURNS float AS $$
BEGIN
    RETURN 6371 * acos(
        cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon2) - radians(lon1)) +
        sin(radians(lat1)) * sin(radians(lat2))
    );
END;
$$ LANGUAGE plpgsql;

-- Créer des triggers pour la maintenance automatique (optionnel)
-- Ces triggers peuvent être ajoutés plus tard selon les besoins

-- Donner les permissions appropriées
GRANT ALL PRIVILEGES ON DATABASE risk_insight TO risk_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO risk_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO risk_user; 