from typing import List, Dict
import itertools
import flask
from flask import Flask, Response

import mariadb
import json

app = Flask(__name__)
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': 3306,
    'database': 'start_wars_db'
}


@app.route('/')
def index() -> dict:
    return {
        "films": "http://0.0.0.0:5000/films/",
        "people": "http://0.0.0.0:5000/people/",
        "planets": "http://0.0.0.0:5000/planets/",
        "species": "http://0.0.0.0:5000/species/",
        "starships": "http://0.0.0.0:5000/starships/",
        "vehicles": "http://0.0.0.0:5000/vehicles/"
    }


##################################### People API ##############################################
# Get person per ID data from mariadb
@app.route('/people/<person_id>')
def get_person(person_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM people INNER JOIN people_film ON people.person_film_id = '
                   f'people_film.person_film_id WHERE person_id = {person_id}')
    film_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM people INNER JOIN people_specy ON people.person_specy_id = '
                   f'people_specy.person_specy_id WHERE person_id = {person_id}')
    species_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM people INNER JOIN people_vehicle ON people.person_vehicle_id = '
                   f'people_vehicle.person_vehicle_id WHERE person_id = {person_id}')
    vehicles_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM people INNER JOIN people_starship ON people.person_starship_id = '
                   f'people_starship.person_starship_id WHERE person_id = {person_id}')
    starships_result = [link for link in cursor]
    cursor.execute(f'SELECT name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, '
                   f'created, edited, url FROM people WHERE person_id = {person_id} GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12')
    pers_dic = dict()
    for (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, created, edited,
         url) in cursor:
        pers_dic["name"] = name
        pers_dic["height"] = height
        pers_dic["mass"] = mass
        pers_dic["hair_color"] = hair_color
        pers_dic["skin_color"] = skin_color
        pers_dic["eye_color"] = eye_color
        pers_dic["birth_year"] = birth_year
        pers_dic["gender"] = gender
        pers_dic["homeworld"] = homeworld
        pers_dic["films"] = list(itertools.chain.from_iterable(film_result))
        pers_dic["species"] = list(itertools.chain.from_iterable(species_result))
        pers_dic["vehicles"] = list(itertools.chain.from_iterable(vehicles_result))
        pers_dic["starships"] = list(itertools.chain.from_iterable(starships_result))
        pers_dic["created"] = created
        pers_dic["edited"] = edited
        pers_dic["url"] = url

    cursor.close()
    connection.close()
    return pers_dic


# Get all People Data
@app.route('/people/')
def get_people():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct person_id) as nbr_people FROM people')
    result_set = cursor.fetchall()
    people = []
    count = 0
    for row in result_set:
        count = row[0]

    for person_id in range(1, int(count) + 1):
        people.append(get_person(str(person_id)))
    return {"result": people,
            "count": count + 1}


##################################### Films API ##############################################
# Get film per ID data from mariadb
@app.route('/films/<film_id>')
def get_film(film_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM films INNER JOIN film_characters ON films.film_character_id = '
                   f'film_characters.film_character_id WHERE film_id = {film_id}')
    character_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM films INNER JOIN film_planet ON films.film_planet_id = '
                   f'film_planet.film_planet_id WHERE film_id = {film_id}')
    planet_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM films INNER JOIN film_vehicle ON films.film_vehicle_id = '
                   f'film_vehicle.film_vehicle_id WHERE film_id = {film_id}')
    vehicles_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM films INNER JOIN film_starship ON films.film_starship_id = '
                   f'film_starship.film_starship_id WHERE film_id = {film_id}')
    starships_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM films INNER JOIN film_specy ON films.film_specy_id = '
                   f'film_specy.film_specy_id WHERE film_id = {film_id}')
    species_result = [link for link in cursor]
    cursor.execute(f'SELECT title, episode_id, opening_crawl, director, producer, release_date, '
                   f'created, edited, url FROM films WHERE film_id = {film_id} GROUP BY 1,2,3,4,5,6,7,8,9')
    film_dic = dict()
    for (title, episode_id, opening_crawl, director, producer, release_date, created, edited, url) in cursor:
        film_dic["title"] = title
        film_dic["episode_id"] = episode_id
        film_dic["opening_crawl"] = opening_crawl
        film_dic["director"] = director
        film_dic["producer"] = producer
        film_dic["release_date"] = release_date
        film_dic["characters"] = list(itertools.chain.from_iterable(character_result))
        film_dic["planets"] = list(itertools.chain.from_iterable(planet_result))
        film_dic["species"] = list(itertools.chain.from_iterable(species_result))
        film_dic["vehicles"] = list(itertools.chain.from_iterable(vehicles_result))
        film_dic["starships"] = list(itertools.chain.from_iterable(starships_result))
        film_dic["created"] = created
        film_dic["edited"] = edited
        film_dic["url"] = url

    cursor.close()
    connection.close()
    return film_dic


