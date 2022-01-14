import requests
import mariadb
import time

root_url = 'https://swapi.dev/api/'


def get_obj_urls(obj):
    """ Return a list url pointing to a specific object. The Argument obj can be
    starships, starships ..."""
    r = requests.get(root_url + obj)
    count = r.json().get("count")
    urls = []
    for index in range(1, count + 1):
        urls.append(root_url + obj + "/" + str(index))
    return urls


def get_id_and_link(url):
    """Get the id of a given url. e.g. https://swapi.dev/api/starships/1/ should return 1"""
    return url.strip("/").split("/")[-1], url


def complete_with_none(obj_list, length):
    """If the length of the given list is less than the given length, then comple the list with a tuple of None"""
    if length > len(obj_list):
        return obj_list + ([(None, None)] * (length - len(obj_list)))
    return obj_list


def add_starship_associated_data(table_name, obj_id, obj_id_name, obj_link, obj_link_name, cursor):
    """Add Records to the satellite classes of starships"""
    statement = "INSERT INTO  " + table_name + " (  " + obj_id_name + ", " + obj_link_name + ") Values (%s, %s)"
    data = (obj_id, obj_link)
    if obj_id is not None:
        cursor.execute(statement, data)


def add_starship_data(request_response, starship_url, starship_pilot_id, starship_film_id, cursor):
    """ Add starship records into the table starships. See file star_wars.sql for more information. """
    statement = f"INSERT INTO starships (starship_id, starship_pilot_id, starship_film_id, name, " \
                f"model, manufacturer, cost_in_credits," \
                " length, max_atmosphering_speed, crew, passengers, cargo_capacity," \
                " consumables, hyperdrive_rating, MGLT, starship_class, created, edited, url) " \
                "Values (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (get_id_and_link(starship_url)[0],
            starship_pilot_id,
            starship_film_id,
            request_response.get("name"),
            request_response.get("model"),
            request_response.get("manufacturer"),
            request_response.get("cost_in_credits"),
            request_response.get("length"),
            request_response.get("max_atmosphering_speed"),
            request_response.get("crew"),
            request_response.get("passengers"),
            request_response.get("cargo_capacity"),
            request_response.get("consumables"),
            request_response.get("hyperdrive_rating"),
            request_response.get("MGLT"),
            request_response.get("starship_class"),
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
    tmp_pilots_links = []

    if response.get("films") is not None:
        for link in response.get("films"):
            tmp_films_links.append(get_id_and_link(link))

    if response.get("pilots") is not None:
        for link in response.get("pilots"):
            tmp_pilots_links.append(get_id_and_link(link))

    max_length = max(len(tmp_pilots_links), len(tmp_films_links))
    films_links = complete_with_none(tmp_films_links, max_length)
    pilots_links = complete_with_none(tmp_pilots_links, max_length)
    return films_links, pilots_links, response


def load_all_data():
    """Load at once data into starships, starships_film, starships_specy, starships_vehicle, starships_starship"""
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
        for url in get_obj_urls("starships"):
            interner_objs = get_intern_links(url)
            films_links = interner_objs[0]
            pilots_links = interner_objs[1]
            response = interner_objs[2]

            for index in range(0, len(films_links)):
                add_starship_data(response, url, pilots_links[index][0], films_links[index][0],  cursor)
                add_starship_associated_data("starship_film", films_links[index][0], "starship_film_id",
                                             films_links[index][1],
                                             "link",
                                             cursor)
                add_starship_associated_data("starship_pilot", pilots_links[index][0], "starship_pilot_id",
                                             pilots_links[index][1],
                                             "link",
                                             cursor)

        connection.commit()
        cursor.close()
        connection.close()
        print("Successfully added entry to database --> starships Tables")
    except Exception as e:
        print(f"error adding entry to database: {e}")


if __name__ == '__main__':
    load_all_data()
