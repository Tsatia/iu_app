import requests
import mariadb
import time

root_url = 'https://swapi.dev/api/'


def get_obj_urls(obj):
    """ Return a list url pointing to a specific object. The Argument obj can be
    planets , planets  ..."""
    r = requests.get(root_url + obj)
    count = r.json().get("count")
    urls = []
    for index in range(1, count + 1):
        urls.append(root_url + obj + "/" + str(index))
    return urls


def get_id_and_link(url):
    """Get the id of a given url. e.g. https://swapi.dev/api/planets /1/ should return 1"""
    return url.strip("/").split("/")[-1], url


def complete_with_none(obj_list, length):
    """If the length of the given list is less than the given length, then comple the list with a tuple of None"""
    if length > len(obj_list):
        return obj_list + ([(None, None)] * (length - len(obj_list)))
    return obj_list


def add_planet_associated_data(table_name, obj_id, obj_id_name, obj_link, obj_link_name, cursor):
    """Add Records to the satellite classes of planets """
    statement = "INSERT INTO  " + table_name + " (  " + obj_id_name + ", " + obj_link_name + ") Values (%s, %s)"
    data = (obj_id, obj_link)
    if obj_id is not None:
        cursor.execute(statement, data)


def add_planet_data(request_response, planet_url, planet_resident_id, planet_film_id, cursor):
    """ Add planet records into the table planets . See file star_wars.sql for more information. """
    statement = f"INSERT INTO planets  (planet_id, planet_resident_id, planet_film_id, name, " \
                f"diameter, rotation_period, orbital_period," \
                " gravity, population, climate, terrain, surface_water," \
                " created, edited, url) " \
                "Values  ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (get_id_and_link(planet_url)[0],
            planet_resident_id,
            planet_film_id,
            request_response.get("name"),
            request_response.get("diameter"),
            request_response.get("rotation_period"),
            request_response.get("orbital_period"),
            request_response.get("gravity"),
            request_response.get("population"),
            request_response.get("climate"),
            request_response.get("terrain"),
            request_response.get("surface_water"),
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
    tmp_residents_links = []

    if response.get("films") is not None:
        for link in response.get("films"):
            tmp_films_links.append(get_id_and_link(link))

    if response.get("residents") is not None:
        for link in response.get("residents"):
            tmp_residents_links.append(get_id_and_link(link))

    max_length = max(len(tmp_residents_links), len(tmp_films_links))
    films_links = complete_with_none(tmp_films_links, max_length)
    residents_links = complete_with_none(tmp_residents_links, max_length)
    return films_links, residents_links, response


def load_all_data():
    """Load at once data into planets , planets _film, planets _specy, planets _planet, planets _planet"""
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
        for url in get_obj_urls("planets"):
            interner_objs = get_intern_links(url)
            films_links = interner_objs[0]
            residents_links = interner_objs[1]
            response = interner_objs[2]

            for index in range(0, len(films_links)):
                add_planet_data(response, url, residents_links[index][0], films_links[index][0], cursor)
                add_planet_associated_data("planet_film", films_links[index][0], "planet_film_id",
                                           films_links[index][1],
                                           "link",
                                           cursor)
                add_planet_associated_data("planet_resident", residents_links[index][0], "planet_resident_id",
                                           residents_links[index][1],
                                           "link",
                                           cursor)

        connection.commit()
        cursor.close()
        connection.close()
        print("Successfully added entry to database --> planets  Tables")
    except Exception as e:
        print(f"error adding entry to database: {e}")


if __name__ == '__main__':
    load_all_data()
