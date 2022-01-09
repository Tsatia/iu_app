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
        'database': 'iu_test_db'
    }
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM iu_test')
    results = [{name: description} for (name, description) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'name_description': name_description()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
