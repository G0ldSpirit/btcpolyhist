# 📊 Bitcoin Up/Down Market Tracker

> Système complet pour tracker et analyser les marchés horaires "Bitcoin Up or Down" sur Polymarket

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)

## 🎯 Qu'est-ce que c'est ?

Un tracker en temps réel des marchés Bitcoin horaires sur Polymarket qui :

- 📈 **Récupère automatiquement** tous les marchés BTC Up/Down
- 🔄 **Suit les prix** en temps réel (toutes les 30s)
- 📊 **Calcule les séries** (streaks) de résultats consécutifs
- 🎨 **Affiche un dashboard** web élégant avec statistiques

## ⚡ Démarrage Ultra-Rapide

```bash
# Installation
pip install -r requirements.txt

# Lancement (Windows)
START_DASHBOARD.bat

# Lancement (Linux/Mac)
./start_dashboard.sh
```

**C'est tout !** Le dashboard s'ouvre automatiquement dans votre navigateur.

📖 [Guide de démarrage détaillé →](QUICKSTART.md)

## 🖼️ Aperçu

Le dashboard affiche :

```
┌─────────────────────────────────────┐
│      Série Actuelle                 │
│      🟢 5 x UP consécutifs          │
└─────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total: 42    │ UP: 23 (55%) │ DOWN: 19     │ Record: 5    │
└──────────────┴──────────────┴──────────────┴──────────────┘

📈 Liste des marchés avec prix temps réel et résultats
```

## ✨ Fonctionnalités

- ✅ **Scraper intelligent** : Récupère 100+ marchés via API Polymarket
- ✅ **Tracking temps réel** : Prix UP/DOWN mis à jour automatiquement
- ✅ **Analyse de séries** : Détecte les patterns de résultats consécutifs
- ✅ **Dashboard responsive** : Interface web moderne
- ✅ **Persistance complète** : Conservation de tous les marchés résolus
- ✅ **Multi-plateforme** : Windows (.bat) + Linux/Mac (.sh)

## 🔧 Corrections Appliquées

Ce projet inclut les corrections critiques pour le bug `stats: null` :

1. ✅ Conservation de TOUS les marchés (pas seulement les 50 premiers)
2. ✅ Les marchés résolus ne sont plus perdus entre iterations
3. ✅ Calcul des stats sur l'ensemble complet des données
4. ✅ Gestion robuste du cas "aucun marché résolu"
5. ✅ Dashboard ne crash plus si stats vide

## 📁 Structure du Projet

```
btcpolyhist/
├── final_complete_scraper.py    # Scraper des marchés (API Gamma)
├── realtime_tracker.py           # Tracker temps réel (API CLOB)
├── dashboard.html                # Interface web
├── requirements.txt              # Dépendances Python
├── START_DASHBOARD.bat           # Lancement auto (Windows)
├── start_dashboard.sh            # Lancement auto (Linux/Mac)
├── README.md                     # Ce fichier
├── QUICKSTART.md                 # Guide de démarrage rapide
└── README_COMPLET.md             # Documentation technique complète
```

## 🚀 Utilisation

### Option 1 : Lancement Automatique (Recommandé)

**Windows :**
```bash
START_DASHBOARD.bat
```

**Linux/Mac :**
```bash
./start_dashboard.sh
```

### Option 2 : Lancement Manuel

```bash
# 1. Scanner les marchés (une fois par jour)
python final_complete_scraper.py

# 2. Lancer le tracker temps réel
python realtime_tracker.py

# 3. Ouvrir dashboard.html dans votre navigateur
```

## 📊 Données Affichées

### Série Actuelle
- Nombre de UP ou DOWN consécutifs en ce moment
- Indication visuelle (🟢 pour UP, 🔴 pour DOWN)

### Statistiques
- Total de marchés résolus
- Pourcentage UP vs DOWN
- Records de séries maximales
- Nombre de résultats par type

### Marchés
- Liste complète avec date/heure
- Prix temps réel pour marchés actifs
- Résultats finaux pour marchés fermés
- Volume et liquidité

## 🔑 APIs Utilisées

- **Polymarket Gamma API** : Récupération des métadonnées des marchés
- **Polymarket CLOB API** : Récupération des prix en temps réel

Aucune authentification requise, APIs publiques.

## 📖 Documentation

- [🚀 QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide (3 minutes)
- [📚 README_COMPLET.md](README_COMPLET.md) - Documentation technique complète
  - Architecture détaillée
  - Explication des APIs
  - Personnalisation avancée
  - Résolution de problèmes
  - Roadmap et améliorations futures

## 🐛 Résolution de Problèmes

| Problème | Solution |
|----------|----------|
| Stats = null | Normal si aucun marché résolu. Attendez une heure. |
| Pas de liquidité | Les nouveaux marchés mettent 5-10 min. Patience. |
| Erreur API | Vérifiez votre connexion Internet. |
| Dashboard vide | Attendez 3-5s que le tracker génère le JSON. |

📖 [Guide complet de troubleshooting →](README_COMPLET.md#-problèmes-connus-et-solutions)

## 🛠️ Prérequis

- Python 3.7 ou supérieur
- Module `requests` (installé via requirements.txt)
- Connexion Internet

## 🤝 Support

Pour toute question :

1. Consultez [QUICKSTART.md](QUICKSTART.md) pour le guide de démarrage
2. Lisez [README_COMPLET.md](README_COMPLET.md) pour les détails techniques
3. Vérifiez la section "Résolution de Problèmes" ci-dessus

## 📜 License

Ce projet est à usage éducatif et personnel. Les données proviennent de Polymarket et sont soumises à leurs conditions d'utilisation.

## 🎓 Contexte

Ce projet a été créé pour :
- Apprendre à utiliser les APIs Polymarket
- Analyser les patterns de marchés prédictifs Bitcoin
- Pratiquer le web scraping et data analysis en Python
- Créer un dashboard temps réel avec HTML/CSS/JavaScript

---

**Créé avec ❤️ pour tracker les marchés Bitcoin sur Polymarket**

[⬆ Retour en haut](#-bitcoin-updown-market-tracker)
