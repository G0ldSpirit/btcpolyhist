# 🚀 Démarrage Rapide - Bitcoin Market Tracker

## Installation (1 minute)

```bash
# Cloner le repo
git clone <url-du-repo>
cd btcpolyhist

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation (3 clics)

### Windows

1. **Double-cliquez sur** `START_DASHBOARD.bat`
2. Le système se lance automatiquement
3. Le dashboard s'ouvre dans votre navigateur

### Linux/Mac

```bash
# Rendre les scripts exécutables (première fois seulement)
chmod +x *.sh

# Lancer le système complet
./start_dashboard.sh
```

## C'est tout ! 🎉

Le système va :
1. ✅ Récupérer ~100-120 marchés Bitcoin (si première utilisation)
2. ✅ Lancer le tracker temps réel (mise à jour toutes les 30s)
3. ✅ Ouvrir le dashboard dans votre navigateur

## Ce que vous allez voir

### Dashboard

- **Série actuelle** : Combien de UP ou DOWN consécutifs en ce moment
- **Statistiques** : Total résolus, % UP/DOWN, records
- **Liste des marchés** : Tous les marchés avec leurs résultats ou prix en temps réel

### Exemple de données

```
Série actuelle: 🟢 5 x UP

Statistiques:
- Total résolus: 42 marchés
- UP: 23 (54.8%)
- DOWN: 19 (45.2%)
- Record UP: 5
- Record DOWN: 4
```

## Commandes Manuelles (optionnel)

Si vous préférez lancer les composants séparément :

### 1. Scanner les marchés (une fois par jour)

```bash
# Windows
RUN_COMPLETE_SCRAPER.bat

# Linux/Mac
python3 final_complete_scraper.py
```

### 2. Lancer le tracker

```bash
# Windows
RUN_TRACKER.bat

# Linux/Mac
python3 realtime_tracker.py
```

### 3. Ouvrir le dashboard

Double-cliquez sur `dashboard.html` ou ouvrez-le dans votre navigateur.

## Arrêter le système

- **Windows** : Fermez la fenêtre du tracker
- **Linux/Mac** : Appuyez sur `Ctrl+C` dans le terminal

## Fichiers Générés

Après le premier lancement, vous verrez ces fichiers :

- `btc_markets_complete.json` : Tous les marchés scrapés
- `btc_tracker_state.json` : État en temps réel (marchés + stats)

**Note** : Ces fichiers sont dans `.gitignore` et ne seront pas committés.

## Besoin d'aide ?

Consultez `README_COMPLET.md` pour :
- Architecture technique détaillée
- Explications des APIs Polymarket
- Personnalisation avancée
- Résolution de problèmes

## Prérequis

- Python 3.7+
- Module `requests` (installé via requirements.txt)
- Connexion Internet

## FAQ Ultra-Rapide

**Q: Aucun marché affiché ?**
R: Attendez 3-5 secondes que le tracker génère le fichier JSON

**Q: Stats = null ?**
R: Normal si aucun marché résolu encore. Attendez qu'une heure passe.

**Q: "Pas de liquidité" sur marchés actifs ?**
R: Les nouveaux marchés mettent 5-10 min à avoir des ordres. Patience !

**Q: Le tracker plante ?**
R: Vérifiez votre connexion Internet et relancez.

---

**C'est parti ! 🚀**
