import requests
import mariadb
import time

root_url = 'https://swapi.dev/api/'


def get_obj_urls(obj):
    """ Return a list url pointing to a specific object. The Argument obj can be
    species , species  ..."""
    r = requests.get(root_url + obj)
    count = r.json().get("count")
    urls = []
    for index in range(1, count + 1):
        urls.append(root_url + obj + "/" + str(index))
    return urls


def get_id_and_link(url):
    """Get the id of a given url. e.g. https://swapi.dev/api/species /1/ should return 1"""
    return url.strip("/").split("/")[-1], url


def complete_with_none(obj_list, length):
    """If the length of the given list is less than the given length, then comple the list with a tuple of None"""
    if length > len(obj_list):
        return obj_list + ([(None, None)] * (length - len(obj_list)))
    return obj_list


def add_specie_associated_data(table_name, obj_id, obj_id_name, obj_link, obj_link_name, cursor):
    """Add Records to the satellite classes of species """
    statement = "INSERT INTO  " + table_name + " (  " + obj_id_name + ", " + obj_link_name + ") Values (%s, %s)"
    data = (obj_id, obj_link)
    if obj_id is not None:
        cursor.execute(statement, data)


def add_specie_data(request_response, specie_url, specie_person_id, specie_film_id, cursor):
    """ Add specie records into the table species . See file star_wars.sql for more information. """
    statement = f"INSERT INTO species  (specie_id, specie_person_id, specie_film_id, name, " \
                f"classification, designation, average_height," \
                " average_lifespan, eye_colors, hair_colors, skin_colors, language," \
                " homeworld,  created, edited, url) " \
                "Values  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (get_id_and_link(specie_url)[0],
            specie_person_id,
            specie_film_id,
            request_response.get("name"),
            request_response.get("classification"),
            request_response.get("designation"),
            request_response.get("average_height"),
            request_response.get("average_lifespan"),
            request_response.get("eye_colors"),
            request_response.get("hair_colors"),
            request_response.get("skin_colors"),
            request_response.get("language"),
            request_response.get("homeworld"),
            request_response.get("created"),
            request_response.get("edited"),
            request_response.get("url"))
    cursor.execute(statement, data)


def get_intern_links(url):
    """For a given url (url associated with id), add each key response of type in a new list with the name of the
    key. """
    r = requests.get(url)
    response = r.json()
    tmp_films_links = []
    tmp_people_links = []

    if response.get("films") is not None:
        for link in response.get("films"):
            tmp_films_links.append(get_id_and_link(link))

    if response.get("people") is not None:
        for link in response.get("people"):
            tmp_people_links.append(get_id_and_link(link))

    max_length = max(len(tmp_people_links), len(tmp_films_links))
    films_links = complete_with_none(tmp_films_links, max_length)
    people_links = complete_with_none(tmp_people_links, max_length)
    return films_links, people_links, response


def load_all_data():
    """Load at once data into species , species _film, species _specy, species _specie, species _specie"""
    try:
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': 3306,
            'database': 'start_wars_db'
        }
        connection = mariadb.connect(**config)
        cursor = connection.cursor()
        for url in get_obj_urls("species"):
            interner_objs = get_intern_links(url)
            films_links = interner_objs[0]
            people_links = interner_objs[1]
            response = interner_objs[2]

            for index in range(0, len(films_links)):
                add_specie_data(response, url, people_links[index][0], films_links[index][0], cursor)
                add_specie_associated_data("specie_film", films_links[index][0], "specie_film_id",
                                           films_links[index][1],
                                           "link",
                                           cursor)
                add_specie_associated_data("specie_person", people_links[index][0], "specie_person_id",
                                           people_links[index][1],
                                           "link",
                                           cursor)

        connection.commit()
        cursor.close()
        connection.close()
        print("Successfully added entry to database --> species  Tables")
    except Exception as e:
        print(f"error adding entry to database: {e}")


if __name__ == '__main__':
    load_all_data()
