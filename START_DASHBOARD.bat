@echo off
echo ========================================
echo  BITCOIN TRACKER - LANCEMENT COMPLET
echo ========================================
echo.

REM Verifier si btc_markets_complete.json existe
if not exist "btc_markets_complete.json" (
    echo Premiere utilisation - Recuperation des marches...
    python final_complete_scraper.py
    echo.
)

REM Lancer le tracker en arriere-plan
echo Demarrage du tracker temps reel...
start "Bitcoin Tracker" python realtime_tracker.py

REM Attendre 3 secondes pour que le tracker genere le fichier JSON
timeout /t 3 /nobreak >nul

REM Ouvrir le dashboard
echo Ouverture du dashboard...
start "" dashboard.html

echo.
echo ========================================
echo  SYSTEME LANCE !
echo ========================================
echo.
echo - Tracker: Fenetre separee (mise a jour toutes les 30s)
echo - Dashboard: Ouvert dans votre navigateur
echo.
echo Pour arreter le tracker, fermez sa fenetre.
echo.
pause
