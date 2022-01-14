from typing import List, Dict
from flask import Flask
import mariadb
import json

app = Flask(__name__)


def name_description() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': 3306,
        'database': 'start_wars_db'
    }

    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT film_id, link FROM films inner join film_characters ON films.film_character_id = film_characters.film_character_id')
    results = [{person_id: person_film_id} for (person_id, person_film_id) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'name_description': name_description()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
