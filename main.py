import mysql.connector
import requests
from ConectaBanco import ConexãoBanco


banco = ConexãoBanco()


urls = {
    "pokemon": "https://pokeapi.co/api/v2/pokemon/",
    "move": "https://pokeapi.co/api/v2/move/",
}


pokelist = []
movelist = []


for key, url in urls.items():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Conexão realizada com a URL {url}")
            if key == "pokemon":
                for pokemon in response.json()["results"]:
                    pokelist.append(pokemon["name"])  
            elif key == "move":
                for move in response.json()["results"]:
                    movelist.append(move["name"])
        else:
            print(key, "NOT OK")
    except requests.RequestException as e:
        print("Failed to use the URL:", url, "\n\nError:", e)


try:
    conexao = mysql.connector.connect(
        host=banco.host,
        user=banco.user,
        password=banco.password,
        database=banco.database
    )
    
    conexao.autocommit = False
    cursor = conexao.cursor()
    
    for pokemon in pokelist:
        select = "INSERT INTO pokemon.t_pokemon (nome) VALUES (%s);"
        cursor.execute(select, (pokemon,))
        print(f"Inserted {pokemon}")

    conexao.commit()
    
except mysql.connector.Error as e:
    print("Não foi possível se conectar, erro: ", e)
    conexao.rollback()

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão com o banco de dados encerrada.")
