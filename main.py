from pokmemon import PokemonData
import requests

urls = {
    "pokemon": "https://pokeapi.co/api/v2/pokemon/",
    "evolution": "https://pokeapi.co/api/v2/evolution-chain/",
    "move": "https://pokeapi.co/api/v2/move/",
    "BatleStyle" : "https://pokeapi.co/api/v2/move-battle-style"
}

pokelist = []

for key, url in urls.items():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(key, "OK")
        else:
            print(key, "NOT OK")
    except requests.RequestException as e:
        print("Failed to use the URL:", url, "\n\nError:", e)

