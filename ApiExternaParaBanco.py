from ConectaBanco import ConexãoBanco
import mysql.connector
import requests
from random import choice


banco = ConexãoBanco()


urls = {
    "pokemon": "https://pokeapi.co/api/v2/pokemon/",
    "move": "https://pokeapi.co/api/v2/move/",
}


pokelist = []
movelist = []
habilidade_id =[]


def make_request(urls):
    for key, url in urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"conection realized with the URL {url}")
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

def insertHabilidades(cursor, movelist, habilidade_id):
    
    for move in movelist:
        selectMove = "SELECT skills FROM habilidades WHERE skills = %s;"
        cursor.execute(selectMove, (move,))
        movesExists = cursor.fetchall()
        if any(move == moveinList[0] for moveinList in movesExists):
            print(f"Move {move} já existe")
        else:
            insertMove = "INSERT INTO habilidades (skills) VALUES (%s);"
            cursor.execute(insertMove, (move,))
            print(f"Move {move} inserido")

        cursor.execute("SELECT id FROM pokemon.habilidades;")
        habilidades = cursor.fetchall()


    for habilidade in habilidades:
        habilidade_id.append(habilidade[0])
    return habilidade_id


def insertPokemons(cursor, pokelist, habilidade_id):
    for pokemon in pokelist:
        habilidadeAleatoria = choice(habilidade_id)
        selectPokemon = "SELECT nome FROM pokemon.t_pokemon WHERE nome = %s;"
        cursor.execute(selectPokemon, (pokemon, ))
        pokemonsExists = cursor.fetchall()
        if any(pokemon == pokemoninList[0] for pokemoninList in pokemonsExists):
            print(f"Pokemon {pokemon} já existe")
        else:
            insertPokemon = "INSERT INTO pokemon.t_pokemon (nome, habilidade_id) VALUES (%s, %s);"
            cursor.execute(insertPokemon, (pokemon, habilidadeAleatoria, ))
            print(f"Pokemon {pokemon} inserido com a habilidade {habilidadeAleatoria}")
            


def conectDatabase(movelist, pokelist, habilidade_id):
    conexao = mysql.connector.connect(
        host=banco.host,
        user=banco.user,
        password=banco.password,
        database=banco.database
    )
    
    conexao.autocommit = False

    try:
        cursor = conexao.cursor()
        habilidade_id = insertHabilidades(cursor, movelist, habilidade_id)
        insertPokemons(cursor, pokelist, habilidade_id)
        conexao.commit()









    except mysql.connector.Error as e:
        print("Could not connect to the database., erro: ", e)
        conexao.rollback()

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Database connection closed.")
        


    
    
    

if __name__ == "__main__":
    make_request(urls)
    conectDatabase(pokelist, movelist, habilidade_id)