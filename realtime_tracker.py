#!/usr/bin/env python3
"""
Bitcoin Up/Down Market Tracker - Temps Réel
Suit les prix en temps réel et calcule les statistiques de séries

🔧 CORRECTIONS APPLIQUÉES:
- ✅ Conserve TOUS les marchés (pas seulement les 50 premiers)
- ✅ Ne perd plus les marchés résolus entre iterations
- ✅ Calcule les stats sur l'ensemble complet
- ✅ analyze_streaks retourne toujours un objet stats valide
"""

import requests
import json
from datetime import datetime
import time
import os

# Configuration
CLOB_API_BASE = "https://clob.polymarket.com"
MARKETS_FILE = "btc_markets_complete.json"
STATE_FILE = "btc_tracker_state.json"

def get_price_from_clob(token_id):
    """
    Récupère le prix d'un outcome via l'API CLOB
    Args:
        token_id: Le clobTokenId de l'outcome
    Returns:
        float: Prix entre 0 et 1, ou None si erreur
    """
    url = f"{CLOB_API_BASE}/book?token_id={token_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Récupérer le meilleur bid (prix d'achat)
        if data.get('bids') and len(data['bids']) > 0:
            best_bid = data['bids'][0]
            return float(best_bid['price'])

        return None

    except Exception as e:
        print(f"   ⚠️  Erreur prix token {token_id[:10]}...: {e}")
        return None

def update_market_prices(market):
    """
    Met à jour les prix UP et DOWN d'un marché actif
    Args:
        market: Dict contenant les infos du marché
    Returns:
        Dict: Marché avec prix mis à jour
    """
    clob_token_ids = market.get('clob_token_ids', [])

    if len(clob_token_ids) < 2:
        market['up_price'] = None
        market['down_price'] = None
        market['last_price_update'] = None
        return market

    # clobTokenIds[0] = UP, clobTokenIds[1] = DOWN
    up_price = get_price_from_clob(clob_token_ids[0])
    down_price = get_price_from_clob(clob_token_ids[1])

    market['up_price'] = up_price
    market['down_price'] = down_price
    market['last_price_update'] = datetime.now().isoformat()

    return market

def analyze_streaks(markets):
    """
    Analyse les séries de résultats UP/DOWN

    🔧 CORRECTION CRITIQUE: Retourne TOUJOURS un objet stats valide,
    même s'il n'y a aucun marché résolu

    Args:
        markets: Liste de tous les marchés (résolus + actifs)
    Returns:
        Dict: Statistiques des séries (jamais None)
    """
    # Filtrer seulement les marchés résolus
    resolved = [m for m in markets if m.get('closed', False) and m.get('result')]

    # ✅ CORRECTION: Toujours retourner un objet stats
    if not resolved:
        return {
            "total_resolved": 0,
            "up_count": 0,
            "down_count": 0,
            "current_streak": 0,
            "current_type": None,
            "max_up_streak": 0,
            "max_down_streak": 0,
            "up_percentage": 0.0,
            "down_percentage": 0.0
        }

    # Trier par date et heure
    resolved.sort(key=lambda m: (m['date'], m['time']))

    # Compter UP vs DOWN
    up_count = sum(1 for m in resolved if 'Up' in m.get('result', ''))
    down_count = sum(1 for m in resolved if 'Down' in m.get('result', ''))

    # Analyser les séries
    current_streak = 0
    current_type = None
    max_up_streak = 0
    max_down_streak = 0
    temp_up_streak = 0
    temp_down_streak = 0

    for market in resolved:
        result = market.get('result', '')

        if 'Up' in result:
            temp_up_streak += 1
            temp_down_streak = 0
            current_type = 'UP'
            current_streak = temp_up_streak
        elif 'Down' in result:
            temp_down_streak += 1
            temp_up_streak = 0
            current_type = 'DOWN'
            current_streak = temp_down_streak

        max_up_streak = max(max_up_streak, temp_up_streak)
        max_down_streak = max(max_down_streak, temp_down_streak)

    total = len(resolved)
    up_pct = (up_count / total * 100) if total > 0 else 0.0
    down_pct = (down_count / total * 100) if total > 0 else 0.0

    return {
        "total_resolved": total,
        "up_count": up_count,
        "down_count": down_count,
        "current_streak": current_streak,
        "current_type": current_type,
        "max_up_streak": max_up_streak,
        "max_down_streak": max_down_streak,
        "up_percentage": round(up_pct, 1),
        "down_percentage": round(down_pct, 1)
    }

def load_markets():
    """
    Charge les marchés depuis le fichier JSON
    Returns:
        List: Liste de tous les marchés
    """
    if not os.path.exists(MARKETS_FILE):
        print(f"❌ Fichier {MARKETS_FILE} non trouvé!")
        print(f"   Exécutez d'abord: python final_complete_scraper.py")
        return []

    try:
        with open(MARKETS_FILE, 'r', encoding='utf-8') as f:
            markets = json.load(f)
        print(f"✅ {len(markets)} marchés chargés depuis {MARKETS_FILE}")
        return markets
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return []