# Get all films Data
@app.route('/films/')
def get_films():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct film_id) as nbr_films FROM films')
    result_set = cursor.fetchall()
    films = []
    count = 0
    for row in result_set:
        count = row[0]

    for film_id in range(1, int(count) + 1):
        films.append(get_film(str(film_id)))
    return {"result": films,
            "count": count + 1}


##################################### starships API ##############################################
# Get starship per ID data from mariadb
@app.route('/starships/<starship_id>')
def get_starship(starship_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM starships INNER JOIN starship_pilot ON starships.starship_pilot_id = '
                   f'starship_pilot.starship_pilot_id WHERE starship_id = {starship_id}')
    pilot_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM starships INNER JOIN starship_film ON starships.starship_film_id = '
                   f'starship_film.starship_film_id WHERE starship_id = {starship_id}')
    film_result = [link for link in cursor]
    cursor.execute(
        f'SELECT name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, '
        f'cargo_capacity,  consumables, hyperdrive_rating, MGLT, starship_class, '
        f'created, edited, url FROM starships WHERE starship_id = {starship_id} GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16')
    starship_dic = dict()
    for (name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity,
         consumables, hyperdrive_rating,
         MGLT, starship_class, created, edited, url) in cursor:
        starship_dic["name"] = name
        starship_dic["model"] = model
        starship_dic["manufacturer"] = manufacturer
        starship_dic["cost_in_credits"] = cost_in_credits
        starship_dic["length"] = length
        starship_dic["max_atmosphering_speed"] = max_atmosphering_speed
        starship_dic["crew"] = crew
        starship_dic["passengers"] = passengers
        starship_dic["cargo_capacity"] = cargo_capacity
        starship_dic["consumables"] = consumables
        starship_dic["hyperdrive_rating"] = hyperdrive_rating
        starship_dic["MGLT"] = MGLT
        starship_dic["starship_class"] = starship_class
        starship_dic["pilots"] = list(itertools.chain.from_iterable(pilot_result))
        starship_dic["films"] = list(itertools.chain.from_iterable(film_result))
        starship_dic["created"] = created
        starship_dic["edited"] = edited
        starship_dic["url"] = url

    cursor.close()
    connection.close()
    return starship_dic


# Get all starship Data
@app.route('/starships/')
def get_starships():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct starship_id) as nbr_starships FROM starships')
    result_set = cursor.fetchall()
    starships = []
    count = 0
    for row in result_set:
        count = row[0]

    for starship_id in range(1, int(count) + 1):
        starships.append(get_starship(str(starship_id)))
    return {"result": starships,
            "count": count + 1}


##################################### vehicles API ##############################################
# Get vehicles per ID data from mariadb
@app.route('/vehicles/<vehicle_id>')
def get_vehicle(vehicle_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM vehicles INNER JOIN vehicle_pilot ON vehicles.vehicle_pilot_id = '
                   f'vehicle_pilot.vehicle_pilot_id WHERE vehicle_id = {vehicle_id}')
    pilot_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM vehicles INNER JOIN vehicle_film ON vehicles.vehicle_film_id = '
                   f'vehicle_film.vehicle_film_id WHERE vehicle_id = {vehicle_id}')
    film_result = [link for link in cursor]
    cursor.execute(
        f'SELECT name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, '
        f'cargo_capacity,  consumables, vehicle_class, '
        f'created, edited, url FROM vehicles WHERE vehicle_id = {vehicle_id} GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14')
    vehicle_dic = dict()
    for (name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity,
         consumables, vehicle_class, created, edited, url) in cursor:
        vehicle_dic["name"] = name
        vehicle_dic["model"] = model
        vehicle_dic["manufacturer"] = manufacturer
        vehicle_dic["cost_in_credits"] = cost_in_credits
        vehicle_dic["length"] = length
        vehicle_dic["max_atmosphering_speed"] = max_atmosphering_speed
        vehicle_dic["crew"] = crew
        vehicle_dic["passengers"] = passengers
        vehicle_dic["cargo_capacity"] = cargo_capacity
        vehicle_dic["consumables"] = consumables
        vehicle_dic["vehicle_class"] = vehicle_class
        vehicle_dic["pilots"] = list(itertools.chain.from_iterable(pilot_result))
        vehicle_dic["vehicles"] = list(itertools.chain.from_iterable(film_result))
        vehicle_dic["created"] = created
        vehicle_dic["edited"] = edited
        vehicle_dic["url"] = url

    cursor.close()
    connection.close()
    return vehicle_dic


