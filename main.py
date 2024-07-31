import mysql.connector
import requests
from ConectaBanco import ConexãoBanco

banco = ConexãoBanco()

urls = {
    "pokemon": "https://pokeapi.co/api/v2/pokemon/",
    "evolution": "https://pokeapi.co/api/v2/evolution-chain/",
    "move": "https://pokeapi.co/api/v2/move/",
    "BatleStyle" : "https://pokeapi.co/api/v2/move-battle-style"
}


def AcessarJson():
    
    for key, url in urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Conexão realizada com a url {url}")
            else:
                print(key, "NOT OK")
        except requests.RequestException as e:
            print("Failed to use the URL:", url, "\n\nError:", e)

def startConnection():
    try:
        mydb = mysql.connector.connect(
            host = banco.host,
            user = banco.user,
            password = banco.password,
            database = banco.database
            )
        
        mydb.cursor()
        
    except Exception as e:
        print("Não foi possível se conectar, erro: ", e)


startConnection()
AcessarJson()