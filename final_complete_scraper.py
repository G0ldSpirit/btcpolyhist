#!/usr/bin/env python3
"""
Bitcoin Up/Down Market Scraper - Polymarket
Récupère les marchés horaires BTC avec leurs clobTokenIds via l'API Gamma
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
    """
    Génère le slug Polymarket pour un marché BTC Up/Down
    Format: bitcoin-up-or-down-{month}-{day}-{hour}{am/pm}-et
    """
    month_name = MONTHS[date.month]
    day = date.day
    return f"bitcoin-up-or-down-{month_name}-{day}-{hour_str}-et"

def get_market_by_slug(slug):
    """
    Récupère les informations d'un marché via l'API Gamma
    Retourne: dict avec condition_id, clobTokenIds, question, volume, etc.
    """
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
    """
    Génère la liste des heures au format Polymarket (12AM, 1AM, ..., 11PM)
    """
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

def scrape_markets(days_back=3, days_forward=1):
    """
    Scrape les marchés BTC Up/Down pour une période donnée
    Args:
        days_back: Nombre de jours dans le passé
        days_forward: Nombre de jours dans le futur
    Returns:
        Liste de marchés avec toutes leurs données
    """
    markets = []
    hours_list = generate_hours_list()

    # Générer les dates à scanner
    today = datetime.now()
    start_date = today - timedelta(days=days_back)
    end_date = today + timedelta(days=days_forward)

    print(f"🔍 Scan des marchés du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}")
    print(f"📊 Période: {days_back} jours passés + aujourd'hui + {days_forward} jour(s) futur(s)")
    print(f"⏰ {len(hours_list)} heures par jour = {(days_back + 1 + days_forward) * len(hours_list)} marchés potentiels\n")

    current_date = start_date
    total_found = 0
    total_checked = 0

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"\n📅 Scanning {date_str}...")

        for hour_str in hours_list:
            slug = generate_slug(current_date, hour_str)
            total_checked += 1

            # Progress indicator
            if total_checked % 10 == 0:
                print(f"   ... vérifié {total_checked} marchés ({total_found} trouvés)")

            market_data = get_market_by_slug(slug)

            if market_data:
                # Extraire les informations importantes
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
                    "outcomes": market_data.get("outcomes", []),
                    "outcome_prices": market_data.get("outcomePrices", [])
                }

                markets.append(market_info)
                total_found += 1

                status = "✅ Résolu" if market_info["closed"] else "⏳ En cours"
                result_str = f" - {market_info['result']}" if market_info["result"] else ""
                print(f"   ✓ {hour_str}: {status}{result_str}")

            # Petit délai pour éviter de surcharger l'API
            time.sleep(0.1)

        current_date += timedelta(days=1)

    print(f"\n✅ Scan terminé: {total_found} marchés trouvés sur {total_checked} vérifiés")
    return markets

def extract_result(market_data):
    """
    Extrait le résultat d'un marché fermé
    Retourne: "Up ✅", "Down ✅", ou None
    """
    if not market_data.get("closed", False):
        return None

    outcome_prices = market_data.get("outcomePrices", [])
    outcomes = market_data.get("outcomes", [])

    if len(outcome_prices) >= 2 and len(outcomes) >= 2:
        # Le prix "1" indique le résultat gagnant
        if outcome_prices[0] == "1":
            return f"{outcomes[0]} ✅"
        elif outcome_prices[1] == "1":
            return f"{outcomes[1]} ✅"

    return None

def save_markets(markets, filename="btc_markets_complete.json"):
    """
    Sauvegarde les marchés dans un fichier JSON
    """
    # Trier par date et heure
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
    """
    Point d'entrée principal
    """
    print("=" * 60)
    print("🔍 BITCOIN UP/DOWN MARKET SCRAPER - POLYMARKET")
    print("=" * 60)
    print()

    # Scanner 3 jours passés + aujourd'hui + 1 jour futur = ~120 marchés
    markets = scrape_markets(days_back=3, days_forward=1)

    if markets:
        save_markets(markets)
        print("\n✅ Scraping terminé avec succès!")
    else:
        print("\n❌ Aucun marché trouvé")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
