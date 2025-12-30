#!/usr/bin/env python3
"""
Test pour vérifier ce qu'un marché fermé retourne vraiment
"""

import requests
import json
from datetime import datetime, timedelta

GAMMA_API_BASE = "https://gamma-api.polymarket.com"

# Tester avec hier
yesterday = datetime.now() - timedelta(days=1)
month_name = {12: "december", 11: "november", 10: "october"}[yesterday.month]

# Test avec plusieurs heures d'hier
test_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"]

print("🔍 Test des marchés d'HIER pour voir les résultats\n")

for hour in test_hours:
    slug = f"bitcoin-up-or-down-{month_name}-{yesterday.day}-{hour}-et"
    url = f"{GAMMA_API_BASE}/markets?slug={slug}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                market = data[0] if isinstance(data, list) else data

                closed = market.get("closed", False)
                outcomes = market.get("outcomes", [])
                outcome_prices = market.get("outcomePrices", [])

                print(f"✅ {hour}:")
                print(f"   Closed: {closed}")
                print(f"   Outcomes: {outcomes}")
                print(f"   Outcome Prices: {outcome_prices}")

                if closed and len(outcome_prices) >= 2:
                    if outcome_prices[0] == "1":
                        print(f"   Résultat: {outcomes[0]} ✅")
                    elif outcome_prices[1] == "1":
                        print(f"   Résultat: {outcomes[1]} ✅")
                    else:
                        print(f"   ⚠️  Aucun prix = '1'")
                else:
                    print(f"   ⚠️  Marché pas fermé ou pas de prix")
                print()
    except Exception as e:
        print(f"❌ {hour}: Erreur {e}\n")
