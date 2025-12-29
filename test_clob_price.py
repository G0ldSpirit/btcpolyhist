#!/usr/bin/env python3
"""
Script de test pour vérifier si on peut récupérer les prix CLOB
"""

import requests
import json

# Token ID UP du marché December 30, 12PM ET
token_id = "51624178524108904446726756803451891577804212205372703886513751733655325600146"

url = f"https://clob.polymarket.com/book?token_id={token_id}"

print(f"🔍 Test API CLOB")
print(f"URL: {url}")
print(f"Token ID: {token_id[:20]}...\n")

try:
    response = requests.get(url, timeout=5)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("✅ Réponse reçue:")
        print(json.dumps(data, indent=2))

        if data.get('bids') and len(data['bids']) > 0:
            best_bid = data['bids'][0]
            print(f"\n✅ Prix trouvé: {float(best_bid['price']):.3f}")
        else:
            print("\n⚠️  Pas de bids (ordres d'achat) - Marché sans liquidité")

    elif response.status_code == 404:
        print("❌ 404 Not Found - Token ID non trouvé dans le CLOB")
        print("\nCauses possibles:")
        print("  1. Marché trop récent (pas encore actif sur CLOB)")
        print("  2. Marché fermé (retiré du CLOB)")
        print("  3. Token ID invalide")

    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erreur: {e}")
