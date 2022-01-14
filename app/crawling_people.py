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


def add_person_associated_data(table_name, obj_id, obj_id_name, obj_link, obj_link_name, cursor):
    """Add Records to the satellite classes of People"""
    statement = "INSERT INTO  " + table_name + " (  " + obj_id_name + ", " + obj_link_name + ") Values (%s, %s)"
    data = (obj_id, obj_link)
    if obj_id is not None:
        cursor.execute(statement, data)


def add_person_data(request_response, person_url, person_film_id, person_specy_id, person_vehicle_id,
                    person_starship_id, cursor):
    """ Add person records into the table people. See file star_wars.sql for more information. """
    statement = f"INSERT INTO people (person_id, person_film_id, person_specy_id, person_vehicle_id, " \
                f"person_starship_id, name, height," \
                " mass, hair_color, skin_color, eye_color, birth_year," \
                " gender, homeworld, created, edited, url) " \
                "Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (get_id_and_link(person_url)[0],
            person_film_id,
            person_specy_id,
            person_vehicle_id,
            person_starship_id,
            request_response.get("name"),
            request_response.get("height"),
            request_response.get("mass"),
            request_response.get("hair_color"),
            request_response.get("skin_color"),
            request_response.get("eye_color"),
            request_response.get("birth_year"),
            request_response.get("gender"),
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
    tmp_species_links = []
    tmp_vehicles_links = []
    tmp_starships_links = []

    if response.get("films") is not None:
        for link in response.get("films"):
            tmp_films_links.append(get_id_and_link(link))

    if response.get("species") is not None:
        for link in response.get("species"):
            tmp_species_links.append(get_id_and_link(link))

    if response.get("vehicles") is not None:
        for link in response.get("vehicles"):
            tmp_vehicles_links.append(get_id_and_link(link))

    if response.get("starships") is not None:
        for link in response.get("starships"):
            tmp_starships_links.append(get_id_and_link(link))

    max_length = max(len(tmp_starships_links), len(tmp_films_links), len(tmp_vehicles_links), len(tmp_species_links))
    films_links = complete_with_none(tmp_films_links, max_length)
    starships_links = complete_with_none(tmp_starships_links, max_length)
    vehicles_links = complete_with_none(tmp_vehicles_links, max_length)
    species_links = complete_with_none(tmp_species_links, max_length)
    return films_links, starships_links, vehicles_links, species_links, response



def load_all_data():
    """Load at once data into people, people_film, people_specy, people_vehicle, people_starship"""
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
        for url in get_obj_urls("people"):
            interner_objs = get_intern_links(url)
            films_links = interner_objs[0]
            starships_links = interner_objs[1]
            vehicles_links = interner_objs[2]
            species_links = interner_objs[3]
            response = interner_objs[4]
            for index in range(0, len(species_links)):
                add_person_data(response, url, films_links[index][0], species_links[index][0],
                                vehicles_links[index][0],
                                starships_links[index][0], cursor)
                add_person_associated_data("people_film", films_links[index][0], "person_film_id",
                                           films_links[index][1],
                                           "link",
                                           cursor)
                add_person_associated_data("people_specy", species_links[index][0], "person_specy_id",
                                           species_links[index][1],
                                           "link",
                                           cursor)
                add_person_associated_data("people_vehicle", vehicles_links[index][0], "person_vehicle_id",
                                           vehicles_links[index][1],
                                           "link",
                                           cursor)
                add_person_associated_data("people_starship", starships_links[index][0], "person_starship_id",
                                           starships_links[index][1],
                                           "link",
                                           cursor)
        connection.commit()
        cursor.close()
        connection.close()
        print("Successfully added entry to database --> People Tables")
    except Exception as e:
        print(f"error adding entry to database: {e}")


if __name__ == '__main__':
    print("Waiting for Server to start ...")
    time.sleep(40)  # wait for the server to start up
    load_all_data()