# Get all vehicles Data
@app.route('/vehicles/')
def get_vehicles():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct vehicle_id) as nbr_vehicles FROM vehicles')
    result_set = cursor.fetchall()
    vehicles = []
    count = 0
    for row in result_set:
        count = row[0]

    for vehicle_id in range(1, int(count) + 1):
        vehicles.append(get_vehicle(str(vehicle_id)))
    return {"result": vehicles,
            "count": count + 1}


##################################### species API ##############################################
# Get species per ID data from mariadb
@app.route('/species/<specie_id>')
def get_specie(specie_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM species INNER JOIN specie_person ON species.specie_person_id = '
                   f'specie_person.specie_person_id WHERE specie_id = {specie_id}')
    person_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM species INNER JOIN specie_film ON species.specie_film_id = '
                   f'specie_film.specie_film_id WHERE specie_id = {specie_id}')
    film_result = [link for link in cursor]
    cursor.execute(
        f'SELECT name, classification, designation, average_height, average_lifespan, eye_colors, hair_colors, '
        f'skin_colors, '
        f'language,  homeworld, '
        f'created, edited, url FROM species WHERE specie_id = {specie_id} GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13')
    specie_dic = dict()
    for (
            name, classification, designation, average_height, average_lifespan, eye_colors, hair_colors, skin_colors,
            language,
            homeworld, created, edited, url) in cursor:
        specie_dic["name"] = name
        specie_dic["classification"] = classification
        specie_dic["designation"] = designation
        specie_dic["average_height"] = average_height
        specie_dic["average_lifespan"] = average_lifespan
        specie_dic["eye_colors"] = eye_colors
        specie_dic["hair_colors"] = hair_colors
        specie_dic["skin_colors"] = skin_colors
        specie_dic["language"] = language
        specie_dic["homeworld"] = homeworld
        specie_dic["people"] = list(itertools.chain.from_iterable(person_result))
        specie_dic["films"] = list(itertools.chain.from_iterable(film_result))
        specie_dic["created"] = created
        specie_dic["edited"] = edited
        specie_dic["url"] = url

    cursor.close()
    connection.close()
    return specie_dic


# Get all species Data
@app.route('/species/')
def get_species():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct specie_id) as nbr_species FROM species')
    result_set = cursor.fetchall()
    species = []
    count = 0
    for row in result_set:
        count = row[0]

    for specie_id in range(1, int(count) + 1):
        species.append(get_specie(str(specie_id)))
    return {"result": species,
            "count": count + 1}


##################################### planets API ##############################################
# Get planets per ID data from mariadb
@app.route('/planets/<planet_id>')
def get_planet(planet_id):
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT distinct link FROM planets INNER JOIN planet_resident ON planets.planet_resident_id = '
                   f'planet_resident.planet_resident_id WHERE planet_id = {planet_id}')
    resident_result = [link for link in cursor]
    cursor.execute(f'SELECT distinct link FROM planets INNER JOIN planet_film ON planets.planet_film_id = '
                   f'planet_film.planet_film_id WHERE planet_id = {planet_id}')
    film_result = [link for link in cursor]
    cursor.execute(
        f'SELECT name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, '
        f'surface_water,  '
        f'created, edited, url FROM planets WHERE planet_id = {planet_id} GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12')
    planet_dic = dict()
    for (name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water,
         created, edited, url) in cursor:
        planet_dic["name"] = name
        planet_dic["diameter"] = diameter
        planet_dic["rotation_period"] = rotation_period
        planet_dic["orbital_period"] = orbital_period
        planet_dic["gravity"] = gravity
        planet_dic["population"] = population
        planet_dic["climate"] = climate
        planet_dic["terrain"] = terrain
        planet_dic["surface_water"] = surface_water
        planet_dic["residents"] = list(itertools.chain.from_iterable(resident_result))
        planet_dic["films"] = list(itertools.chain.from_iterable(film_result))
        planet_dic["created"] = created
        planet_dic["edited"] = edited
        planet_dic["url"] = url

    cursor.close()
    connection.close()
    return planet_dic


# Get all planets Data
@app.route('/planets/')
def get_planets():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT count(distinct planet_id) as nbr_planets FROM planets')
    result_set = cursor.fetchall()
    planets = []
    count = 0
    for row in result_set:
        count = row[0]

    for planet_id in range(1, int(count) + 1):
        planets.append(get_planet(str(planet_id)))
    return {"result": planets,
            "count": count + 1}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
