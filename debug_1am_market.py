#!/usr/bin/env python3
"""
Test pour vérifier le marché December 30, 1AM ET spécifiquement
"""

import requests
import json

slug = "bitcoin-up-or-down-december-30-1am-et"
url = f"https://gamma-api.polymarket.com/markets?slug={slug}"

print(f"🔍 Vérification du marché: {slug}\n")

try:
    response = requests.get(url, timeout=10)
    data = response.json()

    if data:
        market = data[0] if isinstance(data, list) else data

        print("📊 Données brutes de l'API:")
        print(f"Question: {market.get('question')}")
        print(f"Closed: {market.get('closed')}")
        print(f"Outcomes: {market.get('outcomes')}")
        print(f"Outcome Prices: {market.get('outcomePrices')}")

        outcomes = market.get('outcomes', [])
        outcome_prices = market.get('outcomePrices', [])

        # Parser si c'est une string
        if isinstance(outcomes, str):
            outcomes = json.loads(outcomes)
        if isinstance(outcome_prices, str):
            outcome_prices = json.loads(outcome_prices)

        print(f"\n📋 Après parsing:")
        print(f"Outcomes: {outcomes}")
        print(f"Outcome Prices: {outcome_prices}")

        print(f"\n🎯 Logique d'extraction:")
        print(f"outcome_prices[0] ({outcome_prices[0]}) == '1' ? {outcome_prices[0] == '1'}")
        print(f"outcome_prices[1] ({outcome_prices[1]}) == '1' ? {outcome_prices[1] == '1'}")

        if outcome_prices[0] == "1":
            print(f"\n✅ Résultat: {outcomes[0]} ✅")
        elif outcome_prices[1] == "1":
            print(f"\n✅ Résultat: {outcomes[1]} ✅")
        else:
            print(f"\n❌ Aucun prix = '1' trouvé!")

except Exception as e:
    print(f"❌ Erreur: {e}")
