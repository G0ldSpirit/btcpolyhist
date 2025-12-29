#!/bin/bash

echo "========================================"
echo " BITCOIN TRACKER - LANCEMENT COMPLET"
echo "========================================"
echo ""

# Vérifier si btc_markets_complete.json existe
if [ ! -f "btc_markets_complete.json" ]; then
    echo "Première utilisation - Récupération des marchés..."
    python3 final_complete_scraper.py
    echo ""
fi

# Lancer le tracker en arrière-plan
echo "Démarrage du tracker temps réel..."
python3 realtime_tracker.py &
TRACKER_PID=$!

# Attendre 3 secondes pour que le tracker génère le fichier JSON
sleep 3

# Ouvrir le dashboard
echo "Ouverture du dashboard..."
if command -v xdg-open > /dev/null; then
    xdg-open dashboard.html
elif command -v open > /dev/null; then
    open dashboard.html
else
    echo "Veuillez ouvrir dashboard.html manuellement dans votre navigateur"
fi

echo ""
echo "========================================"
echo " SYSTEME LANCE !"
echo "========================================"
echo ""
echo "- Tracker PID: $TRACKER_PID (mise à jour toutes les 30s)"
echo "- Dashboard: Ouvert dans votre navigateur"
echo ""
echo "Pour arrêter le tracker: kill $TRACKER_PID"
echo ""
echo "Appuyez sur Entrée pour arrêter le tracker et fermer..."
read

# Arrêter le tracker
kill $TRACKER_PID 2>/dev/null
echo "Tracker arrêté."
