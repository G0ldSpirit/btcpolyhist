#!/usr/bin/env python3
"""
Bitcoin Up/Down Market Scraper - VERSION ACTIVE MARKETS ONLY
Récupère UNIQUEMENT les marchés actifs (aujourd'hui + demain)
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
    except requests.RequestException as e:
        print(f"❌ Erreur API pour {slug}: {e}")
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

def extract_result(market_data):
    """Extrait le résultat d'un marché fermé"""
    if not market_data.get("closed", False):
        return None

    outcome_prices = market_data.get("outcomePrices", [])
    outcomes = market_data.get("outcomes", [])

    if len(outcome_prices) >= 2 and len(outcomes) >= 2:
        if outcome_prices[0] == "1":
            return f"{outcomes[0]} ✅"
        elif outcome_prices[1] == "1":
            return f"{outcomes[1]} ✅"
    return None

def scrape_active_markets():
    """
    Scrape UNIQUEMENT les marchés actifs (aujourd'hui + 2 jours futurs)
    Ces marchés ont de la liquidité sur le CLOB
    """
    markets = []
    hours_list = generate_hours_list()

    # Scanner aujourd'hui + 2 jours futurs (marchés avec liquidité)
    today = datetime.now()

    print(f"🔍 Scan des marchés ACTIFS")
    print(f"📊 Période: Aujourd'hui + 2 jours futurs")
    print(f"⏰ {len(hours_list)} heures par jour = {3 * len(hours_list)} marchés potentiels\n")

    total_found = 0

    for day_offset in range(3):  # 0 = aujourd'hui, 1 = demain, 2 = après-demain
        current_date = today + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")

        day_label = "Aujourd'hui" if day_offset == 0 else f"J+{day_offset}"
        print(f"\n📅 {day_label} ({date_str})...")

        for hour_str in hours_list:
            slug = generate_slug(current_date, hour_str)
            market_data = get_market_by_slug(slug)

            if market_data:
                market_info = {
                    "slug": slug,
                    "date": date_str,
                    "time": hour_str,
                    "condition_id": market_data.get("conditionId", ""),
                    "question": market_data.get("question", ""),
                    "closed": market_data.get("closed", False),
                    "result": extract_result(market_data),
                    "clob_token_ids": market_data.get("clobTokenIds", []),
                    "volume": market_data.get("volume", "0"),
                    "outcomes": str(market_data.get("outcomes", [])),
                    "outcome_prices": str(market_data.get("outcomePrices", []))
                }

                markets.append(market_info)
                total_found += 1

                status = "✅ Résolu" if market_info["closed"] else "⏳ Actif"
                result_str = f" - {market_info['result']}" if market_info["result"] else ""
                print(f"   ✓ {hour_str}: {status}{result_str}")

            time.sleep(0.1)

    print(f"\n✅ Scan terminé: {total_found} marchés actifs trouvés")
    return markets

def save_markets(markets, filename="btc_markets_complete.json"):
    """Sauvegarde les marchés"""
    markets.sort(key=lambda m: (m['date'], m['time']))

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(markets, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Données sauvegardées dans {filename}")

    # Statistiques
    resolved = sum(1 for m in markets if m['closed'])
    active = len(markets) - resolved

    print(f"\n📊 Statistiques:")
    print(f"   Total: {len(markets)} marchés")
    print(f"   Résolus: {resolved}")
    print(f"   Actifs: {active}")

    if resolved > 0:
        up_count = sum(1 for m in markets if m.get('result') and m.get('result').startswith('Up'))
        down_count = sum(1 for m in markets if m.get('result') and m.get('result').startswith('Down'))
        print(f"\n   Résultats:")
        print(f"   🟢 Up: {up_count} ({up_count/resolved*100:.1f}%)")
        print(f"   🔴 Down: {down_count} ({down_count/resolved*100:.1f}%)")

def main():
    print("=" * 60)
    print("🔍 BITCOIN MARKET SCRAPER - MARCHÉS ACTIFS SEULEMENT")
    print("=" * 60)
    print()

    markets = scrape_active_markets()

    if markets:
        save_markets(markets)
        print("\n✅ Scraping terminé avec succès!")
        print("\n💡 Ces marchés ont de la liquidité sur le CLOB")
        print("   Le tracker pourra récupérer leurs prix en temps réel")
    else:
        print("\n❌ Aucun marché trouvé")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
