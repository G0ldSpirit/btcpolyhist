# 📊 Bitcoin Up/Down Market Tracker - Polymarket

Système complet pour tracker les marchés horaires "Bitcoin Up or Down" sur Polymarket avec statistiques de séries en temps réel.

## 🎯 Fonctionnalités

- ✅ **Scraping automatique** : Récupère tous les marchés BTC horaires via API Polymarket
- ✅ **Tracking temps réel** : Suit les prix UP/DOWN toutes les 30 secondes
- ✅ **Analyse de séries** : Calcule les streaks (séries consécutives) de UP/DOWN
- ✅ **Dashboard web** : Interface visuelle élégante avec statistiques
- ✅ **Persistance des données** : Conservation de tous les marchés résolus

## 🔧 Corrections Appliquées

Ce projet inclut les corrections suivantes pour résoudre le bug `stats: null` :

1. ✅ **Conserve TOUS les marchés** (pas seulement les 50 premiers)
2. ✅ **Ne perd plus les marchés résolus** entre les itérations
3. ✅ **Calcule les stats sur l'ensemble complet** (résolus + actifs)
4. ✅ **analyze_streaks retourne toujours un objet stats valide** (jamais `null`)
5. ✅ **Dashboard gère le cas stats null** sans crash

## 📁 Structure du Projet

```
btcpolyhist/
├── final_complete_scraper.py    # Scraper des marchés (API Gamma)
├── realtime_tracker.py           # Tracker temps réel (API CLOB)
├── dashboard.html                # Interface web
├── btc_markets_complete.json     # Données des marchés (généré)
├── btc_tracker_state.json        # État en temps réel (généré)
├── RUN_COMPLETE_SCRAPER.bat      # Lance le scraper
├── RUN_TRACKER.bat               # Lance le tracker
├── START_DASHBOARD.bat           # Lance tout automatiquement
└── README_COMPLET.md             # Documentation
```

## 🚀 Installation

### Prérequis

- Python 3.7+
- Module `requests`

```bash
pip install requests
```

## 📖 Utilisation

### Méthode 1 : Lancement Automatique (Windows)

Double-cliquez sur `START_DASHBOARD.bat`

Cela va :
1. Scanner les marchés (si première utilisation)
2. Lancer le tracker en arrière-plan
3. Ouvrir le dashboard dans votre navigateur

### Méthode 2 : Lancement Manuel

#### Étape 1 : Scanner les marchés (une fois par jour)

```bash
python final_complete_scraper.py
```

ou double-cliquez sur `RUN_COMPLETE_SCRAPER.bat`

