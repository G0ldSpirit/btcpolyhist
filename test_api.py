#!/usr/bin/env python3
"""
Script de test pour vérifier ce que l'API Gamma retourne
"""

import requests
import json

# Tester avec un marché récent
slug = "bitcoin-up-or-down-december-30-12pm-et"
url = f"https://gamma-api.polymarket.com/markets?slug={slug}"

print(f"🔍 Test API Gamma")
print(f"URL: {url}")
print(f"Slug: {slug}\n")

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data:
        market = data[0] if isinstance(data, list) else data

        print("✅ Réponse reçue:")
        print(json.dumps(market, indent=2))

        print("\n" + "="*60)
        print("📊 Informations importantes:")
        print(f"Question: {market.get('question', 'N/A')}")
        print(f"Closed: {market.get('closed', 'N/A')}")
        print(f"Condition ID: {market.get('conditionId', 'N/A')}")
        print(f"\nClob Token IDs: {market.get('clobTokenIds', 'N/A')}")
        print(f"Tokens (autre format): {market.get('tokens', 'N/A')}")

        # Chercher tous les champs contenant "token"
        print("\n🔍 Tous les champs contenant 'token':")
        for key, value in market.items():
            if 'token' in key.lower():
                print(f"  {key}: {value}")
    else:
        print("❌ Aucune donnée retournée")

except Exception as e:
    print(f"❌ Erreur: {e}")
