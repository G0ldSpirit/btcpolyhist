#!/usr/bin/env python3
"""
Bitcoin Up/Down Historical Scraper - MARCHÉS PASSÉS UNIQUEMENT
Récupère l'historique des marchés résolus pour analyser les séries
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuration
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
MONTHS = {
    1: "january", 2: "february", 3: "march", 4: "april",
    5: "may", 6: "june", 7: "july", 8: "august",
    9: "september", 10: "october", 11: "november", 12: "december"
}

def generate_slug(date, hour_str):
    """Génère le slug Polymarket"""
    month_name = MONTHS[date.month]
    day = date.day
    return f"bitcoin-up-or-down-{month_name}-{day}-{hour_str}-et"

def get_market_by_slug(slug):
    """Récupère les informations d'un marché via l'API Gamma"""
    url = f"{GAMMA_API_BASE}/markets?slug={slug}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
        return data[0] if isinstance(data, list) else data
    except requests.RequestException:
        return None

def generate_hours_list():
    """Génère la liste des heures (12AM, 1AM, ..., 11PM)"""
    hours = []
    for h in range(24):
        if h == 0:
            hours.append("12am")
        elif h < 12:
            hours.append(f"{h}am")
        elif h == 12:
            hours.append("12pm")
        else:
            hours.append(f"{h-12}pm")
    return hours

def extract_result(market_data, debug=False):
    """Extrait le résultat d'un marché fermé"""
    if not market_data.get("closed", False):
        return None

    outcome_prices = market_data.get("outcomePrices", [])
    outcomes = market_data.get("outcomes", [])

    # ✅ FIX CRITIQUE: Parser les strings JSON en listes
    if isinstance(outcome_prices, str):
        try:
            outcome_prices = json.loads(outcome_prices)
        except:
            return None

    if isinstance(outcomes, str):
        try:
            outcomes = json.loads(outcomes)
        except:
            return None

    if debug:
        print(f"    DEBUG: closed={market_data.get('closed')}")
        print(f"    DEBUG APRÈS PARSING:")
        print(f"    DEBUG: outcomes={outcomes} (type: {type(outcomes)})")
        print(f"    DEBUG: outcome_prices={outcome_prices} (type: {type(outcome_prices)})")
        if len(outcome_prices) >= 2:
            print(f"    DEBUG: outcome_prices[0]={outcome_prices[0]} (type: {type(outcome_prices[0])})")
            print(f"    DEBUG: outcome_prices[0] == '1' ? {outcome_prices[0] == '1'}")

    if len(outcome_prices) >= 2 and len(outcomes) >= 2:
        if outcome_prices[0] == "1":
            return f"{outcomes[0]} ✅"
        elif outcome_prices[1] == "1":
            return f"{outcomes[1]} ✅"
    return None

def scrape_historical_markets(days_back=7):
    """
    Scrape UNIQUEMENT les marchés PASSÉS (résolus)

    Args:
        days_back: Nombre de jours dans le passé (défaut: 7 jours)

    Returns:
        Liste de marchés résolus avec leurs résultats
    """
    markets = []
    hours_list = generate_hours_list()

    # Scanner uniquement dans le PASSÉ
    today = datetime.now()
    start_date = today - timedelta(days=days_back)
    end_date = today  # Jusqu'à aujourd'hui inclus (pour avoir les dernières heures)

    print(f"🔍 Scan de l'HISTORIQUE des marchés Bitcoin Up/Down")
    print(f"📅 Période: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")
    print(f"⏰ {days_back} jours × {len(hours_list)} heures = {days_back * len(hours_list)} marchés potentiels\n")

    total_found = 0
    total_resolved = 0
    debug_shown = False  # Pour afficher le debug une seule fois

    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"\n📅 {date_str}...")

        day_resolved = 0

        for hour_str in hours_list:
            slug = generate_slug(current_date, hour_str)
            market_data = get_market_by_slug(slug)

            if market_data:
                # Extraire le résultat (avec debug pour le premier marché fermé)
                is_closed = market_data.get("closed", False)
                enable_debug = is_closed and not debug_shown
                result = extract_result(market_data, debug=enable_debug)
                if enable_debug:
                    debug_shown = True

                market_info = {
                    "slug": slug,
                    "date": date_str,
                    "time": hour_str,
                    "condition_id": market_data.get("conditionId", ""),
                    "question": market_data.get("question", ""),
                    "closed": market_data.get("closed", False),
                    "result": result,
                    "clob_token_ids": market_data.get("clobTokenIds", []),
                    "volume": market_data.get("volume", "0"),
                    "outcomes": market_data.get("outcomes", []),
                    "outcome_prices": market_data.get("outcomePrices", [])
                }

                markets.append(market_info)
                total_found += 1

                # Afficher uniquement si résolu avec résultat
                if market_info["closed"] and result:
                    print(f"   ✅ {hour_str}: {result}")
                    day_resolved += 1
                    total_resolved += 1

            time.sleep(0.1)

        if day_resolved > 0:
            print(f"   → {day_resolved} marchés résolus ce jour")

        current_date += timedelta(days=1)

    print(f"\n✅ Scan terminé: {total_found} marchés trouvés")
    print(f"📊 Marchés résolus avec résultat: {total_resolved}")

    return markets

