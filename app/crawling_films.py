import requests
import mariadb
import time

root_url = 'https://swapi.dev/api/'


def get_obj_urls(obj):
    """ Return a list url pointing to a specific object. The Argument obj can be
    people, starships ..."""
    r = requests.get(root_url + obj)
    count = r.json().get("count")
    urls = []
    for index in range(1, count + 1):
        urls.append(root_url + obj + "/" + str(index))
    return urls


def get_id_and_link(url):
    """Get the id of a given url. e.g. https://swapi.dev/api/people/1/ should return 1"""
    return url.strip("/").split("/")[-1], url


def complete_with_none(obj_list, length):
    """If the length of the given list is less than the given length, then comple the list with a tuple of None"""
    if length > len(obj_list):
        return obj_list + ([(None, None)] * (length - len(obj_list)))
    return obj_list


def add_film_associated_data(table_name, obj_id, obj_id_name, obj_link, obj_link_name, cursor):
    """Add Records to the satellite classes of People"""
    statement = "INSERT INTO  " + table_name + " (  " + obj_id_name + ", " + obj_link_name + ") Values (%s, %s)"
    data = (obj_id, obj_link)
    if obj_id is not None:
        cursor.execute(statement, data)


def add_film_data(request_response, film_url, film_character_id, film_planet_id, film_starship_id,
                  film_vehicle_id, film_specy_id, cursor):
    """ Add film records into the table people. See file star_wars.sql for more information. """
    statement = f"INSERT INTO films (film_id, film_character_id, film_planet_id, film_starship_id, " \
                f"film_vehicle_id, film_specy_id, title, episode_id," \
                " opening_crawl, director, producer, release_date," \
                " created, edited, url) " \
                "Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (get_id_and_link(film_url)[0],
            film_character_id,
            film_planet_id,
            film_starship_id,
            film_vehicle_id,
            film_specy_id,
            request_response.get("title"),
            request_response.get("episode_id"),
            request_response.get("opening_crawl"),
            request_response.get("director"),
            request_response.get("producer"),
            request_response.get("release_date"),
            request_response.get("created"),
            request_response.get("edited"),
            request_response.get("url"))
    cursor.execute(statement, data)


def get_intern_links(url):
    """For a given url (url associated with id), add each key response of type in a new list with the name of the
    key. """
    r = requests.get(url)
    response = r.json()
    tmp_characters_links = []
    tmp_planets_links = []
    tmp_species_links = []
    tmp_vehicles_links = []
    tmp_starships_links = []

    if response.get("characters") is not None:
        for link in response.get("characters"):
            tmp_characters_links.append(get_id_and_link(link))

    if response.get("planets") is not None:
        for link in response.get("planets"):
            tmp_planets_links.append(get_id_and_link(link))

    if response.get("vehicles") is not None:
        for link in response.get("vehicles"):
            tmp_vehicles_links.append(get_id_and_link(link))

    if response.get("starships") is not None:
        for link in response.get("starships"):
            tmp_starships_links.append(get_id_and_link(link))

    if response.get("species") is not None:
        for link in response.get("species"):
            tmp_species_links.append(get_id_and_link(link))

    max_length = max(len(tmp_starships_links), len(tmp_planets_links), len(tmp_characters_links),
                     len(tmp_vehicles_links), len(tmp_species_links))
    characters_links = complete_with_none(tmp_characters_links, max_length)
    planets_links = complete_with_none(tmp_planets_links, max_length)
    starships_links = complete_with_none(tmp_starships_links, max_length)
    vehicles_links = complete_with_none(tmp_vehicles_links, max_length)
    species_links = complete_with_none(tmp_species_links, max_length)
    return characters_links, planets_links, starships_links, vehicles_links, species_links, response


def load_all_data():
    """Load at once data into films, films_film, films_specy, films_vehicle, films_starship"""
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
        for url in get_obj_urls("films"):
            interner_objs = get_intern_links(url)
            characters_links = interner_objs[0]
            planets_links = interner_objs[1]
            starships_links = interner_objs[2]
            vehicles_links = interner_objs[3]
            species_links = interner_objs[4]
            response = interner_objs[5]
            for index in range(0, len(species_links)):
                add_film_data(response, url, characters_links[index][0], planets_links[index][0],
                              starships_links[index][0],
                              vehicles_links[index][0],
                              species_links[index][0],
                              cursor)
                add_film_associated_data("film_characters", characters_links[index][0], "film_character_id",
                                         characters_links[index][1],
                                         "link",
                                         cursor)
                add_film_associated_data("flm_planet", planets_links[index][0], "film_planet_id",
                                         planets_links[index][1],
                                         "link",
                                         cursor)
                add_film_associated_data("film_specy", species_links[index][0], "film_specy_id",
                                         species_links[index][1],
                                         "link",
                                         cursor)
                add_film_associated_data("film_vehicle", vehicles_links[index][0], "film_vehicle_id",
                                         vehicles_links[index][1],
                                         "link",
                                         cursor)
                add_film_associated_data("film_starship", starships_links[index][0], "film_starship_id",
                                         starships_links[index][1],
                                         "link",
                                         cursor)
        connection.commit()
        cursor.close()
        connection.close()
        print("Successfully added entries to databse --> Films Table ")
    except Exception as e:
        print(f"error adding entries to database: {e}")


if __name__ == '__main__':
    # time.sleep(50)  # wait for the server to start up
    load_all_data()