def save_state(markets, stats):
    """
    Sauvegarde l'état actuel (marchés + stats) dans un fichier JSON
    """
    state = {
        "last_update": datetime.now().isoformat(),
        "markets": markets,
        "stats": stats
    }

    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"💾 État sauvegardé dans {STATE_FILE}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")

def track_markets(markets, interval=30):
    """
    🔧 FONCTION CORRIGÉE - Boucle principale du tracker

    CORRECTIONS APPLIQUÉES:
    1. ✅ Traite TOUS les marchés (pas seulement 50)
    2. ✅ Conserve les marchés résolus tels quels
    3. ✅ Met à jour uniquement les marchés actifs
    4. ✅ Calcule les stats sur l'ensemble complet

    Args:
        markets: Liste complète des marchés
        interval: Intervalle entre les mises à jour (secondes)
    """
    print(f"\n🚀 Démarrage du tracker temps réel")
    print(f"   Intervalle: {interval}s")
    print(f"   Total marchés: {len(markets)}")

    iteration = 0

    try:
        while True:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Itération #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")

            # ✅ CORRECTION: Conserver TOUS les marchés
            updated_markets = []

            resolved_count = 0
            active_count = 0
            updated_count = 0

            # ✅ CORRECTION: Traiter TOUS les marchés (pas juste 50)
            for market in markets:
                if market.get('closed'):
                    # ✅ CORRECTION: Garder les marchés résolus tels quels
                    updated_markets.append(market)
                    resolved_count += 1
                else:
                    # Mettre à jour les marchés actifs
                    active_count += 1
                    updated_market = update_market_prices(market)
                    updated_markets.append(updated_market)

                    # Afficher les prix
                    if updated_market.get('up_price') is not None:
                        up = updated_market['up_price']
                        down = updated_market['down_price'] or 0
                        print(f"   📊 {market['time']}: UP {up:.3f} | DOWN {down:.3f}")
                        updated_count += 1
                    else:
                        print(f"   ⏳ {market['time']}: Pas de liquidité")

            # ✅ CORRECTION: Utiliser la liste complète pour les stats
            markets = updated_markets

            # ✅ CORRECTION: Calculer stats sur TOUS les marchés
            stats = analyze_streaks(markets)

            print(f"\n📊 Résumé:")
            print(f"   Total marchés: {len(markets)}")
            print(f"   Résolus: {resolved_count}")
            print(f"   Actifs: {active_count}")
            print(f"   Prix mis à jour: {updated_count}")

            if stats and stats['total_resolved'] > 0:
                print(f"\n🎯 Statistiques de séries:")
                print(f"   Série actuelle: {stats['current_streak']} x {stats['current_type']}")
                print(f"   Record UP: {stats['max_up_streak']}")
                print(f"   Record DOWN: {stats['max_down_streak']}")
                print(f"   UP: {stats['up_count']} ({stats['up_percentage']}%)")
                print(f"   DOWN: {stats['down_count']} ({stats['down_percentage']}%)")

            # Sauvegarder l'état complet
            save_state(markets, stats)

            print(f"\n⏳ Prochaine mise à jour dans {interval}s...")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt du tracker (Ctrl+C)")
        print(f"   {iteration} itérations effectuées")
        save_state(markets, analyze_streaks(markets))
        print("\n✅ État final sauvegardé")

def main():
    """
    Point d'entrée principal
    """
    print("=" * 60)
    print("📊 BITCOIN UP/DOWN TRACKER - TEMPS RÉEL")
    print("=" * 60)
    print()

    # Charger tous les marchés
    markets = load_markets()

    if not markets:
        print("\n❌ Impossible de démarrer sans marchés")
        print("   1. Exécutez: python final_complete_scraper.py")
        print("   2. Puis relancez ce tracker")
        return

    # Statistiques initiales
    resolved = sum(1 for m in markets if m.get('closed'))
    active = len(markets) - resolved

    print(f"\n📈 État initial:")
    print(f"   Total: {len(markets)} marchés")
    print(f"   Résolus: {resolved}")
    print(f"   Actifs: {active}")

    # Calculer les stats initiales
    initial_stats = analyze_streaks(markets)
    if initial_stats['total_resolved'] > 0:
        print(f"\n🎯 Séries:")
        print(f"   Actuelle: {initial_stats['current_streak']} x {initial_stats['current_type']}")
        print(f"   Record UP: {initial_stats['max_up_streak']}")
        print(f"   Record DOWN: {initial_stats['max_down_streak']}")

    # Démarrer le tracking
    track_markets(markets, interval=30)

if __name__ == "__main__":
    main()