def calculate_stats(markets):
    """Calcule les statistiques sur les marchés résolus"""
    resolved_with_results = [m for m in markets if m.get('closed') and m.get('result')]

    if not resolved_with_results:
        print("\n⚠️  Aucun marché résolu avec résultat trouvé")
        return None

    # Trier par date et heure
    resolved_with_results.sort(key=lambda m: (m['date'], m['time']))

    # Compter UP vs DOWN
    up_count = sum(1 for m in resolved_with_results if 'Up' in m.get('result', ''))
    down_count = sum(1 for m in resolved_with_results if 'Down' in m.get('result', ''))

    # Analyser les séries
    current_streak = 0
    current_type = None
    max_up_streak = 0
    max_down_streak = 0
    temp_up_streak = 0
    temp_down_streak = 0

    for market in resolved_with_results:
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

    total = len(resolved_with_results)

    return {
        "total_resolved": total,
        "up_count": up_count,
        "down_count": down_count,
        "current_streak": current_streak,
        "current_type": current_type,
        "max_up_streak": max_up_streak,
        "max_down_streak": max_down_streak,
        "up_percentage": round(up_count / total * 100, 1) if total > 0 else 0.0,
        "down_percentage": round(down_count / total * 100, 1) if total > 0 else 0.0
    }

def save_historical_data(markets, stats, filename="btc_history.json"):
    """Sauvegarde l'historique et les stats"""
    # Trier par date et heure
    markets.sort(key=lambda m: (m['date'], m['time']))

    data = {
        "last_update": datetime.now().isoformat(),
        "markets": markets,
        "stats": stats
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Historique sauvegardé dans {filename}")

def display_stats(stats):
    """Affiche les statistiques"""
    if not stats:
        return

    print(f"\n" + "="*60)
    print("📊 STATISTIQUES DE L'HISTORIQUE")
    print("="*60)
    print(f"Total marchés résolus: {stats['total_resolved']}")
    print(f"\n🟢 UP: {stats['up_count']} ({stats['up_percentage']}%)")
    print(f"🔴 DOWN: {stats['down_count']} ({stats['down_percentage']}%)")
    print(f"\n🎯 Série actuelle: {stats['current_streak']} × {stats['current_type']}")
    print(f"📈 Record UP: {stats['max_up_streak']}")
    print(f"📉 Record DOWN: {stats['max_down_streak']}")
    print("="*60)

def main():
    print("=" * 60)
    print("📜 BITCOIN UP/DOWN - SCRAPER HISTORIQUE")
    print("=" * 60)
    print()

    # Demander combien de jours d'historique
    try:
        days_input = input("Combien de jours d'historique voulez-vous scanner ? (défaut: 7): ").strip()
        days_back = int(days_input) if days_input else 7
    except ValueError:
        days_back = 7

    print(f"\n🔍 Scan de {days_back} jours d'historique...\n")

    # Scanner l'historique
    markets = scrape_historical_markets(days_back=days_back)

    # Calculer les stats
    stats = calculate_stats(markets)

    # Afficher les stats
    display_stats(stats)

    # Sauvegarder
    save_historical_data(markets, stats)

    print("\n✅ Terminé ! Vous pouvez maintenant utiliser le dashboard pour visualiser l'historique.")
    print("   Le fichier btc_history.json contient toutes les données.")

if __name__ == "__main__":
    main()
