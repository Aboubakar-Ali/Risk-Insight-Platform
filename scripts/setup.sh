#!/bin/bash

echo "🚀 Configuration de Risk Insight Platform..."

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Copier le fichier d'environnement
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp env.example .env
    echo "✅ Fichier .env créé. Veuillez configurer vos variables d'environnement."
fi

# Construire et démarrer les services
echo "🔨 Construction des images Docker..."
docker-compose build

echo "🚀 Démarrage des services..."
docker-compose up -d

echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier que les services sont démarrés
echo "🔍 Vérification des services..."

if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend démarré avec succès"
else
    echo "❌ Erreur lors du démarrage du backend"
fi

if curl -f http://localhost:3000 &> /dev/null; then
    echo "✅ Frontend démarré avec succès"
else
    echo "❌ Erreur lors du démarrage du frontend"
fi

echo ""
echo "🎉 Risk Insight Platform est prêt !"
echo ""
echo "📱 Accès aux services :"
echo "   - Frontend : http://localhost:3000"
echo "   - Backend API : http://localhost:8000"
echo "   - Documentation API : http://localhost:8000/docs"
echo ""
echo "📚 Documentation :"
echo "   - Architecture : ./docs/architecture.md"
echo "   - Guide d'installation : ./docs/installation.md"
echo ""
echo "🔧 Commandes utiles :"
echo "   - Arrêter les services : docker-compose down"
echo "   - Voir les logs : docker-compose logs -f"
echo "   - Redémarrer : docker-compose restart" 