**Ce que ça fait :**
- Récupère ~100-120 marchés (3 jours passés + aujourd'hui + 1 jour futur)
- Sauvegarde dans `btc_markets_complete.json`
- Affiche les statistiques de scan

**Durée :** ~30-60 secondes

#### Étape 2 : Lancer le tracker temps réel

```bash
python realtime_tracker.py
```

ou double-cliquez sur `RUN_TRACKER.bat`

**Ce que ça fait :**
- Charge tous les marchés de `btc_markets_complete.json`
- Met à jour les prix des marchés actifs toutes les 30s
- Calcule les statistiques de séries
- Sauvegarde l'état dans `btc_tracker_state.json`

**Arrêt :** Ctrl+C

#### Étape 3 : Ouvrir le dashboard

Ouvrez `dashboard.html` dans votre navigateur

**Ce que ça affiche :**
- Série actuelle (grande carte)
- Statistiques (4 cartes)
- Liste de tous les marchés
- Auto-refresh optionnel (décommenter dans le code)

## 🔑 Architecture Technique

### API Polymarket

Le système utilise 2 APIs différentes :

#### 1. API Gamma (récupération des marchés)

```
GET https://gamma-api.polymarket.com/markets?slug={slug}
```

**Retourne :**
- `conditionId` : ID unique du marché
- `clobTokenIds` : Array de 2 token IDs (UP et DOWN)
- `question` : Texte de la question
- `closed` : true/false
- `outcomePrices` : Prix finaux si résolu
- `volume` : Volume total

**Format des slugs :**
```
bitcoin-up-or-down-{month}-{day}-{hour}{am/pm}-et

Exemples:
- bitcoin-up-or-down-december-29-4pm-et
- bitcoin-up-or-down-december-28-11am-et
```

#### 2. API CLOB (prix en temps réel)

```
GET https://clob.polymarket.com/book?token_id={clob_token_id}
```

**Retourne :**
- `bids` : Ordres d'achat (prix réel)
- `asks` : Ordres de vente

**Important :**
- Chaque marché a 2 tokens : `clobTokenIds[0]` = UP, `clobTokenIds[1]` = DOWN
- Il faut 2 appels CLOB par marché pour avoir UP et DOWN

### Structure des Données

#### btc_markets_complete.json

```json
[
  {
    "slug": "bitcoin-up-or-down-december-29-9am-et",
    "date": "2025-12-29",
    "time": "9am",
    "condition_id": "0x875ac6ab...",
    "question": "Bitcoin Up or Down - December 29, 9AM ET",
    "closed": true,
    "result": "Up ✅",
    "clob_token_ids": [
      "32335030373487383042649098981612262759652263219845507081122077665830223113679",
      "115679681161201379691123057461457097804093363865171898940922153203649155991314"
    ],
    "volume": "199462.67787",
    "outcomes": "['Up', 'Down']",
    "outcome_prices": "['1', '0']"
  }
]
```

#### btc_tracker_state.json

```json
{
  "last_update": "2025-12-29T23:00:00",
  "markets": [...],
  "stats": {
    "total_resolved": 40,
    "up_count": 22,
    "down_count": 18,
    "current_streak": 3,
    "current_type": "UP",
    "max_up_streak": 5,
    "max_down_streak": 4,
    "up_percentage": 55.0,
    "down_percentage": 45.0
  }
}
```

## 🐛 Problèmes Connus et Solutions

### 1. "stats": null dans btc_tracker_state.json

**Cause :** Aucun marché résolu encore

**Solution :** Attendre qu'au moins un marché horaire soit fermé. Les marchés ferment automatiquement chaque heure.

**Fix appliqué :**
- `analyze_streaks()` retourne toujours un objet stats valide
- Dashboard affiche un message d'attente si stats vide

### 2. Marchés actifs sans prix

**Symptôme :** "Pas de liquidité" sur marchés récents

**Cause :** Les nouveaux marchés mettent 5-10 min à avoir des ordres

**Solution :** Attendre ou relancer le tracker plus tard

### 3. API Rate Limiting

**Symptôme :** Erreurs 429 ou timeouts

**Solution :** Le tracker a des délais de 0.1s entre appels. Si problème persiste, augmenter `time.sleep()` dans le code.

## 📊 Fonctions Importantes

### analyze_streaks(markets)

Calcule les statistiques de séries sur les marchés résolus.

**Corrections appliquées :**
- ✅ Retourne toujours un objet stats (jamais `None`)
- ✅ Gère le cas où aucun marché n'est résolu
- ✅ Trie chronologiquement avant analyse

### track_markets(markets, interval)

Boucle principale du tracker temps réel.

**Corrections appliquées :**
- ✅ Conserve TOUS les marchés entre itérations
- ✅ Ne perd plus les marchés résolus
- ✅ Met à jour uniquement les marchés actifs
- ✅ Calcule les stats sur l'ensemble complet

## 🎨 Personnalisation

### Changer l'intervalle de mise à jour

Dans `realtime_tracker.py` ligne finale :

```python
track_markets(markets, interval=30)  # Changer 30 en nombre de secondes voulu
```

### Activer l'auto-refresh du dashboard

Dans `dashboard.html`, décommenter la dernière ligne :

```javascript
// Auto-refresh toutes les 30 secondes (optionnel)
setInterval(loadData, 30000);  // Décommenter cette ligne
```

### Scanner plus de jours

Dans `final_complete_scraper.py` fonction `main()` :

```python
markets = scrape_markets(days_back=7, days_forward=2)  # 7 jours passés, 2 futurs
```

## 💡 Améliorations Futures

### Priorité Haute
- [ ] Auto-ajout des nouveaux marchés toutes les heures
- [ ] Notifications push quand série atteint un seuil
- [ ] Export CSV des résultats

### Priorité Moyenne
- [ ] Graphiques Chart.js pour visualiser les séries
- [ ] Mode sombre pour le dashboard
- [ ] Historique des prix (graphique temporel)

### Priorité Basse
- [ ] API REST pour accéder aux données
- [ ] Webhooks Discord/Telegram
- [ ] Machine Learning pour prédictions

## ⚠️ Limitations

1. **API Publique** : Pas d'authentification requise, mais rate limits possibles
2. **Marchés récents** : Les nouveaux marchés n'ont pas de liquidité immédiatement
3. **Horaire ET (Eastern Time)** : Les heures sont en fuseau horaire US
4. **Dépendance API** : Si Polymarket change sa structure, le code doit être adapté

## 🔐 Sécurité et Éthique

- ✅ Utilisation d'APIs publiques uniquement
- ✅ Pas de scraping HTML agressif
- ✅ Délais entre requêtes pour éviter surcharge
- ✅ Pas de trading automatique (lecture seule)

## 📝 Changelog

### Version 1.0 (2025-12-29)

**Corrections majeures :**
- ✅ Fix bug `stats: null` dans btc_tracker_state.json
- ✅ Conservation complète des marchés résolus
- ✅ Gestion robuste du cas sans marchés résolus
- ✅ Dashboard ne crash plus si stats vide

**Fonctionnalités :**
- ✅ Scraper complet avec API Gamma
- ✅ Tracker temps réel avec API CLOB
- ✅ Dashboard responsive
- ✅ Calcul des séries UP/DOWN
- ✅ Fichiers batch pour lancement facile

## 🤝 Support

Pour toute question ou problème :

1. Vérifier que `requests` est installé : `pip install requests`
2. Vérifier que `btc_markets_complete.json` existe (lancer le scraper)
3. Vérifier les logs du tracker pour erreurs API
4. Ouvrir la console du navigateur (F12) pour erreurs dashboard

## 📜 License

Ce projet est à usage éducatif et personnel. Les données proviennent de Polymarket et sont soumises à leurs conditions d'utilisation.

---

**Créé avec ❤️ pour tracker les marchés Bitcoin sur Polymarket**
